# Vuetify AI Implementation Principles

This document is intended for AI coding agents. It supplements the general decision principles for implementing UI with Vuetify in Vue projects.

This document is not a project-level design specification. It does not define concrete colors, font sizes, spacing, or component appearance values. It also does not replace the target project's own `README`, `AGENTS.md`, design system, frontend architecture guidelines, or business documentation.

## Goals

- Keep the application's visual style and interaction patterns consistent.
- Provide responsive layouts that work well for the target devices.
- Keep UI components and styles concise, clearly structured, and maintainable.
- Manage shared components and styles centrally.
- Maximize reuse of official Vuetify capabilities to better achieve the goals above.

## Prerequisites

- Confirm the Vuetify major version actually used by the target project first. Prefer reading `package.json` and the lockfile.
- Do not mix APIs from different Vuetify major versions.
- When an API is uncertain, prefer this skill's local references or the official documentation for the target version.
- Existing project conventions take precedence over this document. If the target project already has a clear design system, layout rules, or component conventions, follow the project conventions first.

## AI Workflow

When handling Vuetify-related tasks, evaluate in this order:

1. Look for existing similar pages, components, theme settings, defaults, and style patterns in the target project.
2. Reuse or appropriately extract an existing project component when its responsibility and contract match.
3. Otherwise decide whether native Vuetify components and public APIs satisfy the requirement.
4. Decide whether the visual semantics should reuse or add theme tokens, Global Defaults, or SASS variables.
5. For one-off or local requirements, prefer Vuetify utility classes before considering scoped CSS.
6. Only add wrappers, global styles, or special implementations when neither Vuetify capabilities nor existing project patterns can reasonably express the requirement.

## Vuetify Capability Map

AI should prefer capabilities already provided by Vuetify:

- Application layout: `v-app`, `v-layout`, `v-main`, app bar, navigation drawer, bottom navigation, footer.
- Responsive layout: grid, display/platform, spacing, flex, sizing, breakpoint utilities.
- Common components: button, card, list, form input, dialog, menu, snackbar, tabs, table, empty state, loading state.
- Component APIs: `variant`, `density`, `size`, `color`, `bg-color`, `rounded`, `elevation`, slots, component-specific props.
- Theme system: theme colors, CSS variables, runtime theme switching, semantic tokens.
- Global configuration: `createVuetify({ defaults })` and local `v-defaults-provider`.
- SASS variables: global fonts, border radius, low-level component variables, and other framework-level visual adjustments.
- Utility classes: spacing, display, flex, text, overflow, position, sizing, elevation, border radius.
- Accessibility foundation: built-in keyboard, focus, and ARIA behavior in components such as dialog, menu, overlay, form, and navigation.

## Capability Selection Principles

Do not treat the following list as a fixed priority order. Choose the appropriate capability based on the type of problem.

- Prefer Vuetify components, props, slots, and composables for structure and interaction.
- Prefer shared components for business structures repeated across pages.
- Prefer Vuetify Global Defaults for stable component default behavior across pages.
- Prefer theme tokens for stable visual semantics across pages.
- Prefer SASS variables or Vuetify config for global low-level visual adjustments.
- Before using SASS variables, confirm that the project has configured the Vuetify Sass compilation pipeline and that the adjustment truly belongs to framework-level low-level variables.
- Prefer utility classes for local layout and one-off minor adjustments.
- Use scoped CSS when utility classes are not suitable for expressing the requirement.
- Global CSS overrides are a last resort. They must be scoped and justified.

## Layout Principles

- Common application shells should prefer the Vuetify Application Layout System.
- `v-app` should serve as the root boundary for application layout.
- Layout components such as app bar, drawer, bottom navigation, footer, and `v-main` should keep clear layout relationships.
- Fixed regions, layout reservation, ordering, and offsets should preferably be handled by the Vuetify layout API.
- Layout component reservation order is affected by template order by default. For dynamic or non-obvious layouts, prefer explicitly controlling order with the layout component's `order` prop.
- Page content regions should have clear boundaries. Avoid letting layout, page, and local containers compete for the main scrolling responsibility.
- If a regular layout needs large amounts of handwritten height, `calc()`, `absolute`, `fixed`, or global overflow hacks to work, first re-check the Vuetify layout documentation and existing project implementations.

Local positioning, `calc()`, or extra wrapper layers are allowed, but they must satisfy these conditions:

- They serve a clear local visual, animation, third-party library, or platform constraint.
- They do not break Vuetify layout registration, reservation, responsive behavior, or accessibility.
- They do not spread a single page's problem into a global layout hack.

## Theme And Style Principles

- Theme tokens should express semantics, not concrete visual values.
- Token lists are usually examples and should not be treated by AI as an allow list. Actual tokens are defined by the target project's theme.
- Do not add global tokens for one-off styles on a single page.
- Do not name tokens after visual or implementation values such as `darkBlue`, `greenButton`, or `customGray`.
- Pages and components may have their own scoped CSS, but styles should remain local, clear, and removable.
- Hardcoded colors are not absolutely forbidden, but if hardcoded colors appear in submitted code, there should be a clear reason why existing theme tokens cannot be used.
- Broad overrides of `.v-*` component classes increase maintenance risk and should be avoided where possible.

When deciding where styles should live:

- Cross-page visual semantics: theme token.
- Cross-page component default behavior: Global Defaults.
- Vuetify low-level global variables: SASS variables.
- Cross-page business UI pattern: shared component.
- Local effect in a single page or component: scoped CSS.
- Temporary or tiny layout adjustment: utility classes.

## Global Defaults Principles

`defaults` refers to Vuetify Global Defaults, the mechanism for centrally configuring component default props through `createVuetify({ defaults })`.

Good candidates for Global Defaults:

- Default component variant, density, size, rounded, elevation, color, and similar props used consistently across most pages.
- Stable default behavior for form inputs, buttons, cards, dialogs, sheets, and app shell components.
- Component default props that clearly belong to foundational design system conventions.

Poor candidates for Global Defaults:

- Special styles for a single business scenario.
- Local layout that appears on only one page.
- Styles that depend on specific business state and change frequently.
- Experimental rules that would passively change behavior across many existing pages.

When a local scope needs consistent default props, consider `v-defaults-provider` instead of modifying global defaults for a local region.

Stable default behavior for nested components can be expressed with contextual defaults, such as configuring internal `VBtn` default props under `VCard`. Do not create extra global CSS just to enforce conventions inside a component tree.

Prop names in defaults should use camelCase.

Note: Vuetify `class` and `style` defaults should be configured under specific component keys. They should not be placed under `global` defaults.

When configuring defaults, remember that `class` and `style` may be passed to internal components in some form inputs or control components. Check the actual rendered structure and impact scope before making changes.

## SASS Variables Principles

- Prefer SASS variables only when the requirement is a framework-level adjustment such as global fonts, border radius, low-level component variables, or utility generation rules.
- If the style is only for a single page, a single component, or a local business state, do not introduce or modify Vuetify Sass settings.
- Vuetify Sass settings files should contain only variables, mixins, and functions. Do not put actual CSS rules in them or import regular style files, to avoid generating duplicate styles.
- Do not `@use 'vuetify/styles'` in Sass files. Use `vuetify/settings` when variables are needed, and use `vuetify` for specific global settings only as directed by the official documentation.
- Enabling SASS variables makes Vuetify recompile from Sass source files and may affect build performance. Do not overuse this when precompiled CSS already satisfies the requirement.

## Component Principles

- Prefer native Vuetify components. Do not duplicate capabilities Vuetify already provides.
- Prefer expressing visual states through component props, `variant`, `density`, `size`, `color`, `bg-color`, `rounded`, `elevation`, and slots.
- Prefer Vuetify form, input, rules, and validation patterns for forms.
- Prefer Vuetify dialog, menu, bottom sheet, snackbar, tooltip, overlay, and similar components for overlay-style interactions.
- When using the activator slot of components such as dialog and menu, bind the slot-provided `props` to the trigger element to avoid losing ARIA, focus, and keyboard interaction attributes.
- States such as loading, empty, error, disabled, and selected should be expressed through Vuetify component states and unified project styling.
- Do not create wrapper components that only forward props for tiny differences.

Wrapper components are allowed when they:

- Encapsulate stable business semantics.
- Remove real repetition across pages.
- Unify complex interactions or complex slot structures.
- Isolate third-party libraries, platform differences, or experimental components.

## Responsive Principles

- Clarify the target devices and primary viewports before designing the layout.
- Prefer Vuetify grid, display/platform, spacing, flex, sizing utilities, and component responsive props.
- Do not write layouts only for the current desktop width.
- Evaluate the impact of fixed sizes, fixed heights, and absolute positioning on small screens, landscape orientation, touch devices, and system safe areas.
- Content-dense pages should prioritize scannability, reachability, and clear scroll boundaries.

## Accessibility Principles

- Prefer built-in Vuetify components for complex interactions, because they usually already handle keyboard behavior, focus, ARIA, and interaction states.
- When customizing dialog, menu, combobox, tabs, tooltip, toast, or form validation, carefully check focus management, keyboard operation, and semantics.
- When using a Vuetify activator slot, preserve and bind the slot props. Custom triggers must not only copy the visual structure.
- Icon buttons should have accessible names and must not rely only on visual icons.
- Form errors, loading, disabled states, and empty states should provide clear feedback to users.
- Do not break default focus, hover, active, or disabled states for visual effects.

## Exception Rules

It is acceptable to break the default principles when:

- Official Vuetify capabilities cannot satisfy the requirement.
- The target project already has an established pattern using the approach.
- There is a clear performance issue.
- There is a clear accessibility requirement.
- A third-party library, native platform, browser, or runtime environment has constraints.
- The user or project conventions explicitly require a specific implementation approach.

When breaking the default principles, AI should explain:

1. Which native Vuetify options were evaluated.
2. Why the native options are insufficient.
3. The impact scope of the current approach.
4. Whether it affects overall consistency.
5. Whether it should be consolidated into a theme token, defaults, SASS variables, or a shared component.

## AI Self Check

Before submitting a Vuetify-related implementation, AI only needs to confirm:

- Whether the Vuetify major version was confirmed, and whether official documentation or local references were checked when the API was uncertain.
- Whether existing project patterns and official Vuetify component capabilities were reused first.
- Whether the layout respects the Vuetify application layout and the target project's own frontend architecture guidelines.
- Whether common visual rules were consolidated into theme, Global Defaults, SASS variables, or shared components instead of being repeatedly scattered across pages.
- Whether local CSS truly serves local requirements and does not break Vuetify states, layout, responsiveness, or accessibility.
- If default rules were broken, whether the reason, impact scope, and alternatives were explained.
