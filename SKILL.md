---
name: wechat-rpa
description: Use when Codex needs Windows PC WeChat/微信 RPA with pywechat, pyweixin, pywechat127, message/file sending, chat history, contacts, friend/group settings, Moments/朋友圈, Favorites/收藏, calls, auto-reply, monitoring, settings, Navigator, Tools, 文件传输助手, 联系人, 群聊, 公众号, 视频号, or 小程序 on this machine.
---

# WeChat RPA

## Overview

Use this skill for Windows PC WeChat UI automation backed by the local `pywechat127` project. It covers setup, package selection, deterministic message sending, verification, and the broader project capability surface.

It cannot replace local prerequisites: Windows desktop access, installed and logged-in PC WeChat, UI tree visibility, `uv`, and permission to control the active desktop must exist.

## Setup And Package Choice

1. Use `scripts/wechat_send.py` for deterministic text sending and verification.
2. Let the script create or reuse `<workspace>\.venv`.
3. Let the script install missing dependencies from the maintained package source:

```text
git+https://github.com/wang930813-blip/wx-rpa.git#subdirectory=src
```

4. Select the package by WeChat version:
   - WeChat/Weixin `4.x`, usually `Weixin.exe` -> `pyweixin`.
   - WeChat `3.9.x` -> `pywechat`.
   - `pywechat` is documented as only usable for 32-bit Windows/3.9; on normal 64-bit Windows 4.x, prefer `pyweixin`.
5. Keep `close_weixin=False` / `close_wechat=False` unless the user explicitly asks to close WeChat.

## Quick Commands

```powershell
$skill = "$env:USERPROFILE\.codex\skills\wechat-rpa"
uv run --python 3.12 python "$skill\scripts\wechat_send.py" --to "文件传输助手" --message "你好"
```

Useful flags:

| Task | Flag |
|---|---|
| Use a specific workspace | `--workspace "C:\path\to\workspace"` |
| Send several texts | repeat `--message "..."` |
| Force reinstall from the configured source | `--force-install` |
| Check setup/backend only | `--ensure-only` |
| Skip UI verification | `--skip-verify` only when UI text cannot be inspected |

## Capability Map

Prefer `pyweixin` for current WeChat 4.x. Use direct package calls for capabilities not wrapped by `scripts/wechat_send.py`.

| Area | What the project can do |
|---|---|
| Messages | Send one/many messages to one/many chats; @ members or @all; quote-reply; send audio/voice files; create message chains/solitaire; check new messages; pull visible messages; dump/search chat history; dump recent sessions; save media; accept group invitations. |
| Files | Send files to one/many chats, optionally with messages; save chat files; export recent files, yearly/monthly WeChat files, videos, photos/media; forward files. |
| Contacts | Read my profile; list friends, WeCom contacts, service accounts, official accounts, groups, recent groups; get detailed profiles; get group members and common groups; handle new friend requests. |
| Friend settings | Add friends; mute/fold/pin chats; star, block, delete friends; clear chat history; change remark, description, phone, privacy; get common groups. |
| GroupSettings / Group settings | Mainly available in `pywechat` 3.9: create groups, rename groups, change own group alias, group remark, member nickname display, mute/sticky/save group, clear/quit, invite/remove/add members, edit notice, read group chat history. |
| Moments/朋友圈 | Post Moments with text/media; post notes to Moments; dump recent posts; dump friend posts; save details; like/comment via callback. |
| Collections/收藏 | Take notes; save favorite files/notes; convert card links to URLs; collect official-account articles. |
| Monitor and AutoReply | Listen to specific chat windows, new session-list messages, new members joining, and new messages; auto-reply current chats, friend chats, group chats, and session-list unread messages; optionally save files/media during monitoring. |
| Calls | Start voice or video calls with a friend; `pywechat` 3.9 also includes group voice-call helpers. |
| Navigator | Open WeChat windows and panels: main window, chat, separate chat, settings, contacts, contact manager, favorites, notes, profile, friend Moments, Moments, channels, search, mini-program pane, chat files, chat history, add-friend panel; search official accounts, channels, mini-programs. |
| Tools | Query install/running state, version, language, current wxid, WeChat paths, message/database/chat-file/video/favorites folders; capture login QR code; inspect UI state helpers. |
| Settings | Log out; change style, language, font size, notification alerts, auto-download size; 3.9 adds toggles for voice-to-text, DPI scaling, save chat history, startup, default browser, auto-update, alert sounds, notification flags, and clearing chat history. |
| Utils and development | Use pywinauto `WindowSpecification` returns for custom RPA; group @/@all helpers; new-message count/scanning; parsing chat history/message types including files, images, videos, links, mini-programs, channels, red packets/transfers. |

For detailed class/method names, read [references/capability-map.md](references/capability-map.md).

## Execution Guidance

- For plain text sending, run `scripts/wechat_send.py` because it installs, selects backend, sends, and verifies.
- For non-text operations, first run `scripts/wechat_send.py --ensure-only` to ensure the environment, then import the selected backend directly:

```python
from pyweixin import Messages, Files, Contacts, FriendSettings, AutoReply, Monitor
from pyweixin import Collections, Call, Moments, Settings, Navigator, Tools
```

- Use `Navigator` when a task requires a live `pywinauto.WindowSpecification`.
- Use `Monitor`/`AutoReply` for listening and replying. For one-shot auto-reply, first scan current unread previews; if the trigger already exists, reply once immediately, otherwise poll only for the requested duration and exit after one reply or timeout.
- Verify every user-visible action with visible WeChat UI text, returned data, exported files, or a fresh read-only check.

## Safety Rules

- Ask for explicit confirmation before destructive or irreversible actions: delete friend, block friend, clear chat history, clear all chat history, quit group, remove group members, log out, change privacy, mass-send, mass-forward, or posting public Moments.
- Do not perform high-frequency bulk operations without user approval; WeChat may log out or trigger risk controls.
- Do not close WeChat unless requested.
- Do not claim success from "no exception" alone. Report verification evidence.
- If a library method is flaky on the current WeChat UI, fall back to pywinauto UI text inspection, a narrower Navigator flow, or a read-only diagnostic before trying another write action.
