Personal customized skill sets.

## Install and update

This directory is now maintained inside `agent-coding-specification`. Use the root [installation guide](../README.md) and `python scripts/install.py` from the repository root to install all managed rules and skills together. The old standalone repository is archived; do not use its GitHub URL for new installations.

Stage framework-reference updates with `python skills/update_skills.py --skill vue,pinia` or list sources with `--list`. Inspect `skills/tmp/update-skills/staged` and merge selected changes deliberately. `--apply` is disabled because wholesale upstream replacement would erase personal conventions and workflow fixes. Existing nested skills and newer local Vuetify references must survive a merge.

See [PROVENANCE.md](PROVENANCE.md) for migration and local/system skill sources. `system-overrides.json` lists bundled skills whose original Codex paths are disabled by the installer. Add a complete fork and its resources before adding a name there.

## Markdown Style

- Do not hard-wrap Chinese Markdown prose to a fixed column width. Keep each paragraph and list item on one physical line unless a Markdown structural boundary, code block, table, or intentional hard break requires a new line.
- Format Chinese Markdown with Prettier `--prose-wrap never` or equivalent behavior.

## Sources

These paths are used by `update_skills.py`.

| Local path | Source |
| --- | --- |
| `web-project/SKILL.md` | Local aggregate entry point; maintained in this repository. |
| `web-project/vue/` | `https://github.com/antfu/skills.git` -> `skills/vue` |
| `web-project/vue/pinia/` | `https://github.com/antfu/skills.git` -> `skills/pinia` |
| `web-project/vue/vue-router/` | `https://github.com/JetBrains/skills.git` -> `vue-router-best-practices` |
| `web-project/vue/vuetify/` | Locally maintained against official Vuetify documentation; do not overwrite from the old generated source. |
| `web-project/react/` | `https://github.com/vercel-labs/agent-skills.git` -> `skills/react-best-practices` |
| `web-project/react/ant-design/` | `https://github.com/ant-design/antd-skill.git` -> `skills/ant-design` |
| `web-project/vite/` | `https://github.com/antfu/skills.git` -> `skills/vite` |
| `web-project/pnpm/` | `https://github.com/antfu/skills.git` -> `skills/pnpm` |
| `web-project/design/` | `https://github.com/github/awesome-copilot.git` -> `skills/penpot-uiux-design` |
