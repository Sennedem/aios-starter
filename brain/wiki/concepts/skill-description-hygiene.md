---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, skills, description, routing]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/techniques/skill-description-audit]]"]
---

# Skill description hygiene

Because [[wiki/concepts/progressive-disclosure|progressive disclosure]] routes purely on a skill's description text, the description is the dispatch mechanism. It does more than document the skill. Three rules, per Nate Herk relaying Barry Zhang and Mahesh Murag [04:04-04:25]:

1. **One job per skill.** Two overlapping descriptions ("help with content" and "create marketing assets") leave Claude guessing which one applies to a request.
2. **Use the words a real person would use**, not internal jargon. For example: "Use this when the user asks for a carousel, carousel slides, or a LinkedIn document post," instead of an abstract capability statement.
3. **No two skills competing for the same request.** If descriptions overlap, routing becomes ambiguous by construction, and better luck won't fix it.

The stated consequence: **"a skill that Claude can't find is basically a skill that you don't have."** [04:44-04:48] A skill with perfect instructions and a vague description is functionally absent, because it never gets selected.

## Related

- [[wiki/techniques/skill-description-audit|Skill description audit]] is the method for checking a whole set of skills against these rules.
- [[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk on REA]] is about what goes inside a skill (built from analyzed examples). The description rules here still decide whether that skill is ever found.

## In this system

`.claude/rules/common/skills.md` has the three-prompt test for any new or edited description. `/audit` checks the whole skill set for collisions.
