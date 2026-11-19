---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=gQef3d3erOs
tags: [wiki, tool, hermes, agents, harness]
related: ["[[wiki/tools/hostinger-managed-agents]]", "[[wiki/concepts/telegram-as-agent-channel]]", "[[wiki/concepts/managed-vs-vps-agent-hosting]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/concepts/subscription-oauth-vs-api-key-auth]]", "[[wiki/tools/grokbot]]", "[[wiki/tools/trigger-dev]]", "[[wiki/tools/codex-scheduled-tasks]]", "[[wiki/sources/nateherk-managed-hermes-setup]]"]
---

# Hermes agent

Hermes is an agent **harness**: a wrapper around an underlying model (Claude, GPT, Gemini and others) that adds a standing runtime with a persistent chat thread, scheduled tasks, a kanban of what sub-agents are doing, a skills library and a memory layer (user profile, "agent soul", project context). [03:41-03:44] [07:56-08:20] It is reachable through more than one surface at once: a hosted web chat and a Telegram bot both read and write the same thread, so a message sent in one shows up in the other. See [[wiki/concepts/telegram-as-agent-channel|Telegram as an agent channel]]. Source: [[wiki/sources/nateherk-managed-hermes-setup|Nate Herk's managed Hermes setup video]].

It can be deployed two ways: as a managed app on a platform like Hostinger (see [[wiki/tools/hostinger-managed-agents|Hostinger managed agents]]), or self-hosted on a VPS with full root access. The tradeoff is on [[wiki/concepts/managed-vs-vps-agent-hosting|managed vs VPS agent hosting]].

## What the web panel exposes

- **Tasks:** scheduled jobs, comparable to routines in Claude or Codex.
- **Kanban:** what the agent or its sub-agents are working on, and where each item stands.
- **Skills:** prebuilt toggles (Claude Code, Codex, computer use, creative, email, GitHub, media) plus a raw add-a-skill form: name, category, and the skill's YAML frontmatter pasted in. See [[wiki/concepts/agent-skills-as-yaml-frontmatter|agent skills as YAML frontmatter]].
- **Memory:** notes, a user profile, an "agent soul" and project context, organized into "spaces".

Model auth is either a pasted API key or a subscription sign-in; Nate connects a ChatGPT subscription instead of an API key. See [[wiki/concepts/subscription-oauth-vs-api-key-auth|subscription OAuth vs API-key auth]].

## Related harnesses and alternatives

- [[wiki/tools/grokbot|Grokbot]] is the same category of product (bots, routines, marketplace connectors) and adds webhook-triggered routines, which Hermes was not shown to have. See [[wiki/concepts/webhook-vs-cron-routines|webhook vs cron routines]].
- [[wiki/tools/trigger-dev|trigger.dev]] takes the opposite approach: deterministic automations hosted for free with no agent runtime at all, and judgment steps kept on a subscription. If your scheduled work is mostly code-shaped, that split may be all you need.
- [[wiki/tools/codex-scheduled-tasks|Codex scheduled tasks]] show the same "scheduled jobs inside a harness" idea from Codex's side, with a local-vs-cloud tradeoff (cloud runs with the device offline but loses model and reasoning selection) that Hermes's simpler Tasks panel does not surface.

Hermes is worth a look when you want an agent you can reach from your phone, outside a terminal session.
