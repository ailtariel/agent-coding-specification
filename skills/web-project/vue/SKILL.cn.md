---
name: vue
description: 在组件、状态与 view 开发中应用个人 Vue、Pinia 和 Vuetify 约定。
metadata:
  author: Personal revision; original Vue references by Anthony Fu
  source: Personal conventions, with references originally adapted from https://github.com/antfu/skills
  updated: "2026-09-25"
---

# Vue

个人 Vue 开发实践，适用于当前任务，不授权重写无关代码。当前用户指令和更高优先级项目要求优先。使用版本特定 API 前确认已安装版本。

## 代码与职责

- 使用 Composition API、TypeScript 和 `<script setup lang="ts">`。保留 `props.x`，使用 `withDefaults`，不使用 Reactive Props Destructure。不需要深层响应式时优先使用 `shallowRef`。
- App 负责 provider 和全局初始化；layout 负责共享应用外壳和 `RouterView`；page 负责数据编排、操作、内容和主要滚动区域。共享组件通过 props、slots、models、emits 表达差异，不通过路由名称分支适配。
- 功能私有文件就近放置。为独立职责、真实复用或实质降低复杂度而提取，不创建仅转发 props 或提供间距的包装组件。
- `service.ts` 通过已有 HTTP client 调用 API，保留其结果与错误合同。组件、store、composable 通过 service 调用；service 不持有 UI loading 或弹窗。client 以结果返回错误时，由调用者判断成功，不增加 reject 包装或重复错误反馈。
- `store.ts` 默认导出一个 Pinia setup store，整体提供相关共享状态和操作。专属数据处理即使是纯计算也留在 store 内，辅助函数不必全部公开；Pinia 管理的状态必须返回。逻辑复用本身不构成共享状态的理由。
- 模块共享类型放在模块 `types.ts`；组件私有 props、emits 和局部类型留在 setup。使用 `import type`。只有真实跨功能使用时才提升到共享范围。

## 响应式与状态

- A 值基于 B 值进行响应式派生时，一律使用 `computed`，不通过额外可写 ref 与 watcher 维持同步。只有 computed 无法表达的需求，如异步操作或外部副作用，才使用显式声明依赖的 `watch`；计算复杂本身不是理由。
- 个人代码不使用 `watchEffect`、`watchPostEffect` 或 `watchSyncEffect`。这项偏好不限制第三方内部实现。
- VueUse 提供响应式数据操作工具。等待 API 数据就绪后执行操作时，条件回调优先使用 `whenever`，异步流程中等待一次条件成立优先使用 `until`，避免手写 watcher/Promise 包装。它们处理副作用和等待；派生值仍使用 computed。就绪、失败与生命周期细节见 [VueUse](vueuse/SKILL.md)。
- 输入、loading 和交互状态留在 setup；多个消费者需要观察同一操作时才共享状态。编辑草稿是有明确初始化、提交和丢弃行为的独立状态，不用无条件同步覆盖未保存的编辑。
- 直接访问 store 状态，或通过 `storeToRefs` 解构；action 可以直接解构。除有意的编辑草稿外，不通过普通状态解构或 `ref(store.value)` 创建脱离数据源的副本。
- 修改通过所有者更新或失效权威数据源，不为了让 Vue 感知变化而重新加载数据。

## 复用逻辑

- 不属于相应 store 的可复用响应式逻辑放在 `use{ModuleName}.ts`，导出的入口函数同名。仅异步或仅调用 API 不构成使用 `use` 前缀的理由；不据此重命名第三方 API。
- 每次 composable 调用默认拥有局部状态。不创建隐含的模块级单例；有意共享的状态必须明确所有者和生命周期。输入需要保持响应式时接收 ref/getter，在 computed/watch 内读取；返回普通对象中的 ref/computed，不返回 `.value` 快照。
- composable 在有效 setup/effect scope 中使用，并负责清理自己创建的计时器、监听器与订阅。不为普通数据函数增加生命周期包装。
- 与 store 无关的非响应式复用函数放在模块 `utils.ts`，接收普通参数，不使用 `use` 前缀。单组件的简单函数留在 setup，store 专属计算留在 store。

## View 与样式

- 模板通过 props、models、events、slots 声明式绑定。简单显示表达式可内联；业务计算和多步操作放在 setup 或数据所有者中。
- 使用 Vuetify 时，组件和 view 相关功能优先检查已有项目组件或 Vuetify 组件、props、slots、composables、内置 class 能否实现，再编写自定义 UI 或 CSS。没有实际定制需求时保留默认配置。
- 确实需要自定义 CSS 且没有适用的 Vuetify API/class 时，简单一次性声明使用内联 `style`，动态值使用 `:style`。不为单次声明创建 class、文件或包装组件，也不在多个使用处重复同组内联声明。
- `<style scoped>` 存放组件内重复使用的局部 class，或检查公开 API/slot 后确有必要的定点 `:deep()` 覆盖。不写无边界的 `.v-*` 覆盖。
- 已确认的全局语义颜色归 theme，框架样式变量归已有 SASS 入口，组件属性默认值归 `defaults`。页面例外保持局部，没有需求时不创建全局配置。
- 遵循已配置的 formatter。多行插值的开始标签、插值和结束标签分别独占一行，不在多行边界出现 `>{{` 或 `}}</...>`。除非项目明确另选方案，保持 Prettier `htmlWhitespaceSensitivity: "css"`。

## 按需参考

只读取能解决当前问题的资料，不全量加载参考文件或子 skill。

- SFC 宏与版本边界：[script setup](references/script-setup-macros.md)。
- watch 时机、异步失效与 effect 生命周期：[响应式](references/core-new-apis.md)。
- 内置组件的易错边界：[高级模式](references/advanced-patterns.md)。
- Pinia 特定 API：[Pinia](pinia/SKILL.md)；路由守卫和组件复用：[Vue Router](vue-router/SKILL.md)。
- Vuetify 布局、配置与版本特定 API：[Vuetify](vuetify/SKILL.md)。
- 响应式工具与等待数据：[VueUse](vueuse/SKILL.md)。
