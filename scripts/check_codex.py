#!/usr/bin/env python3
"""Verify skill discovery through Codex app-server without starting a model turn."""

import argparse
import json
import os
from pathlib import Path
import platform
import queue
import shutil
import subprocess
import tempfile
import threading


def executable(explicit):
    if explicit:
        return explicit
    found = shutil.which("codex")
    if not found:
        raise RuntimeError("Codex is not on PATH; pass --codex /path/to/executable")
    if os.name == "nt" and Path(found).suffix.lower() != ".exe":
        arch = "aarch64" if platform.machine().lower() in {"arm64", "aarch64"} else "x86_64"
        package = Path(found).parent / "node_modules/@openai/codex"
        candidates = list(package.glob(f"**/vendor/{arch}-pc-windows-msvc/codex/codex.exe"))
        if len(candidates) != 1:
            raise RuntimeError("Cannot resolve npm Codex binary; pass --codex with codex.exe")
        return str(candidates[0])
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", help="Native Codex executable")
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--cwd", type=Path, default=Path.home(), help="Use a neutral directory to verify user-level discovery")
    args = parser.parse_args()
    manifest = json.loads((args.home / ".agents/agent-coding-specification/installed.json").read_text(encoding="utf-8"))
    env = os.environ.copy()
    env["CODEX_HOME"] = manifest["codex_home"]
    responses = queue.Queue()
    binary = executable(args.codex)
    version = subprocess.run([binary, "--version"], capture_output=True, text=True,
                             encoding="utf-8", check=True, timeout=15).stdout.strip()
    print(f"Checking with {version}: {binary}")
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as stderr:
        process = subprocess.Popen([binary, "app-server"], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=stderr, text=True, encoding="utf-8",
                                   env=env, cwd=args.cwd, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)

        def read_output():
            for line in process.stdout:
                try:
                    responses.put(json.loads(line))
                except json.JSONDecodeError:
                    pass
            responses.put({"error": "App server closed before response"})

        threading.Thread(target=read_output, daemon=True).start()

        def request(identifier, method, params):
            process.stdin.write(json.dumps({"id": identifier, "method": method, "params": params}) + "\n")
            process.stdin.flush()
            while True:
                result = responses.get(timeout=30)
                if result.get("id") == identifier or ("error" in result and "id" not in result):
                    if "error" in result:
                        raise RuntimeError(str(result["error"]))
                    return result["result"]

        try:
            request(1, "initialize", {"clientInfo": {"name": "personal-skill-check", "version": "1.0"}, "capabilities": {"experimentalApi": True}})
            process.stdin.write('{"method":"initialized","params":{}}\n')
            process.stdin.flush()
            data = request(2, "skills/list", {"cwds": [str(args.cwd.resolve())], "forceReload": True})
            rows = data["data"]
            entries = [skill for row in rows for skill in row.get("skills", [])]
            errors = [error for row in rows for error in row.get("errors", [])]
            failures = []
            for name, path in manifest["skills"].items():
                matches = [s for s in entries if s["name"] == name and s.get("enabled", True)]
                if len(matches) != 1 or Path(matches[0]["path"]).resolve() != Path(path).resolve():
                    failures.append(f"{name}: expected one enabled skill at {path}; found {[(s.get('path'), s.get('enabled')) for s in matches]}")
            for path in manifest["disabled"]:
                if any(Path(s["path"]).resolve() == Path(path).resolve() and s.get("enabled", True) for s in entries):
                    failures.append(f"Still enabled: {path}")
            for failure in failures:
                print(f"FAIL: {failure}")
            for error in errors:
                print(f"Discovery error: {error}")
            if failures:
                print("Confirm this is the Codex executable used by your editor or terminal. "
                      "Older CLIs may not discover ~/.agents/skills; use --codex /path/to/the/current/binary.")
            print(f"Codex discovery: {len(manifest['skills'])} managed skills; {len(failures)} mismatches; {len(errors)} load errors")
            return int(bool(failures or errors))
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    raise SystemExit(main())
