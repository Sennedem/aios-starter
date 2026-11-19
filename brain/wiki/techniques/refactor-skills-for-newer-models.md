---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FBVNS1l5Vb8
tags: [wiki, technique, prompting, skills, prompt-audit]
related: ["[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/techniques/skill-description-audit]]", "[[wiki/techniques/claude-doctor-setup-audit]]", "[[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1]]", "[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code]]", "[[wiki/sources/nateherk-build-skills-not-agents]]"]
---

# Refactor skills for newer models

Skills and prompts written for older models are often over-specified for Fable 5 and 5.1, and the over-specification actively hurts. From [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|How Anthropic prompts Fable 5.1]], quoting the docs:

> "Skills developed for prior models are often too prescriptive for Claude Fable 5 and Fable 5.1." **[02:44-02:48]**

Nate Herk's gloss: a skill that spells out "do this, this, this, this, this" in detail, the way skills were traditionally taught, can get in the newer model's way. It puts guardrails on a model that no longer needs them and makes it *less* efficient. **[02:48-03:02]**

## The concrete action: run a prompt audit

He cites a tweet from Peter Yang: run the prompt-audit command of the `claude-api` skill on your skills. It surfaces redundancies and rules that can be removed for the latest models. **[03:08-03:21]**

The primary source for the claim is Anthropic's own post (Thariq Shihipar, 2026-07-24): more than 80% of Claude Code's system prompt was removed for Opus 5 and Fable 5 with no measurable eval loss. The tool that post points to is `/doctor`. See [[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk, 10x Claude Code]] and [[wiki/techniques/claude-doctor-setup-audit|Claude doctor setup audit]].

## Two kinds of over-specification

A recipe can be right to be authoritative about its domain content (an agent should not invent a replacement rule) and still carry stale, over-detailed mechanical steps a newer model does not need spelled out. A prompt audit finds the second kind without weakening the first. Skill sets built up over several model generations without a re-audit are the most exposed.

This audit targets over-prescriptive *body* content. [[wiki/techniques/skill-description-audit|Skill description audit]] (from [[wiki/sources/nateherk-build-skills-not-agents|Build skills, not agents]]) targets the *description* line, which decides whether the skill gets picked at all. The two fit in the same pass.

## In this system

`.claude/rules/common/skills.md` covers how skills get patched after a correction, and `/audit` checks descriptions for collisions.
