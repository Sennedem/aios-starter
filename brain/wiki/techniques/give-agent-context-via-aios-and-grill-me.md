---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=gQef3d3erOs
tags: [wiki, technique, context, grill-me, onboarding]
related: ["[[wiki/concepts/claude-md-as-router]]", "[[wiki/tools/hermes-agent]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/techniques/interview-before-building-an-automation]]", "[[wiki/techniques/roast-room-council-debate]]", "[[wiki/sources/nateherk-managed-hermes-setup]]"]
---

# Give your agent a context repo, or interview it into context

A fresh agent does not know who you are, what you work on or how you like things done. Before you rely on it, give it that context. Nate Herk closes his [[wiki/sources/nateherk-managed-hermes-setup|Hermes agent setup video]] with two ways to do it, framed as alternatives depending on what you already have [12:24-14:19].

## Path 1: point it at a repo that already holds your context

If you keep an AI operating system repo (a router file plus notes about you, your projects and your business, backed up to GitHub), point the agent at it: "read through this GitHub repo, this is our file structure, this is my projects, my business context, and just get to know me a little bit."

This works because the repo is structured for an agent to read. A router file (see [[wiki/concepts/claude-md-as-router|CLAUDE.md as router]]) tells it where each kind of fact lives, so it reads only what a task needs instead of everything at once.

## Path 2: let a skill interview you

If you have no such repo, or want to go deeper than what is written down, install an interview skill and have the agent run it on you: "I want you to get to know more about me and my business and my goals... use the grill me skill on me." The skill asks question after question and the agent saves what it learns, so "every time you do a grill me, it's going to get better and smarter."

Nate demos this live: he adds `grill-me` as a custom skill the same way he added an Excalidraw skill earlier (paste the name and YAML frontmatter, see [[wiki/concepts/agent-skills-as-yaml-frontmatter|Agent skills as YAML frontmatter]]), then prompts the agent to use it. That spawns a tracked "brainstorm" project that keeps the conversation in memory.

## Why use both

The two paths cover different gaps. The repo gives the agent the structural picture: what exists, where it lives, what was decided. The interview gets what was never written down: goals, preferences, the reasons behind decisions. Run the interview, write its output into the repo, and the next agent can take path 1 and start with everything.

## The same move elsewhere

Interviewing the human first works beyond onboarding. [[wiki/techniques/interview-before-building-an-automation|Interview before building an automation]] applies it to one design task (destination, timing, scope, cost cap). The roast-room council skill ([[wiki/techniques/roast-room-council-debate|council debate]]) applies it at decision scale: before the debate it asks clarifying questions when it lacks context, four in the demo [07:18-08:50]. All three converge on: give context first, and interview when the context is thin.

## In this system

Path 1 is this repo: `CLAUDE.md` is the router and `brain/` holds the context. Path 2 is `/setup` on a fresh clone (a long first interview that writes the brain) and `/grill-me` afterwards for depth on one topic; both save every answer to `brain/brainstorms/` before asking the next question.
