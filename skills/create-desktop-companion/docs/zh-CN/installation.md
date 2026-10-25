# 安装

[English](../en/installation.md) · [README](../../README.zh-CN.md)

前提：安装 Git 并具有仓库访问权限。有提示时使用正常的 GitHub 认证，不将令牌写入克隆 URL。

Skill 名称为 `create-desktop-companion`。目录名与完整文件应保持一致。安装指南不等于安装桌宠，也不会自动增加图像生成权限。

## 安装本地 Skill

以下命令创建新的克隆目录，不应覆盖已有安装。

### Codex：个人安装（macOS/Linux）

```sh
mkdir -p "$HOME/.agents/skills"
git clone --filter=blob:none --sparse https://github.com/yuejianli-z/chatgpt-codex-pet-skill.git chatgpt-codex-pet-skill
git -C chatgpt-codex-pet-skill sparse-checkout set skills/create-desktop-companion
cp -R chatgpt-codex-pet-skill/skills/create-desktop-companion "$HOME/.agents/skills/create-desktop-companion"
```

项目内使用时，在项目根目录操作，将目标改为 `.agents/skills/create-desktop-companion`。最终入口应为 `.agents/skills/create-desktop-companion/SKILL.md`。

### Claude Code：个人安装（macOS/Linux）

```sh
mkdir -p "$HOME/.claude/skills"
git clone --filter=blob:none --sparse https://github.com/yuejianli-z/chatgpt-codex-pet-skill.git chatgpt-codex-pet-skill
git -C chatgpt-codex-pet-skill sparse-checkout set skills/create-desktop-companion
cp -R chatgpt-codex-pet-skill/skills/create-desktop-companion "$HOME/.claude/skills/create-desktop-companion"
```

项目内安装则使用 `.claude/skills/create-desktop-companion`。启动本地 Claude Code 会话后，通过 `/create-desktop-companion` 调用。本地个人目录不会自动安装到 Cowork 或远程云会话。

### Windows PowerShell

Codex 示例：

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills"
git clone --filter=blob:none --sparse https://github.com/yuejianli-z/chatgpt-codex-pet-skill.git chatgpt-codex-pet-skill
git -C chatgpt-codex-pet-skill sparse-checkout set skills/create-desktop-companion
Copy-Item -Recurse chatgpt-codex-pet-skill/skills/create-desktop-companion "$HOME/.agents/skills/create-desktop-companion"
```

Claude Code 将 `.agents/skills` 改为 `.claude/skills`。没有 Git 时，可下载所需分支的 ZIP，解压后将含有 `SKILL.md` 的目录重命名并复制到同一位置，避免多嵌套一层仓库目录。

## 确认加载与版本

1. 确认所选 Skill 根目录下直接存在 `create-desktop-companion/SKILL.md`。
2. 检查 `VERSION` 与检出的分支或标签。PR 内容不一定已进入默认分支。
3. 启动或重新加载宿主会话，确认可用 Skill 列表中出现该名称；先让助手读取并报告版本，再开始制作。
4. 若未发现，检查宿主信任设置与正式加载说明，不使用虚构安装命令，也不写入私人缓存路径。

以上路径于 2026-10-24 对照 [OpenAI 本地 Skill 文档](https://learn.chatgpt.com/docs/build-skills)与 [Claude Code 文档](https://code.claude.com/docs/en/skills)核对。[Agent Skills 规范](https://agentskills.io/specification)要求名称与父目录一致。这是文档支持的安装路径，不代表每个宿主版本均已完成端到端实测。

更新前保留本地修改，在仓库检出目录通过 Git 获取并检查变化，然后重新复制 Skill 目录。卸载时，仅通过正常可恢复的文件管理方式移除该 Skill 目录。移除 Skill 不会自动删除项目输出或已安装桌宠。

## Python 工具

在包含 `SKILL.md` 的目录执行：

```sh
python3 -m venv "$HOME/.venvs/create-desktop-companion"
. "$HOME/.venvs/create-desktop-companion/bin/activate"
python -m pip install -r requirements.txt
python scripts/preflight.py
```

Windows PowerShell：

```powershell
py -3 -m venv "$HOME/.venvs/create-desktop-companion"
& "$HOME/.venvs/create-desktop-companion/Scripts/python.exe" -m pip install -r requirements.txt
& "$HOME/.venvs/create-desktop-companion/Scripts/python.exe" scripts/preflight.py
```

需要 Python 3.10+ 和 Pillow。控制器测试需要 Node.js；浏览器测试还需要 Playwright 和可运行的 Chromium。ffmpeg 可用于外部视频制作，不是本项目的依赖或内置渲染器。具体输出见[示例](examples.md)，实际测试范围见[验证记录](../validation.md)。

## 制作前提

| 能力 | 用途 | 不具备时 |
|---|---|---|
| 可读取参考图 | 身份检查 | 基于描述规划，并说明缺少视觉证据 |
| 获准的生成/编辑工具 | 制作新图 | 规划动作或检查已有素材 |
| 本地 Python/Pillow | 运行诊断 | 提供操作说明，不声称已测试 |
| 实际尺寸播放 | 动作与观看舒适度 | 保留未观看状态 |
| 宿主导入工具 | 安装 | 仅交付独立资产 |

使用实际可用的服务与宿主。私人参考默认留在本地，外传须有相应许可。费用、条款、素材权利和原生安装与安装本 Skill 分开处理。


仓库根目录不是可安装的 Skill。只复制 `skills/create-desktop-companion`，不要复制仓库根目录或 `examples/characters`。如果本地已有 `chatgpt-codex-pet-skill`，请选择新的检出目录名。更新时先在仓库检出目录审阅更新并保存本地修改，再替换安装副本；安装副本本身不是 Git 检出目录。


## 当前制作补充

按[频率与疲劳设计](exposure-design.md)规划动作及未来展示顺序；按[OpenAI 独立制作与安装](openai-production.md)导出 v2 并在验收后安装。这不替代各宿主的真实触发证据和视觉认可。


虚拟环境放在可分发 Skill 目录之外。发布检查使用干净副本并设置 `PYTHONDONTWRITEBYTECODE=1`；包检查会有意拒绝缓存和本地环境。
