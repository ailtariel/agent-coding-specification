---
name: refactoring-ui
description: Diagnose and refine an existing interface that feels noisy, cramped, unbalanced, washed out, or visually inconsistent. Use for targeted visual improvement rather than new product flows or a wholesale redesign.
---

# Refactoring UI

A locally curated diagnostic workflow adapted from [s0xDk/refactoring-ui-skill](https://github.com/s0xDk/refactoring-ui-skill/tree/48872143abb0a8feb6d9bf58e222afbd800210b0), whose notes draw on Adam Wathan and Steve Schoger's *Refactoring UI*. See [LICENSE](LICENSE). These are conditional design techniques, not a mandatory aesthetic or a copy of the book.

## Establish What Is Wrong

- Turn the complaint into an observable relationship: what attracts attention before the intended content, which heading appears attached to the wrong group, or where material or alignment changes unexpectedly. Treat the causes below as hypotheses; check the actual view, content, and computed styles before choosing one.
- Identify the affected region's primary task and the existing type, spacing, color, and elevation choices. Preserve behavior, information, and requested layout boundaries. A visual cleanup does not authorize hiding labels, removing controls, changing flows, or replacing the design system.
- Compare a small local change against the same content, viewport, theme, and state. Change the suspected cause before adding decoration. When choosing a token, compare the current value with nearby existing choices; introduce a new value only when they cannot express the intended relationship.

## Diagnose By Symptom

| Observed symptom | Check first | Targeted adjustment |
| --- | --- | --- |
| The primary content still fails to stand out after repeated enlargement | Secondary surfaces, icons, or actions compete at similar visual weight | Reduce the competing emphasis before enlarging the primary content again; preserve readable text and recognizable controls |
| Large headings dominate while supporting text becomes tiny | Font size carries almost all the hierarchy | Bring sizes closer and redistribute emphasis through weight and foreground color; a semantic heading does not require a visually dominant style |
| A heading or field label seems attached to the wrong content | The gap separating groups is indistinguishable from the gap inside one group | Adjust the relevant spacing relationship rather than increasing all padding; retain the intended density |
| A destructive action overwhelms the ordinary workflow | Semantic severity has been confused with action priority | Retain its warning meaning while reducing its visual prominence; strong emphasis may belong in a confirmation context where that action is primary |
| Text on a colored surface looks dull or disabled | A neutral grey or transparent foreground was reused without checking this surface | Try an explicit foreground related to the surface hue and verify contrast; do not turn this into a ban on all grey text |
| Status badges dominate a dense list | Saturated solid fills make every status look like a primary action | Compare tinted surfaces with darker colored text, retaining recognizable status distinctions; check the actual foreground/surface pair |
| An icon overpowers nearby text, or a border alternates between invisible and harsh | Filled area or stroke weight differs even when colors match | Balance weight and contrast together: soften the heavy icon, or compare a softer, slightly thicker border; do not weaken a boundary needed to identify a control |
| Mixed-size text looks misaligned on one row | Geometric centering aligns boxes rather than the text being read | Compare baseline alignment for text; keep optical centering where the row mixes controls or icons |
| A form sprawls on wide screens or becomes wider at an intermediate breakpoint | Grid percentages dictate width despite a useful content width | Constrain the content width and give remaining space to an appropriate flexible region; do not impose fixed sidebars on every layout |
| A screenshot or icon looks crude at its displayed size | Fine detail was reduced too far, or a small glyph was enlarged beyond its intended use | Use a relevant crop or a capture at a narrower viewport; choose a suitable optical-size asset rather than scaling every detail uniformly |
| Photo-backed text works in one crop but fails in another | The image's local brightness changes under the text | Control the image region with a scrim or localized contrast treatment, or give the text a stable surface; inspect alternate crops rather than trusting one screenshot |

## Material And Color Corrections

- If a raised surface looks surrounded by a dirty halo, separate the broad soft cast shadow from the tight contact shadow. In a physical elevation treatment, increased distance can broaden the cast shadow while weakening contact; increasing every shadow parameter together makes the object heavier. A flat visual language does not require this treatment.
- When using directional light cues, compare the highlighted edge with the face of the object. A raised edge and a recessed lip imply different profiles; copying a dark-surface highlight onto a light field can create an unintended dark border. Keep light direction consistent rather than applying the same shadow recipe everywhere.
- For a palette gap, derive candidates from the actual roles that need them: an action fill, a supporting surface, and text on that surface. Inspect them together before adding intermediate shades. Do not import the upstream token sheet, force a fixed shade count, or treat equal numeric steps as equal perceived differences.
- If a dark theme loses depth, inspect adjacent surface lightness and edge definition before increasing shadow opacity. If a brighter surface restores separation, recheck its supporting text: improving one boundary can reduce contrast elsewhere. Do not mechanically invert a light palette.
- For transmission, blur, and glass-specific failures, use [Frosted Glass](../frosted-glass.md); avoid compensating for missing background information with heavier shadows or colored panel fills.

## Verify The Hypothesis

Revisit the original symptom in the same state, then check the affected relationships with representative long content, relevant widths, and supported themes. Inspect focus and selection when reducing emphasis. Report what changed visually and what was actually inspected; a CSS edit alone does not demonstrate improvement. Stop when the diagnosed problem is resolved rather than applying every technique to the page.
