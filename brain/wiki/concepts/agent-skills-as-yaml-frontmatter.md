---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [skills, yaml, portability]
related: ["[[wiki/concepts/markdown-portability]]", "[[wiki/tools/hermes-agent]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/claude-code-mods]]"]
---

# Agent skills as YAML frontmatter

A skill, in both Claude Code's and Hermes's sense, is portable because it is just a markdown file: a YAML frontmatter block that declares its name and when to use it, then instructions in the body. Nate Herk shows this in [[wiki/sources/nateherk-managed-hermes-setup|his managed Hermes setup video]] [08:26-09:06]. He opens an Excalidraw-diagram skill from his Claude Code skills folder, copies the whole file, pastes it into Hermes's "add a skill" form (name, category, the pasted frontmatter), and it works there with no format translation and no rewrite. He repeats the same move later with his `grill-me` skill [12:58-13:08].

## Why it ports

The frontmatter (`name` plus `description`, the trigger) is the only part a harness needs to discover the skill. The body is plain instructions any capable model can follow. Claude Code skills use the same shape: a `SKILL.md` per skill folder with `name` and `description` frontmatter, then the instructions.

This is [[wiki/concepts/markdown-portability|markdown portability]] one layer up. That page covers the knowledge base being portable because it is "just markdown files plus routing rules"; here the skills themselves are markdown plus a routing header (YAML frontmatter in place of a CLAUDE.md router table), which is why a skill can be lifted from one harness into another unmodified.

## The frontmatter is also a filter

[[wiki/sources/nateherk-build-skills-not-agents|A separate Nate Herk video]] on Anthropic's Agent Skills adds why the frontmatter exists functionally, beyond copy-paste: the `name` and `description` pair is what [[wiki/concepts/progressive-disclosure|progressive disclosure]] reads before deciding whether to load the rest of the skill at all. A vague description means the skill never loads.

## More data points

- The [[wiki/tools/rea-reverse-engineer-anything|REA skill]] ships in the same `.agents/skills/<name>/SKILL.md` layout and, per its repo, works across Claude Code, Codex, Cursor and Gemini CLI ([[wiki/sources/nateherk-reverse-engineer-anything-skill|source]]).
- [[wiki/sources/nateherk-claude-code-mods|Nate Herk on Claude Code mods]] names the layer skills cannot reach: skills are instructions the model reads, [[wiki/concepts/claude-code-mods|mods]] are runtime code and UI. Both ship through plugins.

## In this system

`.claude/rules/common/skills.md` covers how to write a description that actually triggers. `/audit` checks the skill descriptions for collisions.
