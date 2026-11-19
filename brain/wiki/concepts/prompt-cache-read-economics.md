---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=8IyORt-7rOQ
tags: [concept, claude, pricing, prompt-caching, cost]
related: ["[[wiki/tools/claude-fable-5-1]]", "[[wiki/sources/nateherk-fable-5-1-release]]", "[[wiki/techniques/mod-cache-keeper]]", "[[wiki/techniques/comparing-model-cost-with-cost-and-usage]]"]
---

# Prompt cache-read economics

The same per-token price can still mean a smaller bill. When Anthropic released Fable 5.1 it kept Fable 5's list prices ($10 per million input tokens, $50 per million output tokens) but stated two changes: the model needs fewer tokens for the same work, and the price of **cache reads** went down. A cache read is the discounted rate charged when the model re-reads input it has already processed and cached, instead of paying full input price again [01:06-01:15]. **Anthropic-stated**, relayed in [[wiki/sources/nateherk-fable-5-1-release|Nate Herk's release video]].

## The mechanism

Prompt caching is a general Claude API feature, older than 5.1. A long, mostly static context (a system prompt, a big file, tool schemas) is billed at a fraction of the input price on repeat reads inside the cache window, so you stop paying full price for it every turn. Anthropic's stated savings, about 25% on typical workflows and about 50% on agentic work [01:04-01:20], both come from the lower cache-read rate for 5.1. Token prices in general did not drop.

## Why agentic work benefits more

Agent loops (tool calls, multi-step plans, long sessions) re-read the same accumulated context on almost every turn: the system prompt, the history, tool results already seen. Cache-read pricing governs exactly that repeat volume, so a discount compounds turn after turn in a way a one-shot prompt never sees. This link between the two numbers is Nate's inference. Anthropic does not state it as a mechanism in the video, so check it against the blog text before relying on it.

## The flip side: the cache expires

In [[wiki/sources/nateherk-claude-code-mods|Nate Herk's mods video]], a chat's cache lapses after about 60 idle minutes (creator-stated), and the next message re-bills the whole context at full input price. His [[wiki/techniques/mod-cache-keeper|cache-keeper mod]] shows a countdown so you know when that is about to happen.

## Related

To test a saving claim on your own work, run the same task on both models and compare the cost: [[wiki/techniques/comparing-model-cost-with-cost-and-usage|Comparing model cost]].

## In this system

`.claude/rules/common/model-routing.md` covers picking a model and effort level with cost in mind.
