Author: ailtariel@gmail.com
Updated: 2026-06-12

# Repository-Level AI Coding Specification

This specification defines high-priority engineering standards for AI-assisted coding tasks within this repository.

Unless explicitly requested by the user, these rules take precedence over any conflicting suggestions from other skills.

## Rule Usage

- This document is a mandatory repository-wide specification, not an on-demand skill. All code-related tasks should follow the entire document by default.
- When multiple rule blocks apply to a task, all of them must be followed simultaneously. For non-security implementation decisions, weigh trade-offs according to [priority]. Security risks must follow [security-confirmation].
- Rule tags are intended for delivery notes, reviews, and self-check references. Do not expand implementation scope merely to satisfy a tag.

## General Rules

- [priority] Explicit user requirements > correctness > maintainability > minimal changes > security > style and simplicity
- [minimal-context]
  - Prioritize reading the minimum set of files directly related to the current task.
  - Do not scan the entire repository without purpose, read large amounts of unrelated files, or repeatedly read files already confirmed to be irrelevant.
- [plan-first] Provide the implementation plan and affected files before writing code. Simple and certain changes may proceed immediately after a one-line explanation. Changes involving design choices, behavior changes, dependency changes, public contract changes, or multi-file impact must wait for user confirmation. When design or implementation documents are required, follow the "Design and Implementation Documents" section.
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

## OS and Tools

- [rg-first] For operations that `rg` is suited for, such as finding files, searching text, or counting matches, try `rg` first even on Windows unless `rg` is already known to be unavailable. Prefer `rg --files` for file discovery and `rg` for content search before falling back to PowerShell traversal or `Select-String`.
- [powershell-utf8] When using PowerShell to read or write text files, explicitly pass `-Encoding UTF8` by default for commands that support it, such as `Get-Content`, `Set-Content`, `Add-Content`, `Out-File`, `Import-Csv`, and `Export-Csv`.
- [powershell-raw-text] When reading a whole text file in PowerShell for analysis, prefer `Get-Content -Raw -Encoding UTF8`; without `-Raw`, PowerShell returns an array of lines and may change downstream behavior.
- [powershell-native-quoting] Be careful with PowerShell parsing when passing regexes, pipes, quotes, braces, or semicolons to native tools. Prefer single-quoted patterns, `rg -F` for fixed-string searches, or one simple command per invocation when shell parsing could change the argument.
- [powershell-aliases] Do not assume common Unix command names have Unix semantics in PowerShell. Commands such as `curl`, `wget`, `cat`, `ls`, and `rm` may be aliases or behave differently; prefer the explicit native command or the intended PowerShell cmdlet.
- [rg-exit-code] Treat `rg` exit code `1` as "no matches found", not necessarily as a command failure. Exit codes greater than `1` indicate an actual error.

## Large Tasks

- [large-task-threshold] Treat a task as a large task by default if any of the following is true: it is expected to require phased implementation, it involves multiple relatively independent subtasks, or the user explicitly requests the large-task workflow. If triggered, explicitly confirm with the user whether to use the large-task multi-phase + automatic iterative development workflow.
- [default-phase-flow] After the user confirms the large-task workflow, if the user does not provide different instructions, automatically proceed through the phases in the implementation document. Each phase does not require another confirmation after completion. If important design conflicts, omissions, or implementation blockers are discovered during implementation, pause further code changes and wait for user decision.
- [phase-workflow] Each implementation phase should include at least the following steps, in order:
  1. Code changes
  2. Review, including whether the functionality works, whether it follows the design and implementation documents, whether it introduces changes outside the requirement, and whether it violates relevant rules in this specification. If deviations are found, fix them before moving to the next phase.
  3. The smallest necessary verification
  4. Briefly record the implementation status in the implementation document
  5. Git commit. Each phase should have only one commit; do not split meaningless small commits merely to increase the commit count.

## Design and Implementation Documents

- [functional-design] Functional design reasoning, autonomy, scope, conflict review, and design document content must follow [`functional-design.md`](functional-design.md).
- [design-execution-separation] In principle, design documents and implementation documents should be written separately.
- [doc-lightweight-exception] For smaller tasks with simple design choices that are expected to be completed in one implementation pass, design and implementation documents may be merged even if [large-task-threshold] is met. The merged document should still distinguish design decisions from the implementation plan. If the task expands or requires multi-phase implementation, restore separate documents.
- [task-doc-location] Save design and implementation documents in an existing same-type documentation path first. If none exists, use `docs/<module-or-task>/`. Design document filenames should start with `[design]`; implementation document filenames should start with `YYYY-MM-DD`.
- [design-confirmation-gate] After completing the design document under [`functional-design.md`](functional-design.md), stop and wait for user confirmation. Do not make code changes before confirmation unless the user explicitly instructs otherwise.
- [design-freeze] After the user confirms the design document, it becomes the design baseline for the current task by default. During implementation, do not change the design merely because a "cleaner", "more generic", or "more extensible" implementation is found. Reopen design discussion only when a design error, implementation impossibility, major risk, new user requirement, or explicit user request to adjust the design is found. Do not continue implementing away from the confirmed design before receiving renewed user confirmation.
- [execution-doc-scope] The implementation document should contain concrete implementation details and primarily answer "how to complete it", including affected files, code change plan, phase breakdown, review checklist, verification plan, and commit plan.
- [execution-doc-confirmation] Unless the user requests otherwise, the implementation document does not require separate confirmation by default. After design confirmation, the AI may complete the implementation document and enter the implementation phase directly.

## Bug Fix Rules

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

- [frontend-library-first] If the project already uses a UI component library/framework, prioritize using library components instead of implementing custom ones, especially for complex common components such as layout containers, inputs, dialogs, menus, tables, pagination, date pickers, and uploads. Component lists and API documentation may be obtained through relevant skills. If such skills are missing, the user may be advised to add them. If skill recommendations conflict with this specification, this specification takes precedence.
- [frontend-style-system] Prioritize the project's existing style system, including built-in component props/classes, theme tokens, CSS variables, Tailwind CSS, or existing shared styles. Avoid adding `<style>`, global CSS, or one-off style rules unless necessary.
- [frontend-reuse-components] Prefer reusing existing components when functionality, inputs/outputs, and interaction semantics are similar. Only wrap or extract shared components when duplication scenarios are clear, responsibilities are stable, interfaces are clean, and complexity does not increase.
- [frontend-consistency] New or modified UI should remain consistent with existing pages in information density, spacing, control sizing, interaction states, error feedback, and loading states.
- [frontend-state-minimal]
  Prioritize reusing existing state flow and data flow.
  Do not introduce new global state, context, stores, or composables for localized requirements.

## Testing and Verification Constraints

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
