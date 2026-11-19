---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, context-engineering, claude-code, anthropic]
related: ["[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/smallest-sufficient-context]]", "[[wiki/techniques/refactor-skills-for-newer-models]]"]
---

# Context engineering: then and now

Six older best practices that Anthropic's Claude Code team (Thariq Shihipar, post dated 2026-07-24) calls myths for Claude 5-generation models (Opus 5, Fable 5). Source: the Anthropic post itself. Nate Herk's video ([[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|source page]]) covers only the first and third in any depth.

| Then | Now | Anthropic's example |
|---|---|---|
| Give Claude rules | Let Claude use judgement | Old system prompt: "default to writing no comments... one short line max." New: "Write code that reads like the surrounding code: match its comment density, naming, and idiom." |
| Give Claude examples | Design interfaces | The TodoWrite tool description went from about 9,100 characters of when-to-use lists and examples to one line plus a status enum (`pending`, `in_progress`, `completed`) and one rule: one task `in_progress` at a time. Examples "constrain them to a certain exploration space." |
| Put it all upfront | Progressive disclosure | Verification and code review moved out of the system prompt into skills; some tools load on demand (found via ToolSearch before use). Advice for your CLAUDE.md and SKILL.md: a tree of files loaded at the right time. |
| Repeat yourself | Simple tool descriptions | Delete the duplicate mention in the system prompt; the instruction lives once, in the tool description. |
| Memory in CLAUDE.md (`#` hotkey) | Auto-memory | Claude saves relevant memories itself. |
| Simple specs | Rich references | HTML artifacts, a test suite as the spec, a function to port, rubrics for verifier agents. Prefer files in code over prose or screenshots (an HTML mockup beats a description or a screenshot). |

## Why rules go bad

Rules were insurance against worst cases on weaker models. Spread across a system prompt, skills and user requests, they start to conflict ("leave documentation as appropriate" vs "DO NOT add comments"), and the model has to reason about the clash before acting. Deleting them lets it use the surrounding context. Nate's version: you add a rule after a mistake, a variant of it ends up in CLAUDE.md and in a skill, and the next model upgrade makes it unnecessary while it stays in. **[01:25-01:40 in the video]**

## Layer guidance from the post

- **System prompt:** product context. You will not change it in Claude Code, but spend your time here if you build your own harness.
- **CLAUDE.md:** light. What the repo is for, then gotchas ("types live in one monolithic file"). Skip anything Claude learns from the file system; point to skills for verification and the like.
- **Skills:** lightweight guides. Do not over-constrain "except in highly important areas"; split long ones into many files; encode opinions and knowledge specific to you.
- **References:** @-mention files; references in code form are preferred.

## Applying it to a grown setup

Rows 3 and 4 are the usual risk once a setup has grown: a router CLAUDE.md that restates descriptions already in each skill, and generic rule files loaded every session for work that does not need them. Row 1 can clash with rules you keep on purpose (for example "an authored recipe outranks a brief"); [[wiki/techniques/refactor-skills-for-newer-models|Refactor skills for newer models]] shows how both can hold.

## Caveat

Anthropic's evidence is internal coding evals for its own system prompt, not a claim about any user's CLAUDE.md. The post says "you may need to simplify just like we did", not that you will see the same gain.
