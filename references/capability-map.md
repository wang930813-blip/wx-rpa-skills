# WeChat RPA Capability Map

This file summarizes the capability surface extracted from the workspace `pywechat` project docs and class/method signatures.

## Version Split

- `pyweixin`: WeChat/Weixin 4.1+ on Windows 10/11, current default for modern PC WeChat.
- `pywechat`: WeChat 3.9.x, documented as x86/32-bit oriented; use only when the local WeChat and Windows environment match.

## pyweixin 4.x Classes

### Messages

- `send_messages_to_friend`, `send_messages_to_friends`: text messaging, batch messaging, @ members, @all, optional clear/send delay.
- `reply_with_quote`: quote-reply to a matched historical message.
- `send_audios_to_friend`: send audio/voice files.
- `message_chain`: create group message chain/solitaire.
- `check_new_messages`, `pull_messages`, `listen`-adjacent workflows: retrieve unread or visible messages.
- `dump_recent_sessions`, `dump_sessions`: export recent/current sessions.
- `dump_chat_history`, `search_chat_history`: export or search chat history, optionally saving detail.
- `save_media`: save images/videos from a chat.
- `accept_group_invitation`: inspect and accept group invitation links.

### Files

- `send_files_to_friend`, `send_files_to_friends`: send files, optionally with text messages.
- `save_chatfiles`: save files from a chat.
- `export_recent_files`, `export_wxfiles`, `export_videos`: export WeChat files/videos by recent view or date.

### Contacts

- `check_my_info`: read current account profile.
- `get_friends_info`, `get_wecom_friends_info`, `get_serAcc_info`, `get_offAcc_info`: list contact categories.
- `get_friends_detail`, `get_wecom_friends_detail`, `get_serAcc_detail`, `get_offAcc_detail`: export detailed contact data.
- `get_groups_info`, `get_groupMembers_info`, `get_recent_groups`, `get_common_groups`: group and common-group data.
- `get_friend_profile`: inspect a friend's profile.
- `check_new_friends`: check/verify/clear new friend requests.

### FriendSettings

- Add friend by number, with greeting/remark/chat-only.
- Mute/fold/pin chat, clear history, change privacy, star, delete, block.
- Change remark, description, phone number.
- Query common groups.

### AutoReply And Monitor

- `AutoReply.auto_reply_to_friend`: auto-reply in a separate chat window with callback and optional file/media saving.
- `AutoReply.auto_reply_messages`: auto-reply session-list unread messages with callback, group filtering, never-reply list, page limits.
- `Monitor.listen_on_chat`: listen on a specific chat window.
- `Monitor.listen_on_newMemberJoin`: listen for group member join events.
- `Monitor.listen_on_sessionList`, `Monitor.listen_on_newMessages`: listen to session list and unread message changes.

### Collections

- `take_notes`: create collection notes and optionally share to Moments.
- `save_files`, `save_notes`: export favorite files/notes.
- `cardLink_to_url`: turn card links into URLs.
- `collect_offAcc_articles`: collect official-account articles.

### Call

- `voice_call`, `video_call`: start friend voice/video calls.

### Moments

- `post_moments`: publish text/media Moments.
- `post_notes`: publish note content/files to Moments.
- `dump_recent_posts`, `dump_friend_posts`: export recent/friend Moments, optionally saving detail.
- `like_posts`, `like_friend_posts`: like/comment through callbacks.

### Settings

- Log out.
- Change style, language, font size.
- Configure auto-download size and notification alert map.

### Navigator

- Open main WeChat, settings, contacts, contact manager, collections, notes, chat info, own profile, friend profile, friend Moments, Moments, channels, search, mini-program pane, chat files, dialog/separate dialog, chat-search window, chat history, add-friend panel.
- Search official accounts, channels, mini-programs.
- Capture login QR code.

### Tools

- Get running/install state, version, language, current wxid.
- Locate WeChat executable and folders: wxid, message, favorite temp, database, chat files, video, userlib.
- UI helpers: window centering, scrollability, group-chat detection, own-bubble detection, selection helpers, duration parsing.

## pywechat 3.9 Classes

### Messages

- Send one/many text messages to one/many friends.
- Forward text, links, music/audio, mini-programs, channels.
- Pull messages, check new messages, dump sessions, dump recent sessions.
- Dump chat history and recent chat history.

### Files

- Send files to one/many chats, with optional messages, @, @all, tickle.
- Forward files.
- Save chat files, photos, videos.
- Export files/videos by year/month.

### FriendSettings

- Pin, mute, sticky, clear history, delete friend, add friend.
- Change remark, tags, description, phone, privacy.
- Blacklist/star friend, share contact, get WeChat number, tickle friend.

### GroupSettings

- Pin/create group, rename group, change own alias, group remark.
- Show member nicknames, mute, sticky, save group to contacts.
- Clear history, quit group.
- Invite/remove/add members, edit group notice.
- Read group chat history and recent group chat history.

### Contacts

- Get friend names, friend info/detail, group info, group members, subscribed official accounts.

### Moments

- Dump Moments and recent posts.

### AutoReply And Monitor

- Auto-reply session-list messages.
- Auto-reply to a specific friend or group with callback; group reply can be @-only and @ others.
- Listen on a chat window and optionally save files/media.

### Call

- Voice/video call a friend.
- Voice call members in a group.

### Settings

- Log out.
- Toggle voice-message auto conversion, DPI scaling, save chat history, run at boot, default browser, auto update, web search history, alert sounds, Moments/channel/topstories/miniprogram flags.
- Clear chat history, close auto login, change language.

### Navigator And Tools

- Open settings, dialogs, separate dialogs, session-list friend, friend settings/menu, contacts manager, collections, group settings, Moments, chat files, friend profile, contacts, chat history, mini-program pane, top stories, search, channels, tray windows, mini-programs, official accounts.
- Query install/running state, language, paths, wxid folders, chat-file/video/SnsCache folders.
- Parse message content, Moments content, chat history, latest message.

## Operational Notes

- Most advanced calls are direct package APIs, not currently wrapped by `scripts/wechat_send.py`.
- Prefer read-only diagnostics before write actions when UI state is uncertain.
- For destructive actions, require explicit user confirmation in the current turn.
