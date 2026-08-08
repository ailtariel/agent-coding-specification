# AI Coding Specification

This directory contains default specifications for AI-assisted functional design and implementation in the target workspace or affected repository. Before starting a task, classify its type and read the corresponding specifications.

## Path Resolution And Target Scope

- Unless a rule explicitly says otherwise, references to the repository, project, workspace, current directory, root, source tree, configuration, tests, or documentation mean the target workspace or affected repository where the task is being performed, not the repository that stores this canonical specification.
- Relative implementation or artifact paths such as `docs/`, `src/`, `tests/`, `backend/`, and `web/` must be resolved from the applicable target workspace or affected repository root. For multi-repository tasks, resolve each path within the repository that owns the affected artifact.
- Relative Markdown links between specification documents, such as [`coding-specification.md`](coding-specification.md), are the exception: resolve them relative to the specification file containing the link.
- When the task is maintaining this specification repository itself, this repository is also the target repository, so its workspace paths apply normally.

## Task Types and Specification Routing

- **Functional design tasks:** Analyze requirements, complete or compare approaches, or create or modify functional design documents. Read [`functional-design.md`] if it exists.(functional-design.md).
- **Implementation tasks:** Modify code, configuration, databases, deployment assets, or other implementation artifacts. Read [`coding-specification.md`](coding-specification.md) if it exists, and any specialized implementation specifications in this directory that apply to the task.
- **Mixed tasks:** Complete the design under the functional design specification and obtain user confirmation before proceeding under the implementation specification, unless the user explicitly requests otherwise.
- If the task type changes during execution, read the specifications applicable to the new stage before continuing.

Autonomous decisions permitted during the design stage constitute design outcomes only. They do not automatically authorize corresponding code or other implementation changes.
