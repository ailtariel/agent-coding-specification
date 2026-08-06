作者：ailtariel@gmail.com 更新日期：2026-07-26

# 仓库级 AI 编码规范

本规范定义本仓库中 AI 辅助编码任务的高优先级工程标准。

除非用户明确要求，否则本规范优先于其他 skill 中与之冲突的建议。

## 规则使用方式

- 本文档是仓库级强制规范，不是按需加载的 skill。所有代码相关任务默认都应遵守整份文档。
- 当一个任务同时适用多个规则块时，必须同时遵守所有规则。非安全类实施决策按照 [priority] 权衡取舍；安全风险必须遵守 [security-confirmation]。
- 规则标签用于交付说明、审查和自检。不得仅为了满足某个标签而扩大实施范围。

## 通用规则

- [priority] 用户明确要求 > 正确性 > 可维护性 > 最小修改 > 安全性 > 风格与简洁性
- [minimal-context]
  - 优先读取与当前任务直接相关的最小文件集合。
  - 不得无目的地扫描整个仓库、读取大量无关文件，或重复读取已经确认无关的文件。
- [plan-first] 编写代码前，简要说明预期修改和受影响文件。默认不得创建正式实施计划。只有任务存在尚未解决的设计取舍、需要变更依赖或公共契约、会产生广泛的跨模块行为影响，或者需要分阶段实施或包含多个相对独立的子任务时，才必须提供计划并等待用户确认。行为变更、受影响文件较多或预计修改行数本身均不能单独触发该要求。当任务需要设计或实施文档时，遵守“设计与实施文档”一节。
- [security-confirmation] 必须明确识别并沟通安全风险，但涉及功能、架构、部署或安全策略的实施决策必须由用户确认。
  - AI 应主动指出安全风险和可能的缓解方向。但是，仓库级 AI 编码通常缺少架构、部署、合规和业务风险的完整上下文。收到用户确认前，不得自行实施功能级、架构级、部署级或策略级安全措施。
  - 只有行为明确、不改变公共契约的局部低风险安全加固可以默认实施。
- [behavior-preservation] 除非任务明确要求改变行为，否则默认保留现有运行时行为、异常行为、执行时序、返回结构和副作用。如果当前实现已经正确工作，且任务不要求改变该行为，不得仅因为另一种实现看起来“更整洁”、“更现代”或“更通用”而重写。
- [no-unrelated-churn] 不得随意重构、重新格式化、调整 import 顺序或重命名，除非它们与当前任务直接相关。
- [no-speculation] 没有当前需求来源时，不得进行修改：
  - 不得提前为未来扩展性设计。只实施已确认的需求；不得实现未请求的功能。
  - 不得仅因为“未来可能有用”“未来可能需要扩展”或“顺便改善结构”而重构现有代码。
  - 没有明确计划或需求来源时，不得添加 TODO/FIXME 注释。
- [no-extra-abstraction] 不得引入不必要的抽象层，包括不必要的 class、interface、wrapper 或 helper。
- [abstraction-exception] 只有同时满足以下所有条件时才允许抽象或提取：行为保持不变、可读性不降低、代码总行数显著减少。如果行数反而增加，多数情况下应避免抽象。
  - 优先复用现有 utility。新增非 UI reusable abstraction 时必须满足本规则。
  - [web-component-decomposition-exception] Web UI 组件拆分遵循 [`web-frontend.md`](web-frontend.md)。满足 [web-component-split-consider] 的组件拆分不要求减少代码总行数，但必须保持行为不变、维持或提高可读性，并形成清晰的职责边界。
- [validation-boundary] 避免过度防御式编程：校验外部输入，信任内部数据流。外部输入应只在入口校验；内部流程应遵循既有契约，不得重复 fallback 处理。每条执行链中的外部输入只能校验一次。
- [no-silent-failure] 禁止静默失败。除非用户明确同意降级行为，否则应通过日志或返回响应清晰暴露错误。
- [api-error-detail] 返回 API 错误响应时，只要来源中存在 `error`、`text` 或 `message` 等有意义的错误码或错误文本，就应保留。内容包含敏感信息时，返回前必须脱敏。
- [try-catch] 不得过度使用 try...catch。只在以下情况使用：
  - 失败后执行仍必须继续
  - 需要统一或格式化错误消息
  - 需要资源清理或事务一致性，例如 rollback 或释放连接
- [public-contract] 除非用户明确要求，否则不得修改 public API、database schema、配置格式或环境变量名称。
- [dependency-gate] 不得引入新依赖。如果新依赖确实必要，先说明原因并等待确认。

## 操作系统与工具

- [rg-first] 对查找文件、搜索文本、统计匹配等适合 `rg` 的操作，即使在 Windows 上也应先尝试 `rg`，除非已经确认不可用。文件发现优先使用 `rg --files`，内容搜索优先使用 `rg`，然后才 fallback 到 PowerShell 遍历或 `Select-String`。
- [powershell-utf8] 使用 PowerShell 读写文本文件时，对支持编码参数的命令默认显式传入 `-Encoding UTF8`，例如 `Get-Content`、`Set-Content`、`Add-Content`、`Out-File`、 `Import-Csv` 和 `Export-Csv`。
- [powershell-raw-text] 使用 PowerShell 读取整个文本文件进行分析时，优先使用 `Get-Content -Raw -Encoding UTF8`；没有 `-Raw` 时，PowerShell 返回行数组，可能改变后续行为。
- [powershell-native-quoting] 通过 PowerShell 向 native tool 传递 regex、pipe、quote、brace 或 semicolon 时应谨慎处理解析。Shell 解析可能改变参数时，优先使用单引号 pattern、 `rg -F` 固定字符串搜索，或每次调用只执行一个简单命令。
- [powershell-aliases] 不得假设常见 Unix 命令名在 PowerShell 中具有 Unix 语义。`curl`、 `wget`、`cat`、`ls` 和 `rm` 等命令可能是 alias 或具有不同的行为；优先使用明确的 native command 或目标 PowerShell cmdlet。
- [rg-exit-code] `rg` 退出码 `1` 表示“没有找到匹配”，不一定是命令失败。大于 `1` 的退出码才表示实际错误。

## 大型任务

- [large-task-threshold] 默认在以下任一条件成立时将任务视为大型任务：预计需要分阶段实施；涉及多个相对独立的子任务；或者用户明确要求大型任务 workflow。触发后，应明确向用户确认是否使用大型任务的多阶段加自动迭代开发 workflow。
- [default-phase-flow] 用户确认大型任务 workflow 后，如果没有提供不同指示，则自动按照实施文档中的阶段继续。每个阶段完成后不需要再次确认。如果实施过程中发现重要设计冲突、遗漏或实施阻塞，应暂停进一步代码修改并等待用户决定。
- [phase-workflow] 每个实施阶段至少按以下顺序包含：
  1. 代码修改
  2. 审查，包括功能是否正常、是否遵循设计和实施文档、是否引入需求范围外的修改，以及是否违反本规范相关规则。发现偏差时，修复后才能进入下一阶段。
  3. 最小必要验证
  4. 在实施文档中简要记录实施状态
  5. Git commit。每个阶段只能有一个 commit；不得仅为增加 commit 数量而拆分无意义的小提交。

## 设计与实施文档

- [functional-design] 功能设计的推理、自主决策、范围、冲突审查和设计文档内容必须遵守 [`functional-design.md`](functional-design.md)。
- [design-execution-separation] 原则上，设计文档和实施文档应分别编写。
- [doc-lightweight-exception] 对设计选择简单、预计一次实施即可完成的小型任务，即使触发了 [large-task-threshold]，设计和实施文档也可以合并。合并后的文档仍应区分设计决策与实施计划。如果任务扩大或需要多阶段实施，应恢复为独立文档。
- [task-doc-location] 优先将设计和实施文档保存到现有同类型文档路径。不存在时，使用 `docs/<module-or-task>/`。设计文档文件名应以 `[design]` 开头；实施文档文件名应以 `YYYY-MM-DD` 开头。
- [design-confirmation-gate] 按照 [`functional-design.md`](functional-design.md) 完成设计文档后，停止并等待用户确认。除非用户明确要求，否则确认前不得修改代码。
- [design-freeze] 用户确认设计文档后，它默认成为当前任务的设计基线。实施期间，不得仅因为找到“更整洁”“更通用”或“更易扩展”的实现就改变设计。只有发现设计错误、无法实施、重大风险、新用户需求或用户明确要求调整设计时，才重新开启设计讨论。再次获得确认前，不得继续偏离已确认设计进行实施。
- [execution-doc-scope] 实施文档应包含具体实施细节，主要回答“如何完成”，包括受影响文件、代码修改计划、阶段拆分、审查清单、验证计划和 commit 计划。
- [execution-doc-confirmation] 除非用户另有要求，实施文档默认不需要单独确认。设计确认后，AI 可以完成实施文档并直接进入实施阶段。

## Bug 修复规则

- [root-cause-first] 决定修复方案前先分析根因。
- [simple-bugfix] 对根因和方案明确的局部 bug 修复，可以在简要说明根因、方案和受影响文件后直接修改。只要不引入尚未解决的设计决策、依赖变更或公共契约变更，即使修复会纠正错误行为、更新紧密相关的测试或辅助文件、涉及多个文件，或者超过任意行数阈值，也仍适用本规则。
- [bugfix-plan-gate] 只有在根因或方案仍不确定、存在需要用户选择且有实质差异的方案、需要变更依赖或公共契约、行为影响广泛或跨越模块边界，或者实施需要分阶段进行或包含多个相对独立的子任务时，bug 修复才必须提供实施计划并等待用户确认。文件数量和修改行数不得单独作为触发实施计划的条件。
- [fallback-last] 自动降级或 fallback 行为必须始终是最后选项。
- [no-hardcoded-fix] 未告知用户并获得批准前，不得使用 hardcoded fix。
- [environment-fix-first] 对缺少工具、缺少配置、外部服务不可访问等问题，优先使用环境或配置方案修复：
  - 可以自动修复时，自动修复
  - 无法自动修复时，清楚说明缺少的内容
  - 不得通过吞掉异常或兼容 workaround 绕过问题
- [fallback-confirmation] 只有确认之前所有路径都不可行，并获得用户确认后，才可以考虑自动降级或 fallback 行为。
- [bugfix-delivery] 每次交付必须包括：根因、解决方案、影响范围和验证结果。

## 跨项目功能移植

- [port-source-baseline] 当用户要求把已有功能从源项目移植、复制或迁移到目标项目时，必须将源项目实现视为实施基线，而不是仅作为重新实现的灵感。除非用户明确缩小范围、源能力超出目标项目已确认的设计，或源实现经确认与目标项目不适配，否则应保留其已有能力、行为、边界情况处理和内部支撑实现。对不适配部分的处理以及由此产生的能力削减仍必须遵守 [port-deviation-gate]。
- [port-boundary-analysis] 修改目标项目前，必须从源功能入口开始追踪其直接依赖的所有实施层，并记录源项目到目标项目的对应关系。分析应按实际情况覆盖 UI 或 API 入口、状态与领域逻辑、service 与 data access、持久化、type、configuration、permission、validation、error handling、background behavior、asset、localization 和 test。应沿传递依赖追踪到已有 shared infrastructure 边界；不得假设可见入口就是完整功能。
- [port-functional-unit] 将源功能拆分为内聚且可以独立验证的内部功能单元。功能单元必须包含实现其行为所需的完整纵向切片；它既不是孤立的入口代码片段，也不必等同于整个功能或 module。
- [port-copy-then-adapt] 每次移植一个功能单元。在目标架构和技术允许的范围内，先整体复制该单元及其必要支撑实现和相关测试；再进行适配目标项目所必需的最小修改；只有确认行为等价后，才可以删除不需要的部分。复制、适配和删除在概念上必须分开，使遗漏和有意差异都可以被审查。
- [port-no-reimplementation] 不得用自行设计的新实现替代可用且兼容的源实现，不得只复制可见入口层，也不得通过孤立代码片段重新拼装功能。只有在确认存在导致整体移植不可行的不兼容，或者用户明确要求重新设计时，才可以重新实现。
- [port-review-without-silent-change] 移植分析同时应视为对源实现的一次 review。发现 bug、风险或有明确价值的改进机会时，应主动向用户说明证据和影响，但不得在移植过程中静默修复、重构、优化或以其他方式改变它们。默认保留源实现行为，并将此类修改分别提出；只有获得用户确认后才可以实施。
- [port-deviation-gate] 省略必要的源功能单元、削减能力、改变已有行为，或者以重新实现代替移植前，必须说明不兼容点、受影响行为、推荐方案和备选方案，并等待用户确认。目标项目规范只能作为局部适配的理由，不能作为静默削减能力或重新设计的理由。
- [port-completeness-verification] 必须同时验证源项目到目标项目的对应关系和最终行为。每个已发现的功能单元和支撑依赖都必须归入以下一种状态：已移植、已映射到目标项目既有能力、经确认后有意排除，或说明理由后判定为不适用。先运行最小相关的单元级验证，再验证具有代表性的端到端成功与失败流程；将源项目测试作为移植证据，并移植适用的 regression coverage。

## 代码风格、注释与日志

- [readability] 优先保证可读性。
- [english-code-text] 除非用户明确要求，否则 comment、log 和 documentation 默认使用英文。
- [chinese-markdown-prose-wrap] 不得按固定列宽硬折行中文 Markdown 正文。除非 Markdown 结构边界、代码块、表格或有意的 hard break 要求换行，否则每个段落和列表项应保持在一个物理行内。格式化中文 Markdown 时，使用 `proseWrap: never` 或等效行为。
- [file-size] 单个文件超过 500 行时，只有同时满足以下条件才考虑拆分；这不是强制要求：
  - 职责明确混杂
  - 拆分不会显著增加理解成本或文件导航复杂度
  - 当前修改已经涉及相关区域
- [comments] 注释规则：
  - 为复杂、公共或不明显的逻辑添加注释
  - 复杂 public function 或不明显 function 的注释应解释“为什么”，不要重复代码已经清晰表达的内容
  - 除非测试工具要求，Python 代码不需要 docstring；通常优先在 function declaration 前使用 `#` 注释
  - 重要逻辑分支、业务约束和不明显条件必须添加注释
- [concise-logs] 日志只应包含关键信息，并保持简洁易读。
- [sensitive-logs] 日志通常应避免输出 token、password、secret 或完整敏感用户字段。必要时进行掩码处理。
- [avoid-hardcode] 尽可能避免 hardcode。
  - 对存在明确环境差异、部署差异、用户配置要求或多处复用的值，应考虑参数化或配置化。
  - 如果引入任何 hardcode，必须明确向用户披露。

## 前端

- [frontend-specification] 所有前端任务都必须遵守 [`web-frontend.md`](web-frontend.md)。该文档是框架中立的 Web 前端架构、组件与库选择、feature 边界、状态流、样式、交互、可访问性、国际化、格式化和验证的仓库级权威来源。框架和 UI 库 skill 只补充实施指导，不能覆盖该规范。

## 测试与验证约束

- [test-addition] 默认不为低风险机械修改新增测试。当修改涉及业务行为、public API、权限、route、form、状态转换、async/concurrency/session/token 逻辑、bugfix regression、安全或数据一致性行为，或用户明确要求时，优先新增最小相关测试。
- [reuse-tests] 尽可能复用现有测试；不要优先创建新的 test file。
- [invariant-tests] 不得为已经由上游校验、类型约束或数据库约束保证的不变量编写测试，尤其是可信内部数据流。本规则不适用于外部输入边界、权限、安全或序列化/反序列化边界。
- [no-test-only-abstraction] 不得仅为方便测试而引入 helper、wrapper、composable 或 service abstraction。
- [verification-ladder] 优先使用覆盖已修改行为和可合理推断的直接影响区域的最小相关验证集。必要时根据风险按以下顺序逐级提高验证等级：静态推理 → typecheck → lint → targeted unit test → targeted integration test → E2E → full suite。如果当前验证等级已经足以验证修改或判断失败原因，不得继续升级。
- [full-suite] 只有涉及共享基础设施、global config、public type、auth/session/permission 逻辑、schema/migration 或跨 module 修改时，才应运行 full suite。
- [ui-visual-test] UI 视觉调整默认不新增测试。使用 typecheck/lint 和手工或浏览器视觉确认。
- [e2e-scope] E2E 测试只覆盖真实用户 workflow，不覆盖简单颜色、间距、文本、图标或 prop 修改。
- [snapshot] 默认禁止更新 snapshot，除非 UI 结构发生与需求直接相关的变化。
- [test-expectation] 除非确认原测试错误，否则不得仅为使测试通过而修改 test expectation。
- [unrelated-failures] 测试失败时，先判断失败是否与当前修改有关。不得随意修复无关失败。
- [no-repeat-verification] 除非相关文件再次修改，否则不得重复运行已经通过的验证。
- [test-unavailable] 无法执行测试时，说明原因并提供建议的验证命令。
- [verification-report] 最终交付必须说明运行了哪些验证、未运行哪些验证及其原因。
- [final-review] 最终交付前确认：
  - 实施是否满足用户要求
  - 是否引入了不必要修改
  - 是否遵守本规范相关约束
  - 是否完成必要验证
  - 是否遗漏验证风险或影响范围说明
