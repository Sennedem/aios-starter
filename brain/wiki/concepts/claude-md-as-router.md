---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [claude-code, routing, claude-md]
related: ["[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]", "[[wiki/concepts/llm-wiki-pattern]]", "[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code]]", "[[wiki/techniques/claude-doctor-setup-audit]]"]
---

# CLAUDE.md as router

In this pattern a CLAUDE.md file holds routing rules, not the knowledge itself, so an agent can work out where to look for a specific piece of data without crawling the entire wiki and burning tokens on it. [12:58-13:16]

Nate Herk frames it directly in [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|his Karpathy LLM-wiki video]]: "how can my CLAUDE.md work as a router to be able to look through my past projects, to be able to look through my business context, and find the right spot." The wiki holds the content; CLAUDE.md holds the map. A "where to find things" table (you need X, go to Y) is a router table in exactly this sense, and a wiki index extends the same routing one level deeper.

## Anthropic backs the light router

Anthropic's post on context engineering (via [[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk, 10x Claude Code]]) supports the idea: keep CLAUDE.md light, with what the repo is for, the gotchas, and pointers to deeper skills and files, and drop anything Claude can learn from the file system. Claude Code's doctor command reports duplicated sections and stray CLAUDE.md files that load from other folders; see [[wiki/techniques/claude-doctor-setup-audit|Claude doctor setup audit]].

## In this system

The root `CLAUDE.md` is a router: it points at the rules, registries, skills, other places and the brain, and holds no knowledge itself. `brain/README.md` is the next routing level.
