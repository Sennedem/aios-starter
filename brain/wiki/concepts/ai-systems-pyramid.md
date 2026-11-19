---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, automation, architecture]
related: ["[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/tools/codex-sdk]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]", "[[wiki/techniques/start-low-climb-to-judgment-businesses]]"]
---

# AI systems pyramid

Nate Herk's name for a three-rung escalation ladder, climbed only when the rung below cannot do the job ([[wiki/sources/nateherk-astra-automations-trigger-dev|source]]):

1. A plain script.
2. A script with one or two embedded AI steps (research, drafting).
3. A full agentic harness or loop (the [[wiki/tools/codex-sdk|Codex SDK]] shape, able to decide mid-run to do more work).

Each rung up buys autonomy at a named cost: "the more autonomous your systems get, there's more room for error... you're increasing the risk, you're increasing the cost, you're increasing complexity, you're increasing the maintenance" [29:26-29:41].

The rule, stated directly: "build the simplest solution possible and only move up... when you truly need that functionality" [29:34-29:40]. Start at rung 1 and let a demonstrated need, not convenience or novelty, justify each step up.

## Applies beyond this stack

The pyramid is a design heuristic about where autonomy should live in a system, not a trigger.dev-specific idea. Climbing it means going from a cron job, to a cron job that calls an LLM once, to a standing agent loop, on any host. [[wiki/concepts/deterministic-vs-nondeterministic-automation|Deterministic vs non-deterministic automation]] is how to tell which rung a given step needs, and [[wiki/tools/codex-sdk|Codex SDK]] shows what rung 3 looks like built out.

## Related ladders and evidence

- [[wiki/sources/nateherk-ai-businesses-ranked|Every AI Business Ranked]] gives a second "start simple, climb only when earned" ladder for business models (websites, then workshops and consulting, then judgment roles); see [[wiki/techniques/start-low-climb-to-judgment-businesses|Start low, climb to judgment businesses]]. Different pyramid, same instinct.
- The four client systems in [[wiki/sources/nateherk-4-claude-systems-that-sell|4 Claude Systems That Sell]] mostly sit on rungs 1 and 2: [[wiki/concepts/voice-note-to-document-system|voice note to document]] and the [[wiki/concepts/intake-and-follow-up-funnel-system|intake funnel]] are fixed pipelines with AI steps, and the [[wiki/concepts/company-brain-system|company brain]] climbs toward rung 3 only through add-ons. What sells at $2k to $15k is mostly low-rung automation, not full agent loops.

## In this system

[[references/automation-and-cadence]] applies the same ladder when choosing between a scheduled job, a cloud routine and a full session.
