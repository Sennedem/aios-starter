---
type: note
status: active
updated: 2026-11-16
domain: wiki
parent: "[[wiki/README|Wiki]]"
---

# LLM wiki pattern

A personal knowledge base that a language model builds and maintains for you. The idea was popularised by Andrej Karpathy.

## How it works

1. Drop a source into `raw/` (a transcript, an article, a PDF).
2. The model reads it and writes small pages: one concept, tool or technique per page.
3. Each new page is linked to the pages that already exist, and added to the index.
4. An append-only log records what came in and what changed.

## Why it beats a folder of summaries

A summary is read once and forgotten. A small page with links gets found again every time a later source touches the same idea, and the model can update it with what the new source adds or contradicts.

## In this vault

`/ingest` runs the pattern. [[wiki/tools/obsidian|Obsidian]] is the viewer.
