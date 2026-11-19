---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, claude, effort, model-tier, cost]
related: ["[[wiki/tools/claude-fable-5-1]]", "[[wiki/techniques/model-routing-for-ingest]]", "[[wiki/sources/nateherk-fable-5-1-release]]", "[[wiki/concepts/prompt-cache-read-economics]]", "[[wiki/techniques/comparing-model-cost-with-cost-and-usage]]"]
---

# Effort level vs model tier

A claim from Anthropic's own Fable 5.1 benchmark charts, as read out in [[wiki/sources/nateherk-fable-5-1-release|Nate Herk's release video]]: Fable 5.1 on its **lowest** effort setting outperforms Fable 5 on its **highest** effort settings (max, high, xhigh) on the benchmarks shown, at a fraction of the cost. Nate reads roughly $11.10 for 5.1-low against roughly $44 and $34 for the 5-high variants [02:04-02:35]. The same pattern repeats on the agentic terminal coding and multi-disciplinary reasoning charts [02:38-02:47]. **Anthropic-stated benchmark, creator-read numbers.** Nate: "take these metrics and these benchmarks with a grain of salt. You have to get in there, see how it works" [02:09-02:13].

## The idea in general

Every Claude session has two independent levers: which **model** you run (Fable, Opus, Sonnet, Haiku, and the generation, 5 vs 5.1) and how much **effort** you ask it to spend thinking (low, medium, high, xhigh, max). The intuitive assumption is that low effort on a newer model cannot beat maxed-out effort on the previous one. This claim says that assumption breaks at the 5 to 5.1 boundary: the generational jump is big enough that cheap mode on the new model beats expensive mode on the old one, on quality and cost at once.

## Why it matters if true

If a lower effort tier on a newer generation reliably beats a higher tier on the previous one, the efficient frontier moves. It stops making sense to compensate for an older model's limits by turning effort up once a newer generation is available. The saving then comes on top of [[wiki/concepts/prompt-cache-read-economics|prompt cache-read economics]]: effort-level arbitrage stacked on cache savings.

The practical move: when a new model generation ships, re-check whether a *lower* effort setting on it now covers work that used to need a *higher* setting on the old one. That can be cheaper on both axes at once. The same applies to [[wiki/techniques/model-routing-for-ingest|model routing for ingest]], which treats model and effort as separate levers.

## Caveats

This is one video's read of Anthropic's own marketing benchmark, not an independent replication, and Nate had not run his own before-and-after test at the time (he said a deeper comparison video would follow). Treat it as a hypothesis to check against your own cost and usage numbers ([[wiki/techniques/comparing-model-cost-with-cost-and-usage|how]]), not an established rule.

## In this system

`.claude/rules/common/model-routing.md` sets the default effort per task type; revisit it when a new generation ships.
