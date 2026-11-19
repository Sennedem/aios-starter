---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/ff7om2bBLKM
tags: [wiki, tool, agentmail, email, agents, webhooks]
related: ["[[wiki/tools/grokbot]]", "[[wiki/concepts/agent-to-agent-email]]", "[[wiki/concepts/webhook-vs-cron-routines]]", "[[wiki/sources/nateherk-grokbot-inbox-agentmail]]"]
---

# AgentMail

AgentMail is a service that issues real email inboxes for AI agents (`<name>@agentmail.to` by default, or a custom domain), so an agent gets its own address instead of sharing a human's inbox. [04:14-04:50] It is free to start; the free tier shown in the demo allows about 3 inboxes per account. [04:40-04:44] Source: [[wiki/sources/nateherk-grokbot-inbox-agentmail|Nate Herk's Grokbot inbox video]].

## What it provides (creator-observed)

- **A web app** with per-inbox deliverability stats (sent and received counts) and the raw message thread, which you can read and answer from AgentMail itself, separately from whatever agent is wired to it. [04:19-04:24] [05:04-05:11]
- **Inbox creation:** pick a username, get a default `agentmail.to` address or attach a custom domain. [04:44-04:56]
- **Webhooks:** an endpoint URL that fires on subscribed events (for example "message received"). The URL and a bearer-token key are pasted into the consuming agent platform's routine, which is how a [[wiki/tools/grokbot|Grokbot]] routine wakes up when new mail lands. Auth is a custom header: `Authorization: Bearer <key>`. [08:16-09:41]
- **A native Grokbot connector** for account auth: a one-click "add account" and authorize flow, separate from the webhook wiring needed to trigger routines. [05:15-05:44]

## The gap: inbox-to-webhook mapping needs code

With more than one inbox on an account, AgentMail had no UI control to scope a webhook to one specific inbox, so every webhook fired for every inbox. The only fix shown was asking a coding agent (Codex) for a JavaScript filter keyed to an inbox ID and pasting it into the webhook's "edit transformation" console. Nate says on camera that the product should offer this as a dropdown. This is a creator-observed gap, not a documented limitation. [10:38-11:59]

## Security note (stated in the source)

The webhook URL and its bearer key together are enough for anyone holding both to trigger the connected bot into unwanted actions: "treat it like you treat any API key or password." [13:04-13:33] The lesson holds for any webhook-driven routine, with or without AgentMail.

## When you need it

AgentMail solves agent-to-agent email between separate accounts or harnesses (see [[wiki/concepts/agent-to-agent-email|agent-to-agent email]]). If all your routines and skills live in one repo or one account and can pass context directly, you do not need it.
