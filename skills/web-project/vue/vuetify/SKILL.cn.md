---
name: vuetify-skilld
description: 根据已安装的主版本，实现 Vuetify 组件、布局、主题或版本迁移。
metadata:
  version: 4.1.0
  generated_at: 2026-06-07
  references_synced_at: 2026-06-07
  guidance_updated: "2026-10-08"
---

# Vuetify

尚未加载时，应用共享的 [Vue 个人约定](../SKILL.md)，包括组件／视图复用和样式归属。在引入自定义 UI 前，先检查项目已有组件或 Vuetify 是否能够实现所需的视图／交互。

本地文档快照覆盖 Vuetify 4.1.0，不代表当前最新版本。确认目标项目的依赖版本。对 Vuetify 3，只使用已针对该安装版本核实的 API，不应用 v4 迁移说明。

## 布局偏好

以下是 Vuetify 项目的个人实现偏好：

- 响应式布局、局部横向分组和纵向堆叠优先使用 Flex。只有确需二维对齐或跨行跨列时才使用 CSS Grid，不要仅为间距或等宽卡片引入 Grid。
- App bar 按职责使用 `VAppBarNavIcon`、`VAppBarTitle`、`VDivider`、`VSpacer` 和相应 slot；不使用自定义 CSS 重做它们已有的尺寸、间距和分隔能力，也不要添加不承担布局职责的组件。
- 页面区域优先使用 `VContainer`、`VCard`、`VSheet` 及当前版本支持的 Flex 布局组件和工具类；需要响应式分栏时使用 `VRow` / `VCol`。已有组件适用时，不从通用 `div` 加自定义 CSS 开始。语义内容、测量节点和第三方库宿主仍可使用原生元素。仅在已安装版本导出 `VFlex` 时使用它；Vuetify 3/4 使用现行布局组件和 Flex 工具类。
- 优先使用 Vuetify 响应式工具类、组件属性及 `useDisplay()` 的命名断点。只有配置的断点无法表达需求时，才保留自定义宽度媒体查询或手动宽度比较。`prefers-reduced-motion` 等媒体特性不属于视口断点。

## 加载状态、表单与输入控件操作

- 组件提供内置 `loading` 属性时，优先使用该属性。只有明确的定制需求无法由内置行为满足时，才添加自定义加载指示器；不要为同一操作同时显示两者。
- 不默认给输入控件包裹 `VForm` 或原生 form。只有需要校验、协调字段状态等表单专属能力时，才使用表单。移除不必要的表单包装时，保留所需的键盘操作。
- 属于文本框、自动补全等输入控件自身的操作，优先使用内置按钮或按钮属性，其次在组件的公共 slot 中放置自定义按钮。除非交互确实要求分离，否则不要把输入控件与它的操作做成独立的同级控件。作用于整个筛选组或页面的操作，不属于单个输入控件自身的操作。

## 按需查阅参考资料

- 应用布局、defaults、SASS 和 activator 集成：[实施细节](references/ai-implementation-principles-cn.md)。
- 组件属性、slot 和工具类：[本地文档索引](references/docs/_INDEX.md)。
- Vuetify 4 迁移：[升级指南](references/docs/src/pages/en/getting-started/upgrade-guide.md)；已有旧版网格布局：[网格兼容模式](references/docs/src/pages/en/getting-started/grid-legacy-mode.md)。
- 特定版本的新增功能和修复：[v4.0.1-v4.1.0 Release API 索引](references/releases/v4.0.1-to-v4.1.0-api-index.md)。

围绕当前组件或 API 搜索；普通组件任务不要加载全部文档或完整发布历史。
