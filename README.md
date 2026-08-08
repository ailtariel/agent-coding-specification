# How to use

## Codex CLI

推荐将本仓库作为规范的唯一事实来源，并通过 Codex 全局 `AGENTS.md` 引用其实际路径，不要向每个仓库复制规范文件。

全局 `AGENTS.md` 应放在 Codex Home 中，即 `CODEX_HOME/AGENTS.md`；未设置 `CODEX_HOME` 时，默认位置为 `~/.codex/AGENTS.md`。`~/.agents/skills` 是用户级 skills 的目录，不是 Codex 全局 `AGENTS.md` 的位置。详见 [Codex 官方 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)和 [Codex 官方 skills 文档](https://learn.chatgpt.com/docs/build-skills)。

### 配置方法

1. 确认本仓库的绝对路径，例如：

   ```text
   C:/Workstation/Dev/codes/personal/agent-coding-specification/
   ```

2. 确定 Codex 全局 `AGENTS.md` 的位置，并检查它是否已经存在。PowerShell 示例：

   ```powershell
   $specRepo = (Resolve-Path .).Path
   $codexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
   $globalAgents = Join-Path $codexRoot 'AGENTS.md'

   New-Item -ItemType Directory -Path $codexRoot -Force | Out-Null
   Get-Item -Force -ErrorAction SilentlyContinue $globalAgents
   ```

3. 如果全局 `AGENTS.md` 不存在，复制仓库中的 `AGENTS.global.template.md`：

   ```powershell
   Copy-Item -LiteralPath (Join-Path $specRepo 'AGENTS.global.template.md') -Destination $globalAgents
   ```

   如果文件已经存在，不要覆盖。保留其中已有的全局偏好，并手动合并 `AGENTS.global.template.md` 的内容。

4. 打开全局 `AGENTS.md`，将模板中的路径占位符改为本仓库 `AI-coding-specification/` 目录的实际绝对路径，并补充需要保留的个人偏好：

   ```powershell
   notepad $globalAgents
   ```

5. 检查 Codex Home 中是否存在 `AGENTS.override.md`。如果存在，Codex 会优先读取它而忽略同级 `AGENTS.md`，因此需要将模板规则合并到 `AGENTS.override.md`，或者在确认其内容不再需要后移走该文件。

6. 重新启动 Codex 会话，然后验证实际加载结果：

   ```powershell
   codex --ask-for-approval never "列出当前加载的指令来源，并总结编码规范的优先级。"
   ```

预期结果应包含 Codex Home 下的全局 `AGENTS.md`，并说明 `AI-coding-specification/` 高于通用 skills、框架 skills 和 agent defaults。仓库或子目录中的 `AGENTS.md` 会在全局文件之后加载，因此局部规则应只补充或加强规范，不应削弱全局规范。

后续只需维护本仓库的 `AI-coding-specification/`。只有在本仓库移动到其他位置时，才需要再次修改全局 `AGENTS.md` 中的绝对路径。

## 其它兼容 AGENTS.md 的 agents

把 `AGENTS.md` 和 `AI-coding-specification` 复制到项目根目录。

如果已有 `AGENTS.md`，请自行合并内容。

`AI-coding-specification-cn/` 是本仓库维护中文草稿用的目录，不属于安装内容。

## Claude Code

将 `AGENTS.md` 的内容合并到项目根目录的 `CLAUDE.md`，并保留其中对 `AI-coding-specification/coding-specification.md` 的读取要求。

如果项目同时使用 Codex 和 Claude Code，可以同时维护 `AGENTS.md` 和 `CLAUDE.md`，两者都引用同一份 `AI-coding-specification/coding-specification.md`，避免规则内容分叉。

## Other AI coding tools

如果使用 Cursor、Cline、Roo Code、Continue、Aider、GitHub Copilot 等不一定读取 `AGENTS.md` 的工具，请把 `AGENTS.md` 中的规则入口迁移或合并到该工具实际读取的项目规则文件中。

推荐做法是：不同工具维护各自的入口文件，但都引用同一份 `AI-coding-specification/coding-specification.md`，不要把完整规范复制到多个工具配置里，避免规则内容分叉。

## 扩展

如果你要扩展更多规则，例如：

- 如何维护部署配置文件
- 如何同步管理git issues和PR

你可以在 `AI-coding-specification` 增加相关规则文件，并在 `AGENTS.md` 文档中的 “## Required Reading Order” 一节显式索引它，并说明适用场景。

## Notes

之所以不把它做成skill，是因为仓库级规则通常能拥有比skill更高的优先级，避免这些规则被skill覆盖。

部分规则具有个人/项目倾向性，可能并不适合你的项目，使用前请认真先自行审阅。
