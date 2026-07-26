作者：ailtariel@gmail.com 更新日期：2026-07-26

# Web 前端编码规范

本规范定义本仓库 Web 前端工作的强制性、框架中立工程规则，适用于页面、布局、组件、样式、状态、数据同步、交互、可访问性和前端开发工具。

本规范扩展 [`coding-specification.md`](coding-specification.md)。项目设计文档定义产品特定行为，框架和 UI 库 skill 提供实施细节；两者都不能削弱本规范。

## 规则使用方式

- 无论使用何种框架、渲染模式、组件库或状态管理库，所有 Web 前端任务都必须遵守本文档。
- 同时应用所有相关规则块。本文档与用户已确认的项目设计决策冲突时，实施前停止并确认预期例外。
- 规则标签用于计划、审查、交付说明和自检。不得仅为满足某个标签而扩大实施范围。
- 框架特定的 API、文件类型、宏、hook、composable、组件和格式例外应放入对应框架或 UI 库 skill，不得写入本文档。

## 通用规则

- [web-existing-stack] 保持项目既有的前端框架、组件库、状态流、路由模型、样式系统、formatter 和构建工具，除非用户明确批准变更。
- [web-version-boundary] 应用特定版本的 API、migration 或 breaking-change 指导前，先确认已安装的依赖版本。
- [web-no-parallel-system] 不得为局部需求引入平行的组件库、状态管理系统、utility CSS 框架、样式系统、路由系统或数据获取层。
- [web-existing-patterns] 引入新模式前，先检查现有的同类 page、layout、component、状态流和样式模式。
- [web-single-owner] 每个 application shell、layout region、page region、主滚动容器、overlay、状态来源和反馈渠道必须有一个明确所有者。
- [web-locality] 页面特定的行为、状态、样式和组件应留在最近的 feature 或 page 边界内。只有形成真实的跨页面职责后，才提升其层级。

## Application、Layout 与 Page 边界

使用 application / layout / page 层次：

```text
application
+-- layout 1
|   +-- page 1.1
|   +-- page 1.2
+-- layout 2
    +-- page 2.1
    +-- page 2.2
```

### Application 边界

- [web-application-owner] Application 边界可以负责：
  - 应用级 runtime provider 和 service；
  - 全局模块挂载和初始化；
  - 顶层 overlay；
  - theme、language、timer 和其他跨页面能力；
  - 全局 message、dialog、bottom sheet、snackbar 和其他跨页面交互。
- Application 边界不得负责：
  - 具体页面内容；
  - 页面 form、filter 或 list；
  - 页面级 dialog；
  - 页面业务交互。

### Layout 边界

- [web-layout-owner] Layout 负责一个稳定的 application shell，并可以负责：
  - 子 route 或 page-content outlet；
  - navigation、drawer、header、footer 和其他跨页面 shell region；
  - 共享 layout 边界；
  - 根据 route metadata 得出的 shell 显示规则。
- Layout 不得负责：
  - 页面业务逻辑；
  - 页面级状态或 action；
  - 通过 route name 分支实现页面业务行为。
- 共享 navigation、drawer、header、footer 和其他 shell region 应作为 reusable shell component，再由 layout 组合。
- 一个 application 可以有多个 layout。除非 route 明确切换到其他 layout，否则 page 不得重建已经由 application 或 layout 负责的 shell region。

### Page 边界

- [web-page-owner] Page 负责：
  - feature 内容；
  - 页面级状态和 action；
  - 页面内容容器、padding 和局部 layout；
  - 页面剩余内容区域和主页面滚动行为。
- Page 不得重复 navigation、drawer、header、footer、global overlay 或上层已经负责的 global scroll container。
- 避免仅复制 application 或 layout 职责的 page wrapper。

## Shared Component 与 Feature Component

- [web-shared-component] 当一个 UI 结构或交互模式存在多个真实使用方且职责稳定时，提取 shared component。
- Shared component 应：
  - 通过有文档说明的 input、output 和 extension point 暴露变化；
  - 避免 route name 或 page name 分支；
  - 保持与单一业务领域弱绑定，除非它被明确设计为跨 feature 业务组件。
- 不同使用方需要不同 action 或局部内容时，应提供清晰的 extension point，而不是增加 consumer-specific 分支。
- [web-feature-component] Feature component 可以负责：
  - 一个独立业务能力；
  - 一个 feature 内的可复用模块；
  - 局部交互和 feature 私有 UI 组合。
- Feature component 可以拥有局部样式。在业务特定样式成为稳定跨页面 pattern 前，不得将其提升为 global token 或 global class。
- 除非能够实质降低复杂度，或隔离清晰的平台、浏览器或第三方边界，否则不要为单个调用点创建wrapper component。

## Feature Module 边界

- [web-feature-module] 项目使用模块化结构时，按 feature module 组织产品或业务能力。
- Feature module 可以包含：
  - page 和 route-level UI；
  - domain type；
  - feature state；
  - repository 或 data-access adapter；
  - service；
  - feature-level stateful utility；
  - feature 私有 component。
- Feature 的 page、domain data flow、state、repository、service、stateful utility 和私有 component 应放在最近的 feature 边界内。
- 通用 UI component 区域可以包含页面结构和小型局部交互，但不得拥有大量 domain data flow、persistence、repository、service 或 business workflow。
- Shared component 区域只存放被多个 feature 复用且不绑定单一业务领域的组件。
- Shared library 区域只存放跨 feature 逻辑，不得放置 page 或 UI component。
- 只被单个文件使用的 type 应靠近该文件。被多个文件共享的 type 应移动到最近的 feature-level 或 responsibility-specific type module，不得放入无所不包的 global types 文件。
- 遵循目标项目现有目录名称。不得从通用示例向项目强加框架特定目录结构。

## API 访问与 Transport 边界

- [web-api-layer] Page 和 UI component 不得直接发起 API 请求。API 调用应放入最近的 feature 或 module service、repository、data-access adapter 或 API module。
- [web-shared-api-client] 使用项目既有的 shared API client 统一处理 authentication、base URL、通用 header、error translation 和其他共享 transport 行为。
- [web-api-address] Feature code 应使用相对、path-only API route。Application base URL、origin 和开发代理目标属于 bootstrap 或 configuration 边界，不得在 feature code 中 hardcode。
- [web-transport-exception] Feature 确实需要 absolute URL、独立 client 或不同 transport 时，实施前记录原因、所有权和影响。

## 组件与 UI 库

- [web-library-first] 对 layout、form、dialog、menu、table、pagination、date input、upload、feedback 和其他常见交互，优先使用项目现有 UI 库，不要先使用原生 control 或自定义实现。
- 当 UI 库不负责 document semantic、browser API boundary、generated content、原生 workflow 所需的 hidden input 或特定行为时，仍适合使用原生元素。
- [web-component-reuse] 当职责、交互语义和 input/output contract 一致时，复用现有组件。
- 只有真实复用、稳定业务语义、复杂交互或平台边界能够证明抽象合理时，才提取或包装组件。
- 优先使用库组件 API 和内置可访问性行为，而不是 DOM 模拟或通用容器上的 click handler。
- [web-ui-consistency] 新增和修改的 UI 必须遵循现有的信息密度、间距、控件尺寸、交互、反馈和响应式模式。

## 状态、数据同步与反馈

- [web-state-source] 将项目选定的 framework state、store 或 query cache 视为 UI 响应式来源。Mutation 后不得仅为了强制渲染更新而 reload 数据。
- [web-state-minimal] 局部 UI state 应保持局部。只有多个所有者确实需要同一个来源和生命周期时，才引入 shared 或 global state。
- 远程数据和 cache lifecycle 使用既有的 server-state 或 data-access layer。没有明确的所有权理由时，不得把 server state 复制到第二套 global state system。
- Persistent mutation 的所有者必须在成功后更新或失效自身的权威 state 及直接相关 state。
- Workflow 支持 cancel、reset、dirty state 或延迟保存时，应将 editing buffer 与权威 persisted state 分离。
- Feature-scoped singleton state 只有在共享生命周期明确、能够避免真实的重复 setup，并保持在 feature 边界内时才允许使用。
- [web-feedback-owner] 字段校验和页面局部反馈由对应 form 或 page 负责。
- 系统级操作反馈、global error、confirmation workflow、toast/snackbar message 和跨页面 prompt 应通过既有的应用级反馈所有者处理。
- Loading、empty、error、disabled、selected、success 和 stale state 必须是交互的明确组成部分，而不是偶然出现的渲染分支。

## Dialog 与 Popup Action

- [web-dialog-action-order] Dialog、confirmation prompt 或 popup form 同时包含应用结果的 action 和放弃结果的 action 时，应用结果的 action 放在左侧，放弃结果的 action 放在右侧。
- 应用结果的 action 包括 confirm、save、add、delete、clear、reset、import、keep、ignore 和 apply-filter。
- 放弃结果的 action 包括 cancel、abort、close 和 do-not-apply。
- Selection list、detail dialog、keyboard dialog 等没有显式 cancel action 的交互，无需人为添加 cancel button。
- 已确认的设计文档定义了其他 action order 时，遵循既有产品约定。

## 滚动与布局边界

- [web-scroll-owner] Layout 定义固定 shell region。Page content region 负责剩余内容区域和页面滚动。
- 每个主滚动边界都必须明确。
- 避免多个层级同时作为主滚动容器。
- 不得使用 global overflow rule、任意 height、fixed positioning 或 nested scroll container 掩盖 application / layout / page 职责问题。
- Table、editor、preview、log 或 virtualized collection 等职责明确的局部区域可以使用 local scroll container，但不得意外替代 page 的主滚动职责。
- 评估 fixed size、fixed height 和 absolute positioning 对小屏、横屏、touch device、内容增长和系统 safe area 的影响。

## 样式边界

- [web-style-scope] Global style 负责统一基础外观。Page-local 和 component-local style 只能影响自身边界。
- 根据职责使用项目既有样式系统：
  - 跨页面视觉语义：theme 或 design token；
  - 稳定的跨页面 component 行为：component default 或 shared component；
  - 小型局部 layout 调整：现有 utility class；
  - page 或 component 局部行为：locally scoped style；
  - 大范围 global CSS 或库内部 override：必须说明原因并限制范围的最后手段。
- 不得复制已经由 global theme、component default、framework variable 或 shared component 管理的属性。
- 只有跨页面视觉语义或 component 约定，才可以提升为 global token、global default、global class 或 shared component。
- 不得为单页例外创建 global token 或 default。
- [web-style-colocation] 根据项目既有结构，将 page-specific、component-specific 和 feature-specific style 放在对应 page、component 或 feature 附近。
- 不得在 global stylesheet 中持续累积 page 或 component selector。修改 legacy global selector 时，如果迁移属于当前任务范围，应将直接相关的局部样式移回其所有者。
- 间距和尺寸应施加在负责布局的 element 或 component 上。避免只负责一个 margin、padding、flex、grid 或 width 规则的 wrapper。
- 当现有 semantic token 或响应式行为能够表达需求时，避免 hardcoded color 和 fixed size。真实产品、浏览器、编辑器或平台约束仍可使用固定值。

## 交互、表单与可访问性

- [web-accessibility] 使用语义元素和现有 UI 库的交互组件，保留键盘行为、焦点管理、可访问名称和 disabled state。
- 每个 form control 都需要 accessible label、validation behavior、disabled behavior、submission state 和清晰的 error feedback。
- 仅图标 control 必须有可访问名称。
- 保留 keyboard navigation 和输入法编辑器（IME）组合行为。
- Dialog、menu、tooltip 和其他 overlay 必须保留焦点恢复、Escape 行为、activator 语义和键盘操作。
- 不得仅为视觉样式而移除可见的 focus、hover、active、selected、loading 或 disabled 反馈。
- 不得使用通用 container 上的 click handler 替代库的可访问性行为。

## 双向与 RTL 布局

- [web-logical-direction] Layout spacing 必须支持双向界面。除非有文档说明的视觉需求本质上依赖物理方向，否则优先使用 logical inline/block/start/end property 或 utility，而不是物理 left/right property。
- [web-rtl-source] Application direction、方向性 spacing 和 alignment 决策必须来自同一个集中 configuration 或 token 来源。不得在 page 和 component 中分别重复定义 RTL detection 或 direction rule。

## 国际化与用户可见内容

- [web-i18n] 除非设计文档明确定义内容来自外部或由用户提供，否则用户可见的应用文本使用项目既有国际化机制。
- 每条 locale message 都必须按照项目配置的 message syntax 成功编译。
- 只有 message key 的语义和 interpolation contract 一致时才复用；仅文本相同不足以复用。
- [web-i18n-boundary] Page title、navigation label、button text、form label、placeholder、empty state、validation message 和 API error fallback text 属于 UI chrome，必须使用既有国际化机制。
- 后端提供的业务数据（包括已本地化的业务内容）不能替代国际化 UI chrome。Runtime log 不受 UI 国际化要求约束。
- 框架特定的 message escaping 和 compiler behavior 应放入对应框架或国际化参考。
- Error feedback 应按照 `coding-specification.md` 中的 [api-error-detail] 保留有用的来源详情。

## 格式化与修改范围

- [web-formatting] 使用项目配置的 formatter 作为前端源码和配置文件唯一的格式化权威。
- 仓库提供前端格式检查时，交付前运行该检查。
- 不得手工对齐源码，也不得为规范单个孤立偏好而修改 formatter 配置。
- 格式化修改必须限制在任务明确涉及的前端文件内。

## 本地开发服务器

- [web-dev-server] 当运行时或视觉验证需要时，AI agent 可以启动本地前端服务器。
- Agent 启动的任何服务器必须在交付前停止。
- 不得遗留后台前端进程。

## 测试与验证

- 遵守 `coding-specification.md` 中的 verification ladder、test-addition 规则和报告要求。
- 优先使用静态推理、格式化、typecheck、lint、targeted test、build verification 和 browser 或 visual check 的最小相关组合。
- 纯视觉修改默认不要求自动化测试，但仍应在相关时检查响应式布局、键盘交互、焦点行为以及 loading、empty、error 和 disabled state。

## 最终审查

交付 Web 前端修改前，确认：

1. Application、layout、page、feature 和 shared component 职责各自只有一个明确所有者。
2. Feature module 边界没有让 domain data flow 和 business workflow 进入通用 UI component 或 shared library 区域。
3. Page 和 component 通过既有 API layer 和 shared client 访问服务，没有 hardcoded origin 或 feature-local transport duplication。
4. 新增自定义实现前，已优先复用现有 library component、shared component、状态流和样式模式。
5. Persistent mutation 会更新或失效权威响应式 state。
6. 局部反馈和系统级反馈使用正确的所有者。
7. Dialog action order 遵循本规范或已确认的产品例外。
8. 主滚动和局部滚动边界清晰、支持响应式，并兼容要求的文本方向。
9. 样式与其所有者放在一起，并位于最窄的正确作用域，没有可避免的 global override、一次性 token 或 wrapper element。
10. Form、overlay、icon control、焦点、键盘交互和输入法编辑器行为保持可访问。
11. UI chrome 和后端提供的业务内容遵守正确的国际化边界。
12. 已完成并报告所需的格式化、类型、测试、构建和视觉验证。
