---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, claude-code, mods, prompt-caching, context]
related: ["[[wiki/concepts/claude-code-mods]]", "[[wiki/concepts/prompt-cache-read-economics]]", "[[wiki/sources/nateherk-claude-code-mods]]"]
---

# Mod: Cache keeper

**What it does.** A desktop-app panel that shows the prompt-cache countdown for the current chat, plus a readout like a status line. Nate Herk says Claude named it "cachekeeper" [02:56-04:44]. Source: [[wiki/sources/nateherk-claude-code-mods|Nate Herk, Claude Code mods]].

## Pieces Nate showed

- **Cache timer:** counts back to 60 minutes after each message (he saw 57 jump back to 60). After 60 idle minutes the whole context is billed again at full cost, and the panel shows what that would cost [03:03-03:35]. The 60-minute TTL is creator-stated; the real TTL depends on plan and settings and is unverified here.
- **Session numbers:** context size (109,000 tokens in his demo), the 5-hour and weekly limits, and a running "what this session would have cost on API billing" figure [03:41-04:00].
- **A handoff button:** runs his session-handoff skill, then "clear and continue" runs `/clear` and pastes the handoff message. Two clicks, maybe one; he admits it saves little time [04:02-04:38].
- **A warning** when the cache is about to go cold (5 minutes left): reprompt, compact or hand off [04:39-04:55].

## Setup

No recipe given. Nate's route: ask Claude to build a mod for it, then ask how to turn it on and off [07:14-07:22]. His own mods are a free download from his community, not public here [10:41-10:56].

## Why it matters

It makes [[wiki/concepts/prompt-cache-read-economics|cache-read economics]] visible. It relies on a per-session countdown the mod computes itself; how it does so was not shown.

## In this system

`/save-session` and `/resume-session` are the handoff pair the button automates.
