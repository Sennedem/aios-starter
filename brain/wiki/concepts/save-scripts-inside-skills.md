---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, skills, scripts, dry]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/skills-as-apps-model-as-processor]]", "[[wiki/concepts/corrections-into-durable-instructions]]", "[[wiki/techniques/reverse-engineer-from-the-output]]"]
---

# Save scripts inside skills

Anthropic's team, per Nate Herk, kept watching Claude write the same Python script from scratch every time it needed to style a slide deck. It burned tokens re-deriving code that already existed, and the result came out slightly different each time because the code was regenerated instead of reused. Their fix: have Claude save the proven script inside the skill's own folder, in their words **"a tool for its future self."** The next run executes the saved file instead of rewriting it [01:26-01:55].

This is the standard software **DRY principle** (don't repeat yourself) applied to an agent's own code generation [01:56-02:06]. Nate's own example: a carousel-creation skill that reuses the same renderers, templates and scripts on every run, so Claude's only job is the new content, "literally just changing the text" [02:08-02:24].

## The practical instruction

Tell the agent: *"Save the script you just used inside the skill's scripts folder. Update the SKILL.md so future runs execute that file instead of trying to rewrite it again. Then run the skill again and verify the result."*

Then test it. Run the same type of task twice, compare the important parts, and confirm the skill calls the saved file instead of quietly regenerating it. The surrounding AI output may still vary; the reused code shouldn't [02:26-02:52].

## Related

- [[wiki/concepts/corrections-into-durable-instructions|Corrections into durable instructions]] is the companion mechanism: process fixes go in SKILL.md, while this page is about code the skill has already proven works.
- [[wiki/techniques/reverse-engineer-from-the-output|Reverse-engineer from the output]] ([[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk on REA]]) adds the upstream half. A skill's content can come from analyzing proven outputs (30 best Reels, five good reports) instead of describing the job, and the result is then saved as the skill.
- [[wiki/concepts/skills-as-apps-model-as-processor|Skills as apps, model as processor]] explains why the skill is the right home for the script.

## In this system

`.claude/rules/common/skills.md`: a script that worked goes in the skill's `scripts/` folder, and SKILL.md points at it.
