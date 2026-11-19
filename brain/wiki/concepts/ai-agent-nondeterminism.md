---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, evals, non-determinism, agents]
related: ["[[wiki/techniques/golden-dataset-eval-loop]]", "[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/sources/nateherk-one-person-business-claude]]"]
---

# AI agent non-determinism

A single passing rerun of an AI agent does not prove a fix worked, because agents answer the same input differently from one run to the next. The worked example in [[wiki/sources/nateherk-one-person-business-claude|Nate Herk's one-person business video]]: a support agent scores 88/100 on a 16-test golden dataset (14 pass, 2 fail). One failure gets diagnosed and patched with a tighter instruction. The suite reruns and still scores 88: the original failure is fixed, but a different test now fails, "because these agents can respond a little differently from one run to the next... they are non-deterministic." A third run scores 94. **[04:44-06:00]**

## Why it matters more than it looks

The naive read of a repeated 88 is "the fix didn't work." The real cause is that the test suite samples a fuzzy process that varies per run. Fixing one known failure does not shrink the space of possible failures to zero; it moves which test happens to catch the remaining one. A single test, or a single rerun, cannot tell "the fix failed" apart from "the fix worked and something else drew the short straw this run."

The mitigation is scale, since certainty is not on offer: "fixing just one example doesn't prove the whole agent is reliable... the bigger the golden data set, the more confidence you can have in the quality and performance of these AI agents" [05:14-05:30]. Sixteen tests is a demo-sized dataset, not a claim of completeness. More tests narrow the blind spot that run-to-run variance hides in; they do not remove it.

## How this differs from automation triage

[[wiki/concepts/deterministic-vs-nondeterministic-automation|Deterministic vs non-deterministic automation]] answers which steps in a pipeline need an AI at all. This page covers what that page does not: once a step is correctly routed to an agent, the step itself is not stable across runs of identical input. One passing run is weak evidence; a growing golden dataset (see [[wiki/techniques/golden-dataset-eval-loop|Golden-dataset eval loop]]) is what raises confidence.

Practical corollary for any skill whose prompt gets patched after a failure: rerun the whole verification suite, not only the case that failed, and expect the score to move sideways at least once before it moves up.

## In this system

`.claude/rules/common/skills.md` asks for at least three reruns, or a saved set of known cases, before an agent-produced fix counts as fixed.
