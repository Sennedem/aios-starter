---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, skills, agent-skills, architecture]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/smallest-sufficient-context]]", "[[wiki/tools/rea-reverse-engineer-anything]]"]
---

# Skills as apps, model as processor

Nate Herk's framing of what he says Anthropic's Barry Zhang and Mahesh Murag described: stop building a separate agent for every job. The underlying agent (Claude Code, or any general-purpose harness) became more capable than expected on its own. It can already read files, write code, call tools and work through a task, so the job-specific part needs a **skill** layered on top, and no new agent [00:23-01:03].

The phone analogy (Nate's own explanation, not an Anthropic quote): a phone has a processor and an operating system built by a few large vendors that you don't rebuild yourself, and then apps that each give the same hardware one specific capability. Model = processor, agent runtime = operating system, skill = app. A skill packages "the process, the context, the scripts, and the examples" for one job onto a general-purpose agent [00:59-01:23].

## Why it matters

It turns "which agent should I build for X" into "which skill does the general-purpose agent need for X". The agent stays constant and only the skill changes. Everything else in the source rests on this: [[wiki/concepts/progressive-disclosure|progressive disclosure]] only makes sense if skills are light, swappable modules on a shared runtime.

## The counterweight

[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk, 10x Claude Code]] relays Anthropic's advice that skills should be "lightweight guides", not over-constrained "except in highly important areas". Skills written for older models can now box in the processor. See [[wiki/concepts/smallest-sufficient-context|Smallest sufficient context]].

## Related

- [[wiki/concepts/agent-skills-as-yaml-frontmatter|Agent skills as YAML frontmatter]] covers the portability half of the same claim, from a different Nate Herk video.
- [[wiki/tools/rea-reverse-engineer-anything|REA]] ([[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk's test]]) is a live example: a skill of about 560 lines plus an MCP plug-in layered onto a general agent. Nate's reported effect (slower but better builds) is from a single run, creator-observed.

## In this system

The whole system is built this way: one Claude Code session as the general agent, with each job as a skill in `.claude/skills/`.
