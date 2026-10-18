Personal customized skill sets.

## Install and update

This directory is now maintained inside `agent-coding-specification`. Use the root [installation guide](../README.md) and `python scripts/install.py` from the repository root to install all managed rules and skills together. The old standalone repository is archived; do not use its GitHub URL for new installations.

Stage an upstream Vue entry comparison with `python skills/update_skills.py --skill vue` or list sources with `--list`. Inspect `skills/tmp/update-skills/staged` and merge only useful decision guidance. `--apply` is disabled because wholesale replacement would erase personal conventions and reintroduce removed tutorials. Staged snapshots are temporary comparison inputs, not installed references.

See [PROVENANCE.md](PROVENANCE.md) for migration, cleanup, and local/system skill sources. `system-overrides.json` lists bundled skills whose original Codex paths are disabled by the installer. A fork must include the resources its workflow actually uses, required assets, and license notices.

## Content boundary

Keep personal practices, non-obvious decision boundaries, and workflows that add value beyond existing model knowledge. Public API manuals, command catalogs, release/issue snapshots, generic tutorials, and fixed process rituals do not belong in installed skills, including their references. Resolve version-sensitive details from the target installation, live tool documentation, or matching official sources. See the bilingual [authoring rules](../AI-coding-specification/rules-and-skills-authoring.md).

## Markdown Style

- Do not hard-wrap Chinese Markdown prose to a fixed column width. Keep each paragraph and list item on one physical line unless a Markdown structural boundary, code block, table, or intentional hard break requires a new line.
- Format Chinese Markdown with Prettier `--prose-wrap never` or equivalent behavior.

## Sources

Upstream comparisons are staged by `update_skills.py`; locally maintained skills do not require an upstream snapshot.

| Local path | Source |
| --- | --- |
| `web-project/vue/` | `https://github.com/antfu/skills.git` -> `skills/vue` |
| `web-project/vue/vuetify/` | Local personal conventions; consult official Vuetify sources on demand, without mirroring them. |
| `web-project/visual-design/` | Locally maintained visual refinement preferences, curated from the former visual hierarchy reference. |
| `web-project/visual-design/refactoring-ui/` | Curated diagnostic workflow adapted from [s0xDk/refactoring-ui-skill](https://github.com/s0xDk/refactoring-ui-skill); maintained locally, with upstream MIT notice retained. |

`web-project/` is a grouping directory, not a discoverable skill. It contains Vue, Vuetify, visual-design, and the nested refactoring-ui skill. Vue owns the Pinia, composable, style, and VueUse selection preferences; Vuetify owns its layout and control preferences; visual-design owns visual refinement preferences; refactoring-ui diagnoses visual problems in existing interfaces. RTL/LTR remains in the Web frontend programming specification. English and Chinese entries express the same practices. The installer discovers nested skills without requiring an artificial parent entry.
