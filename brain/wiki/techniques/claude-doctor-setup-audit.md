---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, claude-code, doctor, audit, skills, context-engineering]
related: ["[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code]]", "[[wiki/techniques/skill-description-audit]]", "[[wiki/techniques/refactor-skills-for-newer-models]]", "[[wiki/concepts/smallest-sufficient-context]]"]
---

# Claude doctor setup audit

Run `/doctor` (also `claude doctor`) inside Claude Code. Anthropic's post says the context-engineering best practices were put into it "to rightsize your skills, and CLAUDE.md files." **Anthropic-stated** (post, 2026-07-24). What the report contains below is **creator-observed** from Nate Herk's run on his own setup in a new session, **[07:04-09:25]**; the exact report layout may differ by version.

## What Nate's report listed

1. **Skills table:** each skill, where it is installed, recorded uses since installation, and the estimated token cost of its listing (the YAML frontmatter that loads up front, not the full body). Examples: one skill 111 tokens, another 103, both with zero uses. **[07:19-07:44]**
2. **Unused skills:** flagged 18 older skills with no recorded use and spared ones created a few days earlier (age-aware). Based on the last 50 sessions of that project plus lifetime counters (252 startups, 223 transcripts). **[07:44-08:02]**
3. **Duplication:** a project map repeating the routing map, and repeated sections on templates, references and archiving. About 2,250 characters of cuts, roughly 563 tokens saved. **[08:14-08:27]**
4. **Memory sources broken out:** project CLAUDE.md, user-wide instructions, the auto-memory index, and CLAUDE.local.md (an empty template, about 35 tokens). **[08:27-08:44]**
5. **Hidden loaders:** a CLAUDE.md from a separate project in another folder was also loading, roughly 2,000 tokens he did not know he paid for. **[08:50-09:05]**
6. **Broken skills:** two, one with a wrong file name and one with malformed frontmatter, so Claude never saw the description. It offered to fix them. **[09:06-09:20]**
7. **Settings:** installation, auto-update, auto mode, permissions, hooks. **[09:21-09:27]**

## How to use it (Nate's procedure)

- Read the list before accepting deletions. A skill used through another tool will show zero uses here. **[08:02-08:12]**
- Cadence: monthly if the setup churns, quarterly if it is stable, and on every model switch. **[10:54-11:13]**
- Once you trust it, run it as a local scheduled task in the Claude desktop app (it needs to see local files, so leave the app open) and approve or deny the recommendations the next morning. **[11:20-11:36]**

## Not shown in the video

The `/doctor` output format, any flags, and whether it works in the VS Code extension. Nothing here was run by this wiki, so treat the checklist above as what to look for, not as a spec.

## In this system

`/audit` covers the skill-description side of the same check, and `.claude/rules/common/skills.md` says what a good description must contain.
