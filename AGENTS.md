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

Before making task-related design or implementation decisions (read-only discovery to locate the instructions may proceed):

1. Read the task-relevant parts of the scope or affected repository `README.md` when present. Reuse material already read in this conversation when unchanged.
2. Inspect the `AI-coding-specification/` directory, if it exists. If it contains a `README.md`, read it first and follow its task routing. Then read the rule documents relevant to the current task and treat them as mandatory.
3. For multi-repository tasks, repeat this process in each affected repository by inspecting its local `AGENTS.md`, `README.md`, `AI-coding-specification/` directory before making changes in that repository.

## Functional Design Documents

The `docs/` directory under the current workspace or affected repository may contain functional design documents, product decisions, workflow descriptions, or feature-specific constraints. It does not mean the canonical specification repository's `docs/` directory unless that repository is itself the task target.

Before the following task types, agents must search relevant `docs/` directories and read the directly related documents before changing code:

- Feature changes or new feature implementation.
- Debugging tasks where the error is not a simple syntax error.

Resolve conflicts using explicit instruction priority first. A current user request that clearly replaces an earlier design takes precedence; implement the authorized change and update affected documentation. Existing implementation is evidence, not proof that a conflicting document is correct. Ask only when material ambiguity remains, pause only dependent changes, and continue independent authorized work. Draft or superseded documents are background, not additional active rules.

When relevant documents exist, agents should update those documents by default after completing the code changes, unless the user explicitly asks not to or the change does not affect documented behavior, workflows, constraints, or decisions.

## Authorization And Completion

- Existing user authorization persists across investigation, planning, implementation, and verification. Do not request it again merely because a task has several steps or documents.
- Review-only and design-only requests remain limited to those deliverables.
- Within authorized implementation, complete the goal, relevant checks, and repairs of failures caused by the change. Ask only for unresolved material decisions or actions outside that authorization.
- If an instruction causes a pause, identify its file and clause, the unresolved decision, and the independent work that can continue.

## Execution Requirements

- Do not start implementation before the required documents are read.
- If a missing or unreadable instruction is necessary to determine behavior or authorization, report the exact path and pause only dependent implementation. An absent ordinary README or optional design document does not block read-only investigation or otherwise authorized work.
- Follow the coding specification constraints for planning, changes, and verification when the task involves code changes.
- Before final response for code-related tasks, self-check compliance against the coding specification.

## Conflict Resolution

- Highest priority: explicit user request in current conversation.
- Then: mandatory constraints from the applicable `AI-coding-specification/`.
- Then: stricter or more specific child repository rules, when working inside a child repository.
- Then: applicable skills and optional style preferences.
