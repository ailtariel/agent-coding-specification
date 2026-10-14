# Vuetify 集成细节

内联／scoped／全局样式归属等共享个人实践由 [Vue](../../SKILL.md) 定义。本文只在需要相应能力时提供补充细节。

## 应用布局

在个人 app → layout → page 结构中，app 负责 `VApp`；layout 负责 `VLayout`、已注册的 shell 区域和 `RouterView`；每个路由页面负责自己的 `VMain` 以及主要内容／滚动区域。这是个人职责约定，不是框架要求。保留项目已经明确采用的其他架构。

对于受已注册应用布局偏移影响的内容，使用 `VMain`，不要通过 margin 或固定定位模拟偏移。不同的 shell 使用不同的 layout。需要标准宽度／gutter 时使用 `VContainer`；全宽内容可以在 `VMain` 内直接使用其他合适的子元素。选择容器、Flex 布局和响应式断点时，遵循 [布局偏好](../SKILL.cn.md#布局偏好)。依赖 `VRow` / `VCol` 的行为前，确认已安装版本的布局模式。

优先使用 `order`、`location`、`permanent` 等布局属性，而不是手动定位。注册／模板顺序会影响布局优先级；可以通过 `order` 显式指定。

来源：[应用布局](docs/src/pages/en/features/application-layout.md)、[网格](docs/src/pages/en/components/grids.md)。

## 组件与交互

标题／操作区域使用 `VToolbar`，分组内容使用 `VCard`，轻量 surface 使用 `VSheet`，card 操作使用 `VCardActions`。间距施加在负责该布局的组件上。文档内容、浏览器测量、原生工作流，以及没有 Vuetify 组件负责其结构的片段，仍适合使用原生元素。

将 overlay 的 activator slot `props` 绑定到触发元素，使自定义后仍保留焦点、键盘和 ARIA 行为。使用 Vuetify 表单／输入控件的状态与校验能力，不在通用容器上重新实现。已安装版本的接口约定参见 [组件索引](docs/_INDEX.md)。

## 主题、Defaults 与 SASS

- Global Defaults 配置公共属性。局部 `VDefaultsProvider` 或上下文嵌套 defaults 可以表达区域特定行为，而不改变整个应用。默认属性名使用 camelCase。
- `class` 和 `style` 应配置在具体组件 key 下，而不是 `global` defaults key 下。部分控件会将它们传递给内部元素；需要明确作用位置时，检查实际目标。
- 视觉语义使用已有主题颜色。不要仅为局部样式引入 SASS 编译；修改 SASS 变量前，检查项目是否已配置相应编译链。
- SASS settings 文件只包含变量、mixin 和 function，不包含输出 CSS 的内容或普通样式表导入。不要在 settings 中 `@use 'vuetify/styles'`；按文档使用 `vuetify/settings`。

来源：[主题](docs/src/pages/en/features/theme.md)、[defaults](docs/src/pages/en/features/global-configuration.md)、[SASS](docs/src/pages/en/features/sass-variables.md)。

## 具体 API 问题

- 跨平台快捷键：[`useHotkey` 与 `cmd`](docs/src/pages/en/features/hotkey.md)。
- 日期适配器的解析／序列化：[`useDate`、`parseISO`、`toISO`](docs/src/pages/en/components/date-inputs.md)；确认所配置适配器的日期类型。
- 对精度敏感的数值输入：[数字输入框](docs/src/pages/en/components/number-inputs.md)；UI 数值控件本身不能保证精确十进制运算。
- 已有 Tailwind/Vuetify CSS layer 冲突：[layer 顺序讨论](discussions/discussion-21241.md)。这不构成引入另一套样式系统的授权。
- 特定版本的组件、属性、slot 和修复：[Release API 索引](releases/v4.0.1-to-v4.1.0-api-index.md)。
