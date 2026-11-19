---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=hQvwMj7IJe4
tags: [wiki, technique, ingest, workflow]
related: ["[[wiki/concepts/llm-wiki-pattern]]", "[[wiki/concepts/claude-md-as-router]]", "[[wiki/tools/obsidian]]", "[[wiki/techniques/model-routing-for-ingest]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]"]
---

# Wiki ingest workflow

The end-to-end flow Nate Herk demos for adding a source to an [[wiki/concepts/llm-wiki-pattern|LLM wiki]], from [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|his Karpathy LLM wiki video]] [09:49-11:23].

## Steps

1. **Drop the raw source in.** A PDF gets dragged straight into `raw/`. A web article is handled by pasting the URL in the prompt instead of downloading it.
2. **One instruction covers both.** The prompt used: *"Hey Claude, read this article and ingest it into our wiki here. And I dropped a PDF in the raw called [X], ingest that too."* No page count, naming or folder placement was specified by hand.
3. **The agent decides the page count.** From 2 sources the run produced 20 fully cross-linked wiki pages. Whether a source becomes 1 page or 50 depends on how much distinct, atomic content it holds, with no fixed rule.
4. **Index and log update in the same run.** A new record appears in the index (the table of contents) and in the log (the append-only ingest history). This is how the AI later finds what it created.
5. **Runtime:** his 2-source, 20-page run took 10 to 12 minutes.
6. **Review and correct.** [13:16-14:04] After a batch ingest, open a few of the new pages and check that the organisation makes sense. If it does not, update the *ingest rules* (in CLAUDE.md, see [[wiki/concepts/claude-md-as-router|CLAUDE.md as router]]) so future ingests land correctly, instead of only moving files. Different wikis need different rules depending on the data (meeting transcripts, proposals, videos).

## Bootstrap step (once per new wiki)

Before the first real ingest, the wiki has to exist. Create an Obsidian vault (see [[wiki/tools/obsidian|Obsidian]]), open it in Claude Code, paste in Karpathy's LLM-wiki gist verbatim, and instruct the agent: *"You are now my LLM wiki agent. Implement this exact idea file as my complete second brain. Guide me step by step. Create the CLAUDE.md schema with my full rules. Set up the index, the log, define folder conventions, and show me the first ingest example. From now on, every interaction follows the schema."* [07:12-07:42]

Ingest is a fixed-spec job, so it can run on a cheaper model; see [[wiki/techniques/model-routing-for-ingest|Model routing for ingest]].

## In this system

`/ingest` runs this workflow: a raw copy in the wiki's own `raw/` folder, atomic pages under `brain/wiki/`, and an updated index and log. The bootstrap step is already done.
