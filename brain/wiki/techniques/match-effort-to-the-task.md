---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [wiki, technique, prompting, effort, model-routing]
related: ["[[wiki/techniques/model-routing-for-ingest]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/effort-level-vs-model-tier]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# Match effort to the task

Most people never touch the effort slider and leave Fable 5.1 on its default, **high**. That is usually overkill. Nate Herk's recommended sequence: **start at high, test whether medium does the task just as well, and if it does, try low.** Keep X-high and max for genuinely deep work, "massive massive work or something that needs like deep deep thought." From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]] **[05:04-05:21]**.

Quoted from the docs, per the video:

> "Consider all effort levels": start with the default at high, then test on other levels like low, medium, X-high and max against your own eval, "because some people are like, 'Oh yeah, I drive all the time with X-high and it's perfect for me.'" Maybe, if they are doing deep software engineering and merging many PRs at once. Routine document and spreadsheet work probably does not need X-high or high. **[05:22-05:53]**

He puts Fable 5.1 on low roughly level with Fable 5 on medium or high, and cheaper; some compare Fable 5.1 on low to Opus or "a really, really good Sonnet." **[04:19-04:33]**

## Low effort changes tool-calling, as well as quality

> "At low effort, Cloud Fable 5.1 is less likely than Cloud Fable 5 to call a search or retrieval tool and more likely to answer from memory." **[05:55-06:06]**

So low effort suits ideation and brainstorming, where you want the model's feel without heavy tool use. It is a poor fit for anything that depends on the model checking a live source instead of recalling one.

## Effort can change mid-conversation without losing cache

On Fable 5.1, effort can be changed per message and the prompt cache is kept. On other models a new effort level needs a new top-level request. **[06:19-06:35]**

## Two defaults, two goals

This sequence runs the opposite way from a common budget rule: "default to medium, raise only for real ambiguity." The two optimise different things. The budget rule protects a fixed usage window across a whole day of mixed tasks, where starting every task at high burns it fast. Nate's sequence finds the right level per task, assuming effort is cheap to change. The cache detail above is the strongest argument for testing his way: if switching keeps the cache, starting high once and stepping down is close to free. Treat it as something to test on your own work before changing a default.

## Related

[[wiki/techniques/model-routing-for-ingest|Model routing for ingest]] covers the model-tier axis (which model for which job); this page adds the effort axis within one model. [[wiki/concepts/effort-level-vs-model-tier|Effort level vs model tier]] covers how the two interact across generations. [[wiki/concepts/progressive-disclosure|Progressive disclosure]] is a third budget lever: it controls what gets loaded into context per skill call, whatever the model or effort level.

## In this system

`.claude/rules/common/model-routing.md` defaults to medium and raises effort only for real ambiguity. The test-down sequence on this page is how to check that default on a task you run often.
