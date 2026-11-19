---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, skills, context-management]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/skill-description-hygiene]]", "[[wiki/techniques/match-effort-to-the-task]]", "[[wiki/concepts/context-engineering-then-and-now]]", "[[wiki/concepts/smallest-sufficient-context]]"]
---

# Progressive disclosure

Anthropic's term, relayed by Nate Herk from Barry Zhang and Mahesh Murag, for how a skills-based agent avoids loading everything at once. Claude does not read the full instructions, examples and scripts of every installed skill at the start. It begins with each skill's **name and description** (the YAML frontmatter). Only when a prompt matches a description does it read the full `SKILL.md`, and larger reference files or scripts inside that skill's folder stay unread until the task needs them [03:18-03:41].

Nate's analogy: a mechanic owns hundreds of tools but doesn't dump every one on the bench before changing a tire. He identifies the job and grabs what it needs [03:04-03:17].

## Why it matters

It is a context-budget mechanism, named as the fix for **context rot**: loading irrelevant instructions from every skill would bloat and confuse the working context before the task even starts [03:41-03:53]. The mechanism is only as good as its filter, so the description text carries the weight. See [[wiki/concepts/skill-description-hygiene|Skill description hygiene]].

## Beyond skills

Anthropic's own context-engineering post (via [[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk, 10x Claude Code]]) applies the same idea more widely. Verification and code review moved out of Claude Code's system prompt into skills, some tools load only on demand (found through a tool search), and CLAUDE.md and SKILL.md files should form a tree of files loaded at the right time. See [[wiki/concepts/context-engineering-then-and-now|Context engineering then and now]] and [[wiki/concepts/smallest-sufficient-context|Smallest sufficient context]].

## Related

[[wiki/techniques/match-effort-to-the-task|Match effort to the task]] covers the adjacent token lever: how hard the model thinks, as opposed to what gets loaded.

## In this system

Every skill in `.claude/skills/` follows this shape: frontmatter loaded up front, the body read on a match, `scripts/` and `references/` deeper still. `.claude/rules/common/skills.md` covers how to write the description.
