---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: coding
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/FqnNL8fnUWo
tags: [wiki, tool, codex-sdk, agentic-loop, automation]
related: ["[[wiki/tools/trigger-dev]]", "[[wiki/concepts/subscription-vs-api-hosting]]", "[[wiki/concepts/ai-systems-pyramid]]", "[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]"]
---

# Codex SDK

The programmatic way to run a full Codex **agentic loop** (check a data source, research, decide whether to research more, act) outside the app, hosted on something like [[wiki/tools/trigger-dev|trigger.dev]]. Nate Herk's use case in [[wiki/sources/nateherk-astra-automations-trigger-dev|his Astra automations video]]: an existing Codex routine (a trading-research loop checking Alpaca and logs every 30 minutes) that needs to run programmatically at scale, beyond what a subscription-bound scheduled task allows [26:12-26:44].

## Where it differs from the other automation shapes

A deterministic flow can only budget a fixed number of research steps in advance. The SDK's agentic loop can decide mid-run "wait, let me do more research" and loop back, because it is not following a pre-written sequence [28:44-29:12]. Rebuilt this way, Nate's routine came back as four cooperating tasks: a recurring `check`, plus `pre-flight`, `install plan` and `proof` for setup and verification [31:12-32:45].

## Cost model

It bills on metered API credits, not the flat subscription. That is the price of running outside the app: "paying for Astra via API credits is obviously more expensive than paying for Astra via subscription" [34:56-35:03]. Reserve this path for a loop of judgment that must run unattended at scale, not as a default.

On the [[wiki/concepts/ai-systems-pyramid|AI systems pyramid]] the SDK sits at the top rung, used only when the two simpler shapes below it can't do the job.
