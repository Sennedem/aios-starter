---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/eg_1NXDcoPk
tags: [concept, statelessness, automation, continuity, routines]
related: ["[[wiki/concepts/routine-failure-modes]]", "[[wiki/concepts/intent-and-context-over-task-lists]]", "[[wiki/tools/codex-scheduled-tasks]]"]
---

# Stateless wake-up and handoff log

Every scheduled-agent invocation is a fresh instance with no memory of the previous run's conversation. A bigger context window won't fix that. An explicit record that every run reads and writes will. Stated directly in Nate Herk's GPT-6 Astra trading video: **"Continuity comes from shared records, not the AI remembering the conversation."** [04:06-04:10]

## The loop

Each wake-up:

1. Reads the strategy or plan document and the **previous handoff**.
2. Checks live state (in the source, the brokerage account: positions, orders, cash).
3. Performs its assigned job.
4. Updates the current state record and the progress log.
5. Leaves clear, explicit instructions for the next wake-up, including after a run that did nothing or failed [12:53-13:12].

Without this loop, Nate says it "just feel[s] like you're just kind of like throwing darts at the wall" [04:24-04:27]: each run re-decides from scratch instead of building on the last.

## Record as you go

**"Critical actions get recorded as they happen, so an interrupted run can be recovered without accidentally repeating a trade."** [04:28-04:33] This detail is what makes the pattern robust. If a run crashes mid-action, the log must already show what was attempted before the crash. A log written only at the end of a run leaves the successor free to redo, or double-do, the same action. The three named persistent artifacts are a progress log, an append-only journal, and evidence [04:44-04:55].

## Where it applies

The source is a trading agent, but the pattern fits any recurring stateless job: a cloud routine, a scheduled report, a nightly sync. A handoff log supplies context, and context is what lets a stateless run infer the right intent instead of guessing. See [[wiki/concepts/intent-and-context-over-task-lists|Intent and context over task lists]].

## Related

[[wiki/concepts/routine-failure-modes|Routine failure modes]] lists the cases this log has to survive (first run, crash after an action, overlapping runs, a corrupt log). [[wiki/tools/codex-scheduled-tasks|Codex scheduled tasks]] is the scheduler used in the source.

## In this system

`/save-session` and `/resume-session` apply the same idea to chat sessions. [[references/automation-and-cadence]] covers scheduled routines.
