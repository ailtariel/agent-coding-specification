# Vuetify Skill

This directory contains the local Vuetify skill used by the web-project skill set.

The skill is no longer updated from `skilld-dev/vue-ecosystem-skills`. It is maintained locally so that the bundled references can track the official Vuetify documentation and releases directly.

## Contents

- `SKILL.md` - the runtime skill entry point loaded by Codex when Vuetify guidance is needed.
- `agents/openai.yaml` - UI metadata for the skill.
- `references/docs/` - local mirror of official Vuetify documentation pages.
- `references/releases/` - release notes and release-derived API/component change indexes.
- `references/ai-implementation-principles.md` - local guidance for AI-assisted Vuetify implementation.
- `references/ai-implementation-principles-cn.md` - Chinese translation of the AI implementation principles.

## Current Baseline

- Vuetify baseline: `4.1.0`
- Official docs source: <https://vuetifyjs.com>
- Official repository source: <https://github.com/vuetifyjs/vuetify>
- Docs mirror path in the official repository: `packages/docs/src/pages/en`

The local `references/docs/src/pages/en` mirror should match the official Vuetify repository tag used by `SKILL.md`.

## Updating This Skill

Do not use `update_skills.py` for this skill. That script intentionally excludes Vuetify because this local copy has diverged from the upstream generated skill and includes manually curated references.

Recommended update workflow:

1. Confirm the latest official version:

   ```powershell
   npm view vuetify version dist-tags --json
   ```

2. Fetch the matching official Vuetify tag into `tmp/`:

   ```powershell
   git clone --depth 1 --branch v4.1.0 --filter=blob:none --sparse https://github.com/vuetifyjs/vuetify.git tmp/vuetify-v4.1.0
   git -C tmp/vuetify-v4.1.0 sparse-checkout set packages/docs/src/pages/en packages/vuetify/src/components packages/api-generator
   ```

3. Replace the local docs mirror with the official docs pages for that tag:

   ```powershell
   Remove-Item -Recurse -Force web-project/vue/vuetify/references/docs/src/pages/en
   New-Item -ItemType Directory -Force web-project/vue/vuetify/references/docs/src/pages/en | Out-Null
   Copy-Item -Recurse -Force tmp/vuetify-v4.1.0/packages/docs/src/pages/en/* web-project/vue/vuetify/references/docs/src/pages/en/
   ```

4. Regenerate `references/docs/_INDEX.md` from the local mirror. Keep the index concise: include the total page count and one relative link per markdown page.

5. Review official releases since the previous baseline and update:

   - `references/releases/_INDEX.md`
   - per-version release files under `references/releases/`
   - focused API/component change indexes, when a release contains changes that are useful for agent lookup
   - `SKILL.md` metadata, tags, version boundary, and high-signal API/best-practice bullets

6. Validate the result:

   ```powershell
   # The local markdown set should match the selected official tag.
   # Also run a link check for local markdown links under web-project/vue/vuetify.
   git status --short -- web-project/vue/vuetify
   ```

When updating, prefer official Vuetify docs and release notes over generated third-party summaries. Keep `SKILL.md` small enough for runtime use; put detailed material in `references/`.

## Copyright And License Notes

This skill contains local instructions plus mirrored excerpts/files from the official Vuetify documentation and release material. Preserve upstream copyright and license notices when copying or updating official content.

Vuetify is maintained by the Vuetify project. See the official repository and documentation for authoritative licensing details:

- <https://github.com/vuetifyjs/vuetify>
- <https://vuetifyjs.com/en/about/licensing/>
