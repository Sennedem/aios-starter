---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/ff7om2bBLKM
tags: [concept, agents, routines, webhook, cron, security]
related: ["[[wiki/tools/grokbot]]", "[[wiki/tools/agentmail]]", "[[wiki/concepts/agent-to-agent-email]]", "[[wiki/sources/nateherk-grokbot-inbox-agentmail]]"]
---

# Webhook vs cron routines

A standing agent's routine (a job it runs on its own, without being asked in the moment) can be triggered in two structurally different ways. Both are demoed on the same [[wiki/tools/grokbot|Grokbot]] platform in [[wiki/sources/nateherk-grokbot-inbox-agentmail|Nate Herk's Grokbot inbox video]]: **on a schedule** (cron: wake up every N minutes or hours and check something) or **on an event** (webhook: wake up only when an external system posts to a URL) [00:01-00:11][06:02-06:28].

## The distinction

| | Cron routine | Webhook routine |
|---|---|---|
| Trigger | Fixed clock interval (every 30 minutes, or 6:45am and 6:45pm) | An external event fires an HTTP call to a URL the routine exposes |
| Demoed example | Nat, the inbox janitor, running twice a day | Trader and Stephanie, waking only when a new email arrives through [[wiki/tools/agentmail|AgentMail]]'s webhook |
| Latency | Bounded by the interval; it can sit idle for up to that long before reacting | Near-immediate; it reacts the moment the event fires |
| Setup cost | Just a schedule | A URL and auth key are generated on the agent side and pasted into the triggering service, plus a filter if several inboxes or sources share one webhook (see the mapping gap on [[wiki/tools/agentmail|AgentMail]]) |
| Security surface | Nothing beyond the agent's own access | The URL and bearer key together let **anyone holding both trigger the routine**; the source calls this a password-equivalent secret [13:04-13:33] |

## Why it matters

Cron is the simpler default, and most scheduled digests and briefs run that way. A webhook routine is what makes real **agent-to-agent** triggering possible without either side polling. See [[wiki/concepts/agent-to-agent-email|Agent-to-agent email]] for the email case demoed here.

The lesson that holds whatever tool you use: treat a webhook's URL and auth key as a credential. Store them like a password, never as a plain config value.

## In this system

`scripts/routines/morning-brief.md` and `scripts/routines/weekly-review.md` are cron-style routines. [[references/automation-and-cadence]] covers scheduling.
