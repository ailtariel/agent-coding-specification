---
name: writing-plans
description: Create an implementation plan when requested or when complex dependencies, trade-offs, or phases need a durable plan.
---

# Writing Plans

Use the project's planning and documentation rules. A simple change usually needs a brief explanation in the conversation, not a plan file. Pure UI work follows any project documentation exemption.

For a useful plan, capture the goal and acceptance criteria, important decisions, affected responsibilities/files, dependencies between coherent tasks, and the smallest relevant verification. Include code only where it clarifies a difficult contract or decision; do not prewrite the entire implementation. Choose task sizes by meaningful outcomes, not elapsed minutes.

Use the existing documentation location. If none exists and a durable plan is needed, use `docs/<task>/YYYY-MM-DD-implementation.md`. Keep unresolved decisions visible and distinguish them from routine implementation choices.

Review coverage, dependencies, and assumptions once; correct substantive gaps. Testing strategy and commit boundaries follow the project and user authorization, not a mandatory TDD recipe or per-step commit cycle.

After planning, continue implementation if already authorized and no material decision blocks it. A request for a plan alone ends with the plan. Ask only for unresolved consequential choices, and continue independent authorized work. Execution does not require another skill or a particular agent topology.
