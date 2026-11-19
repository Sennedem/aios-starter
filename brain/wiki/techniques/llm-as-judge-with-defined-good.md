---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [wiki, technique, prompting, verification, llm-as-judge]
related: ["[[wiki/concepts/prove-its-work]]", "[[wiki/concepts/persona-review-panel]]", "[[wiki/techniques/golden-dataset-eval-loop]]", "[[wiki/concepts/ai-agent-nondeterminism]]", "[[wiki/techniques/stopping-criterion-for-self-improvement-loops]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# LLM-as-judge with defined good

Most creative or subjective work has no objective pass/fail check. The answer is still to verify it: build your own LLM-as-judge. That means you define, explicitly, what good looks like and how to test whether an output is good, and you hand that definition to the model as the judging spec. From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|Nate Herk, How Anthropic prompts Fable 5.1]] **[07:36-07:54]**.

Nate frames this as a substitute for the objective case: "if you were literally trying to optimize the performance of something so that X equals 10, that's something that objectively can be proven." Most work is not like that, so the judge has to be built. **[07:31-07:41]**

## Why "define good" carries the weight

A judge without an explicit definition of good re-runs the same untrusted judgment that produced the draft. That is a second opinion with the same blind spots, and it verifies nothing. The definition has to come from the human's own review standard: "how would you check this output if a human came to you and gave it to you? ... apply your own taste, apply your own judgment. Let the AI models do it first" **[06:51-07:07]**. The model doing the judging should not invent it.

The same applies to briefs for agents: a brief that lists only past defects produces work that avoids those defects and is still mediocre. State the positive bar as well as the failure list. Nate's full line, "you define the goal, but you also need to very firmly define what does good look like and how do you test if X is good" **[07:47-07:54]**, holds for a decision review as much as for a deliverable.

## Concrete forms of a defined good

- **Persona review panel.** [[wiki/sources/nateherk-build-skills-not-agents|Another Nate Herk video]] gives a reusable version for subjective work: a [[wiki/concepts/persona-review-panel|persona review panel]] (beginner, skeptical buyer, audience member) with the filter "act on issues that recur, not every note". That turns "defined good" into something a skill can run.
- **Golden dataset.** [[wiki/sources/nateherk-one-person-business-claude|A later Nate Herk video]] gives the numeric sibling: a [[wiki/techniques/golden-dataset-eval-loop|golden-dataset eval loop]], where "defined good" is a fixed set of test conversations with **known-correct** agent behaviour, scored objectively (14/16, 88, 94). It adds a wrinkle: because the agent being judged is non-deterministic, even a defined-good judge has to be rerun in full, not only on the case that failed. See [[wiki/concepts/ai-agent-nondeterminism|AI agent non-determinism]].
- **The negative case.** [[wiki/sources/nateherk-make-it-better-100-times|Nate Herk, "Make it better" 100 times]] ran 100 rounds of "improve" with no judge and no defined good; the only per-round metric was lines of code, which always grows and says nothing about quality. Quality peaked in the first 15 to 32 rounds and regressions went uncaught. The judge has to sit inside the loop as well as at the end. See [[wiki/techniques/stopping-criterion-for-self-improvement-loops|Stopping criterion for self-improvement loops]].

## In this system

`.claude/rules/common/agents.md` requires a "What GOOD looks like" line in every multi-step brief, and `/jury` ends a contested decision in a verdict plus the cheapest test.
