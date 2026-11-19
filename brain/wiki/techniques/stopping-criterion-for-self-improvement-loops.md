---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=DByAR5Su1Yw
tags: [wiki, technique, iteration, evals, verification, claude-code]
related: ["[[wiki/sources/nateherk-make-it-better-100-times]]", "[[wiki/concepts/forced-iteration-degrades-output]]", "[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/techniques/golden-dataset-eval-loop]]", "[[wiki/concepts/tell-it-what-done-looks-like]]"]
---

# Stopping criterion for self-improvement loops

How to stop an "improve it N times" loop before it degrades. Nate Herk's source ([[wiki/sources/nateherk-make-it-better-100-times|Make it better 100 times]]) shows the failure and does not give the fix. The rules below are this wiki's synthesis of that failure against other pages, so read them as **untested proposals** (the video itself ran no judged loop).

## What the failed run lacked, and what to add

| Missing in the 100-round run | Add |
|---|---|
| A target state ("innovate" has no end) | A written done condition up front: what the page must do and what it must not contain. See [[wiki/concepts/tell-it-what-done-looks-like|Tell it what done looks like]] |
| A judge comparing round N to N-1 | A fixed rubric or golden checklist the loop scores against each round, written by the human, not by the looping model. See [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]] |
| A keep-or-revert step | Keep the change only if the score rises; otherwise revert. In the run, regressions (a removed nav, a dead section) stayed |
| A way to say "nothing left" | Allow a no-change round. Nate had to forbid it to get past round 20 to 25; the unforced stop was a legitimate signal **[00:44-00:55]** |
| A full regression check | After each change, re-test everything that already worked, not only the new thing. See [[wiki/techniques/golden-dataset-eval-loop|Golden-dataset eval loop]] step 4 |
| An outside input | Inject real references each round (the run never used web search, so it recycled its own priors) **[12:36-13:10]** |

## Stop rules worth trying

1. **Plateau stop:** halt after K rounds in a row (say 3 to 5) where the judge's score does not improve. In the run, Sonnet flagged nothing from round 32 to 100. **[05:05-05:07]**
2. **Budget stop:** cap rounds or cost up front (Opus took 8.5 hours and about $137 API-equivalent for a result Nate disliked). **[12:04-12:12]**
3. **Best-so-far snapshot:** keep the highest-scoring version and return that, not the last one. In the run, round 100 was not the best version by Nate's own judgment: he asks whether he would have stopped at round 65, and says of Opus he might have stopped at round 32. **[06:22-06:30, 10:28-10:35]**
4. **Human checkpoint every 10 to 15 rounds**, because taste is where the loop ran out. **[01:15-01:28]**

## Calibrate the judge before trusting it

A judge that cannot tell a good round from a bad one is worse than none. Run the rubric on a known-good version and a known-bad one first. If it cannot separate them, the stop rule it feeds is fiction. Lines of code, the per-round metric in the video, is exactly such a metric: a bad build can satisfy it.

## In this system

`.claude/rules/common/verification.md` ("Know when an improve loop must stop": a judge before round 1, keep the best so far, allow a no-change round, stop on plateau) and `.claude/rules/common/agents.md` (do not ship a gate you have not calibrated).
