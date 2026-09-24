---
name: vuetify-skilld
description: 'Vue 项目的 Vuetify 参考。代码 import "vuetify"，或使用 Vuetify 组件、layout、theme 时使用。应用特定版本的 migration 或 breaking-change 指导前，先确认已安装的主版本。'
metadata:
  version: 4.1.0
  generated_at: 2026-06-07
  references_synced_at: 2026-06-07
---

# vuetifyjs/vuetify `vuetify@4.1.0`

**标签：** latest: 4.1.0、v3-stable: 3.12.8、v2-stable: 2.7.2、v1-stable: 1.5.24、dev: 4.1.0-beta.1

**参考：** [文档](./references/docs/_INDEX.md) · [v4.0.1-v4.1.0 Release API 索引](./references/releases/v4.0.1-to-v4.1.0-api-index.md) · [AI 实施原则](./references/ai-implementation-principles.md)

## 版本边界

本 skill 按照 Vuetify 4.1.0 参考资料更新。应用 API 变更、migration note 或 breaking-change 指导前，检查目标项目的 `package.json` 或 lockfile，并确认已安装的 Vuetify 主版本。

- 对 Vuetify 4 项目或明确的 Vuetify 4 migration 任务，使用下方 v4 指导。
- 对 Vuetify 3 项目，只使用已确认存在于 Vuetify 3 的通用 component/layout/theming 指导；相比 v4 migration note，优先使用项目本地代码和已安装 package 的文档。
- 版本未知时，先询问或检查依赖，然后再修改代码。

## 实施 workflow

按以下顺序应用 Vuetify 指导：

1. 阅读目标项目的前端规则，并检查现有的同类 page、theme、defaults 和 shared component。
2. 确认已安装的 Vuetify 主版本；API 或行为不确定时检查本地 reference。
3. 优先使用已经负责所需结构或交互的原生 Vuetify component、prop、slot、composable 或 utility。
4. 当职责和交互契约一致时，复用现有项目组件。
5. 稳定的跨页面视觉语义放入 theme token，稳定的 component 行为放入 Global Defaults，重复的业务 UI 放入 shared component。
6. 局部需求使用 utility class 或 scoped CSS。大范围 global CSS 和 `.v-*` override 是必须限制范围的最后手段。

详细决策模型参见 [AI 实施原则](./references/ai-implementation-principles.md)。

## 组件职责

当 Vuetify 组件已经负责相同的可见结构或交互时，不要从通用 `div` 加自定义 CSS 开始。

| 职责 | 首选 Vuetify 能力 |
| --- | --- |
| 应用根 | `VApp` |
| 注册的应用 layout 区域 | `VLayout` |
| 应用主导航 | `VNavigationDrawer` |
| 应用级 top bar | `VAppBar` 和 `VAppBarTitle` |
| 受 application chrome 影响的路由页面内容 | 每个 routed page 各自拥有一个 `VMain` |
| 页面宽度、水平 gutter 和页面 padding | `VContainer` |
| 响应式页面 grid | `VRow` 和 `VCol` |
| 带 action 的 page 或 panel header | `VToolbar` |
| 通用分组内容或可见 surface | `VCard` |
| 轻量视觉 surface | `VSheet` |
| Card heading、body 和 action | `VCardTitle`、`VCardText`、`VCardActions` |
| List 和 navigation collection | `VList` 和 `VListItem` |
| Form 和 validation | `VForm` 和 Vuetify input component |
| Dialog 内容 | 包含结构化 `VCard` 的 `VDialog` |
| Feedback state | Vuetify progress、empty-state、alert 和 snackbar component |

原生元素仍适合文档内容、原生浏览器 workflow 所需的 hidden input、浏览器 measurement 或 scroll boundary、生成的 Markdown 内容，以及不承担可见布局职责的 Vue control-flow fragment。

如果原生 wrapper 带有 background、border、elevation、padding、width、grid、flex 或 positioning class，应先确认该职责是否应由 Vuetify component 承担。

## Application Layout

- 使用 `VApp` 作为 Vuetify 应用根边界。
- 在 app -> layout -> page 结构中，app 负责 `VApp`；layout 负责 `VLayout`、已注册的 shell region 和 `RouterView`；每个 routed page 负责自己的 `VMain`。
- 默认不得在 app 或 layout 中放置一个共享 `VMain`。Page 自己拥有 `VMain`，可以让每条 route 独立控制内容结构、高度、滚动、padding、full-width region 和其他页面特定布局行为，同时继续使用已注册 application shell 提供的 offset。
- `VMain` 只用于受已注册 application-layout region 影响的内容。不得使用任意 margin、padding、fixed positioning 或 global overflow rule 模拟它保留的 offset。
- 优先使用 `order`、`location`、`permanent` 和响应式行为等 layout prop，而不是手工定位。Template order 会影响注册优先级；优先级不清晰时使用 `order`。
- 常规 routed page 通常应以自己的 `VMain` 开始；页面需要标准宽度和 gutter 时，再在其中使用 `VContainer`。Full-width 页面内容可以在 `VMain` 内直接使用其他合适的 child。结构随 breakpoint 变化时使用 `VRow` 和 `VCol`。
- Route 需要不同 application shell 时，应显式切换到另一个 layout。不得通过在 app/layout 中共享 `VMain`，或在 page 内重新创建已注册 shell region 来解决 shell 差异。
- 主 scroll region 应有一个清晰所有者。不得让 layout、page 和 local container 争夺主滚动。
- 如果普通 shell 需要大量手写 height、`calc()`、absolute/fixed positioning 或 overflow hack，添加 CSS 前先重新检查 application layout 模型。

## 页面 surface 与间距

- 对具有 surface 语义的通用分组 block 使用 `VCard`。对 message bubble 或 highlight region 等轻量 surface 使用 `VSheet`。
- 水平 title/action region 使用 `VToolbar`；属于 card 的 action 使用 `VCardActions`。
- Vuetify flex utility 只用于已经有组件负责可见 block 的小型一维 group。响应式页面结构使用 grid。
- 间距施加在负责布局的 Vuetify component 上。避免仅负责一个 margin、padding、flex 或 width 规则的 wrapper。
- 优先使用 prop、theme token 和 utility class，而不是 inline style 或 scoped CSS。真实产品、浏览器、编辑器或平台约束可以使用固定像素值。

## 表单、Overlay 与可访问性

- 使用带有明确 label、validation、disabled state、loading state 和 error feedback 的 Vuetify form 和 input component。
- 除非目标项目定义了另一种既有模式，否则使用 `VCard`、`VCardTitle`、`VCardText` 和 `VCardActions` 构建 dialog 内容。
- 对 dialog、menu、tooltip 和相关 overlay，将 activator slot 的 `props` 绑定到 trigger，保留 ARIA、焦点和键盘行为。
- 仅图标按钮必须有可访问名称。
- 保留输入法编辑器（IME）组合、键盘导航、焦点恢复、Escape 行为和内置的 disabled/loading state。
- 不得使用通用 container 上的 click handler 替代 Vuetify 交互语义。

## 样式归属

选择作用域最窄的正确样式机制：

- 跨页面视觉语义：theme token；
- 稳定的跨页面 component default：Global Defaults；
- 框架级底层视觉调整：SASS variable；
- 重复的跨页面业务 pattern：shared component；
- 局部 component effect：scoped CSS；
- 小型局部 layout 调整：utility class。

不得为单页例外添加 global token 或 default。避免大范围 override Vuetify internal class。 `class` 和 `style` default 应配置在具体 component key 下，而不是 `global` defaults key 下。

## API 变更

本节记录特定版本的 API 变更，应优先关注最近的 major/minor release。

- 对 v4.0.1 到 v4.1.0 之间引入的 component/API 变更，扫描完整 release note 前优先使用聚焦的 release-derived 索引：[v4.0.1-v4.1.0 Release API 索引](./references/releases/v4.0.1-to-v4.1.0-api-index.md)

- BREAKING：`VRow` / `VCol` Grid——完全重构，使用 CSS `gap`，不再使用 negative margin。移除 `dense` prop（使用 `density="compact"`）；移除 `VRow` 的 `align`/`justify` 和 `VCol` 的 `order`/`align-self`，改用 utility class [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING：MD3 Typography——为符合 Material Design 3 重命名 variant： `h1`-`h3` -> `display-*`、`h4`-`h6` -> `headline-*`、 `subtitle-1`/`body-1` -> `body-large`、`button`/`subtitle-2` -> `label-large` [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING：MD3 Elevation——elevation level 从 25 个（0-24）减少到 6 个（0-5），与 MD3 density-independent pixel level 对齐 [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING：`VBtn` Defaults——默认移除 `text-transform: uppercase`。 `$button-stacked-icon-margin` Sass variable 替换为 `$button-stacked-gap` [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING：`VSelect` / `VAutocomplete` / `VCombobox`——`item` slot prop 重命名为 `internalItem`。`item` prop 现在是 `internalItem.raw` 的 alias [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- BREAKING：`VForm` Slot——`isValid`、`errors` 和 `isDisabled` slot variable 现在是已解包值，不再是 `Ref` object [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- NEW：`VSnackbarQueue`——在 v4 中重写，支持同时显示多个 snackbar；`default` slot 重命名为 `item` [来源](./references/releases/v4.0.0-beta.2.md)

- NEW：`VRow` `gap` prop——提供细粒度 grid spacing 控制，接受 number、string 或 `[x, y]` array [来源](./references/docs/src/pages/en/getting-started/upgrade-guide.md)

- NEW：`VAvatarGroup`（experimental）——新的 labs component，支持以 overlapping 方式分组多个 avatar [来源](./references/releases/v4.0.0-beta.2.md)

- NEW：`VCommandPalette`（experimental）——新的 labs component，为 application command 提供 search 和 action interface [来源](./references/releases/v4.0.0-beta.0.md)

- NEW：v4.1.0 将多个 labs/component 提升为 core framework：validation rule、`VIconBtn`、 `VStepperVertical`、`VPullToRefresh`、`VFileUpload`、`VDateInput`、`VColorInput` 和 `VPicker` [来源](./references/releases/v4.1.0.md)

- NEW：v4.1.0 增加 table 和 data-table 改进：`VDataTable` sortable header `aria-sort`、selection aria label、带 `side` 的 object `loading`、`expanded` slot transition 支持、filtered `itemsLength`、mobile header slot、group-by `v-model:opened` 和 search match highlighting [来源](./references/releases/v4.1.0.md)

- NEW：v4.1.0 增加 `hover-elevation` prop 和 CSS utility、任意 `rounded` 值、可选 theme page transition，以及供 `VCommandPalette` / `VOverlay` 使用的 viewport location strategy [来源](./references/releases/v4.1.0.md)

- NEW：v4.1.0 component 增补包括 `VSwitch` `size` 和 square `inset`、`VTable` `caption` slot / `gridlines`、`VNumberInput` `grouping`、`VTooltip` `color` 和 `target="cursor"`、`VProgressLinear` `split`、`VSparkline` marker/tooltip，以及 calendar/date-picker 交互改进 [来源](./references/releases/v4.1.0.md)

- NEW LABS：v4.1.0 新增 `VDateRangePicker`、`VHeatmap`、`VHighlight` 和 `VMonthPicker` labs component [来源](./references/releases/v4.1.0.md)

- FIXED：v4.0.8/v4.0.9 包含重要的 focus-trap、overlay、select/menu、SSR `VProgressLinear`、transparent theme color 和 `VForm` 性能修复 [来源](./references/releases/v4.0.8.md) [来源](./references/releases/v4.0.9.md)

**其他变更：** `VCalendar` 从 labs 提升 · `VHotkey` 从 labs 提升 · `VToolbar` 新增 `location` prop · `VAvatar` 新增 `badge` prop · `VProgressCircular` 新增 `reveal` prop · `VTreeview` 新增 `indent-lines` prop · 新增 `vuetify/styles/core` entry point · 默认使用 `system` theme · 移除 `VSnackbar` `multi-line` · `VContainer` `fill-height` 行为变化 ·通过 UnoCSS 支持 Material Symbols iconset · font 使用 CSS variable · `VDataTable` bottom slot 中的 pagination method · `VCommandPalette` `closeOnSelect` 和 `before-select` · `VAvatarGroup` `limit` overflow 行为变化

## 最佳实践

- 在 `useHotkey` composable 中使用 `cmd` modifier，以实现跨平台兼容；它在 Mac 上自动解析为 Command，在 PC 上解析为 Control [来源](./references/docs/src/pages/en/features/hotkey.md)

```ts
// Preferred: works on both Mac and PC
useHotkey("cmd+s", (e) => saveDocument(e));

// Avoid: hardcoding 'ctrl' may cause conflicts or feel non-idiomatic on Mac
useHotkey("ctrl+s", (e) => saveDocument(e));
```

- 在 `defaults` 配置中的具体 component key 上应用 `class` 和 `style`；`global` defaults key不支持它们 [来源](./references/docs/src/pages/en/features/global-configuration.md)

```ts
// Preferred
createVuetify({
  defaults: {
    VBtn: {
      class: "text-none",
      style: { textTransform: "none" },
    },
  },
});

// Avoid: class and style are ignored in global
createVuetify({
  defaults: {
    global: { class: "text-none" },
  },
});
```

- 通过重新定义 CSS layer 顺序解决 Vuetify 与 TailwindCSS 的样式冲突；将 Vuetify style 放入优先级低于 Tailwind base layer 的专用 layer [来源](./references/discussions/discussion-21241.md)

```css
/* main.css */
@layer theme, base, vuetify, components, utilities;
@import "vuetify/styles" layer(vuetify);
@import "tailwindcss";
```

- 高精度十进制运算使用 `v-text-field` 配合 `decimal.js`；`VNumberInput` 内部使用 `toFixed()`，可能受到标准 JavaScript 浮点数精度问题影响 [来源](./references/docs/src/pages/en/components/number-inputs.md)

- 使用 global state（例如 Pinia）配合 `v-snackbar-queue` 集中管理 snackbar message；通过向 shared array push，可以从 application 任意位置触发 notification [来源](./references/docs/src/pages/en/components/snackbar-queue.md)

```vue
<template>
  <v-app>
    <v-snackbar-queue v-model="messages.queue" />
  </v-app>
</template>
```

- 使用 `order` prop 显式控制 layout component 的优先级；它覆盖仅由 markup order 决定优先级的默认行为 [来源](./references/docs/src/pages/en/features/application-layout.md)

```vue
<v-navigation-drawer />
<v-app-bar :order="-1" />
```

- 使用 `useDate()` 的 `parseISO` 和 `toISO` method 标准化 date string；`VDateInput` 和其他 date component 内部预期并返回原生 JavaScript `Date` object [来源](./references/docs/src/pages/en/components/date-inputs.md)

- 对 keyboard-driven power-user workflow 使用 `v-command-palette`（experimental）；它提供预配置、可访问且可搜索的 dialog interface，并自动实施 ARIA best practice [来源](./references/docs/src/pages/en/components/command-palettes.md)

- 在 Vuetify 4 migration 期间，通过 `@layer vuetify-overrides` block 恢复之前的 negative-margin/padding grid 行为；现有 layout 依赖 legacy system 而不是新的 CSS `gap` property 时需要此设置 [来源](./references/docs/src/pages/en/getting-started/grid-legacy-mode.md)

```scss
@layer vuetify-overrides {
  .v-row {
    gap: unset;
    margin: calc(var(--v-col-gap-y) * -0.5) calc(var(--v-col-gap-x) * -0.5);
  }
}
```

- 在引入 local wrapper 或第三方替代方案前，将 v4.1.0 中已提升的 component 视为 Vuetify core capability：`VIconBtn`、`VStepperVertical`、`VPullToRefresh`、`VFileUpload`、 `VDateInput`、`VColorInput` 和 `VPicker` [来源](./references/releases/v4.1.0.md)

- 使用 Vuetify table 时，优先使用新的 v4.1.0 table accessibility 和 structure prop/slot，而不是 custom table markup：`aria-sort`、selection aria label、`caption` slot、向 `<table>` 透传 aria、`gridlines`、`expanded` slot transition 和 mobile header slot [来源](./references/releases/v4.1.0.md)
