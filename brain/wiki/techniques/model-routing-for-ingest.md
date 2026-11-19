---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=hQvwMj7IJe4
tags: [wiki, technique, ingest, model-routing]
related: ["[[wiki/techniques/match-effort-to-the-task]]", "[[wiki/concepts/effort-level-vs-model-tier]]", "[[wiki/techniques/wiki-ingest-workflow]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]", "[[wiki/sources/nateherk-fable-5-1-release]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]"]
---

# Model routing for ingest

Split the model choice by task: use a cheaper workhorse model (Opus or Sonnet tier) for the mechanical work of ingesting sources into a wiki, and save the frontier model (Fable) for synthesis once the data is in. From [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|Nate Herk's Karpathy LLM wiki video]] [07:44-07:59].

In Nate's words: "we are using Fable here... you probably don't need Fable. Fable's probably overkill for this. It's about what Fable does *after* you have all that data in there... if you want to switch this back to Opus, run the ingest, and ingest future documents with Opus, that's probably a better call, honestly."

## Why the split holds

Ingestion is pattern-matching and structuring: splitting a source into atomic pages, cross-linking, updating an index and a log. That is a fixed-spec execution task, not a judgment task. Synthesis is where the frontier model's edge showed up. His example: turning a "messy blob of transcript connections" into a beginner-friendly narrative HTML page in one emotionally toned prompt [01:24-02:58], which beat a full day of back-and-forth with a lesser model on the identical database.

The general rule: mechanical grind goes to the cheapest tier, executing a fixed spec goes to a mid tier, and hard synthesis goes to the top tier. Ingest sits in the fixed-spec tier.

## When a new generation ships

[[wiki/sources/nateherk-fable-5-1-release|Nate Herk's Fable 5.1 release video]] adds a wrinkle: Anthropic's own benchmarks reportedly show Fable 5.1 on *low* effort beating Fable 5 on *max* effort, and cheaper (see [[wiki/concepts/effort-level-vs-model-tier|effort level vs model tier]]). So "which model" and "how much effort" may need re-tuning together whenever a new generation ships.

This page routes only by model tier. For the effort axis within one model, see [[wiki/techniques/match-effort-to-the-task|Match effort to the task]] (from [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]]), with its docs-quoted "start high, test medium, then low" sequence.

## In this system

`.claude/rules/common/model-routing.md` holds the routing table; `/ingest` is the ingest job it applies to.
