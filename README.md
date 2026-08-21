# WeChat RPA Skill

Codex skill for Windows PC WeChat automation with the local `pywechat127` package source.

## Dependency Source

The skill installs the WeChat RPA dependency from:

```text
git+https://github.com/wang930813-blip/wx-rpa.git#subdirectory=src
```

It does not bundle or replace local desktop requirements. The target machine still needs Windows, PC WeChat installed and logged in, visible desktop UI access, and `uv` for environment setup.

## What It Covers

- First-use setup with `uv venv` / `uv pip install`.
- Backend selection for WeChat 4.x (`pyweixin`) and WeChat 3.9 (`pywechat`).
- Text message sending with verification through `scripts/wechat_send.py`.
- Direct access guidance for files, contacts, groups, Moments, Favorites, calls, settings, Navigator, monitoring, and auto-reply APIs.
- Safety rules for destructive, public, or bulk WeChat actions.

## Quick Start

```powershell
$skill = "$env:USERPROFILE\.codex\skills\wechat-rpa"
uv run --python 3.12 python "$skill\scripts\wechat_send.py" --to "文件传输助手" --message "你好"
```

For advanced capabilities, read `SKILL.md` and `references/capability-map.md`.
