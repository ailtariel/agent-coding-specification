Author: ailtariel@gmail.com
Updated: 2026-09-17

# Web Frontend Coding Specification

This specification defines mandatory, framework-neutral engineering rules for web frontend work in the target workspace or affected repository. It applies to pages, layouts, components, styles, state, data synchronization, interaction, accessibility, and frontend development tooling.

It extends [`coding-specification.md`](coding-specification.md). Project design documents define product-specific behavior, while framework and UI-library skills provide implementation details. Neither may weaken this specification.

## Rule Usage

- This document is mandatory for all web frontend tasks, regardless of the framework, rendering mode, component library, or state-management library.
- Apply all relevant rule blocks together. When this document conflicts with a project design decision confirmed by the user, stop and confirm the intended exception before implementation.
- Rule tags are intended for plans, reviews, delivery notes, and self-checks. Do not expand implementation scope merely to satisfy a tag.
- Framework-specific APIs, file types, macros, hooks, composables, components, and formatting exceptions belong in the corresponding framework or UI-library skill, not in this document.

## General Rules

- [ui-documentation-exemption] Unless explicitly requested by the user, do not create or update document files such as designs, implementation plans, change records, or verification reports for designing, implementing, or adjusting UI layout, styling, or interface interactions. Do not make document completion or document approval a prerequisite for implementation. This exemption takes precedence over general requirements to create or update documents or record implementation phases.
  - Interface interactions include expanding and collapsing, opening and closing dialogs, hover feedback, focus movement, scrolling, and switching views without changing business semantics. Local UI state changes, displaying existing data, or invoking existing functionality do not by themselves constitute changes to data processing or business functionality.
  - Assess documentation needs only for parts that add or change data fetching, computation, transformation, persistence, API contracts, business rules, or business workflows. Such changes do not automatically require a new document; base that decision on the design decisions that need explanation and retention, and prefer updating existing relevant documents.
  - When a task includes both UI and functional changes, document only the functional and data-processing changes that need explanation. Do not extend the documentation to layout, styling, or purely interface-level interaction details. Page count, changed-file count, visual complexity, or phased implementation must not independently trigger UI documentation requirements.
  - Deliver change explanations and verification results directly in the conversation instead of generating separate document files.
- [web-existing-stack] Preserve the project's established frontend framework, component library, state flow, routing model, styling system, formatter, and build tool unless the user explicitly approves a change.
- [web-version-boundary] Confirm installed dependency versions before applying version-specific API, migration, or breaking-change guidance.
- [web-no-parallel-system] Do not introduce a parallel component library, state-management system, utility CSS framework, styling system, routing system, or data-fetching layer for a localized requirement.
- [web-existing-patterns] Inspect an existing comparable page, layout, component, state flow, and style pattern before introducing a new pattern.
- [web-single-owner] Every application shell, layout region, page region, primary scroll container, overlay, state source, and feedback channel must have one clear owner.
- [web-locality] Keep page-specific behavior, state, styles, and components within the nearest feature or page boundary. Promote them only after a real cross-page responsibility is established.

## File Organization And Responsibility Boundaries

The following example illustrates file ownership. `*` denotes the file extension determined by the technology stack. Create directories and files only as needed, and preserve an existing equivalent structure or framework convention.

```text
src/
├── layouts/
│   └── {layout}/
├── pages/
│   └── {page-or-page-group}/
│       ├── components/
│       │   └── {component}/
│       ├── modules/
│       │   └── {module}/
│       ├── Page.*
│       ├── types.*
│       ├── store.*
│       ├── service.*
│       └── useXxx.*
├── shared/
│   ├── components/
│   │   └── {component}/
│   ├── modules/
│   │   └── {module}/
│   └── libs/
├── routes/
└── stores/
```

Keep page- and module-owned state, types, and data-access files with their owners; the top-level `stores/` directory is only for application-level state. Place a component's implementation and private styles in its corresponding `{component}/` directory; simple components may also use a flat file structure.

- [web-project-structure] When adding or reorganizing files, preserve the project's and framework's established directory conventions and group related files by actual responsibility, not size or name. Create only the directories and layers currently needed; do not restructure the project to fit a template or extract files that only pass calls through. File ownership and dependencies must follow these responsibility boundaries:
  - Application owns application startup, global configuration, and cross-page capabilities, not specific page content or business operations.
  - Layout owns the application shell, such as shared navigation and headers, and the page outlet, not page business logic. Pages must not recreate shell regions already provided by their layout.
  - A page or related page group owns its content composition, business operations, and local state. Keep private components, types, data access, and styles nearby rather than dispersing them into global directories.
  - Components own presentation and interaction and may have local interaction state; modules own business rules, data, and workflows and may contain components; libraries provide technical capabilities independent of specific business domains.
  - Move components or modules and their private dependencies into shared scope only when real cross-feature reuse exists. Consumers access shared code through public interfaces; shared code must not depend back on private page implementations.

## Component Extraction

- [web-component-extraction] Extract components or modules to serve an independent responsibility, real reuse, isolation of complex logic, or independent composition. Do not split merely to reduce line count, move template code, or add a wrapper.
  - Prefer keeping the existing structure when content is simple and has no reuse need, or when it is tightly coupled to its parent and splitting would require extensive dependency passing.
  - Move the complete responsibility and its private dependencies together, adapting to consumers through inputs, outputs, and extension points. Do not share only appearance while duplicating business logic, or adapt through page-name or route branches. Keep components with a single consumer within their feature.

## API Access

- [web-api-layer] Pages and UI components call APIs through their feature's data-access layer rather than issuing requests directly. That layer reuses the project's existing client for authentication, base URLs, common headers, and error translation. Business code uses relative paths only and must not hardcode service addresses or proxy targets. When absolute URLs, a separate client, or another transport are necessary, explain the reason, ownership, and impact before implementation.

## Component Reuse And UI Libraries

- [web-reuse-order] Before implementing a required component or business capability, search and choose in this order: directly reusable project components/modules → extraction of existing project implementations with the same responsibility into reusable components/modules → available components in the project's UI library → custom implementation. Proceed to the next option only when the preceding option has no suitable solution with matching responsibility; do not skip the search and start writing a custom implementation.
  - When using library components, use public APIs and extension points first. Add styles or behavior only when those capabilities are insufficient; do not replace existing interaction and accessibility capabilities with separate DOM or event mechanisms.
  - Whether reused or custom, implementations must follow the project's existing information density, spacing, control sizing, interaction feedback, and responsive patterns.

## Data Sources, Data Flow, And Feedback

- [web-state-source] Each piece of business data is managed by the nearest owner that serves its usage scope, and shared consumers read the same authoritative source. Do not mistake logic reuse for shared state or introduce global state by default merely to reuse code.
  - Compute display and derived values from source data and update them automatically; do not create writable copies requiring manual synchronization. Editing copies are allowed for independent editing, cancellation, or deferred submission, but must have explicit initialization, submission, and discard behavior and must not directly modify shared saved data.
  - Mutations update or invalidate the relevant sources through operations provided by their owner, allowing consumers to receive results through the established reactivity mechanism. Do not conceal broken data flow through direct DOM changes, duplicate copies, or forced page refreshes.
- [web-feedback-owner] Forms or pages own their field and page feedback. System-wide feedback, global errors, and cross-page prompts use the application-level mechanism rather than separate implementations. Handle loading, empty, error, disabled, selected, success, and stale-data states explicitly rather than relying on incidental rendering branches.

## Dialog Action Order

- [web-dialog-action-order] When a dialog contains both applying and abandoning actions, place applying actions (such as save, delete, or apply filters) on the left and abandoning actions (such as cancel or close) on the right in LTR layouts. Do not add a cancel button to an interaction that has no abandoning action. Follow a different product convention when the user has confirmed it.

## CSS And Style Ownership

- [web-style-colocation] The same component owns its DOM and private styles. Organize, move, and scope styles with the component according to framework conventions; do not move them into unrelated files to shorten a file or promote them globally for a local need. Public styles contain only application foundations and stable shared visual rules. Reuse existing themes, tokens, component defaults, or shared components before adding public configuration; do not add it for one-page exceptions.
- [web-style-replacement] When adjusting styles, change the original declarations and remove superseded rules. Do not counteract the old implementation by appending duplicate declarations, increasing specificity, or forcing overrides; explicit variants for themes, breakpoints, and interaction states remain valid. Apply spacing and sizing to the element that owns the layout rather than adding wrappers for individual style properties. Prefer existing semantic configuration and responsive capabilities; fixed values are allowed when required by product or platform constraints.

## Removing Obsolete Implementations

- [web-remove-obsolete] When removing or replacing functionality or visual structure, also remove the DOM, styles, state, logic, and references made unused by the current change. Do not permanently hide old nodes instead of removing them; temporary hiding with a clear interaction purpose is not an obsolete implementation.

## Interaction, Forms, And Accessibility

- [web-accessibility] When adding or adjusting interactions, use semantic elements and existing UI-library components. Do not replace control capabilities with click handlers on generic containers or remove interaction feedback for visual effects.
  - Every form control and icon-only control must have an accessible name. Form controls must preserve validation, disabled and submission states, and error feedback.
  - Preserve keyboard navigation, input method composition, and overlay trigger semantics, focus restoration, and Escape behavior. Focus, hover, active, selected, loading, and disabled states must have visible feedback.

## Bidirectional And RTL Layout

- [web-logical-direction] Layouts must support bidirectional interfaces. Direction, directional spacing, and alignment use a shared configuration or token source; do not repeat RTL detection in pages and components. Prefer logical properties such as inline/block/start/end; use physical properties such as left/right only for visual requirements that explicitly depend on physical direction.

## Internationalization And User-Visible Content

- [web-i18n] Application interface text, including titles, navigation, control labels, placeholders, status messages, validation messages, and error fallback text, must use the project's existing internationalization mechanism. External or user-provided business content and runtime logs are exempt; localized business data from the backend must not replace interface text internationalization.
  - Messages must compile under the project's configured syntax. Reuse message keys only when their meanings and interpolation contracts match; do not merge them merely because the text is identical.
  - Preserve useful source details in error feedback and sanitize sensitive information. Do not replace specific errors with generic translated messages.

## Formatting And Change Scope

- [web-formatting] The project formatter is the sole formatting authority for frontend source and configuration files. Do not manually align code or change configuration for personal preferences. Limit formatting to files involved in the task and run existing formatting checks before delivery.

## Test Design And Use

- [web-persistent-test-scope] Permanent tests verify only data flow and stable business behavior, not DOM, styles, display copy, screenshots, or UI/UX interaction presentation. Classify by assertion content; using a browser or mounting a component does not determine the category. Cover relevant success, failure, and boundary behavior according to change risk, reuse existing tests first, and do not substitute test count or coverage for value or introduce production abstractions for testing convenience.
- [web-data-flow-tests] Data-flow tests must execute the actual implementation and verify the inputs, processing, state changes, and consumer results involved in the current change. When risk spans multiple stages, cover the necessary collaboration; a correct isolated function or an observed call does not prove the entire data flow is correct.
  - Dependencies outside the test scope may be replaced. Do not mock the process being tested or rewrite the implementation in the test.
  - Expected results come from requirements and business contracts and must distinguish correct from incorrect behavior. Do not copy the implementation, generate expectations with the code under test, or bind assertions to source syntax, variable names, internal steps, or component organization. When the business contract is unchanged, do not adjust expectations to match the current implementation merely because of refactoring or test failures.
- [web-temporary-ui-tests] Verify UI/UX during the current development task through manual checks, browser checks, or temporary automation. Keep temporary tests and supporting assets outside formal test directories, exclude them from the feature commit, and remove them after verification. Not retaining UI/UX tests does not permit skipping acceptance checks.
- [web-verification] Choose the smallest set of checks sufficient to verify the current change. Report the actual coverage and unverified areas of static checks, business tests, and UI/UX acceptance separately; a passing result in one category must not stand in for verification of another.

## Final Review

Before delivery, check responsibility boundaries, behavior, and verification results against the rules applicable to the current change and correct deviations. Do not expand the change scope merely for self-review.
