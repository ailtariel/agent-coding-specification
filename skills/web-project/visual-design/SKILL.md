---
name: visual-design
description: Refine or review interface visual hierarchy, density, surfaces, frosted-glass materials, and interaction colors, especially when matching an existing visual language.
---

# Visual Design

Apply these visual presentation preferences within the requested scope. RTL/LTR and mixed-direction text belong to the Web frontend programming specification.

For frosted-glass design or material refinement, read [Frosted Glass](frosted-glass.md) (Chinese): panel transmission versus a frosted canvas, material tuning, and diagnostic visual checks.

For an existing interface that feels noisy, cramped, or unbalanced, use [Refactoring UI](refactoring-ui/SKILL.md) to diagnose the symptom and compare targeted corrections.

## Scope, Hierarchy, And Grouping

- Preserve existing behavior, information, and spatial constraints during visual refinement. For container-only changes, containers may be split or merged without moving content regions or changing their order.
- Follow the existing visual language unless a redesign is requested. Establish a clear visual hierarchy on each page; avoid scattering equally prominent highlights that compete for attention. When the primary content lacks emphasis, first reduce competing emphasis rather than adding more highlights.
- Identify the primary content of the page and of each region. Within the layout constraints, prioritize useful space for that content; keep supporting content compact and quieter. Do not let oversized headings, auxiliary panels, or decorative padding crowd out the primary content.
- Group content belonging to the same task; avoid fragmenting the page into small visual compartments or giving every label, control, or statistic its own card.
- Large uninterrupted content areas still need internal hierarchy based on their content. Use restrained surface differences, type size, spacing, whitespace, or dividers to distinguish meaningful groups while preserving the continuity of the whole. Avoid both an undifferentiated wall of content and separation so strong that related content appears disconnected.
- Use borders sparingly, especially repeated or tightly nested borders. Prefer spacing and typography for grouping before adding enclosing borders; do not stack borders, shadows, and strong surface changes at the same boundary. Preserve boundaries needed to identify controls or focus.
- Move secondary explanation into a tooltip only when the task permits it and keyboard/touch access is preserved; keep essential instructions, errors, and decision-critical content visible.

## Surfaces And Interaction Colors

- Inspect theme and component defaults before adding overrides. Fix repeated visual problems through semantic tokens or shared components; keep exceptions with the component that owns them. Pair foreground and border choices with their actual surface.
- Reduce text emphasis through its foreground color or component variant, not opacity on the entire container: container opacity also changes images, nested controls, focus indicators, and disabled states.
- Keep secondary controls quiet at rest while retaining distinguishable hover, keyboard focus, selected, and disabled states. Reducing visual weight must not erase focus or status information.
- When matching a reference theme, inspect computed styles and CSS variables inside each relevant surface scope. Root variables and screenshots alone miss contextual overrides, transparency, and interaction colors. Distinguish measured values from inferred semantic names and adaptations.

## Visual Verification

- Inspect the affected surfaces in the supported themes and states relevant to the change, including overlays when they inherit the changed styles. Use realistic long or empty content where it can expose changed density, truncation, overflow, or scrolling; check representative hover and keyboard focus states.
- State which appearances were actually checked and which remain unverified. Do not infer contrast compliance from appearance alone or rework unaffected areas merely to make a page-wide pass uniform.
