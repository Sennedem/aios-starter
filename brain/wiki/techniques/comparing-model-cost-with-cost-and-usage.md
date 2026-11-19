---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=8IyORt-7rOQ
tags: [wiki, technique, claude, cost, usage, benchmarking]
related: ["[[wiki/tools/claude-fable-5-1]]", "[[wiki/concepts/effort-level-vs-model-tier]]", "[[wiki/sources/nateherk-fable-5-1-release]]"]
---

# Comparing model cost with /cost and /usage

A quick technique from [[wiki/sources/nateherk-fable-5-1-release|Nate Herk's Fable 5.1 release video]] [03:59-05:09] for checking a vendor's cost claims on your own workload, instead of trusting the benchmark chart alone.

## The method

1. Run the **exact same prompt** against two models or versions in separate sessions. Nate's test prompt: "build me a rotating 3D cartoon bear riding a bike."
2. After each run finishes, pull the actual spend with `/cost` (or `/usage`, which Nate uses interchangeably in the video) instead of estimating from token counts.
3. Compare wall-clock time and dollar cost side by side, and look at the output as well. Cost alone does not tell you whether the cheaper run is also worse.

Nate's result on this one prompt: Fable 5.1 took 6m34s and cost $4.53; Fable 5 cost $5.41 and was slightly faster, but the Fable 5.1 output looked more polished to him (shadows, physics). He says plainly that this is **one sample, not a benchmark**: "not any sort of definitive test" [04:38-04:40].

## Why this beats reading the marketing chart

Anthropic's benchmark chart in this release ([[wiki/concepts/effort-level-vs-model-tier|effort level vs model tier]]) is a vendor-published number on vendor-chosen tasks. A same-prompt `/cost` comparison on a task that matters to you is a cheap, fast way to get a real data point, even if it is a single sample, before you move budget or a workflow onto a new model generation.

Use it before routing a heavy recurring workload onto a new model by default: run it once on the new model and once on the previous one, then compare.

## In this system

`.claude/rules/common/model-routing.md` sets the default model and effort per task type; this A/B check is how to test a change to that table before you make it.
