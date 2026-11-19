---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=9hetShMMp2s
tags: [wiki, source, youtube, claude-code, mods, plugins]
related: ["[[wiki/concepts/claude-code-mods]]", "[[wiki/techniques/mod-next-steps-toast]]", "[[wiki/techniques/mod-cache-keeper]]", "[[wiki/techniques/mod-recording-mode]]", "[[wiki/techniques/mod-goal-tracker]]", "[[wiki/techniques/mod-collision-guard]]"]
---

# Nate Herk: "Claude Code Mods Are Game Changers. Set Up These 5 NOW."

YouTube, 11.3 min, Nate Herk | AI Automation, published 2026-10-02: https://www.youtube.com/watch?v=9hetShMMp2s.

## What it is

A tour of five mods Nate built or installed after Anthropic launched mods (official post 2026-10-01). The demos run in the Code tab of the Claude desktop app.

## Takeaways

1. **What mods are** [01:55-02:10]: plugins with a bit of code, installed through the plugin command in the CLI or the desktop app, and creatable in plain language. Verified against Anthropic's announcement: TypeScript functions shipped in plugins, unsandboxed. See [[wiki/concepts/claude-code-mods|Claude Code mods]].
2. **Method** [02:11-02:40]: Nate had Claude mine his session logs for repeated phrases and tasks and suggest the top five mods. The idea is reusable; the result is creator-claimed.
3. **The five** (one technique page each):
   - [[wiki/techniques/mod-next-steps-toast|Next steps]] [00:34-01:20, setup 01:43]
   - [[wiki/techniques/mod-cache-keeper|Cache keeper]] [02:56-04:55]
   - [[wiki/techniques/mod-recording-mode|Recording mode]] [05:21-07:20]
   - [[wiki/techniques/mod-goal-tracker|Goal tracker]] [07:22-09:10]
   - [[wiki/techniques/mod-collision-guard|Collision guard]] [09:13-10:32]
4. **Official examples** [00:15-00:33]: token weather (how full the context is), blast radius (preview what a delete would remove), replay theater (step through edits as diffs). Shown from the release tweet; not built in the video.
5. **Distribution** [10:36-10:56]: all five sit behind his free community ("all YouTube resources"). The alternative is to give the transcript to an agent and describe what you want [10:56-11:06].

## Grading

| Claim | Grade |
|---|---|
| Mods ship in plugins and work in the CLI and the desktop app | Anthropic-stated, verified |
| Claude can write and install a mod from natural language | Anthropic-stated |
| The prompt cache expires after 60 idle minutes | Creator-stated, unverified |
| Mods differ from hooks (they can draw UI and ask a question instead of only blocking) | Anthropic-stated |
| Each mod "works" | Shown on screen once each, no stress test |
| Recording mode keeps secrets safe | Not tested; it only blurs the display |

## Skeptic note

Mostly demo and no code shown, so nobody can follow setup steps from the video. The real steps are "paste the link to Claude" or join a mailing list and community funnel (the free community plus an SOP lead magnet at [04:57-05:27]). He admits next steps and the handoff button save little time, and that the collision guard could be a skill or a CLAUDE.md line. Mods are unsandboxed code on your machine; "paste this into Claude and say set it up" skips the review step Anthropic itself warns about. Some of the "mods" are prompt behaviour with a coat of UI.

## In this system

`scripts/hooks/collision-guard.mjs` covers the same ground as the collision-guard mod, as a hook instead of a mod.
