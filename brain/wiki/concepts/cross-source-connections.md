---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [knowledge-management, wiki]
related: ["[[wiki/concepts/llm-wiki-pattern]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]", "[[wiki/techniques/wiki-ingest-workflow]]"]
---

# Cross-source connections

The concrete payoff of a wiki over a pile of separate per-source summaries: when two sources go into the same wiki, the AI can notice that they reference each other and surface that as its own shared page. Reading the sources one at a time, that connection is easy to miss.

## The example [11:24-11:53]

In [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|his Karpathy LLM-wiki video]], Nate Herk ingested two AI-safety documents into one wiki: Anthropic's Claude Fable 5 / Mythos 5 system card (a PDF dropped in `raw/`) and an OpenAI article previewing GPT-5.6 Soul (a URL). The ingest created 20 cross-linked pages from those two sources. One of them, "Frontier Model Cybersecurity", captured that OpenAI had benchmarked GPT-5.6 Soul against Mythos Preview.

He flags a caveat worth keeping: OpenAI compared against the April predecessor, not Mythos 5 itself, and the two labs used different eval harnesses, so the numbers do not line up directly. The wiki surfaced the connection; it did not validate the comparison. That check still falls to a human or a research agent, which is why claims should be triangulated instead of trusted from one source.

## Why it takes a wiki, not summaries

Two standalone summary docs never get re-read against each other unless a human cross-checks them by hand. A wiki's cross-linking makes the AI surface the overlap during ingest, because it reads the whole graph (index plus existing pages) and not only the new source. The effect grows with the wiki: the first ingest has nothing to connect to, and each later one has more.

## In this system

`/ingest` reads the index and existing pages before filing a new source. [[references/research-source-objectivity]] covers how to check a surfaced claim.
