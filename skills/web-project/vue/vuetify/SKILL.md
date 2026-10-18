---
name: vuetify-skilld
description: Apply personal Vuetify layout, styling, form, and interaction conventions using the project's installed version.
---

# Vuetify

Apply [Vue personal conventions](../SKILL.md) when not already loaded. These are personal implementation choices, not claims that Vuetify requires this architecture.

## Layout And Styling

- App owns `VApp`; layout owns `VLayout`, registered shell regions, and `RouterView`; each routed page owns its `VMain` and primary scroll region. Preserve an explicitly established alternative project architecture.
- Use layout registration and component APIs for shell offsets, order, dimensions, and positioning. Do not recreate those responsibilities with margins, fixed positioning, or child-page CSS.
- Prefer Flex for rows and stacks; use Grid for actual two-dimensional alignment or spanning. Prefer appropriate Vuetify containers and surfaces over generic wrappers. Use responsive columns only when needed.
- Compose app bars with the matching Vuetify title, navigation, spacing, separator, and slot capabilities. Do not recreate their geometry or insert components that serve no layout role.
- Prefer configured breakpoints, responsive utilities, and component props before custom viewport tests. Media features such as reduced motion are separate concerns.

## Inputs And Feedback

- Prefer built-in loading feedback; a custom indicator requires a customization need the built-in behavior cannot meet. Do not show both for one operation.
- Do not wrap inputs in a form by default. Use one for form-specific capabilities such as validation or coordinated submission, preserving required keyboard behavior.
- For an input's own action, prefer its built-in action, then a public slot. Use a separate sibling control only when the interaction requires separation. Actions on a filter group belong to the group.
