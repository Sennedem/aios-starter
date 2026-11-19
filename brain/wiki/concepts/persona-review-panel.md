---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, skills, verification, persona, review]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/techniques/verify-before-returning]]", "[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/techniques/roast-room-council-debate]]"]
---

# Persona review panel

For subjective output (a script, an ad, anything without an objective pass or fail), Anthropic's suggested fix is to have a few sub-agent **personas** review it and discuss. Nate Herk relays this from Barry Zhang and Mahesh Murag. A beginner flags where it got confused, a skeptical buyer flags what it doesn't believe, and an agent playing the real target audience flags where it would click away [07:31-07:46].

The discipline that makes it work: **don't accept every note**. Chasing every individual reaction makes the output worse. The skill looks for issues that **recur across personas**, makes the strongest revisions for those, and runs the review again. Sometimes hearing the different perspectives surfaces something useful even without a literal fix [07:46-07:59].

## Why it counts as verification

Claude reading its own work and saying "looks good to me" is no check at all. Verification needs evidence from outside the first draft: a screenshot, a test result, a source, a reference example, **or feedback from several distinct agent perspectives**. The persona panel is one concrete way to manufacture that outside evidence for subjective work [07:59-08:09]. It is also one way to build the defined-good judge that [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]] asks for on taste or strategy work.

## Related

- [[wiki/techniques/roast-room-council-debate|Roast room council debate]] ([[wiki/sources/nateherk-roast-room|source]]) is a heavier sibling. Personas debate a choice before it is made (vote, score, cross-attack), each backed by an [[wiki/concepts/expert-persona-brain-files|expert brain folder]], instead of reviewing a finished piece. Both sources use one distinct lens per persona; neither tests whether the personas stay true to their role.
- [[wiki/techniques/verify-before-returning|Verify before returning]] shows where the panel fits in the check-before-return loop.

## In this system

`/jury` runs the decision version of this panel, with a buyer seat that role-plays the person who pays. `/second-opinion` and `/review-deliverable` review one finished piece.
