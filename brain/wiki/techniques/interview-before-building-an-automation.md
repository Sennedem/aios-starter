---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, planning, interview]
related: ["[[wiki/techniques/give-agent-context-via-aios-and-grill-me]]", "[[wiki/concepts/ai-systems-pyramid]]", "[[wiki/techniques/roast-room-council-debate]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]", "[[wiki/sources/nateherk-roast-room]]"]
---

# Interview before building an automation

Before the coding agent writes a line, have it interview you about the automation instead of starting from your one-line ask. From [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk's automations video]]: "the first step is just the planning... you need to help me plan this out and then actually build it" [02:30-02:33].

## What the interview pins down

- **Destination:** where the output lands (a ClickUp DM, email, a channel).
- **Timing:** what schedule, and how much lateness is tolerable.
- **Scope:** which data sources are in bounds now and which come later.
- **Research boundaries:** public web only, or also private sources such as meeting notes or Drive.
- **A per-run cost cap:** "there's really no reason why you should be spending more than, you know, 25 cents for research at this point" [03:34-04:39].

## Why it matters more as autonomy grows

Nate ties this to the [[wiki/concepts/ai-systems-pyramid|AI systems pyramid]]: "especially the more autonomous your systems get, there's more room for error... so build the simplest solution possible" [29:26-29:36]. He runs the same interview before building the highest-autonomy (SDK) automation as before the simple scheduled one [29:19-29:24].

## The same pattern elsewhere

[[wiki/sources/nateherk-roast-room|The roast-room video]] repeats it inside a decision skill ([[wiki/techniques/roast-room-council-debate|council debate]]): the skill asks first (event size, budget, who sits at the table) before running the debate. [[wiki/techniques/give-agent-context-via-aios-and-grill-me|Give your agent a context repo, or interview it into context]] is the same discipline applied to general personal and business context. Across three sources the default is the same: when the thing being built will run unattended, the agent interviews the human before acting instead of inferring intent.

## In this system

`/grill-me` runs this kind of interview on any topic and saves every answer before the next question.
