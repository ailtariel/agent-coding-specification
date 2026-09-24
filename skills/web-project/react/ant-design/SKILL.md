---
name: ant-design
description: Implement or troubleshoot Ant Design, ProComponents, or Ant Design X APIs, themes, forms, tables, and streaming UI.
---

# Ant Design

## S - Scope
- Target: `antd@^6` + React 18-19, with `ant-design-pro@^5` / `@ant-design/pro-components` and `@ant-design/x@^2` when needed.
- Tooling: `@ant-design/cli` for offline component metadata, demos, changelogs, migrations, linting, doctor checks, and usage analysis.
- Focus: decision guidance only; no end-user tutorials.
- Source policy: official docs only; no undocumented APIs or internal `.ant-*` coupling.

### Personal defaults
- Language: TypeScript.
- Styling: tokens first, then `classNames`/`styles`; avoid global overrides.
- Provider: one root `ConfigProvider` unless strict isolation is required.

### Mandatory rules
- Query uncertain or version-sensitive component APIs with the available CLI or matching official docs. Reuse verified results; mechanical text/style changes do not require an API query.
- Always use `--format json` with `antd` CLI commands.
- Confirm the installed major version before applying version-specific guidance; match it with `--version <x.y.z>` or let the CLI auto-detect from local `node_modules`.
- Select checks for the changed behavior. Use `antd lint <changed-path> --format json` when available and useful, alongside required project checks; do not install it merely to complete a minor change.
- If the CLI fails, report the limitation and use matching official docs or installed package types to continue. Preparing or submitting a tool bug report is separate work and requires user intent; a CLI failure does not itself block the product task.
- For component questions, first map the component name to the official route slug `{components}` (lowercase kebab-case, e.g. `TreeSelect -> tree-select`, `Button -> button`), then request docs in this order (CN first, EN fallback):
  1. `https://ant.design/components/{components}-cn`
  2. `https://ant.design/components/{components}`
  - Examples: `tree-select-cn -> tree-select`, `button-cn -> button`.
- Use only documented antd/Pro/X APIs.
- Do not invent props/events/component names.
- Do not rely on internal DOM or `.ant-*` selectors.
- Reuse the existing theme first. Use global tokens for app-wide semantics, component tokens for component-wide changes, and public `classNames`/`styles` for local adjustments. Do not create global tokens for a one-off change.

## P - Process
### 1) Classify
- Identify layer: core antd, Pro, or X.
- Confirm version, rendering mode (CSR/SSR/streaming), data scale, and whether `@ant-design/cli` should be the primary lookup path.

### 2) Query authoritative sources
- Prefer local `@ant-design/cli` first for structured lookup:
  - `antd info` for props/API
  - `antd demo` for a working baseline
  - `antd doc` for full docs
  - `antd token` / `antd semantic` for theming and styling hooks
  - `antd doctor`, `antd lint`, `antd usage`, `antd migrate`, `antd changelog` when debugging or upgrading
- Then request the official component docs (`-cn` first, EN fallback) when narrative docs or cross-checking are needed.

### 3) Decide
- Provider baseline: CSR -> `ConfigProvider`; SSR -> `ConfigProvider` + `StyleProvider`.
- Theming baseline: global tokens -> component tokens -> `classNames`/`styles`.
- Output recommendation + risk + verification points (SSR/a11y/perf), citing CLI findings when used.

## O - Output
Report only decisions and verification relevant to the requested change. The following are conditional topics, not a mandatory report template.
- Provide short decision rationale (1-3 sentences).
- Include minimal provider/theming strategy.
- Include concrete SSR/a11y/perf checks.
- For Pro: include route/menu/access and CRUD schema direction.
- For X: include message/tool schema and streaming state direction.

## References

| File | Use when |
| --- | --- |
| `references/antd-cli.md` | You need the exact offline CLI workflow for API lookup, demos, linting, doctor checks, migration, changelog review, usage analysis, or bug reporting. |

## Regression checklist
Check only components and behavior affected by the change; skip unrelated entries.
- [ ] One root `ConfigProvider`; SSR style order/hydration verified.
- [ ] Tokens first; no broad global `.ant-*` overrides.
- [ ] Table has stable `rowKey`; sort/filter/pagination entry is unified.
- [ ] Select remote mode disables local filter when using remote search.
- [ ] Upload controlled/uncontrolled mode is explicit with failure/retry path.
- [ ] Pro route/menu/access remain consistent with backend enforcement.
- [ ] X streaming supports stop/retry and deterministic tool rendering.
- [ ] CLI results, when used, match the target version; any lookup limitation is reported.
