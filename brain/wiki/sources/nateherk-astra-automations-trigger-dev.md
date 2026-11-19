---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/FqnNL8fnUWo
tags: [wiki, source, youtube, automation, codex, trigger-dev, routines]
related: ["[[wiki/tools/trigger-dev]]", "[[wiki/tools/codex-sdk]]", "[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/techniques/stress-test-with-subagents]]", "[[wiki/concepts/subscription-vs-api-hosting]]", "[[wiki/concepts/routine-drift]]", "[[wiki/techniques/env-file-as-portable-key-vault]]", "[[wiki/techniques/interview-before-building-an-automation]]", "[[wiki/concepts/ai-systems-pyramid]]", "[[wiki/tools/hermes-agent]]"]
---

# Nate Herk: "How to Build GPT-6 Astra Automations (that don't eat your usage limit)"

YouTube, 35:25, Nate Herk | AI Automation, published 2026-09-16: https://youtu.be/FqnNL8fnUWo.

**Core claim:** an automation built and iterated inside Codex but left running there as a scheduled task burns the same weekly usage limit as a live chat. So anything that can be turned into deterministic code should go to a free, independent host (trigger.dev), and Codex is kept for the one-time build plus the genuinely unpredictable steps. [00:00-01:29]

## Three automation shapes, one pattern

Every build follows the same path: plan, build in Codex, verify locally, push to GitHub, and let trigger.dev pull, host and schedule it.

1. **Scheduled:** a 6 a.m. weekday trigger reads Google Calendar, drafts a brief and sends it as a ClickUp DM. [[wiki/tools/trigger-dev|trigger.dev]] hosts the schedule; only the research and drafting steps are AI. See [[wiki/concepts/deterministic-vs-nondeterministic-automation|deterministic vs non-deterministic automation]].
2. **Webhook:** a form submission fires the same kind of flow (draft an outreach recommendation, DM it). It could be built with zero AI if the message were pure placeholders. QA'd by telling Codex to "spin up 50 sub agents... try to break it"; see [[wiki/techniques/stress-test-with-subagents|stress-test with subagents]].
3. **Codex SDK:** a full agentic trading-research loop (check Alpaca, research, decide, loop back if unsatisfied, email a trade recommendation), ported from an existing Codex routine so it can run programmatically at scale. It bills on metered API credits, not the subscription; see [[wiki/tools/codex-sdk|Codex SDK]] and [[wiki/concepts/subscription-vs-api-hosting|subscription vs API hosting]].

## Supporting lessons

- An agent-hosted routine "went rogue after a month", reinterpreting its own instructions. The fix was hard-coding the channel and message IDs into a script. See [[wiki/concepts/routine-drift|routine drift]].
- Keys live in a portable `.env`, not in app plugins. See [[wiki/techniques/env-file-as-portable-key-vault|.env as a portable key vault]].
- Before building, have the agent interview you on destination, timing, scope and a per-run cost cap. See [[wiki/techniques/interview-before-building-an-automation|interview before building an automation]].
- The standing principle: build the simplest deterministic thing and climb the [[wiki/concepts/ai-systems-pyramid|AI systems pyramid]] only when you have to.

## The triage this video teaches

| The step is… | Run it as |
|---|---|
| Deterministic (same input, same output) | A script on a free host or CI runner (trigger.dev, GitHub Actions) with its own credentials |
| One AI step inside a fixed flow | A subscription-billed cloud routine |
| A loop of judgment that decides its own next step | An interactive session, or the SDK on metered credits when it must run unattended |

Free schedulers can be late: trigger.dev's free plan can delay a 6 a.m. run by up to an hour [08:04-08:14], and GitHub's own docs warn that scheduled workflows may be delayed or dropped under load. For anything time-sensitive, prefer an event trigger (a push or a webhook) over a clock.

The same reasoning argues against a standing hosted agent such as [[wiki/tools/hermes-agent|Hermes]] when your scheduled work is mostly code-shaped.

## In this system

[[references/automation-and-cadence]] sets out where each kind of recurring job runs.
