---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=hQvwMj7IJe4
tags: [wiki, source, youtube, llm-wiki, second-brain, obsidian]
related: ["[[wiki/concepts/llm-wiki-pattern]]", "[[wiki/tools/obsidian]]", "[[wiki/techniques/model-routing-for-ingest]]", "[[wiki/concepts/flat-vs-foldered-wiki-structure]]", "[[wiki/techniques/wiki-ingest-workflow]]", "[[wiki/concepts/cross-source-connections]]", "[[wiki/concepts/claude-md-as-router]]", "[[wiki/concepts/markdown-portability]]"]
---

# Source: "Fable 5 + Karpathy's LLM Wiki is Basically Cheating" (Nate Herk)

YouTube video (14:35) by Nate Herk | AI Automation: https://www.youtube.com/watch?v=hQvwMj7IJe4.

Nate runs "Herk 2", his own AI-OS-style workspace with several separate LLM wikis (a wiki of his YouTube transcripts, and a "Herk brain" wiki of meeting transcripts). Claude Code with Fable 5 builds and maintains them, using Andrej Karpathy's LLM-wiki gist as the founding spec and Obsidian as the graph front end. The pattern itself is written up on [[wiki/concepts/llm-wiki-pattern|LLM wiki pattern]]; this page is the source and its takeaways.

## Key takeaways

- **[00:18-00:29]** A wiki of his own YouTube transcripts becomes a second brain. He never linked concepts by hand: he told Claude Code to ingest the videos and it built the cross-links itself. See [[wiki/concepts/llm-wiki-pattern|LLM wiki pattern]].
- **[01:24-02:58]** Fable 5's edge is synthesis once the data is in, since any model can ingest. A one-prompt "make this understandable to a beginner" pass beat a full day of manual Opus 4 iteration on the same database. Tone and audience work is where the frontier model earns its cost; ingestion doesn't need it. See [[wiki/techniques/model-routing-for-ingest|model routing for ingest]].
- **[05:10-05:25]** The pattern comes from Karpathy's gist on personal LLM knowledge bases: index sources, let an LLM build the base, use Obsidian as the front end. See [[wiki/tools/obsidian|Obsidian]].
- **[08:20-08:45]** Structure isn't fixed up front; it emerges per data type. His meeting-transcript wiki stayed flat, while his YouTube wiki grew subfolders (concepts, sources, tools, techniques). Flat is sometimes better because it is easier for the AI to search. See [[wiki/concepts/flat-vs-foldered-wiki-structure|flat vs foldered wiki structure]].
- **[09:49-11:23]** Ingest demo: drop a PDF in `raw/` or paste a URL, give one instruction, and the AI creates as many cross-linked pages as the source warrants (his run: 2 sources became 20 pages). See [[wiki/techniques/wiki-ingest-workflow|wiki ingest workflow]].
- **[11:24-11:53]** The payoff of a wiki over separate summaries: two independently ingested sources referenced each other (OpenAI's GPT-5.6 Soul system card benchmarked against Anthropic's Mythos Preview), and the connection surfaced as a shared page only because both lived in one wiki. Reading them separately, he would have missed it. See [[wiki/concepts/cross-source-connections|cross-source connections]].
- **[12:58-13:16]** CLAUDE.md acts as a router, so agents find the right wiki content without spending tokens crawling everything. See [[wiki/concepts/claude-md-as-router|CLAUDE.md as router]].
- **[14:04-14:16]** Because the wiki is markdown files plus routing rules, it isn't locked to one agent: Claude Code, Codex or any other harness can use it. See [[wiki/concepts/markdown-portability|markdown portability]].

## In this system

This vault's `wiki/` folder follows the pattern, and `/ingest` runs it: raw copy in, small linked pages out, index and log updated.
