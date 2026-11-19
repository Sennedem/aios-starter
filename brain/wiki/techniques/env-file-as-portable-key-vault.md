---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, secrets, portability]
related: ["[[wiki/tools/trigger-dev]]", "[[wiki/concepts/subscription-vs-api-hosting]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]"]
---

# .env file as a portable key vault

Keep API keys in a plain `.env` file instead of pasting them into each app's own connector or plugin settings, because credentials stored in a connector do not travel. From [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk's automations video]]: "those will not transfer over to trigger.dev, which is why I really like to use plugins not very much. I like to use the .env file and I like to put all my API keys in there so that if I ever need to move them over to cloud code or if I need to move them over to trigger.dev, I already have them in one spot and I can just copy and paste them" [09:36-09:53].

## What makes it safe as well as convenient

Even inside a private GitHub repo, "the API keys, the calendar snapshots, and anything sensitive are excluded from Git... that's the whole point of the `.env`" [13:44-13:51]. The file is gitignored, so pushing the automation's code to GitHub never leaks the keys with it.

On the hosting side the values still have to be moved by hand into the host's environment-variable store (Codex did this through the CLI for trigger.dev, [17:21-17:34]). The `.env` is the single source of truth you copy from; the host does not read it directly.

## The tool-agnostic version

One `.env`, one gitignore entry, and keys copied (or pushed by CLI) into whichever runtime needs them next: Codex, Claude Code, a GitHub Action's secrets store, or trigger.dev's environment variables. You stop re-entering credentials per app and losing track of which app holds which key.

A gitignored `.env` also does not reach a second machine through git, so moving it there is a manual step (a password manager or a USB stick).

## In this system

Keys live in a gitignored `.env`, `.env.example` lists the names, and `connections.md` records which service is connected without ever holding a secret. `scripts/hooks/metered-guard.mjs` blocks a command that spends metered credits until you approve it.
