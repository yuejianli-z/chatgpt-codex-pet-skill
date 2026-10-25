# Installation

[中文](../zh-CN/installation.md) · [README](../../README.md)

Prerequisites: Git and access to the repository. Use your normal GitHub authentication when prompted; never put a token in a clone URL.

The skill's name is `create-desktop-companion`. Keep that directory name and the complete contents together. Installing the instructions does not install a pet or add image-generation access.

## Local skill installation

From a terminal, choose one destination. The commands below create a new checkout and must not overwrite an existing installation.

### Codex: personal installation (macOS/Linux)

```sh
mkdir -p "$HOME/.agents/skills"
git clone --filter=blob:none --sparse https://github.com/yuejianli-z/chatgpt-codex-pet-skill.git chatgpt-codex-pet-skill
git -C chatgpt-codex-pet-skill sparse-checkout set skills/create-desktop-companion
cp -R chatgpt-codex-pet-skill/skills/create-desktop-companion "$HOME/.agents/skills/create-desktop-companion"
```

For repository-local use, run from your project root and replace the destination with `.agents/skills/create-desktop-companion`. The expected entrypoint is `.agents/skills/create-desktop-companion/SKILL.md`.

### Claude Code: personal installation (macOS/Linux)

```sh
mkdir -p "$HOME/.claude/skills"
git clone --filter=blob:none --sparse https://github.com/yuejianli-z/chatgpt-codex-pet-skill.git chatgpt-codex-pet-skill
git -C chatgpt-codex-pet-skill sparse-checkout set skills/create-desktop-companion
cp -R chatgpt-codex-pet-skill/skills/create-desktop-companion "$HOME/.claude/skills/create-desktop-companion"
```

For project-local use, choose `.claude/skills/create-desktop-companion` instead. Start a local Claude Code session and invoke `/create-desktop-companion`. Local personal folders do not automatically install a skill into Cowork or remote cloud sessions.

### Windows PowerShell

For Codex:

```powershell
New-Item -ItemType Directory -Force "$HOME/.agents/skills"
git clone --filter=blob:none --sparse https://github.com/yuejianli-z/chatgpt-codex-pet-skill.git chatgpt-codex-pet-skill
git -C chatgpt-codex-pet-skill sparse-checkout set skills/create-desktop-companion
Copy-Item -Recurse chatgpt-codex-pet-skill/skills/create-desktop-companion "$HOME/.agents/skills/create-desktop-companion"
```

For Claude Code, substitute `.claude/skills` for `.agents/skills`. If Git is unavailable, download the intended branch's ZIP, extract it, and rename/copy the directory containing `SKILL.md` to the same destination. Avoid an extra nested repository folder.

### Verify discovery and version

1. Check that `create-desktop-companion/SKILL.md` exists directly under your chosen skill root.
2. Check `VERSION` and your checked-out branch/tag. PR changes are not necessarily on the default branch.
3. Start or reload the host session and confirm the skill appears in its available skills. Ask it to read the skill and report its version before starting production.
4. If discovery fails, check the host's trust/settings and documented loader. Do not invent an install command or move files into a private cache.

Paths above were checked against [OpenAI's local skill documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code's skill documentation](https://code.claude.com/docs/en/skills) on 2026-10-24. The [Agent Skills specification](https://agentskills.io/specification) requires the skill name to match its parent directory. These are documented installation locations, not a claim of an end-to-end installation test on every host/version.

To update, review upstream changes in the repository checkout and copy the updated skill folder after preserving local edits. To uninstall, remove only this skill directory using your normal recoverable file-management workflow. Removing the skill does not remove generated project files or installed pets.

## Python tools

From the directory containing `SKILL.md`:

```sh
python3 -m venv "$HOME/.venvs/create-desktop-companion"
. "$HOME/.venvs/create-desktop-companion/bin/activate"
python -m pip install -r requirements.txt
python scripts/preflight.py
```

Windows PowerShell:

```powershell
py -3 -m venv "$HOME/.venvs/create-desktop-companion"
& "$HOME/.venvs/create-desktop-companion/Scripts/python.exe" -m pip install -r requirements.txt
& "$HOME/.venvs/create-desktop-companion/Scripts/python.exe" scripts/preflight.py
```

Python 3.10+ and Pillow are required. Node.js runs controller tests; Playwright and a Chromium executable are additional prerequisites for browser tests. ffmpeg is optional for external video production, not a repository dependency or bundled renderer. See [examples](examples.md) for concrete outputs and [validation](../validation.md) for actual test coverage.

## Production prerequisites

| Capability | Needed for | Without it |
|---|---|---|
| Readable references | Identity review | Work from descriptions, disclose missing visual evidence |
| Authorized image generation/editing | New artwork | Plan actions or inspect supplied assets |
| Local Python/Pillow | Diagnostics | Provide instructions; do not claim checks ran |
| Actual-size playback | Motion and viewing comfort | Mark visual playback unreviewed |
| Host import tools | Installation | Deliver standalone assets only |

Use the provider and host you have access to. Keep private references local unless their transfer is authorized. Fees, terms, asset rights, and native installation remain separate from installing this skill.


The repository checkout is not itself the installable skill. Copy only `skills/create-desktop-companion`, not the repository root or `examples/characters`. Use a new checkout name if `chatgpt-codex-pet-skill` already exists. For updates, review upstream changes in the checkout, then replace the installed copy after preserving local edits. The installed copy is not a Git checkout.


## Current production extension

Use [exposure-aware design](exposure-design.md) for design priority and presentation ordering, and [OpenAI production/delivery](openai-production.md) for the independent v2 export and post-approval installation workflow. These supplement, rather than replace, host-specific evidence and visual acceptance.


Keep virtual environments outside the distributable skill directory. Run release checks on a clean copy with `PYTHONDONTWRITEBYTECODE=1`; caches and local environments are intentionally rejected by the package checker.
