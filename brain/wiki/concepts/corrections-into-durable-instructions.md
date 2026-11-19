---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, skills, anthropic, continuous-learning]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/save-scripts-inside-skills]]", "[[wiki/techniques/verify-before-returning]]", "[[wiki/concepts/markdown-portability]]"]
---

# Corrections into durable instructions

If a correction ends with "fix it" and the chat is closed, the lesson is usually thrown away: the output improves once and the process stays broken. Anthropic's design intent for skills (per [[wiki/sources/nateherk-build-skills-not-agents|Nate Herk]], relaying Barry Zhang and Mahesh Murag) is that anything Claude writes down can be used efficiently by a future version of itself, provided the correction goes to the right durable place. **[04:56-05:35]**

Three destinations, by type of mistake: **[05:44-05:57]**

- Wrong process: edit `SKILL.md` directly.
- Missing voice, brand or examples: add a reference file.
- A repeated mistake: add an explicit rule that prevents it, not a vague reminder.

Then rerun the same task and verify the fix. A correction that is not re-tested is a guess. **[05:57-06:10]**

Nate's own habit, given as an example: when an agent says it cannot find a file he knows exists, he does not just hand it the path. He asks it to backtrack, show where it searched, explain why it missed the file, and update the routing so the next run starts in the right place. **[05:10-05:26]**

## The "model-proof" caveat

No skill can force a weaker model to perform like a stronger one; different models read the same skill differently. What ports is the process, not identical output, because Agent Skills are an open format usable across compatible harnesses (Claude Code, Codex, Hermes and others). The practical test: run an important skill on another compatible agent. If the result falls apart, look for hidden assumptions or model-specific instructions and tighten the skill. **[06:11-06:43]**

## Related

[[wiki/concepts/save-scripts-inside-skills|Save scripts inside skills]] is the code version of the same idea; this page is the process, voice and rule version. The portability side is on [[wiki/concepts/markdown-portability|Markdown portability]].

## In this system

`.claude/rules/common/skills.md` routes every correction to one of these places. `/writing` keeps a learnings file it updates from feedback, and `/second-opinion` runs the "try it on another model" test.
