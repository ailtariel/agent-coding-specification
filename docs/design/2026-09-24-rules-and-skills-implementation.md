# Consolidation implementation

- [x] Read source and target guidance; verify complete source copy by hashes.
- [x] Revise EN/CN specifications, task routing, and workflow/framework skills; preserve personal preferences.
- [x] Add portable installation, backup/restore and validation, with Windows/WSL/macOS documentation.
- [x] Run isolated installer tests and skill validation; review remaining conflicts.
- [x] Install and verify Windows and Ubuntu using the same installer.
- [x] Archive the former source repository and leave a redirect notice; record final validation.

No automatic commit or publication is part of this task. Migration maps the former `web-project/`, `README.md`, and `update_skills.py` into `skills/`; skill updates remain staged for manual merge so they cannot erase personal revisions.

## Verification on 2026-09-24

- Ten isolated installer tests passed on both Windows (Python 3.13.5) and Ubuntu (Python 3.12.3), covering preservation, repeat installation, preview, drift, custom Codex Home, AGENTS.override, existing config, legacy migration, rollback, and link rejection.
- All 16 skill declarations passed the installed skill-creator validator. Independent static scenario review covered simple changes, partly ambiguous review feedback, framework routing, CLI applicability, personal Vue preferences, and already-authorized implementation. Remaining approval and dialog-order conflicts were corrected; this was a document review, not a model eval.
- Both real profiles installed successfully and passed `install.py --check`. Windows repeat installation reported `Already current: 16 skills`.
- Codex `skills/list` found all 16 managed skills at their installed paths, with zero mismatches and zero load errors on Windows VS Code's Codex 0.155.0-alpha.16.3 and Ubuntu's Linux CLI 0.139.0. The bundled OpenAI Docs path is disabled. No model task was started.
- The Windows npm CLI 0.87.0 does not discover `~/.agents/skills`; the README explains selecting the actual editor executable and using the Linux login PATH in WSL. This task did not upgrade CLI packages.
- The archive `C:/workstation/dev/personal/skill-sets.pre-migration-20260924/` retains a clean original worktree at `9ae1f3128475641a443ff52a2d30e3de96113346`. All 420 source paths exist in the migrated tree. The former root was held open by another process, so its contents were moved individually and a redirect README replaces the planned junction.
- Links in all 14 root/specification Markdown files resolve. `git diff --check` passed. Upstream listing works; `--apply` rejects before writing.
- macOS installation is documented using the same standard-library installer; no macOS runtime test was available.

## Installation backups

- Windows: `C:/Users/xing.lin/.agents/agent-coding-specification/backups/20260924T115620.456842Z`
- Ubuntu: `/home/xinglin/.agents/agent-coding-specification/backups/20260924T115640.018107Z`

Restart existing Codex sessions to load the new configuration and skill descriptions. Existing unrelated user skills and configuration were retained.
