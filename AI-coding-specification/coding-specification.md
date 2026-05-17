Author: ailtariel@gmail.com
Updated: 2026-05-17

# Repository-Level AI Coding Specification

This specification defines high-priority engineering standards for AI-assisted coding tasks within this repository.

Unless explicitly requested by the user, these rules take precedence over any conflicting suggestions from other skills.

## Rule Usage

- This document is a mandatory repository-wide specification, not an on-demand skill. All code-related tasks should follow the entire document by default.
- The "Applicable Scenarios", "Key Triggers", and "Execution Requirements" under each rule block help the AI map concrete tasks to relevant rules precisely. They are not used to exclude other applicable rules.
- When multiple rule blocks apply to a task, all of them must be followed simultaneously. For non-security implementation decisions, weigh trade-offs according to [priority]. Security risks must follow [security-confirmation].
- Rule tags are intended for delivery notes, reviews, and self-check references. Do not expand implementation scope merely to satisfy a tag.

## General Rules

Applicable Scenarios: All AI-assisted code modification tasks.

Key Triggers: Implementation, refactoring, abstraction, dependencies, public APIs, schemas, configuration, environment variables, error handling, security risks.

Execution Requirements: Clarify the implementation plan and affected files before coding. Keep changes minimal and necessary. Do not introduce unconfirmed behavior, dependencies, or public contract changes.

- [priority] Explicit user requirements > correctness > maintainability > minimal changes > security > style and simplicity
- [minimal-context]
  - Prioritize reading the minimum set of files directly related to the current task.
  - Do not scan the entire repository without purpose, read large amounts of unrelated files, or repeatedly read files already confirmed to be irrelevant.
- [plan-first] Provide the implementation plan and affected files before writing code. Simple and certain changes may proceed immediately after a one-line explanation. Changes involving design choices, behavior changes, dependency changes, public contract changes, or multi-file impact must wait for user confirmation.
- [security-confirmation] Security risks must be explicitly identified and communicated, but implementation decisions involving functionality, architecture, deployment, or security strategy must be confirmed by the user.
  - AI should proactively point out security risks and possible mitigation directions. However, repository-level AI coding usually lacks complete context about architecture, deployment, compliance, and business risk. Before receiving user confirmation, do not independently implement functionality-, architecture-, deployment-, or policy-level security measures.
  - Only localized, low-risk security hardening with clear behavior and no public contract changes may be applied by default.
- [behavior-preservation]
  Unless the task explicitly requires behavior changes, preserve existing runtime behavior, exception behavior, execution timing, return structures, and side effects by default.
  If the current implementation already works correctly and the task does not require changing that behavior, do not rewrite it merely because another implementation appears "cleaner", "more modern", or "more generic".
- [no-unrelated-churn] Do not casually refactor, reformat, reorder imports, or rename things unless directly related to the current task.
- [no-speculation]
  Do not make changes without a current requirement source:
  - Do not design for future extensibility in advance. Only implement confirmed requirements; do not implement unrequested features.
  - Do not refactor existing code merely because it "might be useful in the future", "might need future extensibility", or could "improve the structure while we're here".
  - Do not add TODO/FIXME comments without a clear plan or requirement source.
- [no-extra-abstraction] Do not introduce unnecessary abstraction layers (no unnecessary classes, interfaces, wrappers, or helpers).
- [abstraction-exception] Abstraction/extraction is allowed only if all of the following are true simultaneously: behavior remains unchanged, readability does not decrease, and total lines of code are significantly reduced. If line count increases instead of decreases, avoid abstraction in most cases.
  - Reuse existing utilities first. Only extract new reusable components when this rule is satisfied.
- [validation-boundary] Avoid excessive defensive programming: validate external input, trust internal data flow. External input should only be validated at the entry point; internal flows should follow established contracts without repeated fallback handling. External input should only be validated once per execution chain.
- [no-silent-failure] Silent failures are prohibited. Unless the user explicitly agrees to degradation behavior, errors should be exposed clearly through logs or returned responses.
- [api-error-detail] When returning API error responses, preserve meaningful error codes or error text such as `error`, `text`, or `message` from the source whenever available. If the content contains sensitive information, sanitize it before returning.
- [try-catch] Do not overuse try...catch. Use it only in the following situations:
  - Execution must continue even after failure
  - Error messages need to be unified/formatted
  - Resource cleanup or transactional consistency is required (e.g. rollback, releasing connections)
- [public-contract] Do not modify public APIs, database schemas, configuration formats, or environment variable names unless explicitly requested by the user.
- [dependency-gate] Do not introduce new dependencies. If a new dependency is truly necessary, explain the reason and wait for confirmation first.

## Bug Fix Rules

Applicable Scenarios: Bug fixes, exception investigation, test failures, runtime failures, missing tools, missing configuration, inaccessible external services.

Key Triggers: Bugfixes, fixes, errors, failures, exceptions, hardcoding, fallback, compatibility, degradation, bypasses.

Execution Requirements: Analyze the root cause first. For complex or high-impact fixes, provide a plan before implementation. Deliveries must include root cause, solution, impact scope, and verification results.

- [root-cause-first] Analyze the root cause before deciding on a fix.
- [simple-bugfix] For simple and certain bug fixes, modifications may proceed directly after briefly explaining the root cause, solution, and affected files.
- [bugfix-plan-gate] If the modification involves design choices, behavior changes, dependency changes, public contract changes, or multi-file impact, provide a plan and wait for confirmation first. Changes exceeding 10 lines should be treated as requiring additional attention by default.
- [fallback-last] Automatic degradation/fallback behavior must always be the last option.
- [no-hardcoded-fix] Do not use hardcoded fixes without informing the user and receiving approval first.
- [environment-fix-first] For missing tools, missing configuration, inaccessible external services, and similar issues, prioritize environment/configuration-based fixes:
  - Automatically fix the issue if possible
  - If automatic repair is impossible, clearly explain what is missing
  - Do not bypass the issue through exception swallowing or compatibility workarounds
- [fallback-confirmation] Automatic degradation/fallback behavior may only be considered after all previous paths are confirmed infeasible, and only after user confirmation.
- [bugfix-delivery] Every delivery must include: root cause, solution, impact scope, and verification results.

## Code Style, Comments, and Logging

Applicable Scenarios: All changes related to code, comments, logs, technical documentation, naming, formatting, and file structure.

Key Triggers: Comments, logs, naming, formatting, hardcoding, oversized files, readability, sensitive fields.

Execution Requirements: Keep things readable, restrained, and consistent. Avoid unrelated formatting changes. Comments should explain reasons. Logs must not expose sensitive information.

- [readability] Prioritize readability.
- [english-code-text] Comments, logs, and documentation should use English by default unless explicitly requested otherwise by the user.
- [file-size] When a single file exceeds 500 lines, consider splitting it only if all of the following conditions are met (this is not a mandatory requirement):
  - Responsibilities are clearly mixed together
  - Splitting will not significantly increase comprehension cost or file navigation complexity
  - The current modification already touches the related areas
- [comments] Comment guidelines:
  - Add comments for complex, public, or non-obvious logic
  - Comments for complex public functions or non-obvious functions should explain "why", not repeat what the code already clearly expresses
  - Python code does not need docstrings unless required by testing tools; generally prefer `#` comments before function declarations
  - Important logical branches, business constraints, and non-obvious conditions must be commented
- [concise-logs] Logs should contain only key information while remaining concise and readable.
- [sensitive-logs] Logs should generally avoid outputting tokens, passwords, secrets, or full sensitive user fields. Mask them when necessary.
- [avoid-hardcode] Avoid hardcoding whenever possible.
  - Values with clear environment differences, deployment differences, user configuration requirements, or multi-location reuse should be considered for parameterization/configuration.
  - If any hardcoding is introduced, it must be explicitly disclosed to the user.

## Frontend

Applicable Scenarios: All frontend-related modifications involving pages, components, forms, layouts, styles, and interaction state.

Key Triggers: UI, components, pages, forms, layouts, styles, component libraries, reusable components.

Execution Requirements: Prioritize the project's existing component libraries, style systems, and components. Maintain interaction consistency. Avoid duplicate implementations and avoid introducing abstractions for one-time use.

- [frontend-library-first] If the project already uses a UI component library/framework, prioritize using library components instead of implementing custom ones, especially for complex common components such as layout containers, inputs, dialogs, menus, tables, pagination, date pickers, and uploads. Component lists and API documentation may be obtained through relevant skills. If such skills are missing, the user may be advised to add them. If skill recommendations conflict with this specification, this specification takes precedence.
- [frontend-style-system] Prioritize the project's existing style system, including built-in component props/classes, theme tokens, CSS variables, Tailwind CSS, or existing shared styles. Avoid adding `<style>`, global CSS, or one-off style rules unless necessary.
- [frontend-reuse-components] Prefer reusing existing components when functionality, inputs/outputs, and interaction semantics are similar. Only wrap or extract shared components when duplication scenarios are clear, responsibilities are stable, interfaces are clean, and complexity does not increase.
- [frontend-consistency] New or modified UI should remain consistent with existing pages in information density, spacing, control sizing, interaction states, error feedback, and loading states.
- [frontend-state-minimal]
  Prioritize reusing existing state flow and data flow.
  Do not introduce new global state, context, stores, or composables for localized requirements.

## Testing and Verification Constraints

Applicable Scenarios: All code modification deliveries, as well as testing, build, CI, and verification-related tasks.

Key Triggers: Tests, verification, typecheck, lint, pytest, E2E, snapshot, CI, regression, inability to run tests, full suite.

Execution Requirements: Prioritize the smallest relevant verification scope. Escalate verification levels based on risk. Final delivery must explain which verifications were performed, which were not performed, and why.

- [test-addition] By default, do not add tests for low-risk mechanical modifications. When business behavior, public APIs, permissions, routes, forms, state transitions, async/concurrency/session/token logic, bugfix regressions, security, or data consistency behavior changes — or when explicitly requested by the user — prioritize adding the smallest relevant tests.
- [reuse-tests] Reuse existing tests whenever possible; do not prioritize creating new test files.
- [invariant-tests] Do not write tests for invariants already guaranteed by upstream validation, type constraints, or database constraints, especially within trusted internal data flows. This rule does not apply to external input boundaries, permissions, security, or serialization/deserialization boundaries.
- [no-test-only-abstraction] Do not introduce helpers, wrappers, composables, or service abstractions solely for testing convenience.
- [verification-ladder] Prioritize the minimum relevant verification set for the current modification, covering modified behavior and reasonably inferable direct impact areas. Escalate verification levels based on risk in the following order when necessary: static reasoning → typecheck → lint → targeted unit test → targeted integration test → E2E → full suite. If the current verification level is already sufficient to validate the change or determine the failure cause, do not escalate further.
- [full-suite] Full suite runs should only occur when shared infrastructure, global configuration, public types, auth/session/permission logic, schemas/migrations, or multi-module changes are involved.
- [ui-visual-test] UI visual adjustments should not add tests by default. Use typecheck/lint and manual/browser visual confirmation instead.
- [e2e-scope] E2E tests should only cover real user workflows, not simple color, spacing, text, icon, or prop modifications.
- [snapshot] Snapshot updates are prohibited by default unless the UI structure changes and is directly related to the requirement.
- [test-expectation] Do not modify test expectations merely to make tests pass unless the original test is confirmed to be incorrect.
- [unrelated-failures] When tests fail, determine whether the failure is related to the current modification first. Do not casually fix unrelated failures.
- [no-repeat-verification] Do not rerun already-passed verifications unless related files have changed again.
- [test-unavailable] If tests cannot be executed, explain why and provide suggested verification commands.
- [verification-report] Final delivery must explain which verifications were executed, which were not executed, and why.
- [final-review] Before final delivery, verify:
  - Whether the implementation satisfies the user's requirements
  - Whether unnecessary modifications were introduced
  - Whether relevant constraints in this specification were followed
  - Whether necessary verification has been completed
  - Whether any verification risks or impact scope explanations are missing
