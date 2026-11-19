---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [concept, prompting, verification, subagents]
related: ["[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/techniques/verify-before-returning]]", "[[wiki/concepts/seen-inferred-unknown]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# Prove its work

Nate Herk's favorite of four prompting tricks, "not just for Fable 5.1, but just in general working with AI": apply your own review taste and judgment, but **let the AI apply it first**. Instead of a rough draft, you get something sub-agents have already reviewed and iterated several times before it reaches you [06:48-07:26]. From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]].

The catch: not every output has an objective check. Where it doesn't, you are building your own LLM-as-judge, which means you still have to define what good looks like and how to test for it. It won't get the model 100% of the way, but 97% beats 70% [07:26-08:02].

## The evidence, quoted

> "Make self-verification explicit in long-run prompts", literally telling it: "verify your work with sub agents against the specification." [08:03-08:14]

> "Verify your work however you like." [08:14-08:17]

> "Before reporting progress, audit each claim against a tool result from the session. Only report work you can point to evidence for. If something is not yet verified, say so explicitly." [08:17-08:28]

The last quote is worth pasting into any long-running brief as written: every claim of done points to a tool result, and anything unchecked is reported as unchecked.

## Vision verification

Fable 5.1 has better vision out of the box. On complex visual inputs like dense charts it does its best work when it can **iteratively analyze, crop and visually verify** what it sees, instead of judging a whole image in one pass [08:28-08:48]. For a visual deliverable that is a sharper check than a single look at a screenshot: crop into the parts that can go wrong.

## Related

- [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]] is the subjective-check half of this idea.
- [[wiki/techniques/stress-test-with-subagents|Stress-test with subagents]] is the adversarial sibling. Instead of checking its own work against a spec, a swarm of agents tries to break the finished automation (spam, malformed input, duplicate triggers) before a real user does.
- [[wiki/sources/nateherk-build-skills-not-agents|Nate Herk on Agent Skills]] makes the same argument from the skill-design side: bake the check into the skill (render slides as images and inspect them, open primary sources and match claims to evidence) so the human's first look is the agent's fourth or fifth. See [[wiki/techniques/verify-before-returning|Verify before returning]].
- [[wiki/concepts/seen-inferred-unknown|Seen / inferred / unknown]] applies the rule to an agent's findings about something it investigated ([[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk on REA]]).
- [[wiki/sources/nateherk-make-it-better-100-times|"Make it better" 100 times]] shows the cost of skipping it. Opus's round-100 site shipped with a dead section, a language toggle that doesn't translate and buggy ordering ("it didn't really get tested very well"). A loop that ships every round without self-verification piles up breakage.

## In this system

`.claude/rules/common/verification.md` (done is a claim, verification is evidence; structural checks versus looking at the output) and `/five-gates` for hard tasks.
