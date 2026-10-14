# Bidirectional Content

For apps containing both RTL and LTR content:

- Let the existing i18n integration control the document/app direction and keep the UI library's direction configuration consistent with it. Do not independently hardcode CSS `direction: ltr/rtl` or HTML `dir="ltr/rtl"` in pages and components merely to fix mixed-text rendering. Explicit local direction is appropriate when the content has a known directional requirement.
- Wrap dynamic inline text of unknown direction in `<bdi>`. It defaults to automatic direction and isolates the text from surrounding bidirectional content.
- For an independent dynamic content block, apply `dir="auto"` to its existing suitable container, such as a `div` or `p`; do not add a wrapper solely for this attribute. It provides automatic direction and bidirectional isolation too.
- Automatic direction uses the first applicable strong directional character, not language detection. For independently directed paragraphs, apply `dir="auto"` to each paragraph rather than assuming one outer container determines each paragraph separately.
- Use `text-align: start` when alignment should follow the content direction. Automatic direction does not override an explicit `text-align: left/right/center`. An inline `<bdi>` does not change the surrounding block's alignment.
- `<bdi style="display:block">` can display a text fragment as a block, but CSS does not change its HTML content model: it still accepts phrasing content, not `div`, `p`, or lists. Use a suitable block container with `dir="auto"` for structured content; do not use `<bdi><div>...</div></bdi>`.

The placeholders below represent dynamically inserted text:

```html
<!-- Inline content within surrounding UI text -->
<span>Author: <bdi>{{ authorName }}</bdi></span>

<!-- An independent content block -->
<div dir="auto">{{ content }}</div>
```

Sources: [HTML directionality](https://html.spec.whatwg.org/multipage/dom.html#the-dir-attribute), [bdi content model](https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-bdi-element), [bidirectional rendering](https://html.spec.whatwg.org/multipage/rendering.html#bidi-rendering), [W3C block content guidance](https://www.w3.org/International/questions/qa-html-dir#dirauto).
