---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, cost, hosting, subscription, automation]
related: ["[[wiki/concepts/subscription-oauth-vs-api-key-auth]]", "[[wiki/tools/codex-sdk]]", "[[wiki/tools/trigger-dev]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]", "[[wiki/concepts/routine-drift]]"]
---

# Subscription vs API hosting

There are three cost lanes for running the same AI-driven work. Pick one by where the judgment step needs to live. From [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk, How to Build GPT-6 Astra Automations]].

1. **In-app scheduled task**, billed against the chat subscription's weekly usage cap. Simple, but it "eats at your actual weekly usage limit" even for a job that never needs a live conversation [00:03-00:11].
2. **A hosted deterministic script** ([[wiki/tools/trigger-dev|trigger.dev]], or any free scheduler or webhook host). Free to run, because only code lives there and no model is called.
3. **The SDK path**, which puts the model call itself outside the app and bills it on **metered API credits**: "paying for Astra via API credits is obviously more expensive than paying for Astra via subscription". Reserve it for loops that must run programmatically and at scale [34:56-35:03]. See [[wiki/tools/codex-sdk|Codex SDK]].

## The picking rule

If a step needs no judgment, host it free (lane 2). If an otherwise scheduled flow needs an occasional AI decision, that one call can ride lane 2's script as a single API call, or stay in lane 1 if it is low-volume and covered by the subscription. Move to lane 3 (metered, agentic, programmatic) only when the loop itself, and not just one AI step, must run unattended at real scale.

## Related

[[wiki/concepts/subscription-oauth-vs-api-key-auth|Subscription OAuth vs API-key auth]] establishes that a subscription's flat allowance beats metered per-token cost for the same work. This page adds the third lane: a free host for the fully deterministic slice. Both agree: never default to the metered lane when a cheaper one covers the job. Moving the fixed parts into a script also stops [[wiki/concepts/routine-drift|routine drift]].

## In this system

[[references/automation-and-cadence]] covers where scheduled work runs. `scripts/hooks/metered-guard.mjs` blocks metered spend until you approve it.
