---
name: vuetify-skilld
description: Implement Vuetify components, layouts, themes, or migrations using the installed major version.
metadata:
  version: 4.1.0
  generated_at: 2026-06-07
  references_synced_at: 2026-06-07
  guidance_updated: "2026-10-08"
---

# Vuetify

Apply the shared [Vue personal conventions](../SKILL.md), including component/view reuse and style placement, when not already loaded. Check whether existing project components or Vuetify can implement the requested view/interaction before introducing custom UI.

The local documentation snapshot covers Vuetify 4.1.0; this is not a claim about the latest release. Confirm the target dependency version. For Vuetify 3, use only APIs verified against that installed version; do not apply v4 migration notes.

## Layout Preferences

These are personal implementation preferences for Vuetify projects:

- Prefer Flex for responsive layouts and local rows or stacks. Use CSS Grid only when an actual two-dimensional alignment or spanning requirement justifies it; do not use it merely for spacing or equal-width cards.
- Compose app bars with `VAppBarNavIcon`, `VAppBarTitle`, `VDivider`, `VSpacer`, and the app bar slots where their roles apply. Do not recreate their sizing, spacing, or separation with custom CSS, or add components that serve no layout role.
- Prefer `VContainer`, `VCard`, `VSheet`, and supported flex layout components/utilities for page regions. Use `VRow`/`VCol` when responsive columns are needed. Do not start with generic `div` wrappers and custom CSS where these components fit; native semantic content, measurement nodes, and library host elements remain appropriate. Use `VFlex` only when the installed version exports it; Vuetify 3/4 use current layout components and flex utilities.
- Use Vuetify responsive utilities, component props, and named `useDisplay()` breakpoints before custom width media queries or manual width comparisons. Keep a custom query only for a requirement the configured breakpoints cannot express. Media features such as `prefers-reduced-motion` are separate from viewport breakpoints.

## Loading, Forms, And Input Actions

- Prefer a component's built-in `loading` prop when available. Add a custom loading indicator only for an explicit customization requirement that the built-in behavior cannot meet; do not display both for the same operation.
- Do not wrap input controls in `VForm` or a native form by default. Use a form only when its form-specific capabilities, such as validation or coordinated field state, are needed. Preserve required keyboard actions when removing an unnecessary form wrapper.
- For actions belonging to text fields, autocompletes, and other input controls, use built-in buttons or button props first, then a custom button in the component's public slot. Do not place the input and its action as separate sibling controls unless the interaction requires that separation. Actions applying to a whole filter group or page are not actions of an individual input.

## References On Demand

- Application layout, defaults, SASS, and activator integration: [implementation details](references/ai-implementation-principles.md).
- Component props, slots, and utilities: [local documentation index](references/docs/_INDEX.md).
- Vuetify 4 migration: [upgrade guide](references/docs/src/pages/en/getting-started/upgrade-guide.md); existing legacy grid layouts: [grid legacy mode](references/docs/src/pages/en/getting-started/grid-legacy-mode.md).
- Version-specific additions and fixes: [v4.0.1-v4.1.0 release API index](references/releases/v4.0.1-to-v4.1.0-api-index.md).

Search for the component or API in question; do not load the entire documentation or release history for ordinary component work.
