# Large Tasks

Read only for the corresponding task. Core coding authorization, scope, and verification rules still apply.


- [large-task-threshold] Use a proportionate phased plan when complex dependencies or implementation stages need to be retained. Multiple independent subtasks do not automatically require formal documents or confirmation; follow the core authorization rule.
- [default-phase-flow] With implementation authorization, proceed through phases without repeated confirmation. Pause only work dependent on a new blocking decision and continue independent work.
- [phase-workflow] Each implementation phase should include at least the following steps, in order:
  1. Code changes
  2. Review, including whether the functionality works, whether it follows the design and implementation documents, whether it introduces changes outside the requirement, and whether it violates relevant rules in this specification. If deviations are found, fix them before moving to the next phase.
  3. The smallest necessary verification
  4. Briefly record the implementation status in the implementation document
  5. Git commit when requested or included in the authorized workflow. Prefer one coherent commit per phase; do not create meaningless tiny commits.
