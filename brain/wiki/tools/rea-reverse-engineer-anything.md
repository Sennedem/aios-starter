---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: coding
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=rL5tw6h78zo
tags: [wiki, tool, skills, reverse-engineering, claude-code, github]
related: ["[[wiki/sources/nateherk-reverse-engineer-anything-skill]]", "[[wiki/techniques/reverse-engineer-from-the-output]]", "[[wiki/concepts/seen-inferred-unknown]]"]
---

# REA: Reverse Engineer Anything

An open-source agent skill plus MCP server that lets a coding agent (Claude Code, Codex, Cursor, Gemini CLI) take apart an existing app, work out how one feature behaves, and rebuild it. Repo: `github.com/morluto/rea` (MIT; also `rea.tools` and the `rea-agents` npm package). Checked against the repo's `SKILL.md` and a third-party write-up (Lucija Tomšić, 2026-10-18). The repo warns that lookalike copies exist, so only the official sources count. Tested in [[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk's REA video]].

## What it is, in layers

| Layer | What | Source |
|---|---|---|
| Skill | A `SKILL.md` of about 560 lines in `.agents/skills/reverse-engineer-anything/`: a framework for decompile, understand, recreate | repo (read) |
| Plumbing | An MCP server and CLI connecting the agent to existing analysis tools (Ghidra, Hopper, IDA) for native binaries, plus web, Electron and Android inspection | third-party write-up; the tools underneath are old (Ghidra 2019, IDA 1990s) |
| Output | Findings tagged with evidence, confidence and limits, i.e. [[wiki/concepts/seen-inferred-unknown|seen / inferred / unknown]] | repo and Nate Herk |

## Claims vs what happened

| Claim | What Nate Herk's tests showed | Grade |
|---|---|---|
| "Software is done" (Matthew Berman post) | Nate calls it a half-joke; he cloned functionality, not UI or backend (his Loom clone stores locally and looks different) | hype, rejected |
| REA gives much better builds | Same prompt, two agents, one with REA: the one without finished first, the REA one was slower but "much better". A single run of his own, no scoring | creator-empirical, n=1 |
| It is a new idea | Nate: reverse-engineering the output is what he already did for Reels and skills; REA's value is a "practical, thought-through framework" | his verdict, plausible |
| Works for any app | Needs setup per app type; quality depends on the model doing the writing; the Loom analysis was over 1 GB, so a summary layer is mandatory | creator-observed |
| 192k stars, trending | Stated on screen at [13:27]; a later write-up says 299k+. Popularity is not evidence of quality | verified as popular only |

## Limits (stated by Nate, the repo or the write-up)

- Nate's best results were single **features** (Loom's camera bubble, Langfuse-style eval views), never a whole product. "Reverse engineer Loom" was too broad; "pick the features I like" worked. [07:36-07:55]
- Native-binary support is flagged experimental by the repo; the heavier tools (IDA, Hopper) need their own licences.
- Legal: stick to what you may lawfully inspect; never copy exact code or assets, and never sell a clone. Many licences forbid disassembly. Nate covers this briefly at [11:09-11:25].
- The model you use still sees what REA finds, even though the analysis runs locally.
- A viral claim of an Adobe clone is disputed; unverified either way.

## When you need it

Install it only if you actually take apart software. The transferable part is the method, [[wiki/techniques/reverse-engineer-from-the-output|reverse-engineer from the output]], which works with files, reports and videos you already have and needs no install.
