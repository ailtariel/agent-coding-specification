# How to use

## CODEX CLI 及其它兼容 AGENTS.md 的agents

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
