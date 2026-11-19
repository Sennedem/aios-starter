---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [markdown, agent-agnostic, portability]
related: ["[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/concepts/corrections-into-durable-instructions]]", "[[wiki/tools/obsidian]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]"]
---

# Markdown portability

A wiki of this kind is plain markdown files plus routing rules, nothing more. [14:04-14:16] So the knowledge base is not locked into whichever agent built it: Claude Code, Codex or any other coding agent that can read files and follow a CLAUDE.md-style router can use the same wiki. Nate Herk's line in [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|his Karpathy LLM-wiki video]]: "everything in this wiki, it's just a markdown file... with routing... you're not locked down to using this only in Claude Code."

The corollary: the front end ([[wiki/tools/obsidian|Obsidian]], or a generated HTML view) is a convenience for humans, not a dependency for the agent doing the reading and writing. A knowledge base with no code and no binaries stays usable by whatever agent or harness comes next.

## One layer up: skills

[[wiki/sources/nateherk-managed-hermes-setup|A separate Nate Herk video]] shows the same portability for individual skills: a skill is markdown plus YAML frontmatter, so it can be copy-pasted from Claude Code into Hermes unmodified. See [[wiki/concepts/agent-skills-as-yaml-frontmatter|Agent skills as YAML frontmatter]].

## The caveat

[[wiki/sources/nateherk-build-skills-not-agents|A third Nate Herk video]] adds the "model-proof" limit: what ports is the process a skill encodes, not identical output across models and harnesses. Test an important skill on another compatible agent (Codex, Hermes) and tighten it if the result falls apart. See [[wiki/concepts/corrections-into-durable-instructions|Corrections into durable instructions]].
