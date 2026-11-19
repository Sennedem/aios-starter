---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/HIRDzMtuWFk
tags: [wiki, source, youtube, skills, anthropic, agent-skills]
related: ["[[wiki/concepts/skills-as-apps-model-as-processor]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/skill-description-hygiene]]", "[[wiki/concepts/save-scripts-inside-skills]]", "[[wiki/concepts/corrections-into-durable-instructions]]", "[[wiki/concepts/persona-review-panel]]", "[[wiki/techniques/skill-description-audit]]", "[[wiki/techniques/verify-before-returning]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/concepts/parallelize-and-delegate]]", "[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/concepts/markdown-portability]]", "[[wiki/techniques/refactor-skills-for-newer-models]]", "[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/techniques/match-effort-to-the-task]]"]
---

# Nate Herk: "Anthropic Engineer Explains: What to Build Instead of AI Agents"

YouTube, 9:47, Nate Herk | AI Automation, published 2026-09-13: https://youtu.be/HIRDzMtuWFk. Nate relays what he says two Anthropic engineers who created Agent Skills, **Barry Zhang and Mahesh Murag**, described: they stopped building a separate agent per job, because the underlying agent runtime had become general-purpose enough that the job-specific part could live in a lighter layer. **[00:23-01:01]**

**Attribution note:** the core claim is presented as relayed from the two named engineers, but the video shows no verbatim doc quotes (unlike [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|"How Anthropic prompts Fable 5.1"]], which quotes the prompting docs directly). Everything below is Nate's synthesis of that conversation, mixed with worked examples from his own setup (a carousel-creation workflow, a grill-me skill); those are flagged as his own where they appear.

## The model

Model = processor, agent runtime = operating system, skills = apps. A few vendors build the processor and the OS; you choose and install the apps, and each app gives the same underlying agent one specific capability. **[00:36-01:03]** See [[wiki/concepts/skills-as-apps-model-as-processor|skills as apps, model as processor]].

## The four practical tricks

1. **Save scripts inside skills** instead of having Claude re-derive the same code every run. See [[wiki/concepts/save-scripts-inside-skills|save scripts inside skills]]. **[01:26-02:58]**
2. **Progressive disclosure** (name and description loaded first, the full SKILL.md only on a match) depends on **skill-description hygiene**: one job per skill, wording a real person would use, no overlap. See [[wiki/concepts/progressive-disclosure|progressive disclosure]], [[wiki/concepts/skill-description-hygiene|skill description hygiene]], and the audit in [[wiki/techniques/skill-description-audit|the description-audit prompt and 3-prompt test]]. **[03:02-04:48]**
3. **Turn corrections into durable instructions** instead of a one-off "fix it". See [[wiki/concepts/corrections-into-durable-instructions|corrections into durable instructions]]. **[04:54-06:43]**
4. **Verify before returning:** bake acceptance-criteria checks and, for subjective work, a [[wiki/concepts/persona-review-panel|persona review panel]] into the skill itself, so "your first look is the agent's fourth or fifth". See [[wiki/techniques/verify-before-returning|verify before returning]]. **[06:43-09:00]**

## What to check in your own setup

Three gaps this video tends to expose in a skills-first setup: no one has ever run the three-prompt description test across all skills; only one or two skills learn from corrections; and skills that generate reusable code have no `scripts/` folder to keep it in.

## Cross-source connections

Confirms or extends [[wiki/concepts/prove-its-work|prove its work]], [[wiki/concepts/parallelize-and-delegate|parallelize and delegate]] (the persona panel is delegation applied to subjective review), [[wiki/concepts/tell-it-what-done-looks-like|tell it what done looks like]] (skills as the durable version of "what done looks like"), [[wiki/concepts/agent-skills-as-yaml-frontmatter|agent skills as YAML frontmatter]] (the description as a filter, not only a label), [[wiki/concepts/markdown-portability|markdown portability]], [[wiki/techniques/refactor-skills-for-newer-models|refactor skills for newer models]] (over-prescriptive skill bodies vs under-specified descriptions: a different axis on the same file), [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]] (the persona panel is one implementation of a defined-good judge) and [[wiki/techniques/match-effort-to-the-task|match effort to the task]] (progressive disclosure is a token-budget mechanism next to effort level).

## In this system

`.claude/rules/common/skills.md` encodes tricks 1 to 3 (keep proven scripts, log corrections, the three-prompt description test), `/audit` checks descriptions for collisions, and `.claude/rules/common/verification.md` covers trick 4.
