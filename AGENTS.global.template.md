# Global Agent Working Rules

## User Preferences

- Add personal global preferences here.

## Canonical Coding Specification

The canonical coding specification is located at:

`C:/absolute/path/to/agent-coding-specification/AI-coding-specification/`

For every software design, implementation, debugging, review, or maintenance task, read `README.md` in that directory before making delivery-related decisions or changes. Follow its task routing and read every specification required for the current task.

## Workspace Specification Overlay

After reading the canonical specification routing, inspect `AI-coding-specification/` in the current workspace and in every affected repository. If such a directory exists, read its `README.md` first when present, follow its task routing, and read its additional task-relevant rule files before making delivery-related decisions or changes.

Merge the canonical and workspace specifications by filename:

- When a workspace specification file has the same filename as a canonical specification file, the workspace file replaces the canonical file for that workspace. Do not apply the canonical version of that file.
- Apply non-conflicting, differently named rule files from both locations.
- If differently named applicable rule files conflict, stop before implementation and ask the user which rule should govern.
- For multi-repository tasks, resolve this overlay separately for every affected repository.

The resulting applicable specification set is mandatory. Generic skills, reusable `SKILL.md` instructions, framework best-practice skills, and agent defaults may supplement it, but must not override, weaken, or bypass it. If a skill conflicts with the applicable specification set, follow the specification and mention the conflict when relevant.

This precedence rule does not override explicit user instructions in the current conversation, system/developer/tool safety policies, or platform-enforced constraints. Other repository-specific instructions may add stricter or more specific requirements but must not weaken the applicable specification set unless the user explicitly requests an exception.

If the canonical specification directory or a required file cannot be read, stop before implementation and report the missing or inaccessible path.
