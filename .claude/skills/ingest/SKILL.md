---
name: ingest
description: Ingest an external knowledge source (article URL, PDF, transcript, video transcript, notes) into the brain's learning wiki at brain/wiki/. Saves a raw copy, splits the source into atomic cross-linked pages, and updates the wiki index and log, surfacing links and conflicts with what the wiki already holds. Use when the user says "/ingest <source>", "ingest this into the wiki", "save this to the wiki", "file this article". Not for the user's own curated context (context, projects and decisions stay hand-curated).
---

# /ingest: external knowledge into the learning wiki

Turns one external source into permanent, compounding knowledge: a raw copy in `brain/wiki/raw/`, atomic cross-linked pages in `brain/wiki/{sources,concepts,tools,techniques}/`, and an updated index and log. The payoff is cross-source connections: when a new source touches a concept the wiki already has, the link (or the conflict) gets surfaced instead of lost.

## Boundaries

- **External knowledge only.** Never ingest the user's own curated context: `brain/context/`, `brain/projects/` and `brain/decisions/` stay hand-curated and out of this wiki.
- **Free only.** No paid APIs. Get content from captions, free web reads and local files.
- **Filing, not writing.** This is knowledge filing; the `writing` skill is not involved.
- **Raw is immutable.** Files in `brain/wiki/raw/` are never edited after ingest.
- If `brain/wiki/README.md` or `brain/wiki/log.md` does not exist yet, create it (frontmatter `type: index` or `type: log`, `domain: wiki`, `updated:`) before the first ingest.

## Flow

### 1. Get the source content

| Source type | How |
|---|---|
| Video URL | Get the transcript first: captions via `yt-dlp --write-auto-subs --skip-download <url>`, or the optional `watch` skill from github.com/bradautomates/claude-video |
| Article URL | a web fetch or scrape tool |
| PDF or local file | Read it |
| Pasted text or an existing transcript | use as is |

### 2. Save the raw copy

Write `brain/wiki/raw/<yyyy-mm-dd>-<slug>.md` with frontmatter:

```markdown
---
type: reference
domain: wiki
updated: <today>
tags: [raw]
source: <url or file origin>
ingested: <today>
---
```

The body is the raw material (transcript, article text, extracted PDF text). Binaries stay where they live; the raw file holds the extracted text and a pointer.

### 3. Split into atomic pages (delegated)

Dispatch one general-purpose agent with `model: sonnet` (fixed-spec work, not main-model work). Its prompt must include:

- Paths: the raw file, `brain/wiki/README.md` (current index), `brain/wiki/log.md`, `brain/conventions.md`.
- **Read the index first** so wikilinks land on existing pages: extend an existing page rather than creating a near-duplicate.
- Split the source into atomic pages, typically 5 to 15:
  - `sources/<slug>.md`: the source itself (what it is, author, date, key takeaways, links to every page split from it).
  - `concepts/`: one idea per page.
  - `tools/`: one tool or product per page, only when the source says something substantive about it.
  - `techniques/`: actionable how-tos.
- Every page: frontmatter per `brain/conventions.md` (`type: reference`, `domain: wiki`, `parent: "[[wiki/README|Learning wiki]]"`, `updated`, `tags`, optional `related`) and `[[wikilinks]]` between related pages.
- **Cross-source pass:** where this source confirms, contradicts or extends an existing wiki page, edit that page: add the link and a one-line note naming both sources. These connections are the point; list them explicitly in the return brief.
- Update `brain/wiki/README.md` (one line per new page, in the right folder section) and append one entry to `brain/wiki/log.md` (date, source, page count, connections found).
- Return a brief of 15 lines max: pages created, pages extended, cross-source connections.

### 4. Report to the user

Lead with the connections found (new against existing knowledge), then the page count and where. If the wiki structure is starting to stop making sense (duplicates, an overstuffed folder), flag it; don't silently reorganise.

## Notes

- Batch ingests (several sources at once): one agent per source, in parallel, each given the same index snapshot.
  - No up-front page ownership is needed for overlapping sources. Tell each agent: create pages only with Write, extend only with Edit, never write files through the shell, and Glob for near-duplicates right before creating. Write refuses to overwrite an unread file and Edit refuses a file changed since it was read, so a collision becomes "read it and extend it" instead of a duplicate or a lost edit.
  - Agents return their index lines and log line instead of editing `README.md` and `log.md`. The main session merges them, then checks that every non-raw page is indexed and every wikilink resolves (a wikilink inside a table cell is written `[[x\|y]]`; strip that backslash before resolving).
- Structure is not sacred: if a new category clearly earns its own folder (for example `comparisons/`), create it and note it in the wiki README.
