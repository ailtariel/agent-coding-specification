作者：ailtariel@gmail.com 更新日期：2026-09-24

# 仓库级 AI 编码规范

本规范定义目标工作区或受影响仓库中 AI 辅助编码任务的高优先级工程标准。

除非用户明确要求，否则本规范优先于其他 skill 中与之冲突的建议。

## 规则使用方式

- 本文档是仓库级强制规范，不是按需加载的 skill。所有代码相关任务默认都应遵守整份文档。
- 当一个任务同时适用多个规则块时，必须同时遵守所有规则。非安全类实施决策按照 [priority] 权衡取舍；安全风险必须遵守 [security-confirmation]。
- 规则标签用于交付说明、审查和自检。不得仅为了满足某个标签而扩大实施范围。

## 通用规则

- [authorization-and-completion] 任务授权在会话中持续有效。明确的实施或修复请求包括范围内必要的调查、设计细化、代码修改、相关验证及修复当前改动引入的问题；只做 review 或设计的请求不授权实施。仅在未获授权的重要产品、架构、依赖、公共契约或不可逆操作需要决定时暂停相关工作；继续独立且已授权的部分。提问前完成可执行的准备，给出具体方案、影响和建议；若规则导致暂停，指出规则文件和条款。完成条件是用户目标已实现、必要检查完成、相关失败已处理，并如实说明未验证范围；不要停在首版实现。

- [priority] 用户明确要求 > 正确性 > 可维护性 > 最小修改 > 安全性 > 风格与简洁性
- [minimal-context]
  - 优先读取与当前任务直接相关的最小文件集合。
  - 不得无目的地扫描整个仓库、读取大量无关文件，或重复读取已经确认无关的文件。
- [plan-first] 编写代码前简要说明预期修改和影响范围。只有复杂依赖、重要设计取舍或实施阶段需要保留时才制定计划；简单修改默认不创建正式计划。需要计划不等于需要审批。文件数、行数或多个独立子任务本身不触发用户确认。按 [authorization-and-completion] 判断是否存在尚未授权的决策。
- [security-confirmation] 主动沟通与当前任务直接相关且有证据的安全风险。已经授权的安全修复可继续实施；未获授权的功能、架构、部署或安全策略变更才需用户决定。局部、低风险、行为明确且不改变公共契约的加固可以直接实施。不要因假想风险引入额外审批或扩大范围。
- [behavior-preservation] 除非任务明确要求改变行为，否则默认保留现有运行时行为、异常行为、执行时序、返回结构和副作用。如果当前实现已经正确工作，且任务不要求改变该行为，不得仅因为另一种实现看起来“更整洁”、“更现代”或“更通用”而重写。
- [no-unrelated-churn] 不得随意重构、重新格式化、调整 import 顺序或重命名，除非它们与当前任务直接相关。
- [no-speculation] 没有当前需求来源时，不得进行修改：
  - 不得提前为未来扩展性设计。只实施已确认的需求；不得实现未请求的功能。
  - 不得仅因为“未来可能有用”“未来可能需要扩展”或“顺便改善结构”而重构现有代码。
  - 没有明确计划或需求来源时，不得添加 TODO/FIXME 注释。
- [no-extra-abstraction] 不得引入不必要的抽象层，包括不必要的 class、interface、wrapper 或 helper。
- [abstraction-exception] 本规则适用于后端代码。抽取应服务于明确的职责边界、真实复用或必要的复杂逻辑隔离，并保留已确认行为、改善整体理解和维护成本。优先复用既有能力；不创建只转发调用的无意义层。减少行数可以作为收益，但不是必要条件。
- [validation-boundary] 在外部输入和真实信任边界校验数据。同一可信链路中不重复相同校验或兜底；跨越新的信任边界，或操作需要检查不同业务不变量时，可执行必要校验。不要按代码层数机械增加校验。
- [wrapper-pass-through] 包装函数、对象或服务调用时，默认原样透传其返回值和错误，并保留原有的错误传播方式。没有明确的需求或设计依据时，不得筛选字段、重构或二次包装返回结构、替换错误，或修改原始返回数据。确需转换时，例如适配已定义的契约或对敏感信息脱敏，只能进行该目的所必需的变更，保留其余信息和错误语义。
- [no-silent-failure] 禁止静默失败。除非用户明确同意降级行为，否则应通过日志或返回响应清晰暴露错误。
- [api-error-detail] 返回 API 错误响应时，只要来源中存在 `error`、`text` 或 `message` 等有意义的错误码或错误文本，就应保留。内容包含敏感信息时，返回前必须脱敏。
- [try-catch] 不得过度使用 try...catch。只在以下情况使用：
  - 失败后执行仍必须继续
  - 需要统一或格式化错误消息
  - 需要资源清理或事务一致性，例如 rollback 或释放连接
- [public-contract] 除非用户明确要求，否则不得修改 public API、database schema、配置格式或环境变量名称。
- [dependency-gate] 不得引入未经批准的新依赖。如果新依赖确实必要且尚未获得授权，先说明原因并等待确认。

## 操作系统与工具

- [rg-first] 对查找文件、搜索文本、统计匹配等适合 `rg` 的操作，即使在 Windows 上也应先尝试 `rg`，除非已经确认不可用。文件发现优先使用 `rg --files`，内容搜索优先使用 `rg`，然后才 fallback 到 PowerShell 遍历或 `Select-String`。
- [powershell-utf8] 使用 PowerShell 读写文本文件时，对支持编码参数的命令默认显式传入 `-Encoding UTF8`，例如 `Get-Content`、`Set-Content`、`Add-Content`、`Out-File`、 `Import-Csv` 和 `Export-Csv`。
- [powershell-raw-text] 使用 PowerShell 读取整个文本文件进行分析时，优先使用 `Get-Content -Raw -Encoding UTF8`；没有 `-Raw` 时，PowerShell 返回行数组，可能改变后续行为。
- [powershell-native-quoting] 通过 PowerShell 向 native tool 传递 regex、pipe、quote、brace 或 semicolon 时应谨慎处理解析。Shell 解析可能改变参数时，优先使用单引号 pattern、 `rg -F` 固定字符串搜索，或每次调用只执行一个简单命令。
- [powershell-aliases] 不得假设常见 Unix 命令名在 PowerShell 中具有 Unix 语义。`curl`、 `wget`、`cat`、`ls` 和 `rm` 等命令可能是 alias 或具有不同的行为；优先使用明确的 native command 或目标 PowerShell cmdlet。
- [rg-exit-code] `rg` 退出码 `1` 表示“没有找到匹配”，不一定是命令失败。大于 `1` 的退出码才表示实际错误。

## 大型任务

需要此流程时读取 [large-tasks](large-tasks.cn.md).

## 设计与实施文档

- [functional-design] 功能设计的推理、自主决策、范围、冲突审查和设计文档内容必须遵守 [`functional-design.md`](functional-design.cn.md)。
- [design-execution-separation] 原则上，设计文档和实施文档应分别编写。
- [doc-lightweight-exception] 对设计选择简单、预计一次实施即可完成的小型任务，即使触发了 [large-task-threshold]，设计和实施文档也可以合并。合并后的文档仍应区分设计决策与实施计划。如果任务扩大或需要多阶段实施，应恢复为独立文档。
- [task-doc-location] 优先将设计和实施文档保存到目标工作区或受影响仓库中现有的同类型文档路径。不存在时，使用对应目标仓库根目录下的 `docs/<module-or-task>/`。设计文档文件名应以 `[design]` 开头；实施文档文件名应以 `YYYY-MM-DD` 开头。
- [design-confirmation-gate] 只有用户要求先审设计，或者仍有尚未授权的重要决策时，才在设计后等待确认。用户已授权完整实施且关键决策已明确时，设计细化和文档完成不另设审批关卡。
- [design-freeze] 用户确认设计文档后，它默认成为当前任务的设计基线。实施期间，不得仅因为找到“更整洁”“更通用”或“更易扩展”的实现就改变设计。只有发现设计错误、无法实施、重大风险、新用户需求或用户明确要求调整设计时，才重新开启设计讨论。用户明确的新要求确定相应变更；仅对尚未授权的重要偏离重新确认，继续基线内的独立工作。
- [execution-doc-scope] 实施文档应包含具体实施细节，主要回答“如何完成”，包括受影响文件、代码修改计划、阶段拆分、审查清单、验证计划和 commit 计划。
- [execution-doc-confirmation] 实施文档默认无需单独确认。已有实施授权且无阻塞决策时，完成必要计划后继续执行。
## Bug 修复规则

- [root-cause-first] 决定修复方案前先分析根因。
- [simple-bugfix] 对根因和方案明确的局部 bug 修复，可以在简要说明根因、方案和受影响文件后直接修改。只要不引入尚未解决的设计决策、依赖变更或公共契约变更，即使修复会纠正错误行为、更新紧密相关的测试或辅助文件、涉及多个文件，或者超过任意行数阈值，也仍适用本规则。
- [bugfix-plan-gate] 根因不明确时继续调查；影响广泛、依赖复杂或需要分阶段实施时制定相称的计划。只有未获授权的重要行为、公共契约、依赖或架构取舍才请求用户决定。不要把调查或计划本身变成审批关卡。
- [fallback-last] 自动降级或 fallback 行为必须始终是最后选项。
- [no-hardcoded-fix] 使用 hardcoded fix 需要用户知情批准；已有明确批准按 [authorization-and-completion] 持续有效。
- [environment-fix-first] 对缺少工具、缺少配置、外部服务不可访问等问题，优先使用环境或配置方案修复：
  - 可以自动修复时，自动修复
  - 无法自动修复时，清楚说明缺少的内容
  - 不得通过吞掉异常或兼容 workaround 绕过问题
- [fallback-confirmation] 自动降级或 fallback 行为需要有证据表明之前适用的路径不可行，并获得用户知情批准；该行为已被明确授权时，不再重复请求相同批准。
- [bugfix-delivery] 每次交付必须包括：根因、解决方案、影响范围和验证结果。

## 跨项目功能移植

需要此流程时读取 [feature-porting](feature-porting.cn.md).

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

- [frontend-specification] 所有前端任务都必须遵守 [`web-frontend.md`](web-frontend.cn.md)。该文档是框架中立的 Web 前端架构、组件与库选择、feature 边界、状态流、样式、交互、可访问性、国际化、格式化和验证的仓库级权威来源。框架和 UI 库 skill 只补充实施指导，不能覆盖该规范。

## 测试与验证约束

- [test-addition] 默认不为低风险机械修改新增测试。当修改涉及业务行为、public API、权限、route、form、状态转换、async/concurrency/session/token 逻辑、bugfix regression、安全或数据一致性行为，或用户明确要求时，优先新增最小相关测试。
- [reuse-tests] 尽可能复用现有测试；不要优先创建新的 test file。
- [invariant-tests] 不得为已经由上游校验、类型约束或数据库约束保证的不变量编写测试，尤其是可信内部数据流。本规则不适用于外部输入边界、权限、安全或序列化/反序列化边界。
- [no-test-only-abstraction] 不得仅为方便测试而引入 helper、wrapper、composable 或 service abstraction。
- [verification-ladder] 按变更风险和失败机制选择最小充分的验证组合，覆盖修改行为和可合理推断的直接影响。静态推理、typecheck、lint、单元、集成、E2E 和全量测试是可选工具，不是必须依次经过的阶梯。必要检查通过且无未解决问题后结束，不继续扩大验证。
- [full-suite] 只有涉及共享基础设施、global config、public type、auth/session/permission 逻辑、schema/migration 或跨 module 修改时，才应运行 full suite。
- [ui-visual-test] UI 视觉调整默认不新增测试。使用 typecheck/lint 和手工或浏览器视觉确认。
- [e2e-scope] E2E 测试只覆盖真实用户 workflow，不覆盖简单颜色、间距、文本、图标或 prop 修改。
- [snapshot] 默认禁止更新 snapshot，除非 UI 结构发生与需求直接相关的变化。
- [test-expectation] 除非确认原测试错误，否则不得仅为使测试通过而修改 test expectation。
- [unrelated-failures] 测试失败时，先判断失败是否与当前修改有关。不得随意修复无关失败。
- [no-repeat-verification] 仅当相关代码、依赖、配置、环境或夹具发生变化，或者已有结果存在具体可靠性疑问时，重跑已通过的验证。
- [test-unavailable] 无法执行测试时，说明原因并提供建议的验证命令。
- [verification-report] 最终交付必须说明运行了哪些验证、未运行哪些验证及其原因。
- [final-review] 最终交付前确认：
  - 实施是否满足用户要求
  - 是否引入了不必要修改
  - 是否遵守本规范相关约束
  - 是否完成必要验证
  - 是否遗漏验证风险或影响范围说明
