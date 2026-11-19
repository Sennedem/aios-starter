---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [concept, prompting, delegation, parallelism, subagents]
related: ["[[wiki/techniques/main-session-as-orchestrator]]", "[[wiki/concepts/persona-review-panel]]", "[[wiki/techniques/stress-test-with-subagents]]", "[[wiki/concepts/subagents-over-agent-teams-for-debate]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# Parallelize and delegate

Break a large task into independent pieces, and don't assume one agent has to work through them in order. Nate Herk's assembly-line framing: 80 agents can each pick up one piece, hand off to each other, or all work at once and converge at the end. Not every task parallelizes, but many do. The payoff is faster completion, better focus per agent (each has one job), broader coverage, and context efficiency, because the main session stays clean [08:50-09:27]. From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]].

## The evidence, quoted

Nate reads these from Anthropic's prompting guidance (the captions render "Claude" as "Cloud").

> "Delegation and collaboration: Cloud Fable 5 is significantly more dependable at dispatching and sustaining parallel agents and reliably manages ongoing communication with long-running sub agents and peer agents." [10:18-10:29]

> Batching independent tool calls: "Fable 5.1 usually issues parallel tool calls as expected. When a request names several things to fetch, it issues those calls all in parallel so they can all work at the same time" instead of sitting idle. [10:30-10:41]

> "Parallel sub agents save time and cost through cache reads and avoid bottlenecking on the slowest sub agent." If one agent in an assembly line is slow, every agent after it waits; running them in parallel removes that bottleneck. [10:42-10:59]

## Two claims in one

The quotes mix workflow discipline with a capability claim. The discipline holds for any model: independent legs run at the same time, and each agent hands back a distilled result so the main session's context stays small. The capability claim, that Fable 5.1 is "significantly more dependable" at sustaining long-running parallel and peer-agent communication than earlier models, is vendor documentation. Treat it as untested until your own runs bear it out.

## Related

- [[wiki/techniques/main-session-as-orchestrator|Main session as orchestrator]] is the matching discipline on the main-session side of the split.
- [[wiki/techniques/stress-test-with-subagents|Stress-test with subagents]] applies the pattern to QA: "spin up 50 different sub agents... try to break it". The agents attack the finished work instead of building it.
- [[wiki/sources/nateherk-build-skills-not-agents|A separate Nate Herk video]] on Agent Skills applies it to subjective review. A [[wiki/concepts/persona-review-panel|persona review panel]] of beginner, skeptical-buyer and audience-member sub-agents runs in parallel, and the skill acts only on issues that recur across them.
- [[wiki/concepts/subagents-over-agent-teams-for-debate|Sub-agents over agent teams for debate]] covers when a hub of sub-agents is enough.

## In this system

`.claude/rules/common/agents.md`: independent legs launch in one message, and agents return conclusions, never raw dumps.
