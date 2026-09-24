# Rules and skills consolidation

Status: authorized by the user on 2026-09-24; implementation and local Windows/Ubuntu installation included.

## Decisions

- This repository owns specifications and the full former skill-sets worktree under `skills/`, including references, attribution, scripts, and newer source-only customizations. Preserve the former repository history in an external migration archive. The former root was held open by another process, preventing the planned directory rename and junction; move its contents to the archive and leave a redirect README in that root instead.
- Import the four reviewed user workflow skills and the OpenAI Docs system skill with their resources. Keep upstream provenance. Other system skills remain managed by Codex.
- Apply review findings 1–14, except preserve finding 11's personal preferences (Composition API, TypeScript, script setup, ESM, and avoiding reactive props destructuring). Reconcile conflicting examples rather than removing those preferences.
- Install derived snapshots to each user's own home. Keep a single editable source in this repository. Windows and WSL have distinct home/config paths; macOS uses the same portable installer as WSL.
- Merge a marked rules block into the effective global AGENTS file, preserve other preferences, back up replaced files, and explicitly disable the bundled OpenAI Docs path. Same-name skills are not assumed to override one another.
- Use Python standard library only, with preview, verification, idempotent updates, and backup restoration. Preserve unrelated skills and configuration. Do not install into Docker Desktop's internal distribution.

## Acceptance

All migrated source files are accounted for; local customizations survive upstream staging; rules and skills agree on authorization, validation and testing; personal preferences remain. Installer behavior is checked with isolated homes and on Windows and Ubuntu. Installed files match the source; Codex skill discovery confirms the replacement and disabled system version. macOS commands are documented without claiming a macOS runtime test.
