---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [hosting, agents, tradeoff]
related: ["[[wiki/tools/hermes-agent]]", "[[wiki/sources/nateherk-managed-hermes-setup]]", "[[wiki/tools/hostinger-managed-agents]]", "[[wiki/tools/grokbot]]", "[[wiki/tools/trigger-dev]]"]
---

# Managed vs VPS agent hosting

Two ways to run a standing agent like [[wiki/tools/hermes-agent|Hermes]], with a real cost and control tradeoff and no clear winner. From [[wiki/sources/nateherk-managed-hermes-setup|Nate Herk's managed Hermes setup video]]. [00:19-02:11]

| | Managed (for example Hostinger's Hermes app) | VPS |
|---|---|---|
| Price | About $6/mo, slightly cheaper | Slightly more |
| Server ownership | None to buy or maintain | You buy and maintain it |
| Setup | One click, no Docker, SSH or ENV files | Still close to one click, but Docker, SSH and ENV config required |
| Control | Handled for you: "one managed agent in a box" | Full root access, full config control |
| Channels | Telegram pre-wired | Set up yourself |
| Ongoing ownership | Still yours: updates, backups, firewall rules, container health | The same, plus the server itself |
| Scale | One agent per app; spin up a new app each time | One box can run several agents (multiple Hermes instances, N8N and so on) and scale compute and RAM |

Nate's framing: a VPS "is not just for Hermes, it's basically a private server" you can grow into a general automation box, while managed is optimised for getting one agent running with the least friction. His recommendation: start managed unless you specifically want to scale a multi-tool server. "It really will suffice for probably like 98% of you guys."

## When the question comes up at all

Both options are for an always-on agent you can reach from your phone, separate from your interactive sessions. If your agent is a local terminal session you open when you work, neither applies yet.

## Other hosting shapes

- [[wiki/tools/grokbot|Grokbot]] ([[wiki/sources/nateherk-grokbot-inbox-agentmail|source]]) is a second managed standing-agent app in the same "no server to run" category as Hermes, and adds webhook-triggered routines next to cron ones. See [[wiki/concepts/webhook-vs-cron-routines|Webhook vs cron routines]].
- [[wiki/tools/trigger-dev|trigger.dev]] ([[wiki/sources/nateherk-astra-automations-trigger-dev|source]]) is a third shape the table has no column for: a free task host for deterministic code with no standing agent runtime. It fits when the workload is "run this script on a schedule or webhook", not "keep an agent alive with memory and a chat surface".
