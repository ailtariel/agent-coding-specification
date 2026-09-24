# Personal agent rules and skills

本仓库统一维护个人 AI 编码规范与 skills。规范约束容易反复出现的错误行为，skills 提供具体工作流和技术参考。Composition API、TypeScript、`<script setup>`、ESM、避免 Reactive Props Destructure 等属于有意保留的个人偏好；这些偏好不构成重写无关代码的理由。

## 目录与维护边界

| 路径 | 用途 |
| --- | --- |
| `AGENTS.md` | 仓库／工作区规则入口 |
| `AI-coding-specification/README.md` | 生效规范路由；通用、功能设计、前端、分阶段任务及移植规则 |
| `AI-coding-specification-cn/` | 对应中文维护稿，不安装到 agent 环境 |
| `skills/` | 完整迁入的 skill-sets 内容，以及纳入维护的用户／系统 skills |
| `skills/PROVENANCE.md` | 来源、迁移基线和定制边界 |
| `skills/system-overrides.json` | 需要替代的 Codex 系统 skill 名称 |
| `scripts/install.py` | Windows、WSL、macOS 共用的安装、检查及恢复工具 |
| `scripts/check_codex.py` | 通过 Codex app-server 验证实际 skill 发现结果，不发起模型任务 |

原 `C:/workstation/dev/personal/skill-sets` 的全部 420 个工作树文件已迁入 `skills/`，复制时逐文件校验 SHA-256。原仓库及 Git 历史保留在 `C:/workstation/dev/personal/skill-sets.pre-migration-20260924/`。旧目录因被其他进程占用而无法整体重命名，内容已全部移入归档，只留下 README 指向新位置。后续修改和提交只在本仓库进行。源仓库中的新版 Vue、Vuetify、本地参考文档、许可证和上游来源均保留。

## 安装原理

需要 **Python 3.11+**；安装程序仅使用标准库，不需要管理员、pip、Node 或网络。使用 Codex 的发现验证功能时才需要本机 Codex CLI。

安装目标按当前用户解析：

| 内容 | 位置 |
| --- | --- |
| 生效规范快照 | `~/.agents/agent-coding-specification/specification/` |
| 用户 skills | `~/.agents/skills/` 下的受管目录，保留 frontend 的嵌套结构 |
| 全局规范入口 | `$CODEX_HOME/AGENTS.md`；已有 `AGENTS.override.md` 时修改后者 |
| 默认 Codex Home | 未设置 `CODEX_HOME` 时为 `~/.codex/` |
| 系统 skill 禁用配置 | Codex Home 内的 `config.toml` |
| 安装记录和备份 | `~/.agents/agent-coding-specification/installed.json` 与 `backups/` |

Windows 的 `~` 是当前 Windows 用户目录；WSL 和 macOS 是当前 Unix 用户目录。WSL 与 Windows 各自安装，不共享 `.codex` 配置。安装的规范引用本机快照的绝对路径，因此 WSL 不依赖 Windows 盘持续挂载。

脚本只替换本仓库管理的 skill 目录，保留无关 skills。全局 AGENTS 使用带 `BEGIN/END agent-coding-specification` 标记的区块合并，保留区块外个人内容；能够识别本仓库旧版完整模板时会迁移旧入口并保留 User Preferences。无法识别的旧内容不会自动删除，应检查是否还引用过期规范。

所有待替换内容先备份，再写入并校验；失败时恢复本次已触及的目标。重复安装且源未变化时不产生新备份。不直接修改安装副本；修改本仓库后重新执行安装即可同步。

## Windows

在 PowerShell 中进入本仓库：

```powershell
Set-Location 'C:\workstation\dev\personal\agent-coding-specification'
python --version
python scripts/install.py --dry-run
python scripts/install.py
python scripts/install.py --check
python scripts/check_codex.py
```

如果 Python 命令是 `py -3`，将上述 `python` 替换为 `py -3`。路径包含空格时加引号。预览和 `--check` 不写入安装目标。

验证脚本会打印所用 Codex 的版本和路径。若 PATH 指向旧 CLI，应通过 `--codex` 指定实际使用的编辑器 Codex 可执行文件，例如：

```powershell
python scripts/check_codex.py --codex 'C:\Users\<user>\.vscode\extensions\openai.chatgpt-<version>-win32-x64\bin\windows-x86_64\codex.exe'
```

`<user>` 和 `<version>` 必须替换为本机真实路径。本次机器的 npm CLI 0.87 不识别 `~/.agents/skills`，实际验证使用 VS Code 内置 Codex 0.155.0-alpha.16.3；如果要在旧 CLI 中使用这些 skills，需将 CLI 更新到支持该目录的版本。

## WSL

先从 Windows 查看发行版，再以日常开发用户进入目标发行版，不使用 root：

```powershell
wsl --list --verbose
wsl -d Ubuntu
```

在 WSL 内可以从 Windows 的同一工作树安装：

```bash
cd /mnt/c/workstation/dev/personal/agent-coding-specification
python3 --version
python3 scripts/install.py --dry-run
python3 scripts/install.py
python3 scripts/install.py --check
python3 scripts/check_codex.py
```

也可以使用 WSL 内独立 clone 的本仓库，命令不变。每个需要使用的发行版／用户分别运行安装；Docker Desktop 等内部发行版不属于开发用户安装目标。`CODEX_HOME` 若有定制，使用该用户真实的配置路径。

从 PowerShell 直接执行 WSL 的验证命令时，应使用 `wsl -d Ubuntu -- bash -lc 'python3 /mnt/c/workstation/dev/personal/agent-coding-specification/scripts/check_codex.py'`，以加载 Linux 用户 PATH；也可通过 `--codex /home/<user>/.npm-global/bin/codex` 指定 Linux CLI。裸 `wsl -- command` 在当前机器会先找到 Windows npm 的旧版本。本次 Linux CLI 0.139.0 已通过发现验证。

## macOS

将本仓库 clone 到个人开发目录，确保 Python 3.11+ 已安装，然后：

```bash
cd /path/to/agent-coding-specification
python3 scripts/install.py --dry-run
python3 scripts/install.py
python3 scripts/install.py --check
python3 scripts/check_codex.py
```

不使用 `sudo`。脚本不依赖 Windows junction、GNU 专有命令或 WSL。当前验证环境为 Windows 和 Ubuntu；未进行真实 macOS 运行验证。

## 验证与系统 skill 替代

安装后重新启动 Codex，使 `config.toml` 变更生效。`--check` 验证规范快照、skills、入口区块、禁用配置和安装记录与当前源一致；`check_codex.py` 通过只读 `skills/list` 检查每个受管 skill 只出现一个启用版本，且路径为安装副本。也可在新会话查看 `/skills`，并要求 agent 列出加载的规则来源。

Codex 官方文档说明，同名 skills 不保证合并或覆盖，因此本仓库采用“安装用户副本＋禁用原路径”。目前替代 `openai-docs`：

```toml
[[skills.config]]
path = "/absolute/codex-home/skills/.system/openai-docs/SKILL.md"
enabled = false
```

实际路径由安装程序生成。以后替代其他系统 skill 时，先将其完整目录和资源提取至 `skills/<name>/`，修订后把名称加入 `skills/system-overrides.json`，再安装和验证。不要只复制一个 `SKILL.md`，也不要直接改 `.system` 缓存。Codex 升级后重新运行检查；如果内置路径或发现协议变化，需要相应更新安装配置。

官方说明：[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)、[skills 目录及禁用配置](https://learn.chatgpt.com/docs/build-skills)、[app-server skills/list](https://learn.chatgpt.com/docs/app-server)。

## 更新、恢复与定制路径

日常更新：拉取／修改本仓库，再分别在 Windows、WSL、macOS 运行 `scripts/install.py` 和 `--check`。不需要复制规则到每个项目。

恢复时使用安装输出的备份绝对路径：

```bash
python3 scripts/install.py --restore /home/me/.agents/agent-coding-specification/backups/<timestamp>
```

Windows 对应使用 `python` 和带引号的 Windows 路径。恢复仅处理那次安装替换的目标；如果安装后目标又被修改，脚本拒绝覆盖，需要先保留和处理这些修改。多次安装应按时间倒序恢复，避免覆盖后续版本。

可用 `--codex-home /custom/codex` 指定 Codex 配置目录。`--home /isolated/user` 可测试另一个用户目录；若同时设置了 `CODEX_HOME`，它仍优先，测试时建议同时指定 `--codex-home`。路径被链接到外部位置或与源仓库重叠时，安装器会报告而不是覆盖。

上游 skill 更新仅用于比较：

```bash
python3 skills/update_skills.py --list
python3 skills/update_skills.py --skill vue,pinia
```

检查 `skills/tmp/update-skills/staged/` 后手工合并必要变化；`--apply` 已禁用，防止上游更新抹掉个人偏好和修订后的流程。Vuetify 本地参考资料按自身来源维护。

维护安装器时运行：

```bash
python3 -m unittest discover -s tests -v
```

## 项目补充规范与其他 agents

全局规则先按任务路由加载本仓库规范，再合并当前工作区和受影响仓库的 `AI-coding-specification/`。同名文件由工作区版本替代，不同名相关文件补充。当前用户明确指令优先；重要歧义只暂停依赖部分，不把已授权实施重新转为审批。

其他支持 AGENTS.md 的工具，可把根 `AGENTS.md` 与生效规范目录安装到项目根；已有入口应合并。Claude Code 使用 `CLAUDE.md` 引用相同规范路由；Cursor 等工具使用各自实际读取的入口。Skills 的发现目录随工具不同，需遵循其配置。上述自动安装器和系统 skill 替代机制针对 Codex。

## 规则维护原则

规则应描述清晰的场景、边界和预期结果，避免重复约束、固定仪式和无关流程。共用规范保持跨模型可用；模型特有偏好放在个人配置。按风险选择最小充分验证，保留明确的完成条件和既有授权。中文 Markdown 正文不按固定列宽硬折行。
