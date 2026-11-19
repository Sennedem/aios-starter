---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, claude-code, mods, goal, progress]
related: ["[[wiki/concepts/claude-code-mods]]", "[[wiki/techniques/main-session-as-orchestrator]]", "[[wiki/sources/nateherk-claude-code-mods]]"]
---

# Mod: Goal tracker

**What it does.** When a goal run starts in the Claude desktop app, a pane shows the goal text, the phase (planning), minutes elapsed, the task list Claude generates and which tasks are checked off, a percentage once a plan exists, and an "all tasks" view across other chats running goals [07:22-09:10]. Source: [[wiki/sources/nateherk-claude-code-mods|Nate Herk, Claude Code mods]].

## Why

Nate starts many goal runs and loses track of progress and runtime. With around 12 sessions at once, he wants one place to see all of them [07:25-07:35, 09:03-09:08].

## What Nate showed

The first demo finished instantly (the task was already done). The second showed four tasks ticking off: find comment-fetch tooling, pull comments from the last 10 videos, analyse themes, report the top theme [08:25-08:55]. The percentage was described as coming "once it has a plan" but not demonstrated.

## Setup

Ask Claude to build it; no code was shown [07:35-07:38]. A guess at the mechanism (unverified): it reads Claude's task list and goal state and renders them in a pane, which fits Anthropic's description of mods drawing panes beside the conversation.
