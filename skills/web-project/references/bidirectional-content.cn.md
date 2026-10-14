# 双向文本内容

对于同时包含 RTL 和 LTR 内容的应用：

- 由现有 i18n 集成统一控制文档／应用方向，并保持 UI 组件库的方向配置与其一致。不要仅为修复混合文本显示，就在页面和组件中独立硬编码 CSS `direction: ltr/rtl` 或 HTML `dir="ltr/rtl"`。内容具有已知的方向要求时，可以显式指定局部方向。
- 方向未知的动态行内文本使用 `<bdi>` 包裹。它默认自动判断方向，并将内部文本与周围的双向文本隔离。
- 对独立的动态内容块，在已有合适容器（如 `div` 或 `p`）上设置 `dir="auto"`，不要仅为该属性增加包装层。它同样提供自动方向判断和双向文本隔离。
- 自动方向依据首个适用的强方向字符确定，并非语言检测。各段落需要独立方向时，分别为每个段落设置 `dir="auto"`，不要假设一个外层容器会逐段独立判断。
- 对齐需要跟随内容方向时，使用 `text-align: start`。自动方向不会覆盖显式的 `text-align: left/right/center`；行内 `<bdi>` 也不会改变外层块的对齐。
- `<bdi style="display:block">` 可以将文本片段显示为块，但 CSS 不会改变其 HTML 内容模型：内部仍只能放文本及行内内容，不能放 `div`、`p` 或列表。结构化内容使用合适的块级容器并设置 `dir="auto"`，不要使用 `<bdi><div>...</div></bdi>`。

以下占位符表示动态插入的文本：

```html
<!-- Inline content within surrounding UI text -->
<span>Author: <bdi>{{ authorName }}</bdi></span>

<!-- An independent content block -->
<div dir="auto">{{ content }}</div>
```

来源：[HTML 方向算法](https://html.spec.whatwg.org/multipage/dom.html#the-dir-attribute)、[bdi 内容模型](https://html.spec.whatwg.org/multipage/text-level-semantics.html#the-bdi-element)、[双向文本渲染](https://html.spec.whatwg.org/multipage/rendering.html#bidi-rendering)、[W3C 块级内容指导](https://www.w3.org/International/questions/qa-html-dir#dirauto)。
