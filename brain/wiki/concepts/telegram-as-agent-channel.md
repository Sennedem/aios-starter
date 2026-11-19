---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=gQef3d3erOs
tags: [concept, telegram, agents, channel, mobile]
related: ["[[wiki/tools/hermes-agent]]", "[[wiki/sources/nateherk-managed-hermes-setup]]", "[[wiki/techniques/inbox-triage-routine]]", "[[wiki/tools/codex-scheduled-tasks]]"]
---

# Telegram as an agent channel

Telegram works as a phone-native front end onto a standing agent. It is wired through Telegram's own bot-creation flow, so no custom integration is needed [04:18-07:44]. Shown with [[wiki/tools/hermes-agent|Hermes]] in [[wiki/sources/nateherk-managed-hermes-setup|Nate Herk's managed Hermes setup video]].

## Setup

1. Message **@BotFather** in Telegram and send it the `newbot` command (typed with a leading slash). Name the bot, then choose a **globally unique** username ending in `bot`.
2. BotFather returns an **access token**. Paste it into the agent platform's Telegram connection step.
3. Message **@userinfobot**, send it the `start` command, and copy the numeric **Telegram user ID** it returns. Paste that in too.
4. Open the bot's chat and hit start. Nothing appears to happen yet, and that is expected: the bot stays silent until the platform-side setup (choosing the AI model and so on) is finished. Messages sent before then get no reply and no "typing" indicator. Nate flags this so it doesn't read as broken.

## The payoff: one thread, two windows

Once active, the platform's web chat and the Telegram chat are **the same conversation**, live in both directions. A message typed on the web shows up in Telegram (on a phone too) and the other way round. Nate frames it as choosing "what channel are you speaking through", with one bot behind both. The agent's memory and context carry across.

## Other routes to the same goal

- Codex remote mirrors a phone onto the same synced conversation as the desktop. Nate calls it "very similar to the Grok Bot way or the Cloud Code remote" [15:47-16:27] in his GPT-6 Astra trading video. See [[wiki/tools/codex-scheduled-tasks|Codex scheduled tasks]].
- The Grokbot inbox video ([[wiki/sources/nateherk-grokbot-inbox-agentmail|Nate Herk]]) sends its digest to a chat surface too, a ClickUp DM instead of Telegram. See [[wiki/techniques/inbox-triage-routine|Inbox triage routine]].

Independent tools converge on the same shape for phone access to an agent: one thread, reachable from more than one surface.
