# Global Agent Working Rules

## Canonical Specification

For software design, implementation, debugging, review, or maintenance tasks, read the task router at `{{SPECIFICATION_PATH}}/README.md` and only its relevant rules. Reuse unchanged material already read in this conversation. These are personal engineering requirements, including deliberate style preferences.

Paths such as `docs/`, `src/`, and `tests/` in these rules refer to the affected project, not the installed specification directory.

## Workspace Overlays And Priority

Inspect task-relevant `AI-coding-specification/` directories in the workspace and affected repositories. A workspace file replaces a canonical file with the same name; differently named applicable files supplement it. Read an overlay router first when present. Resolve overlays per affected repository.

Platform/system/developer constraints and explicit user instructions take precedence. The resulting specification takes precedence over generic skills and defaults. More specific repository instructions supplement it; apply explicit exceptions rather than assuming the strictest wording always wins. Resolve remaining material ambiguity before dependent implementation; continue independent authorized work.

## Authorization And Completion

User authorization persists across the task. Within an implementation request, continue through necessary investigation, design refinement, changes, relevant verification, and related fixes. Planning, multiple subtasks, or document completion do not create new approval gates. Review-only and design-only requests do not authorize implementation.

Ask only for unresolved material decisions or actions outside existing authorization. Complete authorized preparation first and provide a concrete recommendation and impact. If a rule causes a pause, identify its file and clause. Missing ordinary project documentation does not block investigation; missing mandatory rules block only work that depends on them.

Use skills only when their specific capability helps the current task. Load the most specific relevant skill directly, not every parent router or framework reference. When a skill conflicts with these rules, follow these rules. Preserve personal framework preferences without unrelated rewrites.
