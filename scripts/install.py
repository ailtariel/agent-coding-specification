#!/usr/bin/env python3
"""Install personal specifications and skills using only Python 3.11+ stdlib."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tomllib
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MARK = "agent-coding-specification"
IGNORE = shutil.ignore_patterns(".git", "__pycache__", "*.pyc", ".DS_Store", "tmp")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def fingerprint(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    if path.is_file():
        return {".": hashlib.sha256(path.read_bytes()).hexdigest()}
    return {
        p.relative_to(path).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(path.rglob("*")) if p.is_file()
        and not any(part in {".git", "__pycache__", "tmp"} for part in p.relative_to(path).parts)
        and p.suffix != ".pyc" and p.name != ".DS_Store"
    }


def skill_name(path: Path) -> str:
    match = re.search(r"^name:\s*['\"]?([a-z0-9-]+)['\"]?\s*$", text(path), re.M)
    if not match:
        raise ValueError(f"Missing or invalid skill name: {path}")
    return match[1]


def merge_block(original: str, body: str, comment: str) -> str:
    begin = f"{comment} BEGIN {MARK}" + (" -->" if comment == "<!--" else "")
    end = f"{comment} END {MARK}" + (" -->" if comment == "<!--" else "")
    if original.count(begin) != original.count(end) or original.count(begin) > 1:
        raise ValueError("Malformed or duplicate managed block; original file left intact")
    block = f"{begin}\n{body.strip()}\n{end}"
    if begin in original:
        return re.sub(re.escape(begin) + r".*?" + re.escape(end), lambda _: block,
                      original, count=1, flags=re.S)
    return original.rstrip() + ("\n\n" if original.strip() else "") + block + "\n"


def migrate_legacy_agents(original: str) -> str:
    legacy = text(ROOT / "scripts/legacy-global-agents.template.md")
    split = "## Canonical Coding Specification"
    if not legacy or split not in original:
        return original
    prefix, tail = original.split(split, 1)
    expected = legacy.split(split, 1)[1]
    normalize = lambda s: re.sub(r"`[^`\n]*AI-coding-specification/`", "`SPEC`", s).strip()
    # Only replace the exact previous generated template; arbitrary prose survives.
    if normalize(tail) != normalize(expected):
        return original
    if not prefix.startswith("# Global Agent Working Rules\n\n## User Preferences\n"):
        return original
    prefs = prefix.split("## User Preferences", 1)[1].strip()
    if prefs == "- Add personal global preferences here.":
        return ""
    return "# User Preferences\n\n" + prefs + "\n"


def configure_skills(original: str, disabled: list[Path]) -> str:
    begin, end = f"# BEGIN {MARK}", f"# END {MARK}"
    if original.count(begin) != original.count(end) or original.count(begin) > 1:
        raise ValueError("Malformed managed config block")
    original = re.sub(re.escape(begin) + r".*?" + re.escape(end), "", original, flags=re.S)
    tomllib.loads(original)
    wanted = {str(p.resolve()) for p in disabled}
    present: set[str] = set()
    sections = re.split(r"(?m)(?=^\s*\[)", original)
    for i, section in enumerate(sections):
        if not re.match(r"\s*\[\[skills\.config\]\]", section):
            continue
        entry = tomllib.loads(section)["skills"]["config"][0]
        if "path" not in entry:
            continue
        path = str(Path(entry["path"]).expanduser().resolve())
        if path in wanted:
            if path in present:
                raise ValueError(f"Duplicate skill config path: {path}")
            present.add(path)
            if re.search(r"(?m)^\s*enabled\s*=", section):
                section = re.sub(r"(?m)^(\s*enabled\s*=\s*)(true|false)", r"\g<1>false", section)
            else:
                section = section.rstrip() + "\nenabled = false\n\n"
            sections[i] = section
    extra = "\n\n".join(
        "[[skills.config]]\npath = " + json.dumps(Path(p).as_posix()) + "\nenabled = false"
        for p in sorted(wanted - present)
    )
    merged = merge_block("".join(sections).rstrip() + "\n", extra or "# No additional overrides.", "#")
    parsed = tomllib.loads(merged)
    disabled_paths = {str(Path(e["path"]).expanduser().resolve())
                      for e in parsed.get("skills", {}).get("config", []) if not e.get("enabled", True)}
    if not wanted <= disabled_paths:
        raise ValueError("Could not disable all bundled skill paths")
    return merged


def guard_target(path: Path, roots: tuple[Path, ...]) -> None:
    # Never follow a destination link into a repository or another user's data.
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        raise ValueError(f"Refusing linked installation target: {path}")
    resolved = path.resolve()
    if not any(resolved != r.resolve() and resolved.is_relative_to(r.resolve()) for r in roots):
        raise ValueError(f"Target outside installation roots: {resolved}")
    if resolved == ROOT or ROOT.is_relative_to(resolved) or resolved.is_relative_to(ROOT):
        raise ValueError(f"Installation target overlaps source repository: {resolved}")


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, target, ignore=IGNORE)
    else:
        shutil.copy2(source, target)


def remove(path: Path, roots: tuple[Path, ...]) -> None:
    guard_target(path, roots)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def build(stage: Path, user_home: Path, codex: Path) -> tuple[list[tuple[Path, Path]], dict]:
    state = user_home / ".agents" / MARK
    user_skills = user_home / ".agents/skills"
    pairs: list[tuple[Path, Path]] = []
    spec = stage / "specification"
    copy(ROOT / "AI-coding-specification", spec)
    pairs.append((spec, state / "specification"))
    names: dict[str, str] = {}
    for source in sorted((ROOT / "skills").iterdir()):
        if not source.is_dir() or not (source / "SKILL.md").exists():
            continue
        staged = stage / "skills" / source.name
        copy(source, staged)
        pairs.append((staged, user_skills / source.name))
        for entry in staged.rglob("SKILL.md"):
            name = skill_name(entry)
            if name in names:
                raise ValueError(f"Duplicate source skill: {name}")
            names[name] = str(user_skills / source.name / entry.relative_to(staged))
    if not names:
        raise ValueError("No installable skills found")
    # Bundled replacements are explicit; leaving other system skills alone is intentional.
    overrides = json.loads(text(ROOT / "skills/system-overrides.json"))
    disabled = []
    for name in overrides:
        if name not in names:
            raise ValueError(f"System override missing from source: {name}")
        disabled.append(codex / "skills/.system" / name / "SKILL.md")
    # Disable old standalone copies of managed names instead of relying on name precedence.
    for parent in (user_skills, codex / "skills"):
        if parent.exists():
            for entry in parent.rglob("SKILL.md"):
                if ".system" in entry.parts:
                    continue
                name = skill_name(entry)
                if name in names and entry.resolve() != Path(names[name]).resolve():
                    if not any(entry.is_relative_to(dst) for _, dst in pairs):
                        disabled.append(entry)
    agents = codex / ("AGENTS.override.md" if (codex / "AGENTS.override.md").exists() else "AGENTS.md")
    body = text(ROOT / "AGENTS.global.template.md").replace("{{SPECIFICATION_PATH}}", (state / "specification").as_posix())
    staged_agents = stage / "AGENTS.md"
    staged_agents.write_text(merge_block(migrate_legacy_agents(text(agents)), body, "<!--"), encoding="utf-8")
    pairs.append((staged_agents, agents))
    config = stage / "config.toml"
    config.write_text(configure_skills(text(codex / "config.toml"), disabled), encoding="utf-8")
    pairs.append((config, codex / "config.toml"))
    manifest = {"version": 1, "source": str(ROOT), "home": str(user_home), "codex_home": str(codex),
                "agents": str(agents), "skills": names, "disabled": [str(p) for p in disabled],
                "targets": {str(dst): fingerprint(src) for src, dst in pairs}}
    manifest_file = stage / "installed.json"
    manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pairs.append((manifest_file, state / "installed.json"))
    return pairs, manifest


def restore(backup: Path, roots: tuple[Path, ...], state: Path) -> None:
    backup = backup.resolve()
    if not backup.is_relative_to((state / "backups").resolve()):
        raise ValueError("Backup must be inside this installation's backups directory")
    record = json.loads(text(backup / "restore.json"))
    for item in record:
        dst = Path(item["target"])
        guard_target(dst, roots)
        saved = backup / item["saved"]
        if not saved.resolve().is_relative_to(backup):
            raise ValueError("Invalid backup member")
        if item["existed"] and not saved.exists():
            raise ValueError(f"Incomplete backup: {saved}")
        if "installed" in item and fingerprint(dst) != item["installed"]:
            raise ValueError(f"Changed since installation; preserve edits before restoring: {dst}")
    for item in reversed(record):
        dst = Path(item["target"])
        remove(dst, roots)
        if item["existed"]:
            copy(backup / item["saved"], dst)
    print(f"Restored {len(record)} targets from {backup}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Target user home (isolated tests or another local profile)")
    parser.add_argument("--codex-home", type=Path, help="Default: CODEX_HOME, otherwise <home>/.codex")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview without writing target files")
    mode.add_argument("--check", action="store_true", help="Verify source, installed snapshots, rules and overrides")
    mode.add_argument("--restore", type=Path, help="Restore a backup created by this installer")
    args = parser.parse_args()
    user_home = args.home.expanduser().resolve()
    codex = (args.codex_home or Path(os.environ.get("CODEX_HOME", str(user_home / ".codex")))).expanduser().resolve()
    state = user_home / ".agents" / MARK
    roots = (user_home / ".agents", codex)
    if args.restore:
        restore(args.restore, roots, state)
        return 0
    with tempfile.TemporaryDirectory(prefix="agent-spec-install-") as temporary:
        pairs, manifest = build(Path(temporary), user_home, codex)
        for _, dst in pairs:
            guard_target(dst, roots)
        changed = [(src, dst) for src, dst in pairs if not dst.exists() or fingerprint(src) != fingerprint(dst)]
        for _, dst in changed:
            print(f"{'Would update' if args.dry_run else 'Out of date' if args.check else 'Update'}: {dst}")
        if args.dry_run:
            print(f"Preview: {len(manifest['skills'])} skills, {len(changed)} changed targets; no target writes")
            return 0
        if args.check:
            print(f"Check: {len(manifest['skills'])} skills; {'PASS' if not changed else 'FAIL'}")
            return 1 if changed else 0
        if not changed:
            print(f"Already current: {len(manifest['skills'])} skills")
            return 0
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        backup = state / "backups" / stamp
        backup.mkdir(parents=True)
        if os.name != "nt":
            backup.chmod(0o700)
        record = []
        # Back up every replacement before touching any target.
        for i, (src, dst) in enumerate(changed):
            item = {"target": str(dst), "saved": str(i), "existed": dst.exists(), "installed": fingerprint(src)}
            if dst.exists():
                copy(dst, backup / str(i))
            record.append(item)
        (backup / "restore.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        touched = []
        try:
            for (src, dst), item in zip(changed, record):
                touched.append(item)
                remove(dst, roots)
                copy(src, dst)
                if fingerprint(src) != fingerprint(dst):
                    raise OSError(f"Verification failed after copy: {dst}")
        except Exception:
            for item in reversed(touched):
                dst = Path(item["target"])
                remove(dst, roots)
                if item["existed"]:
                    copy(backup / item["saved"], dst)
            raise
        print(f"Installed {len(manifest['skills'])} skills. Backup: {backup}")
        print("Restart Codex to reload config. Run --check to verify; /skills shows discovery.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        raise SystemExit(1)
