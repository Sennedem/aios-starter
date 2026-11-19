---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, skills, anthropic, audit]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/skill-description-hygiene]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/techniques/refactor-skills-for-newer-models]]"]
---

# Skill description audit

A runnable prompt for finding ambiguous or overlapping skill descriptions across a whole skill set, from Nate Herk relaying Anthropic's Barry Zhang and Mahesh Murag in [[wiki/sources/nateherk-build-skills-not-agents|Build skills, not agents]] **[04:26-04:36]**:

> "Review all my skill descriptions. For each one, tell me what it does, when it should trigger, and where it overlaps with any other skills. Rewrite only descriptions that are ambiguous."

Then validate each description, rewritten or not, with **three test prompts** **[04:36-04:48]**:

1. An **obvious** request that should trigger it.
2. A **differently worded** request that should still trigger it.
3. An **unrelated** request that definitely should not trigger it.

A skill that fails test 1 or 2 has a description that is too narrow or full of jargon (see [[wiki/concepts/skill-description-hygiene|Skill description hygiene]]). A skill that fails test 3 is competing with another skill for requests it should not own.

## What it is not

[[wiki/techniques/refactor-skills-for-newer-models|Refactor skills for newer models]] targets over-prescriptive *body* content. This audit targets the *description* line, which is the routing key under [[wiki/concepts/progressive-disclosure|progressive disclosure]]: Claude sees only the name and description until one matches, so a skill it cannot find is a skill you do not have. The two audits fit in one pass.

## In this system

`.claude/rules/common/skills.md` holds the three-prompt test, and `/audit` checks every description for collisions on each run.
