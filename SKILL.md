---
name: wechat-rpa
description: Use when Codex needs to send, auto-reply, or verify Windows PC WeChat/微信 messages through pywechat, pyweixin, pywechat127, WeChat RPA, 文件传输助手, 联系人, 群聊, or new-message reminders on this Windows machine.
---

# WeChat RPA

## Overview

Use this skill for Windows PC WeChat UI automation. The skill wraps dependency checks, first-time install, WeChat version/package selection, message sending, and UI text verification.

It cannot replace local prerequisites: Windows desktop access, installed and logged-in PC WeChat, `uv`, and permission to control the active desktop must exist.

## Quick Start

Run the bundled script instead of writing ad hoc pywinauto code:

```powershell
$skill = "$env:USERPROFILE\.codex\skills\wechat-rpa"
uv run --python 3.12 python "$skill\scripts\wechat_send.py" --to "文件传输助手" --message "你好"
```

From a workspace that already has `.venv`, this is also fine:

```powershell
.\.venv\Scripts\python.exe "$env:USERPROFILE\.codex\skills\wechat-rpa\scripts\wechat_send.py" --to "王凯👌" --message "你在干嘛"
```

## Workflow

1. Use `scripts/wechat_send.py` for sending text messages.
2. Let the script create or reuse `<workspace>\.venv`.
3. Let the script install missing dependencies with:

```text
git+https://github.com/wang930813-blip/pywechat.git#subdirectory=src
```

4. Let the script choose the package:
   - WeChat/Weixin `4.x` or `Weixin.exe` -> `pyweixin`.
   - WeChat `3.9.x` -> `pywechat`.
5. Keep `close_weixin=False`; do not close the user's WeChat after an automation task.
6. Verify by reading the visible WeChat UI text after sending. Report the verification evidence, not only exit status.

## Common Commands

| Task | Command |
|---|---|
| Send one message | `uv run --python 3.12 python "$env:USERPROFILE\.codex\skills\wechat-rpa\scripts\wechat_send.py" --to "文件传输助手" --message "你好"` |
| Use a specific workspace | Add `--workspace "C:\path\to\workspace"` |
| Force reinstall from the user's fork | Add `--force-install` |
| Check setup only | Add `--ensure-only` |
| Skip UI verification | Add `--skip-verify` only when the UI cannot be inspected |

## New Message Rules

For a one-shot auto-reply request, first do a read-only scan of current unread session previews with pywinauto UI text. If the trigger text is already present, reply once immediately. If the user asks to listen, poll for the requested duration and exit after one reply or timeout.

For deterministic sending, still call `scripts/wechat_send.py` for the reply itself.

## Common Mistakes

- Do not assume the package is installed. Run the script; it checks and installs.
- Do not install from the original upstream by default. Use the maintained fork URL above.
- Do not import `pywechat` on 64-bit Windows for WeChat 4.x. Use `pyweixin`.
- Do not claim success from "no exception" alone. Verify visible WeChat UI text contains the recipient and message.
- Do not close WeChat unless the user explicitly asks.
