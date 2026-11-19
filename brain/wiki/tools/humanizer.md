---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, tool, writing, skill, ai-tells, claude-code]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]"]
---

# Humanizer (blader/humanizer)

An agent skill that rewrites AI-sounding text without changing what it says, built on Wikipedia's "Signs of AI writing" guide. Item 5 of [[wiki/sources/nateherk-6-best-github-repos-for-claude|Nate Herk's repo list]].

- **Repo:** https://github.com/blader/humanizer (MIT), by Siqi Chen (@blader), who says he had Claude Code read the Wikipedia article and write the skill. A Medium write-up claims about 50,000 installs and a 25-pattern list (secondary, unverified). Several clones exist (Aboudjem/humanizer-skill, marmbiz/humanizer-de and others). Nate did not name the author, so blader's repo being the one he means is likely but not proven.
- **Install (per the README):** on Claude Code 2.1.142 or later, run the plugin command with `marketplace add blader/humanizer`, then `install humanizer@humanizer`. On older versions or other agents: `npx skills add blader/humanizer --global [--agent claude-code|codex]`. Then ask it to humanize a piece of text.

## What Nate said (creator-claimed)

- **[04:19-04:57]** He found it "almost by accident" and has used it on every product since. It knows the tells: "not this, but that" constructions, tee-up setups, groups of three, hype words. Paste website copy or a cold email and ask it to humanize: it keeps the message and drops what makes people scroll away or lose trust.

## Security note

A single Markdown skill: low risk, no scripts in the README as seen. The plugin path adds a marketplace entry, so the safer route is to read the one `SKILL.md` and copy it. Not an MCP.

A generic de-slop pass can fight a writing skill tuned to one person's voice. Run it as the last pass, after the voice rules, and let your own samples and corrections win where they disagree.

## In this system

The `/writing` skill ships this catalogue (vendored from blader/humanizer v4.0.0, MIT) at `.claude/skills/writing/references/humanizer.md` and runs it as the last pass on every draft. `.claude/rules/common/writing.md` applies the same pass to all prose Claude writes in the repo.
