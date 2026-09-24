Author: ailtariel@gmail.com
Updated: 2026-09-24

# Repository-Level AI Coding Specification

This specification defines high-priority engineering standards for AI-assisted coding tasks within the target workspace or affected repository.

Unless explicitly requested by the user, these rules take precedence over any conflicting suggestions from other skills.

## Rule Usage

- This document is a mandatory repository-wide specification, not an on-demand skill. Read this core once for a coding task; apply relevant clauses and load specialized workflows only when routed. Reuse unchanged material already read in this conversation.
- When multiple rule blocks apply to a task, all of them must be followed simultaneously. For non-security implementation decisions, weigh trade-offs according to [priority]. Security risks must follow [security-confirmation].
- Rule tags are intended for delivery notes, reviews, and self-check references. Do not expand implementation scope merely to satisfy a tag.

## General Rules

- [authorization-and-completion] Authorization persists across the conversation. An implementation or fix request includes necessary in-scope investigation, design refinement, edits, relevant verification, and fixing failures caused by those edits; a review-only or design-only request does not authorize implementation. Pause only dependent work for unresolved, unauthorized material product, architecture, dependency, public-contract, or irreversible-action decisions; continue independent authorized work. Complete authorized preparation before asking, and provide a concrete proposal, impact, and recommendation. If a rule causes a pause, identify its file and clause. Complete the user goal, necessary checks, and related fixes, and disclose unverified areas; do not stop at a first implementation.

- [priority] Explicit user requirements > correctness > maintainability > minimal changes > security > style and simplicity
- [minimal-context]
  - Prioritize reading the minimum set of files directly related to the current task.
  - Do not scan the entire repository without purpose, read large amounts of unrelated files, or repeatedly read files already confirmed to be irrelevant.
- [plan-first] Before coding, briefly state the intended change and impact. Use a plan when complex dependencies, important trade-offs, or implementation phases need to be retained; do not create a formal plan for simple changes. Planning does not itself require approval. File count, line count, or multiple independent subtasks do not trigger confirmation. Apply [authorization-and-completion] to unresolved decisions.
- [security-confirmation] Communicate evidenced security risks directly relevant to the task. Proceed with already-authorized security fixes; seek a decision for unapproved changes to functionality, architecture, deployment, or security policy. Localized, low-risk hardening with clear behavior and no public contract change may proceed. Do not introduce approval gates or expand scope because of hypothetical risks.
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
- [abstraction-exception] For backend code, extract only for a clear responsibility boundary, real reuse, or necessary isolation of complex logic, preserving confirmed behavior and improving overall comprehension and maintenance cost. Reuse existing capabilities first; avoid layers that merely forward calls. Reduced line count is a possible benefit, not a prerequisite.
- [validation-boundary] Validate at external-input and actual trust boundaries. Do not repeat identical checks or fallback handling within the same trusted flow. Validate again at a new trust boundary or when an operation requires a different business invariant. Code-layer count does not determine validation placement.
- [wrapper-pass-through] When wrapping functions, objects, or service calls, pass through their return values and errors unchanged by default, preserving how errors propagate. Do not filter fields, restructure or rewrap results, replace errors, or modify the original returned data without an explicit requirement or design basis. Any transformation, such as adapting to a defined contract or sanitizing sensitive information, must be limited to the changes required for that purpose, preserving all other information and error semantics.
- [no-silent-failure] Silent failures are prohibited. Unless the user explicitly agrees to degradation behavior, errors should be exposed clearly through logs or returned responses.
- [api-error-detail] When returning API error responses, preserve meaningful error codes or error text such as `error`, `text`, or `message` from the source whenever available. If the content contains sensitive information, sanitize it before returning.
- [try-catch] Do not overuse try...catch. Use it only in the following situations:
  - Execution must continue even after failure
  - Error messages need to be unified/formatted
  - Resource cleanup or transactional consistency is required (e.g. rollback, releasing connections)
- [public-contract] Do not modify public APIs, database schemas, configuration formats, or environment variable names unless explicitly requested by the user.
- [dependency-gate] Do not introduce unapproved new dependencies. If a new dependency is truly necessary and not already authorized, explain the reason and wait for confirmation first.

## OS and Tools

- [rg-first] For operations that `rg` is suited for, such as finding files, searching text, or counting matches, try `rg` first even on Windows unless `rg` is already known to be unavailable. Prefer `rg --files` for file discovery and `rg` for content search before falling back to PowerShell traversal or `Select-String`.
- [powershell-utf8] When using PowerShell to read or write text files, explicitly pass `-Encoding UTF8` by default for commands that support it, such as `Get-Content`, `Set-Content`, `Add-Content`, `Out-File`, `Import-Csv`, and `Export-Csv`.
- [powershell-raw-text] When reading a whole text file in PowerShell for analysis, prefer `Get-Content -Raw -Encoding UTF8`; without `-Raw`, PowerShell returns an array of lines and may change downstream behavior.
- [powershell-native-quoting] Be careful with PowerShell parsing when passing regexes, pipes, quotes, braces, or semicolons to native tools. Prefer single-quoted patterns, `rg -F` for fixed-string searches, or one simple command per invocation when shell parsing could change the argument.
- [powershell-aliases] Do not assume common Unix command names have Unix semantics in PowerShell. Commands such as `curl`, `wget`, `cat`, `ls`, and `rm` may be aliases or behave differently; prefer the explicit native command or the intended PowerShell cmdlet.
- [rg-exit-code] Treat `rg` exit code `1` as "no matches found", not necessarily as a command failure. Exit codes greater than `1` indicate an actual error.

## Large Tasks

When this workflow applies, read [large-tasks](large-tasks.md).

## Design and Implementation Documents

- [functional-design] Functional design reasoning, autonomy, scope, conflict review, and design document content must follow [`functional-design.md`](functional-design.md).
- [design-execution-separation] In principle, design documents and implementation documents should be written separately.
- [doc-lightweight-exception] For smaller tasks with simple design choices that are expected to be completed in one implementation pass, design and implementation documents may be merged even if [large-task-threshold] is met. The merged document should still distinguish design decisions from the implementation plan. If the task expands or requires multi-phase implementation, restore separate documents.
- [task-doc-location] Save design and implementation documents in an existing same-type documentation path in the target workspace or affected repository first. If none exists, use `docs/<module-or-task>/` under the applicable target repository root. Design document filenames should start with `[design]`; implementation document filenames should start with `YYYY-MM-DD`.
- [design-confirmation-gate] Wait after design only when the user requested a design review before implementation or an important decision remains unauthorized. When end-to-end implementation is authorized and key decisions are settled, design refinement and document completion do not create another approval gate.
- [design-freeze] After the user confirms the design document, it becomes the design baseline for the current task by default. During implementation, do not change the design merely because a "cleaner", "more generic", or "more extensible" implementation is found. Reopen design discussion only when a design error, implementation impossibility, major risk, new user requirement, or explicit user request to adjust the design is found. An explicit new user direction settles the corresponding change; request renewed confirmation only for material departures not already authorized. Continue independent work within the baseline.
- [execution-doc-scope] The implementation document should contain concrete implementation details and primarily answer "how to complete it", including affected files, code change plan, phase breakdown, review checklist, verification plan, and commit plan.
- [execution-doc-confirmation] Implementation documents need no separate confirmation by default. Continue after necessary planning when implementation is already authorized and no blocking decision remains.
## Bug Fix Rules

- [root-cause-first] Analyze the root cause before deciding on a fix.
- [simple-bugfix] For localized bug fixes with a clear root cause and solution, modifications may proceed directly after briefly explaining the root cause, solution, and affected files. This remains true when the fix corrects erroneous behavior, updates tightly coupled tests or supporting files, touches multiple files, or exceeds an arbitrary line-count threshold, provided it introduces no unresolved design decision, dependency change, or public contract change.
- [bugfix-plan-gate] Continue investigating uncertain causes; use proportionate planning for broad impact, complex dependencies, or phased work. Request a decision only for unresolved, unauthorized material behavior, public-contract, dependency, or architecture choices. Investigation and planning are not approval gates.
- [fallback-last] Automatic degradation/fallback behavior must always be the last option.
- [no-hardcoded-fix] Hardcoded fixes require informed user approval; existing explicit approval remains valid under [authorization-and-completion].
- [environment-fix-first] For missing tools, missing configuration, inaccessible external services, and similar issues, prioritize environment/configuration-based fixes:
  - Automatically fix the issue if possible
  - If automatic repair is impossible, clearly explain what is missing
  - Do not bypass the issue through exception swallowing or compatibility workarounds
- [fallback-confirmation] Automatic degradation/fallback behavior requires evidence that the preceding applicable paths are infeasible and informed user approval. Do not request the same approval again when that behavior is already explicitly authorized.
- [bugfix-delivery] Every delivery must include: root cause, solution, impact scope, and verification results.

## Cross-Project Feature Porting

When this workflow applies, read [feature-porting](feature-porting.md).

## Code Style, Comments, and Logging

- [readability] Prioritize readability.
- [english-code-text] Comments, logs, and documentation should use English by default unless explicitly requested otherwise by the user.
- [chinese-markdown-prose-wrap] Do not hard-wrap Chinese Markdown prose to a fixed column width. Keep each paragraph and list item on one physical line unless a Markdown structural boundary, code block, table, or intentional hard break requires a new line. When formatting Chinese Markdown, use `proseWrap: never` or equivalent behavior.
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

- [frontend-specification] All frontend tasks must follow
  [`web-frontend.md`](web-frontend.md). It is the authoritative
  repository-level source for framework-neutral web frontend architecture,
  component and library selection, feature boundaries, state flow, styling,
  interaction, accessibility, internationalization, formatting, and
  verification. Framework and UI-library skills supplement that specification
  with implementation guidance and do not override it.

## Testing and Verification Constraints

- [test-addition] By default, do not add tests for low-risk mechanical modifications. When business behavior, public APIs, permissions, routes, forms, state transitions, async/concurrency/session/token logic, bugfix regressions, security, or data consistency behavior changes — or when explicitly requested by the user — prioritize adding the smallest relevant tests.
- [reuse-tests] Reuse existing tests whenever possible; do not prioritize creating new test files.
- [invariant-tests] Do not write tests for invariants already guaranteed by upstream validation, type constraints, or database constraints, especially within trusted internal data flows. This rule does not apply to external input boundaries, permissions, security, or serialization/deserialization boundaries.
- [no-test-only-abstraction] Do not introduce helpers, wrappers, composables, or service abstractions solely for testing convenience.
- [verification-ladder] Select the smallest sufficient combination of checks for the change risk and failure mechanism, covering modified behavior and reasonably inferable direct impact. Static reasoning, typecheck, lint, unit, integration, E2E, and full-suite tests are options, not mandatory sequential levels. Stop expanding verification once required checks pass and relevant concerns are resolved.
- [full-suite] Full suite runs should only occur when shared infrastructure, global configuration, public types, auth/session/permission logic, schemas/migrations, or multi-module changes are involved.
- [ui-visual-test] UI visual adjustments should not add tests by default. Use typecheck/lint and manual/browser visual confirmation instead.
- [e2e-scope] E2E tests should only cover real user workflows, not simple color, spacing, text, icon, or prop modifications.
- [snapshot] Snapshot updates are prohibited by default unless the UI structure changes and is directly related to the requirement.
- [test-expectation] Do not modify test expectations merely to make tests pass unless the original test is confirmed to be incorrect.
- [unrelated-failures] When tests fail, determine whether the failure is related to the current modification first. Do not casually fix unrelated failures.
- [no-repeat-verification] Repeat a passed check only when relevant code, dependencies, configuration, environment, or fixtures changed, or concrete evidence calls the result into question.
- [test-unavailable] If tests cannot be executed, explain why and provide suggested verification commands.
- [verification-report] Final delivery must explain which verifications were executed, which were not executed, and why.
- [final-review] Before final delivery, verify:
  - Whether the implementation satisfies the user's requirements
  - Whether unnecessary modifications were introduced
  - Whether relevant constraints in this specification were followed
  - Whether necessary verification has been completed
  - Whether any verification risks or impact scope explanations are missing
