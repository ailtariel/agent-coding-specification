---
name: vueuse
description: 为响应式数据、条件等待和浏览器副作用选择 VueUse 工具。
metadata:
  source: https://github.com/vueuse/vueuse
  updated: "2026-09-25"
---

# VueUse

尚未加载时阅读 [Vue 个人约定](../SKILL.md)。VueUse 提供响应式工具，优先复用匹配的工具而非自行实现。采用 API 前检查已安装的 Vue/VueUse 版本与包导出。加入本 skill 不会向目标项目安装依赖；依赖变更遵循已有授权。

Vuetify 项目的组件/view 功能先检查项目组件与 Vuetify 能力；VueUse 补充响应式数据与浏览器副作用能力。派生值仍使用 `computed`，不借 VueUse 建立 watcher 同步的镜像或新的全局状态。

## 等待 API 数据

等待响应式 API 数据就绪时，优先使用 `whenever` / `until`，避免手写 `watch` + Promise 或条件回调包装。

| 需求 | 优先选择 |
| --- | --- |
| 监听条件变为真后执行回调 | `whenever(condition, callback)` |
| 注册时已就绪也立即执行 | `whenever(condition, callback, { immediate: true })` |
| 就绪后只执行一次 | 已安装版本支持时使用 `whenever(condition, callback, { immediate: true, once: true })` |
| 在异步流程中等待一次就绪 | `await until(condition).toBeTruthy()` |

传入 ref/getter，不传 `.value` 快照。`whenever` 随数据源变化触发，不是轮询；`until` 立即检查条件，匹配后停止其 watcher。

就绪必须表示目标请求/对象的数据成功可用。仅 `!loading` 也包括尚未开始与失败。可能失败的等待应观察终态，处理失败后再继续，不只等待成功而无限挂起。当前流程拥有请求 Promise 时直接 await 并判断结果合同，不额外创建响应式等待。

按操作生命周期确定超时/取消策略。`until` 超时默认正常返回；超时应阻止后续操作时设置 `throwOnTimeout: true`。scope 停止 watcher 不会自动结束待定 Promise，也不会取消已经运行的回调。清理自己拥有的 watcher，并在所有者或请求变化后阻止过期的 await 后操作。未核对已安装 API 前不假设存在 `AbortSignal` 参数。

这些工具保持显式依赖，与个人不使用 `watchEffect` 的约定兼容；第三方内部实现不受该约定限制。

## 按需查询其他工具

在[函数索引](https://vueuse.org/functions.html)中只查当前需要的能力，如响应式存储、事件监听、元素观察、防抖/节流和异步状态。请求继续通过既有 service/client，保留错误语义；不为使用 fetch 工具而绕过该层。不创建仅重命名 VueUse 函数的包装。

来源：[仓库](https://github.com/vueuse/vueuse)、[whenever](https://vueuse.org/shared/whenever/)、[until](https://vueuse.org/shared/until/)、[guidelines](https://vueuse.org/guidelines.html)。上游[函数 skill](https://github.com/vueuse/vueuse/tree/main/skills/vueuse-functions)作为对比来源，不复制其宽泛触发条件与完整函数目录。
