---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [concept, prompting, done-definition, goals]
related: ["[[wiki/concepts/intent-and-context-over-task-lists]]", "[[wiki/techniques/refactor-skills-for-newer-models]]", "[[wiki/techniques/verify-before-returning]]", "[[wiki/concepts/forced-iteration-degrades-output]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# Tell it what done looks like

Give the model the finish line instead of a task list. State the outcome, why it matters, what "done" means and any real constraints, then let the model work out the tasks that get it there [00:57-01:18]. From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]].

Nate Herk, citing Boris Cherny (creator of Claude Code): give these models an ambitious goal and get out of their way. He demonstrates by collapsing a long, task-by-task prompt into one line, "create an appealing landing page offering voice agent solutions tailored to our target audience", and the model works out what it needs to do from there [01:29-01:44].

## Why it holds for newer models

> "Cloud Fable 5.1 can execute very long tasks without much guidance on methodology, especially when the goal is clear." [03:22-03:28] (The captions render "Claude" as "Cloud".)

The trick depends on that capability: the model can sustain a long task on its own, but only when the goal is unambiguous. A vague goal with no task list gets neither benefit. That is why the definition of done has to be explicit even when the task breakdown is left out. Write it once at the start and it serves twice: it lets the model work on its own during the task, and it lets you verify the result afterwards.

## Related

- [[wiki/concepts/intent-and-context-over-task-lists|Intent and context over task lists]] is the companion trick (the why, alongside the what).
- [[wiki/sources/nateherk-build-skills-not-agents|A separate Nate Herk video]] makes the durable version of the point: a skill's `SKILL.md` is a done-definition written once and reused every run. See [[wiki/techniques/verify-before-returning|Verify before returning]] for the acceptance-criteria template.
- [[wiki/sources/nateherk-make-it-better-100-times|"Make it better" 100 times]] is the counter-example. An open-ended "innovate" goal with a "must ship a change every time" clause and no done-definition ended in over-engineering ("innovate without a vision turns into adding"). Without that clause the model stopped itself around round 20-25. The ambitious-goal advice only works when the finish line is stated. See [[wiki/concepts/forced-iteration-degrades-output|Forced iteration degrades output]].

## In this system

`.claude/rules/common/verification.md` asks for countable done-conditions before any non-trivial task starts. `/anthropic-prompt` builds them into a prompt.
