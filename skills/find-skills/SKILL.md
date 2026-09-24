---
name: find-skills
description: Find skills when the user asks to discover or extend agent capabilities; ordinary requests to perform a task do not trigger this skill.
---

# Find Skills

Identify the capability the user wants to add and check available skills before searching external catalogs. Search by the actual workflow, not a broad domain. Use `npx skills find <query>` or a relevant official source when appropriate.

Before recommending a skill, inspect its instructions, trigger boundary, required tools, provenance, and compatibility with the user's existing rules. Popularity is supporting evidence, not a quality threshold or proof of suitability. Avoid overlapping skills that merely repeat existing guidance.

Present a small set of relevant options with source links, concrete benefit, prerequisites, and installation commands. Install when the user's request authorizes installation; discovery alone does not authorize it. Follow the requested destination and preserve existing customizations.

If nothing suitable is found, report that clearly. Continue the underlying work if it was already requested and can be done with available capabilities; do not ask again whether to start authorized work.
