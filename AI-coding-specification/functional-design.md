Author: ailtariel@gmail.com
Updated: 2026-07-26

# Repository-Level AI Functional Design Specification

This specification defines high-priority rules for AI-assisted functional design tasks within this repository.

Functional design tasks allow AI to proactively complete design details within established product goals and system architecture. This autonomy does not authorize the AI to expand requirements or alter confirmed designs during implementation.

## Rule Usage

- This document is a mandatory repository-wide specification for functional design tasks, not an on-demand skill.
- When multiple rule blocks apply to a task, all of them must be followed simultaneously.
- Rule tags are intended for design reviews, self-checks, and delivery notes. Do not expand the design scope merely to satisfy a tag.
- Implementation tasks remain governed by [`coding-specification.md`](coding-specification.md). Design-stage autonomy must not be treated as implementation authorization.

## Design Autonomy and Architecture Boundaries

- [architecture-baseline] Designs must be based on the current effective system architecture, confirmed designs, and user requirements.
- [architecture-change-gate] If the architecture is unclear in a way that affects the current design, or if the AI identifies an architectural improvement, it must explain the issue, impact, and recommendation to the user. It must not silently settle or change the architecture.
- [autonomous-detail-design] Without changing the architecture, product goals, public contracts, or important user behavior, the AI may autonomously complete details such as functional flows, domain boundaries, states, error behavior, data flow, and module collaboration.
- [decision-rationale] Important autonomous design decisions should include their rationale. Local, low-impact, and easily reversible details do not require individual user confirmation.
- [minimal-design] Designs must follow the minimal-design principle and must not add functionality, abstractions, or complexity that do not directly serve the current goal.
- [design-conflict] When a new design conflicts with the current effective architecture, a confirmed design, or user requirements, the AI must explicitly identify the conflict and leave the decision to the user. It must not silently choose one side.
- [implementation-evidence] The existing implementation is important evidence for evaluating impact and migration cost, but it must not automatically become a reason to lower the design goal. Capabilities must not be reduced by default merely to reuse or accommodate an internal legacy implementation.
- [confirmed-compatibility] Confirmed public contracts, existing data, and user-visible behavior are design constraints. If the complete goal cannot be achieved while preserving those constraints, the AI must present the impact and available options for the user to decide.
- [no-degraded-default] If the complete design would require major changes to the current implementation, the AI must explain the scope and cost and leave the decision to the user. It must not present only a capability-reduced option.

## Minimal Functional Design

- [necessary-feature] A necessary feature is one without which the current design goal cannot be fully achieved, or confirmed architectural, correctness, security, or data-consistency requirements cannot be met. Necessary features must be designed completely and must not be degraded to accommodate an internal legacy implementation.
- [important-extension] An important extension is a feature that is not required for the current design goal to succeed, but has clear value and a high probability of being needed later. It is excluded from the current implementation by default. The AI may evaluate structural compatibility and leave the decision about current implementation to the user.
- [unimportant-extension] An unimportant extension has little connection to the current goal, has uncertain future demand, or provides insufficient benefit to justify its cost. The first version must not consider it or reserve abstractions, interfaces, or configuration for it.
- [first-version-scope] Unless the user explicitly expands the scope, the first-version design includes only necessary features.
- [forward-compatibility] Structural compatibility for an important extension may be considered only when all of the following conditions are met:
  1. The extension has clear value and remains highly likely to be needed later.
  2. The total cost of supporting structural compatibility now is significantly lower than the cost of restructuring when the extension is implemented later.
  3. The compatibility does not materially increase current complexity or prematurely introduce public contracts, new dependencies, or constraints that are difficult to reverse.
- [total-cost] Cost includes development, comprehension, testing, maintenance, deployment, operations, migration, and future evolution, not only the size of the current code change.

## Dependencies and User Decisions

- [dependency-proposal] A new library or independent service may be proposed only when it provides a clear benefit. The AI must explain the benefit, cost, risks, and alternatives, and leave adoption to the user.
- [user-decision-gate] In the following situations, the AI may provide analysis and a preferred option but must not determine the final direction:
  - Changing the system architecture, module responsibilities, data authority, or trust boundaries.
  - Creating a material conflict with the current effective design or user requirements.
  - Changing product goals, functional scope, or important user behavior.
  - Adding a third-party library, independent service, or deployment component.
  - Changing a public API, persistence structure, or configuration format, or introducing an incompatible migration.
  - Choosing between complete implementation, compatibility, and capability degradation.
  - Introducing material security, deployment, licensing, or long-term maintenance risk.
- [decision-request] When requesting a user decision, provide a recommendation, primary rationale, impact, and alternatives rather than presenting only an unanswered question.

## Functional Design Documents

- [design-document-content] A functional design document should state:
  - Goals, scope, and non-goals.
  - The architecture, existing designs, and key assumptions on which it is based.
  - Necessary features and the core approach.
  - Important behavior, boundaries, states, and error handling.
  - Impact on the existing implementation, public contracts, and data.
  - Important extensions and whether structural compatibility is retained.
  - Risks, trade-offs, and decisions that require user input.
  - Significant rejected alternatives and the reasons for rejecting them, when applicable.
  - Acceptance criteria sufficient to determine whether the design goal has been achieved.
- [page-design-document] A page-specific functional design should describe:
  - Functional modules and business components; do not enumerate pure UI primitives that have no independent functional responsibility.
  - Data services, their responsibilities, authority, inputs, outputs, and important failure behavior.
  - The APIs or transports used by each business data flow and how they support the page workflow.
- [design-review] Before submitting a design for user review, and after each round of user feedback, review it within the current requirement scope for important omissions, ambiguous rules, internal conflicts, conflicts with current effective designs, and conflicts with or impact on the existing implementation. Conflicts that affect design correctness or implementation decisions must be resolved in the design or left for user decision.
- [design-implementation-separation] Design documents must not contain file-level modification steps, function-level implementation details, implementation phases, or specific test steps. Those belong in the implementation document.
