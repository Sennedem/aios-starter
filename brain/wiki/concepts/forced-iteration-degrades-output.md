---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, iteration, over-engineering, evals, claude-code]
related: ["[[wiki/sources/nateherk-make-it-better-100-times]]", "[[wiki/techniques/stopping-criterion-for-self-improvement-loops]]", "[[wiki/concepts/ai-website-slop]]", "[[wiki/concepts/tell-it-what-done-looks-like]]"]
---

# Forced iteration degrades output

When you loop an agent on "make it better" and **require it to ship a change every round**, quality rises for a stretch, plateaus, then declines: the agent stops improving and starts adding to satisfy the rule. From [[wiki/sources/nateherk-make-it-better-100-times|Nate Herk, "Make it better" 100 times]].

## The pattern as observed (one run per model, creator-reported)

1. **Early rounds carry the value.** Round 1 was the biggest jump for both models, and the best individual additions appeared by round 15 to 32 (Opus: QR-to-SMS ordering at round 15, a drink matcher at round 32; Sonnet: an order-ahead form at round 32). **[08:31-08:58, 09:11-10:05, 04:21-04:46]**
2. **A plateau no tool noticed.** Sonnet's progress tracker flagged no milestone from round 32 to 100, yet the code kept growing in a straight line. Nate: "we don't know if things are actually getting that much better." **[05:05-05:24]**
3. **Then churn and regression.** The agent removed a feature it had added earlier (Sonnet's right-hand nav, gone between rounds 65 and 100), changed the font for its own sake (round 74 vs 100), and on Opus broke working pieces (a dead section, a Spanish toggle that does not translate, buggy ordering). **[06:28-07:06, 11:00-11:40]**
4. **The objective drifts.** "Improve conversions" turned into upsell and forced ordering, a hard sell in place of a soft close. **[13:24-13:34]**

## Why (Nate's diagnosis plus the obvious mechanism)

- "Innovate without a vision turns into adding." **[13:17-13:22]** With no target state, the only way to satisfy "make one bold change" is to add something.
- The "must ship a change every time" clause removes the model's escape hatch. Without it, Nate's earlier run stopped itself at round 20 to 25, saying nothing more could be done. **[00:44-00:55]** That self-stop was the model's own, possibly correct, done signal, and the forced clause overrode it.
- No judge between rounds: nothing compared round N with round N-1, so nothing could reject a regression. The only per-round number was lines of code, which only goes up and says nothing about quality. **[05:10-05:24]**
- Nothing read the web or references either, so each round drew only on the model's own priors. That pool of ideas is finite and gets recycled. **[12:36-13:10]**

## What it does and does not show

- It shows that one recipe (forced change, vague objective, no judge) degrades. It does **not** show that iterating with a judge, a done condition or a keep-or-revert step degrades.
- It is n=1 per model on one site; "Opus over-engineers more than Sonnet" is one draw each. Treat the shape (plateau, then churn) as a plausible hypothesis and the fix below as the testable part.

## The fix

Give the loop a defined good, a keep-or-revert step and a stop rule. See [[wiki/techniques/stopping-criterion-for-self-improvement-loops|Stopping criterion for self-improvement loops]]. Related: [[wiki/concepts/tell-it-what-done-looks-like|Tell it what done looks like]] (the up-front done condition this run lacked) and [[wiki/concepts/ai-website-slop|AI website slop]] (the same site-quality failure from the other side: vague adjectives, no references).

## In this system

`.claude/rules/common/verification.md` puts four guards on any repeated improve pass: a judge before round 1, keep the best so far, "nothing left to improve" counts as a round, and stop on plateau.
