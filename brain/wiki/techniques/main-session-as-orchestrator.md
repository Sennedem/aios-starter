---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [wiki, technique, prompting, delegation, orchestration]
related: ["[[wiki/concepts/parallelize-and-delegate]]", "[[wiki/techniques/mod-collision-guard]]", "[[wiki/techniques/mod-goal-tracker]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]", "[[wiki/sources/nateherk-claude-code-mods]]"]
---

# Main session as orchestrator

Nate Herk's own working pattern, which he calls the biggest lever he has found for stretching Fable 5.1's usage limits. Most of the time he tells the main session **not** to build, code or research anything directly. It only spins up sub-agents, drives strategy, interprets what they return, and spins up more sub-agents. That spends the top model's intelligence on strategy and interpretation instead of execution, and saves tokens. From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]] **[09:35-09:57]**.

## The main session still owns the outcome

> "That doesn't mean that Fable isn't responsible for the outcome. Like, if it's a bad output, then it was Fable 5.1's fault, not all the sub agents' fault." **[09:57-10:04]**

So the main session still has real work: spinning up verifier agents, and on the final pass, before handing the result to the human, getting its own hands dirty. **[10:04-10:17]**

In practice: sub-agents return distilled conclusions, and the orchestrating session checks them against countable done-conditions instead of trusting a sub-agent's own report that it is done.

## Running many sessions in parallel

[[wiki/sources/nateherk-claude-code-mods|Nate Herk's mods video]] covers the failure that comes with running many parallel sessions (he runs about 12 goals at once). His [[wiki/techniques/mod-collision-guard|collision guard]] and [[wiki/techniques/mod-goal-tracker|goal tracker]] mods are orchestration aids: one asks before two chats edit the same file, the other shows every running goal in one pane.

## In this system

`.claude/rules/common/agents.md`: the main session keeps synthesis, routing and decisions; bulk reads and research legs go to subagents with countable done-conditions. `scripts/hooks/collision-guard.mjs` is the parallel-session guard.
