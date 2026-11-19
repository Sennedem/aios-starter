---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, claude-code, mods, plugins, hooks, ui]
related: ["[[wiki/sources/nateherk-claude-code-mods]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/prompt-cache-read-economics]]"]
---

# Claude Code mods

A **mod** is a small TypeScript function that hooks into one of Claude Code's events and can run before, after, instead of, or around it. Mods ship inside **plugins** (installed through Claude Code's plugin command) and work in the CLI and the desktop app. **Anthropic-stated** (launch post, 2026-10-01, at claude.com/blog/claude-code-mods).

## What separates a mod from a hook, a skill, a CLAUDE.md line

| Mechanism | Can do | Cannot do |
|---|---|---|
| CLAUDE.md or skill | Change what the model is told or knows | Run code, draw anything, block a call |
| Hook (settings.json) | Run a command on an event; PreToolUse can block | Rewrite events, draw UI, replace a built-in |
| **Mod** | Everything a hook does, plus rewrite prompts, retry or rewrite tool calls, approve or deny permissions, redact tool output, draw panes, bands, buttons and inputs, replace built-ins | Anything safely: mods are **not sandboxed** and run with the same machine access as Claude Code |

Anthropic's own framing: hooks "can't rewrite events, draw new UI, or replace features. Mods can." The built-in diff command is now itself a mod. Several mods on one event run in load order. Team and Enterprise plans get a `sec-default` mod that stops user mods overriding permission deny rules. (All Anthropic-stated.)

## The five Nate Herk mods

Demonstrated in [[wiki/sources/nateherk-claude-code-mods|the source video]]; each has a technique page:

1. [[wiki/techniques/mod-next-steps-toast|Next steps]]: a per-turn "what now" popup.
2. [[wiki/techniques/mod-cache-keeper|Cache keeper]]: a cache countdown plus a handoff button.
3. [[wiki/techniques/mod-recording-mode|Recording mode]]: blurs or replaces sensitive text on screen.
4. [[wiki/techniques/mod-goal-tracker|Goal tracker]]: a progress pane for long goal runs.
5. [[wiki/techniques/mod-collision-guard|Collision guard]]: asks before editing a file another chat just touched.

## How to make one

Creator-claimed: ask Claude Code in plain language ("build me a mod for X"), then ask how to turn it on and off. Anthropic confirms Claude "can write the TypeScript, install it, and hot reload it in your session." Because mods are unsandboxed code, read what it wrote before enabling it. `claude plugin validate` is the vendor-recommended check for third-party mods (secondary source, unverified).

## Cross-source notes

- Extends [[wiki/concepts/agent-skills-as-yaml-frontmatter|skills as frontmatter]]: skills are the knowledge and instruction layer, mods the runtime and UI layer; both distribute through plugins.
- The cache keeper's countdown applies [[wiki/concepts/prompt-cache-read-economics|cache-read economics]] to your own session: an idle cache costs a full re-read.

## In this system

`scripts/hooks/collision-guard.mjs` does the collision-guard job as a plain hook, without a mod.
