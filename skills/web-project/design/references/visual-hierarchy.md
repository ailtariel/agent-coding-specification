# Visual Hierarchy and Surface Design

Use this reference when refining an existing interface's visual hierarchy, density, surfaces, or interaction colors. Start from its content and workflow, not a decorative style template.

## Scope and Content Priority

- Identify the primary content and primary action for each page and region. Give them the most useful space and contrast; keep supporting controls and metadata compact and quieter.
- Preserve behavior, interaction, information, and the user's spatial constraints. When a task only allows container refinement, replace, split, or merge containers without moving regions or changing their order.
- Moving secondary explanations into tooltips is appropriate only when allowed by the task and the information remains accessible by keyboard and touch. Keep essential instructions, errors, and decision-critical content visible.

## Grouping and Separation

- Group content that belongs to the same task. Avoid a separate card or border around every label, control, or small statistic.
- Separate long continuous content according to meaningful sections. Use spacing, restrained heading scale, subtle surface changes, or a divider; do not stack every separation technique on the same boundary.
- Prefer whitespace and typography before adding borders. Avoid dense nested borders and alternating high-contrast panels that fragment one continuous task.
- Check both extremes: an undifferentiated wall of content and an interface fragmented into many unrelated boxes. The grouping should remain legible without competing with the content.

## Semantic Colors and Interaction States

- Inspect the existing theme and component defaults before adding local CSS. Repeated problems usually belong in semantic tokens or shared components; keep genuine local exceptions with their owner.
- Define colors by role: canvas, navigation, content surface, raised surface, hover, selected, primary text, supporting text, disabled text, subtle border, control border, and focus indicator. Pair foreground and border roles with their actual surface.
- Reserve saturated accents and strong contrast for important actions, selection, status, and focused content. Secondary icons and controls should be quiet at rest and visibly respond to hover and keyboard focus.
- Do not dim an entire container to reduce text brightness: doing so also changes its children, images, focus indicators, and disabled states. Adjust the semantic foreground or component variant instead.
- Treat default, hover, focus-visible, pressed, selected, expanded, and disabled as distinct states. Preserve visible keyboard focus and status semantics when reducing visual weight.
- When extracting a reference theme, inspect computed styles and CSS variables inside each surface scope. Root variables and screenshots alone may miss contextual overrides, transparent layers, and interaction styles. Record measured values separately from inferred semantic names and adaptations.

## Verification

- Inspect realistic populated, empty, and long-content states where relevant. Preserve truncation, overflow, scrolling, and access to every action.
- Check each changed page in both light and dark modes, including its menus, fields, tables, and dialogs. A dark-mode improvement must not silently weaken light-mode contrast.
- Verify hover and keyboard focus on representative controls. Use measured contrast for important foreground/background pairs; do not claim accessibility compliance from appearance alone.
- Keep a page-level record of changes and observed results for broad visual passes. Pages already meeting the goals need no cosmetic churn. Clearly mark unavailable states rather than claiming full coverage.
