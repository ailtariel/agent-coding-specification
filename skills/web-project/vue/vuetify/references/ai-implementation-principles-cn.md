# Vuetify AI 实施原则

本文档面向 AI Coding Agent，补充说明在 Vue 项目中使用 Vuetify 实现 UI 时的通用判断原则。

本文档不是项目级设计规范，不规定具体颜色、字号、间距或组件外观数值；也不替代目标项目自己的 `README`、`AGENTS.md`、设计系统、前端架构规范或业务文档。

## 目标

- 让整个应用的视觉风格、交互方式保持一致。
- 面向目标设备提供良好的响应式布局。
- UI 组件和样式精简、结构清晰、便于维护。
- 集中化管理通用组件和样式。
- 最大化复用 Vuetify 官方能力，以便更好地达成以上目标。

## 使用前提

- 先确认目标项目实际使用的 Vuetify 主版本，优先读取 `package.json` 和 lockfile。
- 不要混用不同 Vuetify 主版本的 API。
- API 不确定时，优先查看本 skill 的本地 references 或目标版本官方文档。
- 项目已有规范优先于本文档；如果目标项目已有明确设计系统、layout 规范或组件约定，应先遵守项目规范。

## AI 工作流

处理 Vuetify 相关任务时，按以下顺序判断：

1. 查找目标项目已有同类页面、组件、theme、defaults 和样式 pattern。
2. 判断需求是否可以由 Vuetify 原生组件和组件 API 表达。
3. 判断是否应该复用已有共享组件，或通过 slot / props 扩展已有组件。
4. 判断视觉语义是否应复用或新增 theme token、Global Defaults、SASS variables。
5. 对一次性或局部需求，优先使用 Vuetify utility classes，再考虑 scoped CSS。
6. 只有在 Vuetify 能力和项目已有 pattern 都不能合理表达需求时，才新增封装、全局样式或特殊实现。

## Vuetify 能力地图

AI 应优先考虑 Vuetify 已提供的能力：

- 应用布局：`v-app`、`v-layout`、`v-main`、app bar、navigation drawer、bottom navigation、footer。
- 响应式布局：grid、display/platform、spacing、flex、sizing、breakpoint utilities。
- 常用组件：button、card、list、form input、dialog、menu、snackbar、tabs、table、empty state、loading state。
- 组件 API：`variant`、`density`、`size`、`color`、`bg-color`、`rounded`、`elevation`、slots、component-specific props。
- 主题系统：theme colors、CSS variables、runtime theme switching、semantic tokens。
- 全局配置：`createVuetify({ defaults })` 和局部 `v-defaults-provider`。
- SASS variables：全局字体、圆角、组件底层变量和其他框架级视觉调整。
- Utility classes：spacing、display、flex、text、overflow、position、sizing、elevation、border radius。
- 可访问性基础：dialog、menu、overlay、form、navigation 等组件内置的键盘、焦点和 ARIA 行为。

## 能力选择原则

不要把下面的列表理解为固定优先级；应按问题类型选择合适能力。

- 结构和交互优先使用 Vuetify 组件、props、slots 和 composables。
- 跨页面重复的业务结构优先沉淀为共享组件。
- 跨页面稳定的组件默认行为优先放入 Vuetify Global Defaults。
- 跨页面稳定的视觉语义优先放入 theme token。
- 全局底层视觉调整优先使用 SASS variables 或 Vuetify config。
- 使用 SASS variables 前应确认项目已配置 Vuetify Sass 编译链，且该调整确实属于框架级底层变量。
- 局部布局和一次性微调优先使用 utility classes。
- utility classes 不适合表达时，可以使用 scoped CSS。
- 全局 CSS override 是最后手段，必须限制范围并说明原因。

## Layout 原则

- 常见应用 shell 应优先使用 Vuetify Application Layout System。
- `v-app` 应作为应用布局根边界。
- app bar、drawer、bottom navigation、footer、`v-main` 等布局组件应保持清晰的布局关系。
- 固定区域、布局占位、顺序和偏移应优先交给 Vuetify layout API 处理。
- layout 组件的占位顺序默认受模板顺序影响；动态或非直观布局应优先使用 layout 组件的 `order` prop 显式控制。
- 页面内容区域应有明确边界，避免 layout、page、局部容器共同争夺主滚动职责。
- 如果常规 layout 需要大量手写高度、`calc()`、`absolute`、`fixed` 或全局 overflow hack 才能工作，应先重新检查 Vuetify layout 文档和项目已有实现。

允许局部使用定位、`calc()` 或额外包装层，但必须满足：

- 它服务于明确的局部视觉、动画、第三方库或平台限制。
- 它不会破坏 Vuetify layout 注册、占位、响应式行为和可访问性。
- 它不会把单个页面的问题扩散为全局布局 hack。

## Theme 与样式原则

- Theme token 应表达语义，而不是具体视觉值。
- token 列表通常只是 examples，不应被 AI 当成 allow list；实际 token 以目标项目 theme 定义为准。
- 不要为了单个页面的一次性样式新增全局 token。
- 不要用 `darkBlue`、`greenButton`、`customGray` 这类视觉值或实现值命名 token。
- 页面和组件允许有自己的 scoped CSS，但样式应保持局部、清晰、可删除。
- 硬编码颜色不是绝对禁止，但提交代码中出现硬编码颜色时，应能说明为什么不能使用已有 theme token。
- 大范围覆盖 `.v-*` 组件类会增加维护风险，应尽量避免。

判断样式放置位置时：

- 跨页面视觉语义：theme token。
- 跨页面组件默认行为：Global Defaults。
- Vuetify 底层全局变量：SASS variables。
- 跨页面业务 UI pattern：shared component。
- 单个页面或组件局部效果：scoped CSS。
- 临时或微小布局调整：utility classes。

## Global Defaults 原则

`defaults` 指 Vuetify Global Defaults，即 `createVuetify({ defaults })` 中集中配置组件默认 props 的机制。

适合放入 Global Defaults：

- 多数页面一致使用的组件默认 variant、density、size、rounded、elevation、color 等。
- 稳定的表单输入、按钮、卡片、dialog、sheet、app shell 组件默认行为。
- 明确属于设计系统基础约定的组件默认 props。

不适合放入 Global Defaults：

- 单一业务场景的特殊样式。
- 只在一个页面出现的局部布局。
- 依赖具体业务状态频繁变化的样式。
- 会让大量已有页面被动改变行为的实验性规则。

局部范围需要统一默认 props 时，可以考虑 `v-defaults-provider`，不要为了局部区域修改全局 defaults。

稳定的嵌套组件默认行为可以使用 contextual defaults 表达，例如在 `VCard` 下配置内部 `VBtn` 的默认 props；不要为了组件树内部约定创建额外全局 CSS。

defaults 中的 prop 名称应使用 camelCase。

注意：Vuetify 的 `class` 和 `style` defaults 应配置在具体组件 key 下，不应放在 `global` defaults 中。

配置 defaults 时应注意，`class` 和 `style` 在某些表单输入或控制组件中可能被传递到内部组件；修改前应检查实际渲染结构和影响范围。

## SASS Variables 原则

- 只有当需求属于全局字体、圆角、组件底层变量、utility 生成规则等框架级调整时，才优先考虑 SASS variables。
- 如果只是单个页面、单个组件或局部业务状态的样式，不应引入或修改 Vuetify Sass settings。
- Vuetify Sass settings 文件只应放变量、mixin 和 function；不要放实际 CSS 规则或导入普通样式文件，以免重复生成样式。
- Sass 文件中不要 `@use 'vuetify/styles'`；需要变量时使用 `vuetify/settings`，需要特定全局设置时再按官方文档使用 `vuetify`。
- 开启 SASS variables 会让 Vuetify 使用 Sass 源文件重新编译，可能影响构建性能；已有预编译 CSS 能满足需求时不要过度使用。

## 组件原则

- 优先使用 Vuetify 原生组件，不要复制 Vuetify 已有能力。
- 视觉状态优先通过组件 props、variant、density、size、color、bg-color、rounded、elevation 和 slots 表达。
- 表单优先使用 Vuetify form/input/rules/validation pattern。
- overlay 类交互优先使用 Vuetify dialog、menu、bottom sheet、snackbar、tooltip、overlay 等组件。
- 使用 dialog、menu 等组件的 activator slot 时，应把 slot 传出的 `props` 绑定到触发元素上，避免丢失 ARIA、焦点和键盘交互属性。
- loading、empty、error、disabled、selected 等状态应使用 Vuetify 组件状态和项目统一样式表达。
- 不要为了微小差异创建只转发 props 的包装组件。

允许创建包装组件的情况：

- 封装稳定业务语义。
- 消除跨页面真实重复。
- 统一复杂交互或复杂 slot 结构。
- 隔离第三方库、平台差异或实验性组件。

## 响应式原则

- 先明确目标设备和主要 viewport，再设计布局。
- 优先使用 Vuetify grid、display/platform、spacing、flex、sizing utilities 和组件 responsive props。
- 不要只为当前桌面宽度写布局。
- 固定尺寸、固定高度和绝对定位应评估小屏、横屏、触摸设备和系统安全区域的影响。
- 内容密集页面应优先保证可扫描性、可触达性和滚动边界清晰。

## 可访问性原则

- 优先使用 Vuetify 内建组件承载复杂交互，因为它们通常已经处理了键盘、焦点、ARIA 和交互状态。
- 自定义 dialog、menu、combobox、tabs、tooltip、toast、form validation 时，要特别检查焦点管理、键盘操作和语义。
- 使用 Vuetify activator slot 时必须保留并绑定 slot props；自定义触发器不能只复制视觉结构。
- 图标按钮应有可访问名称，不能只依赖视觉图标。
- 表单错误、loading、disabled、empty state 应清晰反馈给用户。
- 不要为了视觉效果破坏组件默认的焦点、hover、active、disabled 状态。

## 例外规则

允许突破默认原则的情况：

- Vuetify 官方能力无法满足需求。
- 目标项目已有 pattern 已经采用该方案。
- 存在明确性能问题。
- 存在明确可访问性要求。
- 第三方库、原生平台、浏览器或运行环境有限制。
- 用户或项目规范明确要求特定实现方式。

突破默认原则时，AI 应说明：

1. 已评估哪些 Vuetify 原生方案。
2. 原生方案为何不足。
3. 当前方案的影响范围。
4. 是否会影响整体一致性。
5. 是否需要沉淀为 theme token、defaults、SASS variables 或共享组件。

## AI Self Check

提交 Vuetify 相关实现前，AI 只需确认：

- 是否确认了 Vuetify 主版本，并在 API 不确定时查阅官方文档或本地 references。
- 是否优先复用了项目已有 pattern 和 Vuetify 官方组件能力。
- 布局是否尊重 Vuetify application layout，并符合目标项目自己的前端架构规范。
- 通用视觉规则是否沉淀到 theme、Global Defaults、SASS variables 或共享组件，而不是重复散落在页面里。
- 局部 CSS 是否确实服务局部需求，并且没有破坏 Vuetify 状态、布局、响应式或可访问性。
- 若突破默认规则，是否说明了原因、影响范围和替代方案。
