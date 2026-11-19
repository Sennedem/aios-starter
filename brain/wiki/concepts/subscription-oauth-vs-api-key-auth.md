---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=gQef3d3erOs
tags: [concept, auth, oauth, subscription, agents, cost]
related: ["[[wiki/tools/hermes-agent]]", "[[wiki/concepts/subscription-vs-api-hosting]]", "[[wiki/concepts/webhook-vs-cron-routines]]", "[[wiki/tools/grokbot]]", "[[wiki/sources/nateherk-managed-hermes-setup]]"]
---

# Subscription OAuth vs API-key model auth

When a harness like [[wiki/tools/hermes-agent|Hermes]] needs to talk to an underlying model, it can authenticate in one of two ways. You paste a metered **API key**, or you connect a **subscription** (ChatGPT, in Nate Herk's demo) through an OAuth-style flow: open a link, sign into the account, copy a short code back into the harness [03:41-04:16]. From [[wiki/sources/nateherk-managed-hermes-setup|Nate Herk's managed Hermes setup video]].

Nate's reasoning for the subscription route: "you're going to get way more inference, it's going to be way cheaper". A flat-rate subscription's usage allowance goes further than paying per token through a metered key for the same work. The trade-off: once connected, the harness can only use the models that subscription exposes. In his case that meant GPT-family models only, because he signed in through ChatGPT and Codex instead of an OpenAI API key.

## The general rule

Before you paste an API key into a tool, check whether a subscription you already pay for can sign in instead. Metered credits are for work the subscription cannot cover.

## Related

- Codex follows the same pattern from the other vendor: it signs in through ChatGPT-subscription OAuth instead of an API key (shown in Nate Herk's GPT-6 Astra trading video). An account login may not expose every model the API offers, so check that the model you want is available on that login before you build on it. See [[wiki/tools/codex-scheduled-tasks|Codex scheduled tasks]].
- A third lane exists for fully deterministic work: a free host that makes no model call at all. See [[wiki/concepts/subscription-vs-api-hosting|Subscription vs API hosting]].
- [[wiki/tools/grokbot|Grokbot]]'s marketplace connectors ([[wiki/sources/nateherk-grokbot-inbox-agentmail|Nate Herk's Grokbot inbox video]]) use another auth shape: a one-click "add account" authorize flow per service (Gmail, AgentMail), plus a manually copied webhook URL and bearer key for triggering routines. [[wiki/concepts/webhook-vs-cron-routines|Webhook vs cron routines]] has the security note on that combination.

## In this system

`.claude/rules/common/model-routing.md` covers cost-aware model choice, and `scripts/hooks/metered-guard.mjs` blocks any command that spends metered credits until you approve that spend.
