---
name: vue
description: 按个人 Composition API 和 TypeScript 约定实现 Vue SFC、响应式、生命周期和 composable。
metadata:
  author: Anthony Fu
  version: "2026.1.31"
  source: Generated from https://github.com/vuejs/docs, scripts at https://github.com/antfu/skills
---

# Vue

> 基于 Vue 3.5。始终使用 Composition API 和 `<script setup lang="ts">`。

## Vue 生态索引

- **Vue Core**：继续阅读本文件及其 `references/` 目录，获取 Composition API、SFC 宏、响应式、生命周期和内置组件相关指导。
- **Pinia**：store、getter、action、plugin、SSR、测试和 store 组合请阅读 [pinia/SKILL.md](pinia/SKILL.md)。
- **Vue Router**：guard、param、导航循环、同路由更新和生命周期交互请阅读 [vue-router/SKILL.md](vue-router/SKILL.md)。
- **Vuetify**：代码 import `vuetify`，或使用 Vuetify 组件、layout、theme 或 migration 行为时，阅读 [vuetify/SKILL.md](vuetify/SKILL.md)。

## 个人偏好

- 优先使用 TypeScript，而不是 JavaScript
- 优先使用 `<script setup lang="ts">`，而不是 `<script>`
- 如果不需要深层响应式，为提高性能优先使用 `shallowRef`，而不是 `ref`
- 始终使用 Composition API，而不是 Options API
- 不鼓励使用 Reactive Props Destructure；使用 `props.x` 和 `withDefaults`，即使当前版本支持响应式解构。
- 这些是有意保留的个人倾向，适用于本次编写的代码；不因此重写无关旧代码。更高优先级项目约束或当前用户要求仍优先。

## 应用与组件职责

在带路由的 Vue 应用中使用清晰的职责边界：

- **App root**：负责 provider、全局初始化、theme、locale 设置、顶层 overlay 和所有 route 共享的能力。它不应包含 feature page 内容或页面局部 workflow。
- **Route layout**：负责稳定的 application chrome、共享 shell component 和子级 `RouterView`。它不应通过 route name 分支实现页面业务行为。
- **Route page**：负责路由特定的数据编排、页面组合、页面局部状态、操作，以及主要内容区域或滚动区域。
- **Feature component**：负责单个 feature 中聚焦的业务 UI 职责，并可保持为该 feature 私有。
- **Shared component**：负责跨 feature 复用的稳定职责。它通过类型化的 prop、slot、model 和 emit 暴露变化，而不是读取 route name 或无关的 global state。

除非能实质降低复杂度，否则不要为单个调用点创建 wrapper component。优先使用 slot 和 component attribute，而不是仅用于间距或转发 prop 的 wrapper node。

如果项目使用 feature module，应将 feature page、私有组件、类型、store、service 和 composable 放在一起。只有 artifact 存在真实的跨 feature 使用方，并且不再依赖单个 feature 的内部契约时，才将其移动到 shared 目录。

## 状态与数据流

- 将 Vue 或 store state 视为 UI 渲染的响应式事实来源。不要仅为了让 Vue 感知状态变化而手工 reload 数据。
- 派生状态使用 `computed`。`watch` 或 `watchEffect` 用于副作用、与外部系统同步或生命周期敏感的工作，不要用它们替代 computed value。
- 局部 UI state 保留在对应组件中。只有所有者之间共享的状态才使用 Pinia；server-state caching 使用项目既有的 query/data layer。
- 当 workflow 支持 cancel、reset、dirty state 或延迟保存时，应将 form editing buffer 与权威持久化状态分离。
- Mutation 成功后，应通过权威响应式来源自己的 store 或 data layer 更新或失效该来源及直接相关来源。
- 避免以丢失响应式的方式解构 reactive object。遵循目标 Vue 版本支持的 prop 和响应式模式。

## Composable 与类型边界

- Composable 用于封装可复用的有状态 Vue 逻辑，不要仅为了把几行代码移出组件而使用它。
- Composable 以 `use` 命名；调用方需要时接受 reactive input；清理 effect 和外部资源；以普通对象返回 ref，使解构能够保留响应式。
- Composable 中的 module-level singleton state 就是 global state。只有共享生命周期是明确且有意的设计时才使用；feature-scoped cache 应保持在 feature 边界内。
- 仅一个 SFC 使用的类型可以保留在该 SFC 中。共享类型应移动到最近的 feature-level 或 responsibility-specific 类型模块，不要放入无所不包的 global types 文件。

## 模板与格式化指导

- 保持模板易读，由项目配置的 formatter 决定换行、缩进和 attribute layout。
- 避免密集的单行 component tree。当 named slot 和聚焦的 child component 能够澄清稳定职责时，应使用它们。
- 当 interpolation 内容跨越多行时，将 opening tag、interpolation 和 closing tag 分别放在独立行。避免在多行边界出现 `>{{` 或 `}}</...>`。
- 除非项目有经过明确考虑的替代配置，否则保持 Prettier 默认的 `htmlWhitespaceSensitivity: "css"`。仅为规范一个模板而修改它，可能改变 inline element 之间有意义的空白。

## 核心

| 主题 | 说明 | 参考 |
| --- | --- | --- |
| Script Setup 与宏 | `<script setup>`、defineProps、defineEmits、defineModel、defineExpose、defineOptions、defineSlots、泛型 | [script-setup-macros](references/script-setup-macros.md) |
| 响应式与生命周期 | ref、shallowRef、computed、watch、watchEffect、effectScope、生命周期 hook、composable | [core-new-apis](references/core-new-apis.md) |

## 功能

| 主题 | 说明 | 参考 |
| --- | --- | --- |
| 内置组件与指令 | Transition、Teleport、Suspense、KeepAlive、v-memo、自定义指令 | [advanced-patterns](references/advanced-patterns.md) |

## 快速参考

### 组件模板

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";

const props = defineProps<{
  title: string;
  count?: number;
}>();

const emit = defineEmits<{
  update: [value: string];
}>();

const model = defineModel<string>();

const doubled = computed(() => (props.count ?? 0) * 2);

watch(
  () => props.title,
  (newVal) => {
    console.log("Title changed:", newVal);
  },
);

onMounted(() => {
  console.log("Component mounted");
});
</script>

<template>
  <div>{{ title }} - {{ doubled }}</div>
</template>
```

### 关键 import

```ts
// Reactivity
import {
  ref,
  shallowRef,
  computed,
  reactive,
  readonly,
  toRef,
  toRefs,
  toValue,
} from "vue";

// Watchers
import { watch, watchEffect, watchPostEffect, onWatcherCleanup } from "vue";

// Lifecycle
import {
  onMounted,
  onUpdated,
  onUnmounted,
  onBeforeMount,
  onBeforeUpdate,
  onBeforeUnmount,
} from "vue";

// Utilities
import { nextTick, defineComponent, defineAsyncComponent } from "vue";
```
