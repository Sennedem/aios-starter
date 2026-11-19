---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=oz2CwrPV2Rg
tags: [wiki, source, youtube, context-engineering, claude-code, skills, doctor, anthropic]
related: ["[[wiki/concepts/smallest-sufficient-context]]", "[[wiki/concepts/context-engineering-then-and-now]]", "[[wiki/techniques/claude-doctor-setup-audit]]", "[[wiki/techniques/read-only-workflow-audit-prompt]]", "[[wiki/techniques/refactor-skills-for-newer-models]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/skills-as-apps-model-as-processor]]", "[[wiki/concepts/tell-it-what-done-looks-like]]", "[[wiki/concepts/claude-md-as-router]]", "[[wiki/techniques/skill-description-audit]]"]
---

# Nate Herk: "Anthropic Engineers Just 10x'd Everyone's Claude Code"

YouTube, 12.4 min, Nate Herk | AI Automation, published 2026-10-08: https://www.youtube.com/watch?v=oz2CwrPV2Rg. Sponsor read at 03:31 (HyperAgent); community plug at 09:27.

## What the "10x" actually is

Not a release. It is an Anthropic engineering blog post, **"The new rules of context engineering for Claude 5 generation models"** by Thariq Shihipar (member of technical staff), published **2026-07-24** on claude.com, plus the `/doctor` command (`claude doctor`) that ships its advice. Checked against the post itself (claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models). The post says "over 80%" of Claude Code's system prompt was removed "for models like Claude Opus 5 and Claude Fable 5 with no measurable loss on our coding evaluations." The "10x" in the title is clickbait: the post claims no speed or quality multiple, only no regression at a fraction of the prompt. Nate says the post also covers 5.1; the post text names Opus 5 and Fable 5 only.

## Claims, graded

| Claim | Timestamp | Grade |
|---|---|---|
| Over 80% of Claude Code's system prompt removed, no measurable eval loss | 00:24-00:40 | **Anthropic-stated** (post, verified) |
| The old "default to no comments" rule replaced by "match the surrounding code's comment density, naming, idiom" | 01:15-01:24 | **Anthropic-stated** (the post quotes both prompts) |
| Use the smallest context that gets the result; minimal is not the same as short | 02:11-02:28 | Anthropic applied-AI guidance as relayed; the "minimal is not short" line is not in the post, so **creator-relayed** |
| A 2025 paper: five models, performance drops with longer input, by 13.9% to 85% | 02:32-02:46 | **Creator-cited, not checked.** Nate himself says it is old, with different models and controlled experiments |
| Loading MCP tool definitions on demand: 85% fewer tokens; MCP evals 49% to 74% (Opus 4), 79.5% to 88.1% (Opus 4.5) | 02:57-03:13 | **Creator-cited, not in this post.** Appears to come from an earlier Anthropic tool-search write-up; not re-verified |
| Boris Cherny: "every 6 months you should delete all of your skills" | 01:01-01:05 | **Unverified hearsay**, no source shown |
| `/doctor` audits skills (usage counts, token cost of the listing), memory files, duplicated instructions, broken skills, plugins and settings | 07:04-09:25 | **Creator-observed on his own setup**; the post confirms `/doctor` carries the best practices but does not describe this report format |
| A fresh run (no skills, no CLAUDE.md) gave better content structure than his full AI OS setup; the full-setup run was prettier | 04:23-05:00 | **Creator-observed, n=1**, not an eval |
| Audit of his YouTube workflow: 25 video folders with a script, only 3 with a `sources.md`; 3 edits suggested | 10:01-10:48 | **Creator-observed**; the 3 edits were not shown |

## Takeaways

1. The principle: rules written for weaker models become constraints on stronger ones, and conflicting rules across the system prompt, skills and CLAUDE.md make the model deliberate over contradictions. See [[wiki/concepts/context-engineering-then-and-now|context engineering: then and now]]. **[00:24-01:27]**
2. Use the smallest sufficient context, with the caveat that needed detail stays. See [[wiki/concepts/smallest-sufficient-context|smallest sufficient context]]. **[02:11-03:20]**
3. What to keep when pruning a skill: intent and why, voice, goals, audience and business facts (what Claude cannot infer). Cut what it can look up (folder listings), duplicate copies, and procedures that apply to one task only (load those on demand). CLAUDE.md stays a starting point: what the project is for, gotchas and landmines, and pointers to deeper files. **[05:58-06:57]**
4. `/doctor` as the audit tool: [[wiki/techniques/claude-doctor-setup-audit|Claude doctor setup audit]]. **[07:04-09:25]**
5. A read-only audit prompt for a workflow's handoffs: [[wiki/techniques/read-only-workflow-audit-prompt|read-only workflow audit prompt]]. **[09:43-10:52]**
6. Cadence: run the audit monthly if the setup churns, quarterly if it is stable, and every time a new model drops. Once you trust it, schedule it as a local task in the Claude desktop app and wake up to approve or deny the recommendations. His closing frame: a "self-improving, self-cleaning" AI OS fixes human inconsistency (forgotten updates, duplicates, stale entries). **[10:54-12:00]**

## Skeptic note

- The video re-wraps a free, 7-minute Anthropic post with a hot title. Read the post for the rules; use the video only for the `/doctor` screenshots.
- The one real experiment (full setup vs fresh) is a single run judged by eye. It supports "my skill was over-constraining", not "delete your skills." The honest conclusion he reaches himself: keep branding and format in a skill, give intent, and leave structure to the model.
- Nate puts Boris's "delete every 6 months" next to the post's own "avoid overconstraining, **except in highly important areas**". Those exceptions are what a recipe or rule written after a known failure is for; do not read this as licence to strip load-bearing rules.
- Gaps between post and video: the post says move verification and review into on-demand skills and use deferred tool loading. Nate's "delete 80% of your instructions" framing is stronger than anything the post claims for user setups, where it says "you may need to simplify."

## Cross-source connections

Extends [[wiki/techniques/refactor-skills-for-newer-models|refactor skills for newer models]] (the same claim, now with the primary source and a tool), [[wiki/concepts/progressive-disclosure|progressive disclosure]] (Anthropic now applies it to tools and CLAUDE.md too), [[wiki/concepts/skills-as-apps-model-as-processor|skills as apps]], [[wiki/concepts/tell-it-what-done-looks-like|tell it what done looks like]] (the same "outcome, why and constraints, then get out of the way" Nate repeats at 01:43-01:56), [[wiki/concepts/claude-md-as-router|CLAUDE.md as router]] and [[wiki/techniques/skill-description-audit|skill description audit]].

## In this system

`/audit` checks skill descriptions for collisions, and `.claude/rules/common/skills.md` holds the rules for what a skill keeps. Run `/doctor` after a model change, as the video suggests.
