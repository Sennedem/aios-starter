---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, claude-code, mods, concurrency, parallel-agents]
related: ["[[wiki/concepts/claude-code-mods]]", "[[wiki/techniques/main-session-as-orchestrator]]", "[[wiki/sources/nateherk-claude-code-mods]]"]
---

# Mod: Collision guard

**What it does.** Before every Edit, Write or NotebookEdit, it checks whether the target file was touched in the last 30 minutes by another chat. If so, it asks you in the UI how to proceed: proceed, move to a worktree, cancel, or type something else [09:13-10:21]. Source: [[wiki/sources/nateherk-claude-code-mods|Nate Herk, Claude Code mods]].

## What Nate showed

A recorded demo. Chat 1 changed a price from 29 to 39 in an HTML file. Chat 2, asked to add a "most popular" badge to the pro plan, stopped with "another open chat edited the file just now", then went ahead after he clicked proceed [09:27-10:32].

## Mod vs hook

Nate says it differs from a PreToolUse hook because it neither blocks nor acts automatically; it puts a question to you [10:01-10:12]. That is a real mod capability: Anthropic says mods can approve or deny permission requests and draw UI, and hooks cannot draw UI. He also concedes a skill or a CLAUDE.md rule could approximate it [10:12-10:19].

## Setup

Ask Claude to build it; no code was shown. Where the "touched" signal comes from (a shared log or the file's modified time) was not shown either, so false positives and missed collisions are untested.

## In this system

`scripts/hooks/collision-guard.mjs` is a hook version of the same check. It records which session edited which file in a ledger (`tmp/edit-ledger.json`) and asks before a second session edits a file another session touched recently, which answers the "where does the signal come from" gap above.
