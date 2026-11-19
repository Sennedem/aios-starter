---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=gQef3d3erOs
tags: [wiki, source, youtube, hermes, agents, hosting]
related: ["[[wiki/concepts/managed-vs-vps-agent-hosting]]", "[[wiki/tools/hostinger-managed-agents]]", "[[wiki/concepts/subscription-oauth-vs-api-key-auth]]", "[[wiki/concepts/telegram-as-agent-channel]]", "[[wiki/tools/hermes-agent]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/techniques/give-agent-context-via-aios-and-grill-me]]", "[[wiki/concepts/cross-source-connections]]"]
---

# Source: "Set Up a Personal Hermes in 14 Mins (no VPS or mac mini)" (Nate Herk)

YouTube video (14:20) by Nate Herk | AI Automation, published 2026-08-27: https://www.youtube.com/watch?v=gQef3d3erOs. The whole video is a spoken walkthrough; nothing load-bearing sits only on screen.

Nate stands up a personal Hermes agent, his always-on "Claude Code or Codex in your pocket", using Hostinger's **managed** app instead of a self-hosted VPS. The full path: Hostinger account, managed Hermes app, connect a ChatGPT subscription instead of an API key, wire up Telegram through BotFather, activate, tour the web panel (tasks, kanban, skills, memory), add an API key through environment variables, and finally feed the agent real context before relying on it.

## Key takeaways

- **[00:19-02:11]** Managed vs VPS Hermes: managed starts at about $6 a month (slightly cheaper than a VPS), with no server to buy or maintain, no Docker, SSH or env files to touch, and Telegram pre-wired. But it is "one agent in a box", spun up fresh per app. A VPS costs a bit more and needs Docker, SSH and env configuration, but gives full root access and can host several agents (Hermes, N8N and others) on one box that scales. Nate's call: managed is "easier, simpler, and will suffice for probably like 98% of you guys." See [[wiki/concepts/managed-vs-vps-agent-hosting|managed vs VPS agent hosting]].
- **[02:12-03:37]** Setup starts in Hostinger's hPanel, under AI Agents (Open Claw, Hermes and N8N are the three managed options): Hermes Agent, "Get new app", then a plan (skip the bundled AI credits; the free web-scraping credits and Agentic Mail are optional). Nate's affiliate link and 10% coupon (yearly plans only) are how the video makes money, not part of the technique. See [[wiki/tools/hostinger-managed-agents|Hostinger managed agents]].
- **[03:41-04:16]** Hermes is a harness that wraps a model (Claude, GPT, Gemini and others). Instead of pasting an API key, Nate connects his **ChatGPT subscription** through an OAuth-style flow (open a link, sign in, copy a code back): "you're going to get way more inference, it's going to be way cheaper." See [[wiki/concepts/subscription-oauth-vs-api-key-auth|subscription OAuth vs API-key auth]].
- **[04:18-07:44]** Telegram wiring: message BotFather, send the newbot command, name the bot, pick a globally unique username ending in `bot`, and copy the access token into Hostinger. Then message `userinfobot`, send start, and copy your numeric user ID into Hostinger. Once activated, the web chat and the Telegram chat are **two windows onto the same thread**: a message sent in one shows up live in the other, including from a phone. See [[wiki/concepts/telegram-as-agent-channel|Telegram as an agent channel]].
- **[07:56-09:41]** The managed web panel: a **Tasks** panel for scheduled jobs (like routines), a **Kanban** board that tracks what sub-agents are doing, and a **Skills** panel with prebuilt toggles (Claude Code, Codex, computer use, creative, email, GitHub, media) plus a raw add-a-skill form (name, category, the skill's YAML frontmatter pasted verbatim), demoed by pasting in an Excalidraw diagram skill from his own Claude folder. Also **Memory**: notes, a user profile, an "agent soul" and project context, organized into "spaces". See [[wiki/tools/hermes-agent|Hermes agent]] and [[wiki/concepts/agent-skills-as-yaml-frontmatter|agent skills as YAML frontmatter]].
- **[09:41-12:08]** Adding a credential (a Tavily API key) is a plain environment-variable add in hPanel. Applying changes resets the whole app and asks for the panel password again (copy it from the panel). If the agent still can't see the key, restart the app manually from hPanel instead of pasting it again.
- **[12:24-14:19]** Nate's closing advice: before trusting a personal agent, give it real context about you. Either (a) use his free grill-me skill, which interviews you to build up memory, or (b) **if you already have an AI operating system repo backed up to GitHub, point the agent at it**: "read through this GitHub repo, this is our file structure, this is my projects, my business context." He adds grill-me as a custom skill the same way as the Excalidraw skill (paste the YAML frontmatter, name it) and then prompts the agent to run it. See [[wiki/techniques/give-agent-context-via-aios-and-grill-me|give your agent your AIOS repo or grill-me it for context]].

The closing advice is a good example of [[wiki/concepts/cross-source-connections|cross-source connections]]: a different creator's setup arriving at the same "repo as context, interview to fill gaps" idea.

## In this system

`/grill-me` runs the interview, and this repo is the kind of backed-up AI OS repo you can point another agent at.
