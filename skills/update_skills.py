#!/usr/bin/env python3
"""Update local skills from Git repositories.

Only git-clone based sources are supported. Sources that are not known are
reported and skipped.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TMP_ROOT = ROOT / "tmp" / "update-skills"
REPOS_DIR = TMP_ROOT / "repos"
STAGED_DIR = TMP_ROOT / "staged"


@dataclass(frozen=True)
class SkillSource:
    name: str
    repo: str
    source_path: Path
    target_path: Path
    entries: tuple[str, ...] = ()
    ref: str = "main"


SKILLS: tuple[SkillSource, ...] = (
    SkillSource(
        name="vue",
        repo="https://github.com/antfu/skills.git",
        source_path=Path("skills/vue"),
        target_path=Path("web-project/vue"),
        entries=("SKILL.md", "references", "GENERATION.md"),
    ),
    SkillSource(
        name="pinia",
        repo="https://github.com/antfu/skills.git",
        source_path=Path("skills/pinia"),
        target_path=Path("web-project/vue/pinia"),
    ),
    SkillSource(
        name="vite",
        repo="https://github.com/antfu/skills.git",
        source_path=Path("skills/vite"),
        target_path=Path("web-project/vite"),
    ),
    SkillSource(
        name="pnpm",
        repo="https://github.com/antfu/skills.git",
        source_path=Path("skills/pnpm"),
        target_path=Path("web-project/pnpm"),
    ),
    SkillSource(
        name="vue-router",
        repo="https://github.com/JetBrains/skills.git",
        source_path=Path("vue-router-best-practices"),
        target_path=Path("web-project/vue/vue-router"),
    ),
    SkillSource(
        name="react",
        repo="https://github.com/vercel-labs/agent-skills.git",
        source_path=Path("skills/react-best-practices"),
        target_path=Path("web-project/react"),
        entries=("SKILL.md", "README.md", "AGENTS.md", "metadata.json", "rules"),
    ),
    SkillSource(
        name="ant-design",
        repo="https://github.com/ant-design/antd-skill.git",
        source_path=Path("skills/ant-design"),
        target_path=Path("web-project/react/ant-design"),
    ),
    SkillSource(
        name="design",
        repo="https://github.com/github/awesome-copilot.git",
        source_path=Path("skills/penpot-uiux-design"),
        target_path=Path("web-project/design"),
    ),
)


UNKNOWN_SOURCES: tuple[str, ...] = (
    "web-project: local aggregate entry point; no external git source.",
    "vuetify: locally maintained against official Vuetify docs; do not overwrite from skilld-dev/vue-ecosystem-skills.",
)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"+ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=cwd, check=True)


def repo_dir_for(repo: str) -> Path:
    name = repo.rstrip("/").removesuffix(".git").split("/")[-1]
    owner = repo.rstrip("/").removesuffix(".git").split("/")[-2]
    return REPOS_DIR / f"{owner}__{name}"


def clone_or_update(source: SkillSource) -> Path:
    repo_dir = repo_dir_for(source.repo)
    if repo_dir.exists():
        run(["git", "fetch", "--depth", "1", "origin", source.ref], cwd=repo_dir)
        run(["git", "checkout", "FETCH_HEAD"], cwd=repo_dir)
    else:
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--depth", "1", "--branch", source.ref, source.repo, str(repo_dir)])
    return repo_dir


def ensure_within_root(path: Path) -> Path:
    resolved = path.resolve()
    root = ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise RuntimeError(f"Refusing to write outside repository: {resolved}")
    return resolved


def remove_path(path: Path) -> None:
    ensure_within_root(path)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def copy_tree(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def stage_skill(source: SkillSource, repo_dir: Path) -> Path:
    source_root = repo_dir / source.source_path
    if not source_root.exists():
        raise FileNotFoundError(f"Source path not found for {source.name}: {source_root}")

    staged_target = STAGED_DIR / source.target_path
    if staged_target.exists():
        remove_path(staged_target)
    staged_target.mkdir(parents=True, exist_ok=True)

    if source.entries:
        for entry in source.entries:
            item = source_root / entry
            if item.exists():
                copy_tree(item, staged_target / entry)
            else:
                print(f"warning: {source.name} source entry missing: {entry}", file=sys.stderr)
    else:
        remove_path(staged_target)
        copy_tree(source_root, staged_target)

    return staged_target


def apply_skill(source: SkillSource, staged_target: Path) -> None:
    target = ensure_within_root(ROOT / source.target_path)
    if source.entries:
        target.mkdir(parents=True, exist_ok=True)
        for entry in source.entries:
            staged_entry = staged_target / entry
            target_entry = target / entry
            if not staged_entry.exists():
                continue
            remove_path(target_entry)
            copy_tree(staged_entry, target_entry)
    else:
        remove_path(target)
        copy_tree(staged_target, target)


def parse_skill_filter(raw: str | None) -> set[str] | None:
    if not raw:
        return None
    return {item.strip() for item in raw.split(",") if item.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Update skills from git-clone sources.")
    parser.add_argument("--apply", action="store_true", help="Removed: automatic replacement would erase personal revisions.")
    parser.add_argument("--skill", help="Comma-separated skill names to update.")
    parser.add_argument("--list", action="store_true", help="List known and unknown skill sources.")
    args = parser.parse_args()

    known_names = {source.name for source in SKILLS}
    selected = parse_skill_filter(args.skill)

    if args.apply:
        parser.error("Automatic upstream replacement is disabled for this customized repository. Stage without --apply, inspect the diff, and merge deliberately.")

    if args.list:
        print("Known git-clone sources:")
        for source in SKILLS:
            print(f"- {source.name}: {source.repo} :: {source.source_path} -> {source.target_path}")
        print("\nUnknown sources:")
        for item in UNKNOWN_SOURCES:
            print(f"- {item}")
        return 0

    if selected:
        unknown_requested = selected - known_names
        if unknown_requested:
            print("No git-clone source configured for:", ", ".join(sorted(unknown_requested)), file=sys.stderr)
            return 2

    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    STAGED_DIR.mkdir(parents=True, exist_ok=True)

    sources = [source for source in SKILLS if selected is None or source.name in selected]
    for source in sources:
        print(f"\n== {source.name} ==")
        repo_dir = clone_or_update(source)
        staged_target = stage_skill(source, repo_dir)
        print(f"staged: {staged_target.relative_to(ROOT)}")
        if args.apply:
            apply_skill(source, staged_target)
            print(f"updated: {source.target_path}")

    if not args.apply:
        print("\nStaging complete. Inspect the staged changes and merge intentionally; personal revisions must be preserved.")

    print("\nUnknown sources:")
    for item in UNKNOWN_SOURCES:
        print(f"- {item}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
