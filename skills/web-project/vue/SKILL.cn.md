---
name: vue
description: 在组件、状态与 view 开发中应用个人 Vue、Pinia 和 Vuetify 约定。
metadata:
  author: Personal revision; original Vue references by Anthony Fu
  source: Personal conventions, with references originally adapted from https://github.com/antfu/skills
  updated: "2026-10-18"
---

# Vue

这些是个人 Vue 实现选择，补充 Web 前端编程规范。

## 代码与职责

- 使用 Composition API、TypeScript 和 `<script setup lang="ts">`。保留 `props.x`，使用 `withDefaults`，不使用 Reactive Props Destructure。不需要深层响应式时优先使用 `shallowRef`。
- `service.ts` 通过已有 HTTP client 调用 API，保留其结果与错误合同。组件、store、composable 通过 service 调用；service 不持有 UI loading 或弹窗。client 以结果返回错误时，由调用者判断成功，不增加 reject 包装或重复错误反馈。
- `store.ts` 默认导出一个 Pinia setup store，整体提供相关共享状态和操作。专属数据处理即使是纯计算也留在 store 内，辅助函数不必全部公开；Pinia 管理的状态必须返回。逻辑复用本身不构成共享状态的理由。
- 模块共享类型放在模块 `types.ts`；组件私有 props、emits 和局部类型留在 setup。使用 `import type`。只有真实跨功能使用时才提升到共享范围。

## 变量共享

- [vue-provide-inject-scope] 父子组件之间的简单变量传递直接使用 props。多个组件或 TypeScript 文件之间的大范围共享，优先直接访问所属 store，或由各消费者分别调用相应的 `use{ModuleName}`；分别调用 composable 不等于自动共享状态。业务代码中的 provide/inject 主要用于跨层级但小范围的组件变量传递，例如 A → B → C 中只有 A、C 需要该变量，B 完全不关心。inject 接受方必须是组件，在组件 setup 中直接调用；不得在 store、普通 TypeScript 模块或自定义 composable 中调用，也不得通过 `useContext` 等包装函数绕过。此约束针对业务代码，不限制第三方库内部实现。

## 响应式与状态

- A 值基于 B 值进行响应式派生时，一律使用 `computed`，不通过额外可写 ref 与 watcher 维持同步。只有 computed 无法表达的需求，如异步操作或外部副作用，才使用显式声明依赖的 `watch`；计算复杂本身不是理由。
- 个人代码不使用 `watchEffect`、`watchPostEffect` 或 `watchSyncEffect`。这项偏好不限制第三方内部实现。
- 响应式数据和浏览器副作用优先使用已安装且匹配的 VueUse 工具，不手写同等实现。响应式就绪等待中，条件触发回调优先使用 `whenever`，等待一次条件成立优先使用 `until`；当前流程已拥有请求 Promise 时直接 await，不增加第二次等待。就绪必须表示目标请求的数据成功可用，而非仅 `!loading`；保留失败与所有者生命周期处理。核对已安装 API 的超时／取消语义，不假设停止 watcher 就会结束其 Promise。

## 复用逻辑

- 不属于相应 store 的可复用响应式逻辑放在 `use{ModuleName}.ts`，导出的入口函数同名。仅异步或仅调用 API 不构成使用 `use` 前缀的理由；不据此重命名第三方 API。
- 与 store 无关的非响应式复用函数放在模块 `utils.ts`，接收普通参数，不使用 `use` 前缀。单组件的简单函数留在 setup，store 专属计算留在 store。

## View 与样式

- 使用 Vuetify 时，组件和 view 相关功能优先检查已有项目组件或 Vuetify 组件、props、slots、composables、内置 class 能否实现，再编写自定义 UI 或 CSS。没有实际定制需求时保留默认配置。
- 确实需要自定义 CSS 且没有适用的 Vuetify API/class 时，简单一次性声明使用内联 `style`，动态值使用 `:style`。不为单次声明创建 class、文件或包装组件，也不在多个使用处重复同组内联声明。
- `<style scoped>` 存放组件内重复使用的局部 class，或检查公开 API/slot 后确有必要的定点 `:deep()` 覆盖。不写无边界的 `.v-*` 覆盖。
- 已确认的全局语义颜色归 theme，框架样式变量归已有 SASS 入口，组件属性默认值归 `defaults`。页面例外保持局部，没有需求时不创建全局配置。
- 遵循已配置的 formatter。多行插值的开始标签、插值和结束标签分别独占一行，不在多行边界出现 `>{{` 或 `}}</...>`。除非项目明确另选方案，保持 Prettier `htmlWhitespaceSensitivity: "css"`。

Vuetify 专属布局和控件偏好见 [Vuetify](vuetify/SKILL.md)。
