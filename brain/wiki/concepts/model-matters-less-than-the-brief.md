---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, model-routing, prompting, cost]
related: ["[[wiki/concepts/ai-website-slop]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]", "[[wiki/tools/claude-fable-5-1]]", "[[wiki/sources/nateherk-make-it-better-100-times]]"]
---

# Model matters less than the brief

A controlled comparison from [[wiki/sources/nateherk-fable-5-1-kills-website-slop|Nate Herk, Fable 5.1 kills website slop]]: holding prompt, assets, brand guidelines and skill constant, Fable 5 and Fable 5.1 produced near-identical website output. The seven rules for non-slop sites (brand guidelines, the [[wiki/concepts/three-ps-pain-person-promise|three P's]], scroll feedback, inspiration, reused components, mobile verification, screenshot verification) mattered more than which model ran the job.

## The test

Nate built several perk-form sites, alternating Fable 5 and Fable 5.1, with the "same prompts, the same assets, the same brand guidelines… and they used the same skill" (his [[wiki/tools/scroll-craft|ScrollCraft]] skill). His verdict: "they just felt very similar… not enough for me to be like, 'Wow, Fable 5.1 crushes Fable 5.'" A few minor differences, no clear winner.

## Where the real difference showed up: cost

Across four paired examples, Fable 5.1 was cheaper than Fable 5 on the same job every time:

| Fable 5.1 | Fable 5 |
|---|---|
| 18.24 | 20.22 |
| 14.52 | 14.67 |
| 12.83 | 21.64 |
| 11.18 | 17.37 |

After 5 to 6 hours of work on 5.1 he had used only about 45% of his weekly Fable usage limit, against burning through the same limit in 1 to 2 hours on Fable 5 doing comparable work. He ties this to Anthropic's release-blog claim that 5.1 could run up to 45% cheaper than 5 on heavy agentic and multi-step work, and reports his own results in that range. The exact cost figures and units are on the [[wiki/tools/claude-fable-5-1|Fable 5.1 tool page]].

## Why this matters for prompting

If swapping the model does not fix generic output, the fix for [[wiki/concepts/ai-website-slop|AI website slop]] has to be structural (a skill, named references, explicit inspiration), not "wait for a better model." For budget: with near-identical quality, routing to the cheaper model is close to a free win. This is the checklist test for routing in practice: when the spec is fixed (seven rules plus a skill) and the output can be verified by screenshot, the routing decision should follow cost, not a guess at which model is "better" for creative work.

## A qualifying result

[[wiki/sources/nateherk-make-it-better-100-times|Nate Herk, "Make it better" 100 times]] reached the opposite surface result: with the same loose prompt, Sonnet 5.5 and Opus 5.5 diverged sharply (Opus about 8.5 h, about $137, about 21k lines, and it broke itself; Sonnet about 2 h, about $22 to 30, under 3k lines). Nate's summary: "the model sets the ceiling, the prompt sets the direction". The two fit together: model differences show when the brief leaves room, and a tight brief plus a skill flattens them. One run each, so treat it as suggestive.

## In this system

`.claude/rules/common/model-routing.md` uses the same checklist test: route down when the task has a checklist and a verifiable output.
