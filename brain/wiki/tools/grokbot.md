---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/ff7om2bBLKM
tags: [wiki, tool, grokbot, xai, agents, routines]
related: ["[[wiki/tools/agentmail]]", "[[wiki/tools/hermes-agent]]", "[[wiki/concepts/webhook-vs-cron-routines]]", "[[wiki/techniques/inbox-triage-routine]]", "[[wiki/sources/nateherk-grokbot-inbox-agentmail]]"]
---

# Grokbot

Grokbot is xAI's desktop agent app (creator-observed; the name and vendor are not verified beyond the video). It is a workspace for creating several named **bots**, each with its own prompt or persona, that run scheduled or event-triggered **routines**, connect to third-party services through a built-in **marketplace** of connectors, and can message each other directly inside the same account. [00:56-01:11] [14:05-14:16]

## Core pieces (creator-observed)

- **Bots:** created with a short natural-language prompt ("you are my email management agent, your name is Natie..."). The bot talks back during setup and suggests refinements; it proposed a "newsletters" label on its own. [01:06-02:05]
- **Routines:** a scheduled job whose trigger is not limited to a clock. A routine can fire on a cron schedule (twice daily in the inbox demo) or on a webhook (only when an external event, such as a new email, arrives). See [[wiki/concepts/webhook-vs-cron-routines|webhook vs cron routines]]. [00:01-00:11] [06:02-06:28]
- **Marketplace connectors:** one-click account connections (Gmail, and a native [[wiki/tools/agentmail|AgentMail]] connector) added to a bot so its routines can act on that service. [02:07-02:19] [05:24-05:44]
- **Agent-to-agent chat:** bots inside the same account can message each other with no email or webhook. An inbox only becomes necessary to reach an agent outside the account. [14:05-14:16]

## What it demoed

Two builds in [[wiki/sources/nateherk-grokbot-inbox-agentmail|the source video]]: an inbox-cleanup bot on a cron routine, and a second bot woken by a webhook routine wired to her own AgentMail inbox. The labelling pattern is on [[wiki/techniques/inbox-triage-routine|inbox triage routine]].

## Known rough edge (creator-observed)

With several inboxes connected, there was no UI path to scope one webhook to one inbox. Nate got a JavaScript filter snippet from Codex and pasted it into an "edit transformation" console on the AgentMail side. Likely a first-version gap, not a documented limitation. [10:38-11:59]

## Compared with Hermes

Grokbot is the same category of product as [[wiki/tools/hermes-agent|Hermes agent]]: a persistent bot wrapped around scheduled or triggered routines plus connector auth. Its distinguishing feature, as shown so far, is the webhook-triggered routine. Hermes was only shown running on schedules or through chat, not on inbound events.
