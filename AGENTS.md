# Agent Working Rules

These rules are mandatory for AI agents working within the scope that contains this `AGENTS.md`.

## Authority and Priority

The files under `AI-coding-specification/` are mandatory instructions for the scope that contains this `AGENTS.md`.

If this `AGENTS.md` is located at a single repository root, those instructions are repository-level rules for that repository.

If this `AGENTS.md` is located at a workspace root containing multiple repositories, those instructions are workspace-level rules for all repositories under that workspace, unless a child repository defines stricter local rules.

When these specifications conflict with generic AI skills, reusable `SKILL.md` instructions, framework best-practice skills, or agent defaults, this specification takes precedence.

This does not override explicit user instructions in the current conversation, system/developer/tool safety policies, or platform-enforced constraints. If a skill conflicts with this specification, follow this specification and mention the conflict when relevant.

## Multi-Repository Work

If this scope contains multiple repositories, agents must treat those repositories as potentially related parts of the same workspace/system by default.

For tasks involving multiple repositories, agents must apply this workspace-level specification first, then read each affected repository's local `AGENTS.md`, `README.md`, and relevant `docs/` before making changes.

If local repository rules conflict with this workspace-level specification, follow the stricter or more specific rule unless the user explicitly instructs otherwise.

## Cross-Repository Solution Scope

When a workspace contains multiple repositories, agents must prioritize finding the best solution from the perspective of the whole workspace/system, rather than optimizing only within the single repository that appears most directly related to the symptom.

Agents must not default to a local-only workaround merely because one repository has the highest apparent relevance. During investigation and design, agents must consider whether the cleanest, simplest, or most correct solution belongs in another repository or requires coordinated changes across multiple repositories.

Agents may still implement a single-repository solution when it is genuinely the best system-level solution, when the user explicitly limits scope, or when cross-repository investigation shows no better broader fix.

## Required Reading Order

Before any implementation, code edit, or command execution related to delivery:

1. Read the relevant `README.md` for the current scope or affected repository when the conversation/task is related to that scope or repository.
2. Read `AI-coding-specification/*.md` for the current scope when the task involves code changes.
3. For multi-repository tasks, read each affected repository's local `AGENTS.md`, `README.md`, and directly relevant documents before changing files in that repository.

If additional rule files are added under `AI-coding-specification/`, list them explicitly in this section and describe when each file applies. Do not rely on wildcard reading for mandatory rules.

## Functional Design Documents

The `docs/` directory may contain functional design documents, product decisions, workflow descriptions, or feature-specific constraints.

Before the following task types, agents must search relevant `docs/` directories and read the directly related documents before changing code:

- Feature changes or new feature implementation.
- Debugging tasks where the error is not a simple syntax error.

If multiple documents conflict with each other, if documentation conflicts with the current implementation, or if documentation conflicts with the user's explicit request in the current conversation, stop before code changes and confirm the intended direction with the user.

When relevant documents exist, agents should update those documents by default after completing the code changes, unless the user explicitly asks not to or the change does not affect documented behavior, workflows, constraints, or decisions.

## Execution Requirements

- Do not start implementation before the required documents are read.
- If any required file is missing or path is invalid, stop and report the gap first.
- Follow the coding specification constraints for planning, changes, and verification when the task involves code changes.
- Before final response for code-related tasks, self-check compliance against the coding specification.

## Conflict Resolution

- Highest priority: explicit user request in current conversation.
- Then: mandatory constraints from the applicable `AI-coding-specification/`.
- Then: stricter or more specific child repository rules, when working inside a child repository.
- Then: applicable skills and optional style preferences.
