# Agent Working Rules

These rules are mandatory for AI agents working in this repository.

## Authority and Priority

The files under `AI-coding-specification/` are repository-level mandatory instructions for AI-assisted code changes.

When these specifications conflict with generic AI skills, reusable `SKILL.md` instructions, framework best-practice skills, or agent defaults, this repository specification takes precedence.

This does not override explicit user instructions in the current conversation, system/developer/tool safety policies, or platform-enforced constraints. If a skill conflicts with this specification, follow this specification and mention the conflict when relevant.

## Required Reading Order

Before any implementation, code edit, or command execution related to delivery:

1. Read `README.md` at the repository root only when the conversation/task is related to this repository.
2. Read `AI-coding-specification/coding-specification.md` only when the task involves code changes.

If additional rule files are added under `AI-coding-specification/`, list them explicitly in this section and describe when each file applies. Do not rely on wildcard reading for mandatory rules.

## Execution Requirements

- Do not start implementation before the required documents are read.
- If any required file is missing or path is invalid, stop and report the gap first.
- Follow the coding specification constraints for planning, changes, and verification when the task involves code changes.
- Before final response for code-related tasks, self-check compliance against the coding specification.

## Conflict Resolution

- Highest priority: explicit user request in current conversation.
- Then: repository mandatory constraints from `AI-coding-specification/`.
- Then: applicable skills and optional style preferences.
