---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, tool, web-design, scroll, skill, claude-code]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]", "[[wiki/concepts/ai-website-slop]]", "[[wiki/concepts/layering-for-premium-feel]]", "[[wiki/concepts/scroll-feedback]]", "[[wiki/techniques/screenshot-scroll-verification]]"]
---

# ScrollCraft

Nate Herk's own Claude skill and plugin for building Apple-style scroll-driven websites. Item 4 of [[wiki/sources/nateherk-6-best-github-repos-for-claude|his repo list]]; he discloses that he built it.

- **Repo:** https://github.com/nateherkai/scroll-craft. In [[wiki/sources/nateherk-fable-5-1-kills-website-slop|the earlier "Fable 5.1 kills website slop" video]] it was a free skill inside his community; it is now a public GitHub repo.
- **Install (per the README):** inside Claude Code, run the plugin command with `marketplace add nateherkai/scroll-craft`, then install the `nateherk-design` plugin and invoke its `scroll-craft` skill. Or start Claude with `claude --plugin-dir ./plugins/nateherk-design`.

## What Nate said (creator-claimed)

- **[03:08-04:17]** It gives Claude a real scroll engine plus his design rules (taste, depth, layering, spacing, typography, colour) and a built-in checker that screenshots the scroll and inspects element positions, so Claude fixes defects without being asked. Every site he builds uses it. Not every site needs to be super-immersive. His claim: a basic landing page is a commodity, while brands still pay designers for custom scroll experiences.
- The design logic is the same as the seven rules in the earlier video: [[wiki/concepts/layering-for-premium-feel|layering for premium feel]], [[wiki/concepts/scroll-feedback|scroll feedback]] and [[wiki/techniques/screenshot-scroll-verification|screenshot scroll verification]].

## Security note

A plugin installed from the creator's own marketplace can ship hooks and scripts that run with Claude Code's permissions. Read the plugin's hooks and checker script before enabling it; a skills-only copy is safer. The creator runs a commercial community, so treat "every site uses it" as marketing.

If you already use frontend design skills, the new piece here is the checker's frame-by-frame scroll capture.
