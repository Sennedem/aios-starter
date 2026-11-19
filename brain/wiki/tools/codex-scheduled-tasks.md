---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/TLQLfa7yH4I
tags: [wiki, tool, codex, scheduling, automation, routines]
related: ["[[wiki/tools/hermes-agent]]", "[[wiki/concepts/stateless-wakeup-handoff-log]]", "[[wiki/concepts/telegram-as-agent-channel]]", "[[wiki/concepts/subscription-vs-api-hosting]]"]
---

# Codex scheduled tasks

OpenAI Codex's built-in recurring-task feature, demoed in Nate Herk's "I Turned GPT-6 Astra Into a 24/7 Stock Trader" video as the mechanism for six daily stateless "wake-ups" during a 7-day trading challenge. [09:33-14:20]

## Local vs cloud

Two task types, with a real tradeoff rather than one being an upgrade:

| | Runs with the device offline? | Project, model and reasoning selectable? |
|---|---|---|
| **Local** ("this device") | No, the machine must be on | Yes |
| **Cloud** | Yes | No |

Nate picks local only because he needs to pin the model to GPT-6 Astra on high reasoning: cloud tasks run headless but drop that choice [09:56-10:10]. He notes cloud routines with Astra are possible but out of scope for the video [12:32-12:40].

## One thread for every run, plus auto-compaction

Each scheduled task can point at an existing conversation thread instead of starting a fresh one every run. Nate creates one dedicated "challenge thread" and wires all six routines to run inside it, so a single instruction ("set up six routines, all pointed at this thread") replaces configuring each task by hand [10:10-12:08]. Codex's auto-compaction keeps that thread from filling up with stale context after many runs [10:20-10:23]. That gives continuity on top of the explicit progress log, not instead of it (see [[wiki/concepts/stateless-wakeup-handoff-log|stateless wake-up and handoff log]]).

## What a good routine ends with

A shared end-of-run handoff: what changed, actual outcomes, remaining risk, unresolved issues and the exact next job, even on a no-trade or failed run [12:53-13:12], so the next stateless run always has something concrete to read.

## Codex remote

A phone view onto the same synced thread: messages sent from the phone land in the desktop thread and the other way round, which Nate compares to "the Grok Bot way or the Claude Code remote" [15:47-16:27]. See [[wiki/concepts/telegram-as-agent-channel|Telegram as an agent channel]] for the same phone-access idea through a different mechanism.

## Model and usage caveats

- The model in the video, GPT-6 Astra, is described only as "more powerful" than the model behind an earlier challenge [00:08-00:11], and it fanned out about 10 sub-agents to research the strategy when first asked [01:18-01:21]. Both are creator-observed; no OpenAI model card is cited.
- A model that works in a demo may not be selectable on your login. Codex signed in with a ChatGPT account has been seen rejecting newer model strings that an API key accepts (HTTP 400: `The '<model>' model is not supported when using Codex with a ChatGPT account`). Probe with one call (`codex exec -m <model-string>`) before you build a schedule around a specific model.
- Scheduled runs are ordinary Codex sessions, so they draw on the same plan limits as interactive use. Six routines a day consume real rate-limit headroom.

Hermes's Tasks panel ([[wiki/tools/hermes-agent|Hermes agent]]) solves the same "keep a scheduled agent continuous" problem in a different harness, without surfacing the local-vs-cloud tradeoff.
