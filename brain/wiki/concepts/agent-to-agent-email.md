---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [agents, email, communication]
related: ["[[wiki/tools/agentmail]]", "[[wiki/tools/grokbot]]", "[[wiki/concepts/webhook-vs-cron-routines]]", "[[wiki/sources/nateherk-grokbot-inbox-agentmail]]"]
---

# Agent-to-agent email

Giving an agent its own real email inbox turns email into a channel between agents, as well as between a human and an agent [04:12-04:50][14:05-14:16]. In the demo from [[wiki/sources/nateherk-grokbot-inbox-agentmail|Nate Herk's Grokbot video]], a research bot (GPT-6 Astra) emails a trading bot ("trader") to instruct a trade, and a separate assistant bot (Stephanie) gets her own [[wiki/tools/agentmail|AgentMail]] inbox so that agents outside her own harness account can reach her.

## Why the agent needs its own inbox

Two reasons come up in the source:

1. **Isolation.** One bot's inbox should wake only that bot, not every bot on the account. This is the multi-inbox scoping gap noted on the [[wiki/tools/agentmail|AgentMail]] page.
2. **Reach across a boundary.** Bots inside the same harness account (the same [[wiki/tools/grokbot|Grokbot]] workspace) can already talk to each other directly, no email needed. An inbox only becomes necessary when the message has to leave that account: a different harness, another person's automation, or, as demoed, a different bot owner's Codex or GPT setup [14:05-14:16].

The practical test follows from the second point. If every agent you run lives in one account or one repo and can pass context directly, you do not need agent email. It earns its place when one of your agents must be reachable by an agent you do not control, such as a partner's automation or a client's bot.

## The mechanism

As demoed, agent-to-agent email is not agents reading a mailbox in a loop. It is a webhook: the receiving inbox's provider (AgentMail) fires an event to the receiving agent's routine the moment mail arrives, and that wakes the agent to process the message. See [[wiki/concepts/webhook-vs-cron-routines|Webhook vs cron routines]] for that trigger on its own.
