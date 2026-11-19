---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, automation, reliability, routines]
related: ["[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]", "[[wiki/concepts/routine-failure-modes]]", "[[wiki/concepts/subscription-vs-api-hosting]]", "[[wiki/techniques/env-file-as-portable-key-vault]]"]
---

# Routine drift

An agent-hosted routine doesn't run the same way twice. It re-**interprets** its instruction every time it wakes up, and over enough runs that interpretation walks away from what was intended. Nate Herk's own incident: a simple scheduled routine "started to just go rogue" after about a month, sending to random DM channels including the team channel, because "it was an agent on the back end... just interpreting the message different every time" [10:33-10:46]. From [[wiki/sources/nateherk-astra-automations-trigger-dev|How to Build GPT-6 Astra Automations]].

## The fix

Rewording the prompt leaves the drift in place. What removes it is taking out the interpretation step. Rebuilding the same routine as a script means "hard-coding the direct channel with the channel ID and the message ID and everything that gets sent, rather than giving the agent the full connection... and saying, 'hey, just send it to Nate'" [10:56-11:06]. A script cannot act differently on each run. An agent given a live connection and a goal always can.

## The general rule

Any recurring job whose destination, format or side effects matter should have those hard-coded as literal values (channel IDs, sheet ranges, file paths) instead of re-derived by an agent on each run. The AI handles the genuinely variable content (drafting, research) and never re-decides the fixed scaffolding around it. [[wiki/concepts/deterministic-vs-nondeterministic-automation|Deterministic vs non-deterministic automation]] covers drawing that line up front, before drift starts.

## Related

[[wiki/concepts/routine-failure-modes|Routine failure modes]] is the pre-mortem for the same kind of job. [[wiki/concepts/subscription-vs-api-hosting|Subscription vs API hosting]] shows where the scripted part can run for free.

## In this system

[[references/automation-and-cadence]] for designing recurring work. `.claude/rules/common/skills.md`: a script that worked is saved and reused, never regenerated.
