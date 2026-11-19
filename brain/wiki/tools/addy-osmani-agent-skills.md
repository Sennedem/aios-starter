---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: coding
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, tool, skills, spec-driven, claude-code]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/concepts/skill-description-hygiene]]", "[[wiki/concepts/stateless-wakeup-handoff-log]]"]
---

# Agent Skills (Addy Osmani)

A set of about 25 engineering-workflow skills, one command per phase of a build. Item 6 of [[wiki/sources/nateherk-6-best-github-repos-for-claude|Nate Herk's repo list]].

- **Repo:** https://github.com/addyosmani/agent-skills (MIT; site skills.addy.ie). The README says 25 skills (the site snippet says 24). Commands seen: spec, plan, build, test, review, webperf, code-simplify and ship. Nate states Osmani spent 14 years at Google and now works on Claude Code at Anthropic (creator-claimed, not checked).
- **Install (per the README):** `npx skills add addyosmani/agent-skills`; or, inside Claude Code, the plugin command with `marketplace add addyosmani/agent-skills` and then `install agent-skills@addy-agent-skills`; or clone the repo and start Claude with `claude --plugin-dir`.

## What Nate said (creator-claimed)

- **[05:02-06:24]** It fixes "context rot" after an hour or two of building by moving the plan out of the chat and into files. The spec command writes a spec with you, plan splits it into small tasks, and build works through them one at a time with a check on each. A fresh session can resume from the files. The spec interview surfaces edge cases you would not raise yourself (double bookings, refunds, time zones) and doubles as a client hand-over before building. Easier for newcomers than Superpowers, which he calls "still really good". Matt Pocock's skills are named as a bonus.

## Security note

These are Markdown skills from a well-known individual, but the plugin route can include hooks, so read `hooks/` before installing it as a plugin. It overlaps heavily with Superpowers and with plan mode: installing two spec-and-plan systems side by side risks competing triggers (see [[wiki/concepts/skill-description-hygiene]]).

The durable idea, keeping state in files instead of chat so a fresh session can pick up, is the same one behind [[wiki/concepts/stateless-wakeup-handoff-log|the stateless wake-up and handoff log]].
