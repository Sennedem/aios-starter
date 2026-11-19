---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [knowledge-management, structure, wiki]
related: ["[[wiki/concepts/llm-wiki-pattern]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]"]
---

# Flat vs foldered wiki structure

A wiki's structure is not decided up front. It should follow from the type of data, and the AI re-evaluates it as pages accumulate. [08:20-08:45]

In [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|his Karpathy LLM-wiki video]], Nate Herk runs two differently shaped wikis side by side:

- **His "Herk brain" (meeting transcripts)** stayed flat. Every meeting recording sits directly in the wiki with no subfolders, because no natural grouping had shown up yet, and sometimes flat is better: it is easier for the AI to search a flat set of files than to guess which subfolder something landed in.
- **His YouTube-transcript wiki** grew subfolders on its own (concepts, sources, tools, techniques) because that source type had natural categories.

The deciding factor he gives: keep it flat when flatness makes the AI's search easier. Folders are a convenience, not a requirement, and the structure should be revisited ("run some sweeps through it") instead of fixed at setup.

## Choosing per area

A wiki fed by varied sources (videos, articles, system cards) tends to suit the four-folder shape. An area that fills with one homogeneous source type, such as a flood of similar transcripts, may be better flat. Decide per area instead of forcing one shape everywhere.

## In this system

This wiki uses the foldered shape (`sources/`, `concepts/`, `tools/`, `techniques/`), and `/ingest` files new pages into it.
