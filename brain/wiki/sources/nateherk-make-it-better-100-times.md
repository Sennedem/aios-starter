---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=DByAR5Su1Yw
tags: [wiki, source, youtube, claude, iteration, evals, web-design]
related: ["[[wiki/concepts/forced-iteration-degrades-output]]", "[[wiki/techniques/stopping-criterion-for-self-improvement-loops]]", "[[wiki/concepts/ai-website-slop]]", "[[wiki/concepts/model-matters-less-than-the-brief]]", "[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/techniques/golden-dataset-eval-loop]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]", "[[wiki/tools/scroll-craft]]"]
---

# Nate Herk: "I Told Claude to 'Make it better' 100 Times (It Went Too Far)"

YouTube, 13.8 min, Nate Herk | AI Automation, published 2026-10-30: https://www.youtube.com/watch?v=DByAR5Su1Yw.

## The experiment

Nate took a deliberately awful coffee-shop site and sent Claude Code the **same prompt 100 times in a row**: look at the site first, then innovate, think about UX and outside the box, make **one bold change** that improves conversions or look and feel (not a small tweak), use any tool, and **"you must ship a change every time."** **[00:00-00:45]** He ran it twice: Sonnet 5.5 on medium effort and Opus 5.5 on medium effort. The "must ship" clause exists because an earlier attempt stopped itself at round 20-25, saying nothing more could be done. **[00:44-00:55]**

Control design: each round ran in a **clean room** (fresh session, no skills, no CLAUDE.md, no plugins, no memory), so each model had only its own knowledge and built-in tools. **[01:29-01:42]** Nate watched the results in a local tracking page he built (per-round tool calls, line count, API-equivalent cost, and a "milestone" view). **[01:53-02:10]**

His motive: AI is bad at thinking outside the box, vague "make it prettier" goals hit a ceiling around "80 out of 100", and the last stretch needs a human applying taste. **[01:03-01:28]**

## What happened (timeline)

| Round | Sonnet 5.5 | Opus 5.5 |
|---|---|---|
| 1 | The biggest single jump: first look at its own site, first AI image, first JS, first mobile-ready version. Still plain (a simple punch card, a boring font) **[02:27-02:52]** | The same milestone set, more progress than Sonnet in round 1; still "bland, very boring" **[07:45-08:11]** |
| 2 | A sticky order bar on scroll, "a nice little innovation" **[02:53-03:10]** | |
| 7 | 253 to 419 lines; menu items show a picture **[03:11-03:35]** | First AI video (hero background), dark theme, AI-generated menu images **[08:12-08:30]** |
| 15 | | First form, plus a QR code that pre-fills an SMS with the order. Nate: "that's actually not bad. That's pretty cool" **[08:31-08:58]** |
| 24 | 778 lines; first AI video; a scroll animation; the order box now looks like a receipt **[03:41-04:10]** | |
| 32 | First form (order ahead, pickup). **The last milestone the tracker flagged.** **[04:21-04:46]** | First canvas/WebGL: a drink matcher. Nate "would have kept that change" and says he might stop here **[09:11-10:05]** |
| 33-100 | No milestone flagged. Lines of code rise roughly linearly while per-round cost wobbles: "it's adding a bunch of code and we don't know if things are actually getting that much better" **[05:05-05:24]** | 68 rounds left after round 32 **[10:33]** |
| 65 vs 100 | Round 65 had a right-hand nav bar that is gone by round 100: the model removed a feature it didn't like **[06:28-06:48]**. The round 74 font differs from round 100: "I'm just going to change the font" **[06:57-07:06]** | |
| 100 | Richer (a floating bar, testimonials, falling leaves, hero stats, "only two left baked at 11am", a pop-up), but Nate asks "at what point is this too much?" **[05:25-06:25]** | "Overwhelming", "AI slop": a pumpkin-carving widget, music, a language toggle that doesn't switch to Spanish, a section that "doesn't even work anymore", buggy ordering ("you have to start at the bottom"), a caffeine-in-your-system tracker. "It ended up breaking some of its own stuff" **[10:40-12:00]** |

Final stats **[12:04-12:30]**: Opus ran about 8.5 hours, about $137 API-equivalent, 54 AI images, 3 AI videos, about 21,000 lines. Sonnet ran just under 2 hours, about $22 (his tracker earlier read $29.93; see the grades), 11 images, 2 videos, under 3,000 lines. Both ran on Nate's subscription, so the dollar figures are what API billing would have cost. Neither model ever used web search (no award sites, no 21st.dev inspiration), which surprised him. **[12:36-13:10]**

## Takeaways

1. **Quality peaked early and the rest was churn.** Both models' last genuinely good additions came in the first 15-32 rounds (Opus: the QR/SMS order in round 15, the WebGL matcher in round 32; Sonnet: the form in round 32). Rounds 33-100 added volume, not value. **[04:46-05:24, 10:05-10:35]**
2. **Forcing a change every round turns "improve" into "add".** "Innovate without a vision turns into adding." Nate's own diagnosis: the "you must ship" clause drove the over-engineering. **[06:49-06:56, 13:17-13:22]**
3. **There was no judge except Nate.** The loop had no scorer, no rubric and no keep-or-revert step, so regressions (the removed nav, the broken section, the dead Spanish toggle) piled up silently. Lines of code was the only per-round metric, and it only goes up. **[05:10-05:24, 11:20-11:40]**
4. **Conversion pressure becomes a hard sell.** Both runs drifted toward upsells and forced ordering: "a hard sell, rather than a soft close." **[13:24-13:34]**
5. **The model sets the ceiling, the prompt sets the direction.** The same prompt gave very different results: Opus was more ambitious early and blew up bigger later; Sonnet was smaller, cheaper and steadier. **[13:12-13:19]**
6. **Human taste and references are still needed to reach the 90s.** Nate's bet is that a human applying taste and inspiration beats autonomous iteration past about 80/100. This was his thesis going in; the run illustrates it but does not prove it. **[01:15-01:28, 10:00-10:05, 11:55-12:01]**

The extracted rules live on [[wiki/concepts/forced-iteration-degrades-output|forced iteration degrades output]] and [[wiki/techniques/stopping-criterion-for-self-improvement-loops|stopping criterion for self-improvement loops]].

## Claim grades

| Claim | Grade |
|---|---|
| The setup, prompt text, clean-room condition, round-by-round screenshots and final sites | Demonstrated on screen |
| The round-100 Opus site has dead or buggy features (Spanish toggle, a section, pumpkin ordering) | Demonstrated on screen (Nate clicks them), single viewer |
| "Round 65 or so would have been good enough" | Creator opinion, framed as a question; no rubric or blind comparison |
| Cost, hours, line counts, image and video counts | Creator-claimed from his own tracker (API-equivalent, not billed); Sonnet's cost stated two ways |
| "AI is bad at thinking outside the box"; "capped at 80/100 without a human" | Creator thesis, not tested (no human-in-the-loop arm in the experiment) |
| Milestones | Labels produced by his tracker; how a round qualifies is not explained |

## Skeptic note

- **n=1 per model: one task, one site, one prompt.** No second seed and no second task. "Opus over-engineers more than Sonnet" is one draw each, both on medium effort, with models of different sizes, so it is not a clean model comparison.
- **The failure is largely built into the prompt.** "You must ship a change every time" plus "bold change, not a small tweak" guarantees additive churn, and Nate's earlier unforced run stopped itself at round 20-25. So the lesson is "a forced-change loop with no judge degrades", not "AI iteration degrades". The unforced stop was arguably the model's own correct stopping signal, which he overrode.
- **No quality metric.** "Better" and "too much" are one person's taste, judged from the final sites. There was no per-round scoring and no blind comparison between rounds 32, 65 and 100, and "round 65 is good" was not tested against round 100 with users or a conversion metric.
- **The title ("went too far") is entertainment.** The useful content is the first third of the build and the last two minutes.
- **He promotes his [[wiki/tools/scroll-craft|ScrollCraft]] skill mid-video** [07:09-07:35], in the same breath as noting that the clean room had no skills. The experiment does not test whether that skill would have prevented the drift.
- **Cost and time:** Opus's 4x time and 6x cost for a result Nate called worse by the end is the one robust-looking number, and it too depends on the forced-ship clause.

## Cross-source connections

- [[wiki/concepts/ai-website-slop|AI website slop]] (from [[wiki/sources/nateherk-fable-5-1-kills-website-slop|"Fable 5.1 kills website slop"]]): **extends.** Vague "make it premium" gives slop through genericness; unbounded "make it better" gives slop through accumulation. Both are fixed with concrete references and a vision. The earlier video stresses inspiration sites; here neither model searched the web.
- [[wiki/concepts/model-matters-less-than-the-brief|Model matters less than the brief]]: **partial tension.** Fable 5 and 5.1 produced near-identical sites under a tight brief; here a loose, forced brief makes the model matter a lot. Reconciliation: model differences show up when the brief leaves room and wash out when it is specific.
- [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]] and [[wiki/concepts/tell-it-what-done-looks-like|tell it what done looks like]]: **confirmed by absence.** The loop had neither a defined good nor a done condition, and 100 rounds show the consequence.
- [[wiki/concepts/prove-its-work|Prove its work]] and [[wiki/techniques/golden-dataset-eval-loop|golden-dataset eval loop]]: **confirms.** Step 4 of the eval loop (rerun the full suite after each fix, so a fix that breaks something else is caught) is exactly what this loop lacked; its regressions are the failure that step is built to catch.

## In this system

`.claude/rules/common/verification.md` ("Know when an improve loop must stop") turns this into four guards: a judge before round 1, keep the best so far, "nothing left to improve" is a valid round, and stop on plateau.
