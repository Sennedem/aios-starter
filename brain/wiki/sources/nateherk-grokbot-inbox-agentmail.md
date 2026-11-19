---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/ff7om2bBLKM
tags: [wiki, source, youtube, grokbot, agentmail, agents, inbox]
related: ["[[wiki/tools/grokbot]]", "[[wiki/tools/agentmail]]", "[[wiki/techniques/inbox-triage-routine]]", "[[wiki/concepts/webhook-vs-cron-routines]]", "[[wiki/concepts/agent-to-agent-email]]", "[[wiki/tools/hermes-agent]]", "[[wiki/concepts/managed-vs-vps-agent-hosting]]", "[[wiki/concepts/telegram-as-agent-channel]]"]
---

# Source: "Grok Bot Manages My Inbox (and has its own)" (Nate Herk)

YouTube video (14:29) by Nate Herk | AI Automation, published 2026-09-16: https://youtu.be/ff7om2bBLKM. A spoken walkthrough of a screen demo; nothing load-bearing sits only on screen.

Nate demos two [[wiki/tools/grokbot|Grokbot]] builds. **Nat** is an inbox-cleanup bot on a twice-daily cron routine that labels his own Gmail. **Stephanie** is a second bot given her own email inbox (through [[wiki/tools/agentmail|AgentMail]]), so a different bot can reach her by sending mail, which wakes her through a webhook routine instead of a schedule. A sponsor segment (Clay) and a free-kit plug are left out here.

## Key takeaways

- **[00:56-03:08]** Nat, the inbox janitor: built by describing routing rules in plain language (primary, notifications, outreach, urgent; Grokbot itself suggested adding newsletters), connecting a Gmail account and setting a cron routine at 6:45am and 6:45pm. It **labels and marks read only: "it doesn't draft anything for me"**, then sends a ClickUp DM digest signed "sent by Nat". Setup took under 10 minutes, creator-observed. See [[wiki/techniques/inbox-triage-routine|inbox triage routine]].
- **[00:01-00:54, 05:12-06:02]** The trading-bot framing that opens the video: a separate Grokbot ("trader") wakes on a webhook instead of a cron schedule, firing only when it receives an email from a GPT-6 Astra research bot telling it to place or sell a trade. It is the same routine mechanism as Nat's cron job, triggered by an event instead of a clock. See [[wiki/concepts/webhook-vs-cron-routines|webhook vs cron routines]].
- **[04:12-08:00]** AgentMail gives a bot its own email address (free tier, about 3 inboxes) so agents can email each other like people. Wiring a bot's routine to an AgentMail inbox takes AgentMail's native Grokbot connector for auth, then a **webhook** (URL plus a bearer-token header) on the AgentMail side so a new-message event calls the bot's routine.
- **[10:38-11:59]** AgentMail had no UI to scope one webhook to one inbox when several inboxes share an account. Nate asked Codex for a JavaScript "transformation" snippet and pasted it into the webhook's edit-transformation console to filter by inbox ID. He flags this as a real product gap, not a best practice.
- **[09:03-10:05, 12:01-12:54]** End-to-end test: an email sent into the scoped inbox woke only Stephanie (not the unrelated trader bot watching a different inbox and webhook), and she replied inside the AgentMail thread. That confirms both the webhook-to-routine wake mechanism and the scoping fix, creator-observed on one test message.
- **[13:04-13:33]** Security warning, stated directly: the webhook URL and its bearer key together are enough for **anyone** who obtains both to trigger the bot into unwanted actions. "Treat it like you treat any API key or password." He says he deleted the demo credentials before publishing.
- **[14:05-14:16]** Bots inside the same Grokbot account can already talk to each other without email; AgentMail-style inboxes matter for a bot to reach **agents outside** that account (a different harness, someone else's automation). See [[wiki/concepts/agent-to-agent-email|agent-to-agent email]].

## What carries over

- **Labels only, never drafts.** An inbox bot that only labels and marks read can run unattended; one that drafts or sends needs a human gate. A native mail connector can do the labelling with no separate bot.
- **Webhook credentials are passwords.** Store the URL and key like any API key, and rotate them if they leak.
- **Agent-to-agent mail solves a cross-boundary problem.** If all your routines live in one repo or one account and can pass context directly, you don't need it.

This was the first source in the wiki to show routines triggered by a webhook instead of only by cron, next to [[wiki/tools/hermes-agent|Hermes agent]], [[wiki/concepts/managed-vs-vps-agent-hosting|managed vs VPS hosting]] and [[wiki/concepts/telegram-as-agent-channel|Telegram as an agent channel]].

## In this system

`/inbox-janitor` runs the same labels-only discipline on your Gmail through a mail connector: one label per unread thread, nothing archived, deleted, replied to or drafted.
