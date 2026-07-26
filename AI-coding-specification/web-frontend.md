Author: ailtariel@gmail.com
Updated: 2026-07-26

# Web Frontend Coding Specification

This specification defines mandatory, framework-neutral engineering rules for
web frontend work in this repository. It applies to pages, layouts, components,
styles, state, data synchronization, interaction, accessibility, and frontend
development tooling.

It extends [`coding-specification.md`](coding-specification.md). Project design
documents define product-specific behavior, while framework and UI-library
skills provide implementation details. Neither may weaken this specification.

## Rule Usage

- This document is mandatory for all web frontend tasks, regardless of the
  framework, rendering mode, component library, or state-management library.
- Apply all relevant rule blocks together. When this document conflicts with a
  project design decision confirmed by the user, stop and confirm the intended
  exception before implementation.
- Rule tags are intended for plans, reviews, delivery notes, and self-checks.
  Do not expand implementation scope merely to satisfy a tag.
- Framework-specific APIs, file types, macros, hooks, composables, components,
  and formatting exceptions belong in the corresponding framework or UI-library
  skill, not in this document.

## General Rules

- [web-existing-stack] Preserve the project's established frontend framework,
  component library, state flow, routing model, styling system, formatter, and
  build tool unless the user explicitly approves a change.
- [web-version-boundary] Confirm installed dependency versions before applying
  version-specific API, migration, or breaking-change guidance.
- [web-no-parallel-system] Do not introduce a parallel component library,
  state-management system, utility CSS framework, styling system, routing
  system, or data-fetching layer for a localized requirement.
- [web-existing-patterns] Inspect an existing comparable page, layout,
  component, state flow, and style pattern before introducing a new pattern.
- [web-single-owner] Every application shell, layout region, page region,
  primary scroll container, overlay, state source, and feedback channel must
  have one clear owner.
- [web-locality] Keep page-specific behavior, state, styles, and components
  within the nearest feature or page boundary. Promote them only after a real
  cross-page responsibility is established.

## Application, Layout, And Page Boundaries

Use an application / layout / page hierarchy:

```text
application
+-- layout 1
|   +-- page 1.1
|   +-- page 1.2
+-- layout 2
    +-- page 2.1
    +-- page 2.2
```

### Application Boundary

- [web-application-owner] The application boundary may own:
  - application-wide runtime providers and services;
  - global module mounting and initialization;
  - top-level overlays;
  - themes, languages, timers, and other cross-page capabilities;
  - global messages, dialogs, bottom sheets, snackbars, and other cross-page
    interactions.
- The application boundary must not own:
  - concrete page content;
  - page forms, filters, or lists;
  - page-level dialogs;
  - page business interactions.

### Layout Boundary

- [web-layout-owner] A layout owns one stable application shell and may own:
  - the child route or page-content outlet;
  - navigation, drawers, headers, footers, and other cross-page shell regions;
  - shared layout boundaries;
  - shell visibility rules derived from route metadata.
- A layout must not own:
  - page business logic;
  - page-level state or actions;
  - route-name branches that implement page business behavior.
- Shared navigation, drawer, header, footer, and other shell regions should be
  reusable shell components composed by the layout.
- One application may have multiple layouts. A page must not recreate shell
  regions already owned by its application or layout unless the route
  explicitly switches to a different layout.

### Page Boundary

- [web-page-owner] A page owns:
  - its feature content;
  - page-level state and actions;
  - the page content container, padding, and local layout;
  - the page's remaining content area and primary page scrolling behavior.
- A page must not duplicate navigation, drawers, headers, footers, global
  overlays, or global scroll containers already owned above it.
- Avoid page wrappers that merely reproduce application or layout
  responsibilities.

## Shared And Feature Components

- [web-shared-component] Extract a shared component when a UI structure or
  interaction pattern has multiple real consumers and a stable responsibility.
- A shared component should:
  - expose variation through documented inputs, outputs, and extension points;
  - avoid route-name or page-name branches;
  - remain weakly coupled to one business domain unless it is intentionally a
    cross-feature business component.
- When different consumers need different actions or local content, provide a
  clear extension point instead of adding consumer-specific branches.
- [web-feature-component] A feature component may own:
  - one independent business capability;
  - a reusable module within one feature;
  - local interaction and feature-private UI composition.
- Feature components may own local styles. Do not promote business-specific
  styles into global tokens or global classes until they represent a stable
  cross-page pattern.
- Do not create a wrapper component for one call site unless it materially
  reduces complexity or isolates a clear platform, browser, or third-party
  boundary.

## Feature Module Boundaries

- [web-feature-module] Organize product or business capabilities into feature
  modules when the project uses a modular structure.
- A feature module may contain:
  - pages and route-level UI;
  - domain types;
  - feature state;
  - repositories or data-access adapters;
  - services;
  - feature-level stateful utilities;
  - feature-private components.
- Keep a feature's pages, domain data flow, state, repositories, services,
  stateful utilities, and private components inside the nearest feature
  boundary.
- A general UI-components area may contain page structure and small local
  interactions, but must not own substantial domain data flow, persistence,
  repositories, services, or business workflows.
- A shared-components area is only for components reused by multiple features
  and not bound to one business domain.
- A shared-library area is only for cross-feature logic; do not place pages or
  UI components there.
- Types used by one file should remain close to that file. Types shared by
  multiple files should move to the nearest feature-level or
  responsibility-specific type module, not a catch-all global types file.
- Follow the target project's existing directory names. Do not impose a
  framework-specific directory structure from a generic example.

## API Access And Transport Boundaries

- [web-api-layer] Pages and UI components must not issue API requests directly.
  Put API calls in the nearest feature or module service, repository,
  data-access adapter, or API module.
- [web-shared-api-client] Use the project's established shared API client for
  authentication, base URL handling, common headers, error translation, and
  other shared transport behavior.
- [web-api-address] Feature code should use relative, path-only API routes.
  Application base URLs, origins, and development proxy targets belong to
  bootstrap or configuration boundaries and must not be hardcoded in feature
  code.
- [web-transport-exception] If a feature genuinely requires an absolute URL,
  separate client, or different transport, document the reason, ownership, and
  impact before implementation.

## Components And UI Libraries

- [web-library-first] Use the project's existing UI library before native
  controls or custom implementations for layout, forms, dialogs, menus, tables,
  pagination, date inputs, uploads, feedback, and other common interactions.
- Native elements remain appropriate for document semantics, browser API
  boundaries, generated content, hidden inputs required by native workflows, or
  behavior the UI library does not own.
- [web-component-reuse] Reuse an existing component when its responsibility,
  interaction semantics, and input/output contract match.
- Extract or wrap a component only when real reuse, stable business semantics,
  complex interaction, or a platform boundary justifies the abstraction.
- Prefer library component APIs and built-in accessibility behavior over DOM
  emulation or click handlers on generic containers.
- [web-ui-consistency] New and modified UI must follow existing information
  density, spacing, control sizing, interaction, feedback, and responsive
  patterns.

## State, Data Synchronization, And Feedback

- [web-state-source] Treat the framework state, store, or query cache selected
  by the project as the reactive UI source. Do not reload data merely to force
  a rendering update after a mutation.
- [web-state-minimal] Keep local UI state local. Introduce shared or global
  state only when multiple owners genuinely need one source and lifetime.
- Use the established server-state or data-access layer for remote data and
  cache lifecycle. Do not copy server state into a second global state system
  without a confirmed ownership reason.
- The owner of a persistent mutation must update or invalidate its own
  authoritative state and any directly related state after success.
- Keep editing buffers separate from authoritative persisted state when the
  workflow supports cancel, reset, dirty state, or deferred saving.
- Feature-scoped singleton state is allowed only when its shared lifetime is
  explicit, prevents real duplicate setup, and remains inside the feature
  boundary.
- [web-feedback-owner] Keep field validation and page-local feedback with the
  owning form or page.
- Route system-wide operation feedback, global errors, confirmation workflows,
  toast or snackbar messages, and cross-page prompts through the established
  application-level feedback owner.
- Loading, empty, error, disabled, selected, success, and stale states must be
  deliberate parts of the interaction rather than incidental rendering
  branches.

## Dialog And Popup Actions

- [web-dialog-action-order] When a dialog, confirmation prompt, or popup form
  contains both an action that applies a result and an action that abandons it,
  place the applying action on the left and the abandoning action on the right.
- Applying actions include confirm, save, add, delete, clear, reset, import,
  keep, ignore, and apply-filter operations.
- Abandoning actions include cancel, abort, close, and do-not-apply operations.
- Selection lists, detail dialogs, keyboard dialogs, and similar interactions
  without an explicit cancel action do not need an artificial cancel button.
- Preserve established product conventions when a confirmed design document
  defines a different action order.

## Scrolling And Layout Boundaries

- [web-scroll-owner] The layout defines fixed shell regions. The page content
  region owns the remaining content area and page scrolling.
- Every primary scroll boundary must be explicit.
- Avoid multiple hierarchy levels simultaneously acting as the primary scroll
  container.
- Do not use global overflow rules, arbitrary heights, fixed positioning, or
  nested scroll containers to conceal an application / layout / page ownership
  problem.
- Local scroll containers are allowed for clear local responsibilities such as
  tables, editors, previews, logs, or virtualized collections. They must not
  replace the page's primary scroll ownership accidentally.
- Evaluate fixed sizes, fixed heights, and absolute positioning on small
  screens, landscape orientation, touch devices, content growth, and system
  safe areas.

## Style Boundaries

- [web-style-scope] Global styles own unified foundational appearance.
  Page-local and component-local styles must affect only their owning boundary.
- Use the project's existing style system according to responsibility:
  - cross-page visual semantics: theme or design token;
  - stable cross-page component behavior: component defaults or shared
    component;
  - small local layout adjustment: existing utility classes;
  - page-local or component-local behavior: locally scoped styles;
  - broad global CSS or library internals override: bounded last resort with an
    explained reason.
- Do not duplicate properties already managed by the global theme, component
  defaults, framework variables, or a shared component.
- Promote only cross-page visual semantics or component conventions into
  global tokens, global defaults, global classes, or shared components.
- Do not create global tokens or defaults for one-page exceptions.
- [web-style-colocation] Keep page-specific, component-specific, and
  feature-specific styles next to their owning page, component, or feature
  according to the project's existing structure.
- Do not accumulate page or component selectors in a global stylesheet. When
  touching legacy global selectors, move directly related local styles back to
  their owner when that migration is within the current task scope.
- Apply spacing and sizing to the element or component that owns the layout.
  Avoid wrappers whose only responsibility is one margin, padding, flex, grid,
  or width rule.
- Avoid hardcoded colors and fixed sizes when existing semantic tokens or
  responsive behavior can express the requirement. Fixed values remain valid
  for real product, browser, editor, or platform constraints.

## Interaction, Forms, And Accessibility

- [web-accessibility] Use semantic elements and the existing UI library's
  interaction components so keyboard behavior, focus management, accessible
  names, and disabled states remain intact.
- Every form control needs an accessible label, validation behavior, disabled
  behavior, submission state, and clear error feedback.
- Icon-only controls require an accessible name.
- Preserve keyboard navigation and input method editor composition behavior.
- Dialogs, menus, tooltips, and other overlays must preserve focus restoration,
  escape behavior, activator semantics, and keyboard operation.
- Do not remove visible focus, hover, active, selected, loading, or disabled
  feedback solely for visual styling.
- Do not replace library accessibility behavior with click handlers on generic
  containers.

## Bidirectional And RTL Layout

- [web-logical-direction] Layout spacing must support bidirectional interfaces.
  Prefer logical inline/block/start/end properties or utilities over physical
  left/right properties unless a documented visual requirement is inherently
  physical.
- [web-rtl-source] Application direction, directional spacing, and alignment
  decisions must come from the same centralized configuration or token source.
  Do not redefine RTL detection or direction rules independently in pages and
  components.

## Internationalization And User-Visible Content

- [web-i18n] Use the project's established internationalization mechanism for
  user-visible application text unless a design document explicitly defines
  the content as external or user-provided.
- Every locale message must compile under the project's configured message
  syntax.
- Reuse an existing message key only when its meaning and interpolation
  contract match; identical text alone is insufficient.
- [web-i18n-boundary] Page titles, navigation labels, button text, form labels,
  placeholders, empty states, validation messages, and API error fallback text
  are UI chrome and must use the established internationalization mechanism.
- Backend-provided business data, including localized business content, does
  not replace internationalized UI chrome. Runtime logs are exempt from the UI
  internationalization requirement.
- Framework-specific message escaping and compiler behavior belong in the
  corresponding framework or internationalization reference.
- Error feedback should preserve useful source detail in accordance with
  [api-error-detail] in `coding-specification.md`.

## Formatting And Change Scope

- [web-formatting] Use the project's configured formatter as the single
  formatting authority for frontend source and configuration files.
- Run the repository's frontend formatting check before delivery when one is
  available.
- Do not manually align source or change formatter configuration to normalize
  one isolated preference.
- Formatting changes must remain within frontend files explicitly in scope for
  the task.

## Local Development Servers

- [web-dev-server] An AI agent may start a local frontend server when runtime or
  visual verification requires it.
- Any server started by the agent must be stopped before delivery.
- Do not leave background frontend processes behind.

## Testing And Verification

- Follow the verification ladder, test-addition rules, and reporting
  requirements in `coding-specification.md`.
- Prefer the smallest relevant combination of static reasoning, formatting,
  type checking, linting, targeted tests, build verification, and browser or
  visual checks.
- Visual-only changes do not require automated tests by default, but responsive
  layout, keyboard interaction, focus behavior, loading, empty, error, and
  disabled states must still be checked when relevant.

## Final Review

Before delivering web frontend changes, verify:

1. Application, layout, page, feature, and shared-component responsibilities
   each have one clear owner.
2. Feature module boundaries keep domain data flow and business workflows out
   of general UI-component and shared-library areas.
3. Pages and components use the established API layer and shared client without
   hardcoded origins or feature-local transport duplication.
4. Existing library components, shared components, state flows, and style
   patterns were reused before adding custom implementations.
5. Persistent mutations update or invalidate the authoritative reactive state.
6. Local and system-wide feedback use the correct owners.
7. Dialog action order follows this specification or a confirmed product
   exception.
8. Primary and local scroll boundaries are clear, responsive, and compatible
   with the required text directions.
9. Styles are colocated with their owners and placed at the narrowest correct
   scope without avoidable global overrides, one-off tokens, or wrapper
   elements.
10. Forms, overlays, icon controls, focus, keyboard interaction, and input method
   editor behavior remain accessible.
11. UI chrome and backend-provided business content follow the correct
    internationalization boundaries.
12. Required formatting, type, test, build, and visual verifications were
    completed and reported.
