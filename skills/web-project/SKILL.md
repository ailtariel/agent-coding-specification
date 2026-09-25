---
name: web-project
description: Select frontend skills for cross-stack work or when the relevant framework/tool skill is unclear.
---

# Web Project

Use this router when skill selection is unclear or work spans several frontend technologies. If the relevant skill is already known, load it directly; parent routers are not prerequisites. Read only guidance that changes a decision for the current task, and reuse material already read.

This skill provides framework and tooling references only. If it conflicts with the user's global coding specification or repository-local instructions, follow those higher-priority instructions.

## Index

- [vue](vue/SKILL.md): Vue 3 Composition API, SFCs, and Vue ecosystem routing.
  - [pinia](vue/pinia/SKILL.md): Vue state management and stores.
  - [vue-router](vue/vue-router/SKILL.md): Vue Router guards, params, lifecycle, and navigation gotchas.
  - [vuetify](vue/vuetify/SKILL.md): Vuetify components, layouts, theming, and migration notes.
  - [vueuse](vue/vueuse/SKILL.md): Reactive utilities, conditional callbacks, and waiting for data readiness.
- [react](react/SKILL.md): React and Next.js performance best practices.
  - [ant-design](react/ant-design/SKILL.md): antd 6.x, Ant Design Pro/ProComponents, Ant Design X, and `@ant-design/cli` guidance.
- [vite](vite/SKILL.md): Vite config, plugin API, build, SSR, and migration work.
- [pnpm](pnpm/SKILL.md): pnpm commands, workspaces, dependency resolution, catalogs, patches, and CI usage.
- [uiux-design](uiux-design/SKILL.md): Tool-independent interface design and design review.
- [design](design/SKILL.md): Creating or editing Penpot documents.

## Selection Rules

1. For Vue reactivity, SFC, or component implementation decisions, read `vue/SKILL.md`. A filename alone does not require unrelated references.
2. For Vue state, read `vue/pinia/SKILL.md`.
3. For Vue routes, guards, params, or navigation bugs, read `vue/vue-router/SKILL.md`.
4. For `vuetify` imports or Vuetify components/layout/theme work, read `vue/vuetify/SKILL.md`.
5. For React or Next.js code, read `react/SKILL.md`. Do not load it for non-React frontend projects.
6. For `antd`, `@ant-design/pro-components`, `@ant-design/x`, Ant Design Pro, or `@ant-design/cli` work in React projects, read `react/ant-design/SKILL.md`.
7. For `vite.config.*`, Vite plugins, build/SSR/library mode, or dev server issues, read `vite/SKILL.md`.
8. For `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `.npmrc`, workspace filters, or dependency changes, read `pnpm/SKILL.md`.
9. For explicit UI/UX design or design review, read `uiux-design/SKILL.md`. Read `design/SKILL.md` only for a Penpot document or when the user chooses Penpot.
10. For Vuetify, first identify the installed Vuetify major version from project dependencies. Use Vuetify 4 migration or breaking-change guidance only when the project is on Vuetify 4 or the user explicitly asks about Vuetify 4 migration.
11. For VueUse utility selection or waiting on reactive data, read `vue/vueuse/SKILL.md`. Shared Vue, Pinia, and Vuetify personal practices live in `vue/SKILL.md`; reuse it when already loaded.

## Workflow

1. Detect existing framework, package manager, UI library, and build tool before changing files.
2. Prefer project-local conventions over generic framework defaults.
3. Load detailed nested references only when the current task needs them.
4. Validate with the repository's available scripts, using targeted checks before broad checks.

## Layout

```text
web-project/
+-- vue/
|   +-- pinia/
|   +-- vue-router/
|   +-- vuetify/
|   +-- vueuse/
+-- react/
|   +-- ant-design/
+-- vite/
+-- pnpm/
+-- design/
```
