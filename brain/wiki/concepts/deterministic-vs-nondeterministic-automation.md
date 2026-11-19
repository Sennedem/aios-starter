---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, automation, architecture]
related: ["[[wiki/concepts/ai-systems-pyramid]]", "[[wiki/concepts/routine-drift]]", "[[wiki/concepts/ai-agent-nondeterminism]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]"]
---

# Deterministic vs non-deterministic automation

The core triage question for any automation, whatever hosts it: does this step run the same way every time given the same input (deterministic), or does its outcome genuinely vary per run (non-deterministic)? A trigger firing, reading a calendar or sending a pre-formatted message is deterministic; an AI step deciding what research is worth doing, or drafting message text, is not [04:44-06:00]. From [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk's trigger.dev video]].

## Why it matters more than the platform

"The more deterministic your automation gets, the more of a waste it would be to" run it through a full agentic harness. About 90% of business and personal automations are mostly deterministic scaffolding with one or two AI steps embedded, not agentic end to end [06:27-06:45]. The design move: draw the flow as numbered steps, colour only the genuinely AI-dependent ones, and host the deterministic majority as plain code instead of paying an agent harness's overhead (cost, unpredictability, maintenance) for steps that do not need it.

## Applies with any stack

The video hosts the deterministic steps on trigger.dev, but the same triage decides between a scheduled CI job, a cloud routine and a full agent session on any setup. Get it wrong in the expensive direction and you get [[wiki/concepts/routine-drift|routine drift]]. Get it wrong in the cheap direction and a real judgment call gets flattened into a brittle placeholder script.

## What the triage does not cover

[[wiki/sources/nateherk-one-person-business-claude|A later Nate Herk video]] adds a nuance: this triage decides which steps get an AI at all, but says nothing about how reliable the step is once routed to one. That video's golden-dataset eval shows an agent step scoring 88, then 88, then 94 across three identical-input reruns after a fix. Even a correctly identified AI step varies per run, so a single passing rerun after a patch is weak evidence. See [[wiki/concepts/ai-agent-nondeterminism|AI agent non-determinism]], a separate concern from this hosting triage.

## In this system

[[references/automation-and-cadence]] uses this triage to place each recurring job.
