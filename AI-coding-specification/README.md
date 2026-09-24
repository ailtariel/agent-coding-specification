# AI Coding Specification

This directory contains default specifications for AI-assisted functional design and implementation in the target workspace or affected repository. Before starting a task, classify its type and read the corresponding specifications.

## Path Resolution And Target Scope

- Unless a rule explicitly says otherwise, references to the repository, project, workspace, current directory, root, source tree, configuration, tests, or documentation mean the target workspace or affected repository where the task is being performed, not the repository that stores this canonical specification.
- Relative implementation or artifact paths such as `docs/`, `src/`, `tests/`, `backend/`, and `web/` must be resolved from the applicable target workspace or affected repository root. For multi-repository tasks, resolve each path within the repository that owns the affected artifact.
- Relative Markdown links between specification documents, such as [`coding-specification.md`](coding-specification.md), are the exception: resolve them relative to the specification file containing the link.
- When the task is maintaining this specification repository itself, this repository is also the target repository, so its workspace paths apply normally.

## Task Types and Specification Routing

- **Functional design tasks:** Analyze requirements, complete or compare approaches, or create or modify functional design documents. Read [`functional-design.md`](functional-design.md).
- **Implementation tasks:** Modify code, configuration, databases, deployment assets, or other implementation artifacts. Read [`coding-specification.md`](coding-specification.md) once and apply relevant clauses. For web work read [`web-frontend.md`](web-frontend.md); for complex phased work read [`large-tasks.md`](large-tasks.md); for porting an existing feature read [`feature-porting.md`](feature-porting.md). Do not load unrelated workflows.
- **Mixed tasks:** Follow the design and implementation rules for their respective work. Existing implementation authorization persists through design refinement; pause only when the user requested a design approval gate or a material decision remains unauthorized.
- If the task type changes during execution, read the specifications applicable to the new stage before continuing.

Review-only and design-only requests do not authorize implementation. An end-to-end implementation request does authorize necessary in-scope design refinement, edits, verification, and related fixes. Reuse unchanged rules and documents already read in this conversation. Review tasks read the rules governing the reviewed artifacts; documentation-only edits use the relevant document rather than every implementation workflow.
