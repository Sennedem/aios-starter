---
type: index
status: active
updated: 2026-11-16
domain: wiki
parent: "[[README|Brain]]"
---

# Wiki

This is where outside knowledge goes: videos, articles, PDFs and books. It follows the LLM-wiki pattern: Claude splits each source into small pages, one idea per page, and links them to the pages that already exist. Two sources on the same subject end up connected instead of sitting in two separate summaries.

Run `/ingest <url or file>` and Claude does the filing. Notes about your own work do not belong here; they go in `context/` and `projects/`.

## Structure

- `raw/`: the source as it came in (transcript, article text). Never edited after ingest.
- `sources/`: one page per source: what it is, the main takeaways, links to the pages it produced, and how far to trust it.
- `concepts/`: one idea per page.
- `tools/`: one page per tool or product.
- `techniques/`: how-tos you can act on.
- [[wiki/log|log]]: append-only list of what was ingested and when.

## Index

_Maintained by `/ingest`, one line per page._

### Sources

_None yet._

### Concepts

- [[wiki/concepts/llm-wiki-pattern|LLM wiki pattern]]: raw sources in, small linked pages out, an index and a log, maintained by the model

### Tools

- [[wiki/tools/obsidian|Obsidian]]: the app that shows this vault as linked pages and a graph

### Techniques

_None yet._
