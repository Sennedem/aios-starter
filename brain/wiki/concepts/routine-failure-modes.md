---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/eg_1NXDcoPk
tags: [concept, automation, reliability, failure-modes, routines]
related: ["[[wiki/concepts/stateless-wakeup-handoff-log]]", "[[wiki/concepts/routine-drift]]", "[[wiki/tools/codex-scheduled-tasks]]"]
---

# Routine failure modes

Before relying on a chain of scheduled, stateless agent wake-ups, Nate Herk brainstormed the failure modes with the agent itself (GPT-6 Astra) instead of discovering them live [04:55-05:08]. The source is his video on letting an agent trade stocks. The list, as given:

1. **No previous progress record on the first run**: nothing to hand off from yet.
2. **The next model invocation has no chat history**: the statelessness itself, named as a failure mode to design around instead of being assumed away.
3. **The prior run crashed after sending an order**: the state-critical case. An action was taken, but the record of it may not have been written. See [[wiki/concepts/stateless-wakeup-handoff-log|Stateless wake-up and handoff log]] for the record-as-you-go fix.
4. **Two runs overlap**: a scheduling collision where two wake-ups act on the same state at once.
5. **The log is missing or corrupt**: the shared record the whole continuity mechanism depends on is itself a single point of failure.
6. **The machine or app goes offline**: a run simply doesn't happen when expected.

## Why this generalizes

This is a **pre-mortem for recurring stateless automation**, and nothing on the list is specific to trading. Every item is a property of "an agent wakes up periodically with no memory and acts on shared state", which covers any cron-like routine: a cloud digest, a nightly sync, a scheduled report. The value is in doing the brainstorm before building the routine, so the handoff and log design survives these cases instead of being patched after one happens.

The method is cheap to copy: before you schedule a routine, ask the agent that will run it to list how it could fail, then check that your design answers each item.

## Related

[[wiki/concepts/routine-drift|Routine drift]] is a seventh failure the list misses: the routine runs fine but slowly changes what it does.

## In this system

[[references/automation-and-cadence]] for designing recurring routines. `scripts/routines/morning-brief.md` and `scripts/routines/weekly-review.md` are stateless wake-ups of exactly this kind.
