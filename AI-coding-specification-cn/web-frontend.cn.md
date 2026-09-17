作者：ailtariel@gmail.com 更新日期：2026-09-17

# Web 前端编码规范

本规范定义目标工作区或受影响仓库内 Web 前端工作的强制性、框架中立工程规则，适用于页面、布局、组件、样式、状态、数据同步、交互、可访问性和前端开发工具。

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

## 文件组织与职责边界

以下示例展示文件归属，`*` 表示由技术栈决定的文件扩展名。目录和文件按需创建，已有等价结构或框架约定时沿用原结构。

```text
src/
├── layouts/
│   └── {layout}/
├── pages/
│   └── {page-or-page-group}/
│       ├── components/
│       │   └── {component}/
│       ├── modules/
│       │   └── {module}/
│       ├── Page.*
│       ├── types.*
│       ├── store.*
│       ├── service.*
│       └── useXxx.*
├── shared/
│   ├── components/
│   │   └── {component}/
│   ├── modules/
│   │   └── {module}/
│   └── libs/
├── routes/
└── stores/
```

页面和模块自己的状态、类型及数据访问文件跟随其所有者；顶层 `stores/` 只放应用级状态。组件的实现和私有样式放在对应 `{component}/` 内，简单组件也可直接平铺。

- [web-project-structure] 沿用项目及框架既定的目录约定，按业务职责聚合相关文件；只创建当前需要的目录和层次，不为套用模板重排项目或拆出仅作透传的文件。
- [web-application-owner] Application 负责应用启动、全局配置和跨页面能力，不承载具体页面的内容与业务操作。
- [web-layout-owner] Layout 负责共享导航、页头等应用外壳及页面出口，不承载页面业务；页面不得重复实现所属 layout 已提供的外壳。
- [web-page-owner] Page 或相关页面组负责自身的内容组合、业务操作和局部状态；私有组件、类型、数据访问与样式就近组织，不分散到全局目录。
- [web-component-module-contract] Component 负责展示与交互，可以拥有局部交互状态；module 拥有业务规则、数据和流程，可以包含组件；lib 提供与具体业务无关的技术能力。文件按其实际职责归属，不按大小或名称归类。
- [web-shared-boundary] 仅在出现真实的跨功能复用时，将相应组件或模块及其私有依赖移入共享范围；共享代码通过公开接口供使用方调用，不反向依赖具体页面的私有实现。

## 组件抽取

- [web-component-split-consider] 当一部分内容具有独立职责、真实复用需求、可独立理解的复杂逻辑，或需要由父级独立编排时，应评估抽取为组件；抽取后应形成清晰且内聚的边界，单一使用方的组件保留在所属功能内。
- [web-component-split-avoid] 没有复用需求，且内容简单或与父级高度耦合、拆分会造成大量依赖传递时，优先保持在原组件中；不得仅为减少文件行数、移动 markup 或增加一层包装而抽取。
- [web-component-contract] 抽取组件或模块时，通过明确的输入、输出和扩展点表达变化，迁移其完整职责及自有依赖；不得只共享外观而复制同一业务逻辑，也不得让共享实现通过页面名称或路由分支适配使用方。

## API 访问与 Transport 边界

- [web-api-layer] Page 和 UI component 不得直接发起 API 请求。API 调用应放入最近的 feature 或 module service、repository、data-access adapter 或 API module。
- [web-shared-api-client] 使用项目既有的 shared API client 统一处理 authentication、base URL、通用 header、error translation 和其他共享 transport 行为。
- [web-api-address] Feature code 应使用相对、path-only API route。Application base URL、origin 和开发代理目标属于 bootstrap 或 configuration 边界，不得在 feature code 中 hardcode。
- [web-transport-exception] Feature 确实需要 absolute URL、独立 client 或不同 transport 时，实施前记录原因、所有权和影响。

## 组件复用与 UI 库

- [web-reuse-order] 实现所需组件或业务能力前，按以下顺序查找并选择：项目内可直接复用的组件/模块 → 将项目内职责相同的已有实现抽取为可复用组件/模块 → 查询项目 UI 库中的可用组件 → 自定义实现。只有前一层没有职责匹配且适合复用的方案时，才进入下一层，不得跳过查找而直接手写。
- [web-library-api-first] 使用 UI 库组件时，先通过其公开 API 和扩展接口满足需求；只有公开能力不足时才增加必要的自定义样式或行为，并保留组件原有的交互与可访问性语义，不另写一套 DOM 或事件机制替代它。
- [web-ui-consistency] 新增和修改的 UI 必须遵循项目既有的信息密度、间距、控件尺寸、交互、反馈和响应式模式；自定义实现也不例外。

## 数据来源、数据流与反馈

- [web-state-source] 同一份业务数据应有明确的权威来源，需要共享它的组件从该来源读取，不得为同一职责另建互不联动的可写状态。调用同一段可复用逻辑不等于共享状态，应确认实际使用的是同一数据来源。
- [web-derived-state] 展示值和派生值应从源数据计算，并随源数据变化自动更新；不得通过额外可写副本和人工同步维护本可直接派生的数据。
- [web-state-minimal] 状态放在能够满足其使用范围的最近所有者中；局部状态保持局部，需要共享时再提升，不为代码复用而默认引入全局状态。
- [web-editing-buffer] 需要独立编辑、取消或延迟提交的内容，可以建立编辑副本，但必须与已保存数据区分，并明确初始化、提交和丢弃方式；不能将编辑过程直接作用于共享的已保存数据。
- [web-state-update] 数据修改应经过其所有者提供的操作，并通过项目既有响应式机制更新或失效相关来源，使消费者获得结果；不得依靠直接修改 DOM、重复维护副本或强制刷新页面来掩盖数据流断开。
- [web-feedback-owner] 字段校验和页面局部反馈由对应 form 或 page 负责；系统级操作反馈、全局错误和跨页面提示通过应用级反馈机制处理，避免各处重复实现。
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

## CSS 与样式归属

- [web-style-colocation] 组件的 DOM 与私有样式由同一组件负责，按框架约定放在一起；抽取或移动组件时同步处理其私有样式，不得仅为缩短文件而将样式拆入无关文件。
- [web-style-scope] 全局样式只承载应用基础样式和明确的共享视觉规则；页面或组件的私有样式限制在自身作用域，不得为局部需求将其提升到全局。
- [web-style-reuse] 已有 theme、design token、组件默认值或共享组件负责的样式，应直接复用其配置；只有形成稳定的共享视觉语义时才新增公共配置，不为单页例外创建全局 token 或 default。
- [web-style-replacement] 修改样式时定位并修改原有声明，清理被替代的规则；不得不断追加重复声明、提高选择器优先级或使用强制覆盖来抵消旧实现。主题、响应式断点和交互状态所需的明确样式变体可以保留。
- [web-style-layout] 间距和尺寸施加在实际负责布局的元素或组件上，不为单个样式属性增加包装层；优先使用既有语义配置和响应式能力，确有产品或平台约束时可以使用固定值。

## 移除废弃实现

- [web-remove-obsolete] 功能或视觉结构被移除、替换时，同步清理本次变更涉及且不再使用的 DOM、样式、状态、逻辑和引用，不得以永久隐藏旧节点代替移除；仍有明确交互用途的临时隐藏不属于废弃实现。

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

## 测试用例设计与使用

- [web-persistent-test-scope] 长期保留的前端用例应验证数据流或稳定业务行为，不固化 DOM 结构、样式、展示文案、截图和 UI/UE 交互用例。按断言内容而不是所用工具分类，使用浏览器或挂载组件本身不决定用例是否值得保留。
- [web-data-flow-tests] 数据流测试应覆盖当前改动涉及的数据输入、处理、状态变化及消费者获得的结果；风险跨越多个环节时，验证必要的协作关系，不能以单个函数正确或一次调用发生代替整条数据流正确。
- [web-test-real-implementation] 测试必须执行真实被测逻辑；可以替换测试范围之外的依赖，但不得 mock 掉要验证的数据处理、状态变化或同步过程，也不得在测试中另写一份实现代替被测代码。
- [web-test-oracle] 测试期望应来自需求和业务契约，并能区分正确与错误行为；不得照抄当前实现、用待测代码生成期望值，或通过匹配源码写法证明功能正确。
- [web-test-contract-stability] 断言应针对业务结果，不锁定变量名、内部调用步骤或组件组织方式；业务契约不变的重构不应要求改变测试期望，测试失败也不能通过迎合当前实现来消除。
- [web-test-scope] 按当前变更的风险和直接影响选择必要用例，覆盖相关的正常、异常和边界行为；优先复用已有用例，不以数量或覆盖率代替测试价值，不为测试方便新增生产抽象。
- [web-temporary-ui-tests] UI/UE 在本次开发中通过手工、浏览器或临时自动化验证；临时用例及辅助资产放在正式测试目录之外，不进入功能提交，并在验证完成后清理。UI/UE 不固化不代表可以省略验收。
- [web-verification] 遵守通用规范的验证范围与报告要求，选择能够证明本次改动正确的最小检查组合；区分静态检查、业务测试与 UI/UE 验收各自的覆盖能力，报告实际执行和未验证的部分。

## 最终审查

交付 Web 前端修改前，确认：

1. Application、layout、page、feature 和 shared component 职责各自只有一个明确所有者。
2. Feature module 边界没有让 domain data flow 和 business workflow 进入通用 UI component 或 shared library 区域。
3. Page 和 component 通过既有 API layer 和 shared client 访问服务，没有 hardcoded origin 或 feature-local transport duplication。
4. 组件或模块选型遵循项目直接复用、已有实现抽取、查询 UI 库、自定义实现的顺序。
5. 共享数据来源一致，派生值保持响应式关系，修改会更新或失效相应来源。
6. 局部反馈和系统级反馈使用正确的所有者。
7. Dialog action order 遵循本规范或已确认的产品例外。
8. 主滚动和局部滚动边界清晰、支持响应式，并兼容要求的文本方向。
9. 私有样式跟随组件且作用域明确，没有重复覆盖或以永久隐藏代替移除的废弃实现。
10. Form、overlay、icon control、焦点、键盘交互和输入法编辑器行为保持可访问。
11. UI chrome 和后端提供的业务内容遵守正确的国际化边界。
12. 测试验证真实数据流和业务结果，UI/UE 仅作当次验收，已报告实际验证范围。
