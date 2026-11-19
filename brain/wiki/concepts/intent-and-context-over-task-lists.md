---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, prompting, context]
related: ["[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/concepts/claude-md-as-router]]", "[[wiki/concepts/stateless-wakeup-handoff-log]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# Intent and context over task lists

Fable 5 performs better when it understands *why* a request is being made, not only what the request is. The direct quote Nate Herk reads from the Anthropic docs in [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]]:

> "Claude Fable 5 tends to perform better when it understands the intent behind a request. Context lets it connect the task to relevant information rather than inferring intent on its own." **[02:18-02:28]**

The recommendation: give context about why you are asking, "especially for long-running agents drawing on multiple work streams." **[02:28-02:33]**

## Why it is a separate move from "define done"

[[wiki/concepts/tell-it-what-done-looks-like|Telling it what done looks like]] fixes the target; intent fixes how everything on the way there is read. Without intent, the model has to guess why a step matters and can quietly optimise for the wrong reading of an ambiguous instruction. That risk is highest on long-running runs across several work streams, where the model cannot stop to ask a clarifying question.

## Standing context does this job

Nate draws the connection himself: "building out your own AIOS that has information about context, your goals, your background... is so helpful in driving powerful models like this." **[02:33-02:40]** That is what a router CLAUDE.md plus a knowledge base does. The router holds no knowledge itself; it points a session at the intent, context and background a task needs (see [[wiki/concepts/claude-md-as-router|CLAUDE.md as router]]). Two separate sources land on the same design choice.

## The stateless case

Nate's GPT-6 Astra trading video carries this into a recurring, stateless setting: a scheduled agent has no conversation to infer intent from at all, so [[wiki/concepts/stateless-wakeup-handoff-log|the progress log and handoff pattern]] supplies the context that chat history would. "Continuity comes from shared records, not the AI remembering the conversation" [04:06-04:10]. Same principle (context beats inferred intent), applied where there is no memory to fall back on.

## In this system

`/onboard` and `/grill-me` write your goals and background into the brain, so sessions start with the intent already on file.
