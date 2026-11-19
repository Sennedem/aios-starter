---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [wiki, source, youtube, fable-5-1, prompting, delegation, verification]
related: ["[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/concepts/intent-and-context-over-task-lists]]", "[[wiki/techniques/refactor-skills-for-newer-models]]", "[[wiki/techniques/match-effort-to-the-task]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/concepts/parallelize-and-delegate]]", "[[wiki/techniques/main-session-as-orchestrator]]", "[[wiki/techniques/model-routing-for-ingest]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]"]
---

# Source: "I Analyzed How Anthropic ACTUALLY Prompts Fable 5.1" (Nate Herk)

YouTube video (11:31) by Nate Herk | AI Automation, published 2026-09-02: https://www.youtube.com/watch?v=FBVNS1l5Vb8. Nate pulls four tricks from Anthropic's platform docs on prompting Fable 5.1. He points out that the docs cover each model separately because they behave differently, and that the video condenses what he thinks matters most from a long reference document. **[00:30-00:57]**

One disclaimer he flags up front, quoted from the docs: "Your existing [Claude] Fable 5 prompts should perform well on Claude Fable 5.1 without changes, but a handful of behavioral differences are worth knowing about." Some of what follows is inherited from the Fable 5 docs, some is specific to 5.1. **[01:56-02:11]**

## Key takeaways

- **[00:57-03:38]** Trick 1, tell it the finish line: give the outcome, the why, the definition of done and the real constraints, and let the model derive the task list. Provide intent and context especially for long-running agents with several work streams. Skills written for older models are often too prescriptive for Fable 5.1 and worth auditing. Fable 5.1 can carry long tasks with little methodology guidance when the goal is genuinely clear. See [[wiki/concepts/tell-it-what-done-looks-like|tell it what done looks like]], [[wiki/concepts/intent-and-context-over-task-lists|intent and context over task lists]] and [[wiki/techniques/refactor-skills-for-newer-models|refactor skills for newer models]].
- **[03:41-06:42]** Trick 2, match effort to the task instead of defaulting to high: start high, test medium, then low, and reserve xhigh or max for genuinely deep work. At low effort Fable 5.1 answers from memory more and calls search and retrieval tools less. It supports changing effort per message while keeping the prompt cache, unlike other models. See [[wiki/techniques/match-effort-to-the-task|match effort to the task]].
- **[06:42-08:48]** Trick 3, make it prove its work: review the output the way a human reviewer would before it reaches you; make self-verification against sub-agents explicit in long-running prompts; audit each claim against a tool result and say so explicitly when something isn't verified. Where no objective check exists, build an LLM-as-judge with an explicit definition of what good looks like. Fable 5.1's vision works best when it crops and re-verifies dense visual inputs iteratively. See [[wiki/concepts/prove-its-work|prove its work]] and [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]].
- **[08:48-11:00]** Trick 4, parallelize and delegate: split a large task into independent pieces for several agents instead of one. The docs describe Fable 5.1 as significantly more dependable at sustaining parallel and peer agent communication, and it issues independent tool calls in parallel batches. Parallel sub-agents save time and cost through cache reads and avoid waiting on the slowest agent. Nate's own habit is to keep the main session out of building, coding and researching directly, using it only to spin up agents, drive strategy and interpret, while it still owns the outcome and does the final pass. See [[wiki/concepts/parallelize-and-delegate|parallelize and delegate]] and [[wiki/techniques/main-session-as-orchestrator|main session as orchestrator]].

## Notes on applying it

- **Two ways to set effort.** The docs' sequence starts high and steps down while quality holds. The other common default starts at medium and raises effort only for real ambiguity. The cache-preserving per-message effort change makes stepping cheap either way, so choose deliberately instead of by habit. Details on [[wiki/techniques/match-effort-to-the-task|match effort to the task]].
- **Effort is a second routing axis.** [[wiki/techniques/model-routing-for-ingest|Model routing for ingest]] covers choosing the model tier; this source adds the effort level within one tier.
- **How far to trust it.** Nate is reading and paraphrasing primary Anthropic documentation here rather than presenting his own model of an undocumented system, so the page treats it as close to primary. The one claim to hold loosely is Fable 5.1's relative dependability at parallel and peer agent communication: a docs claim, not something independently confirmed.

## In this system

`/anthropic-prompt` rewrites a rough ask into this anatomy (outcome, why, done-conditions, constraints, verify, delegate, effort). `.claude/rules/common/agents.md` covers delegation, `model-routing.md` covers effort, and `verification.md` covers proving the work.
