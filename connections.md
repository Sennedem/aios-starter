---
type: reference
updated:
---

# Connections: tools, connectors and accounts

The registry of everything this system can reach. Before installing or signing up for something,
check here first: the answer to "do we already have X?" lives in this file. Add a row when a tool
is connected, update the status when it breaks, and never put a secret here (keys live in `.env`,
which is gitignored; `.env.example` lists the names).

Status values: `active`, `broken`, `planned`, `retired`.

## Connectors

MCP servers and claude.ai connectors (mail, calendar, cloud storage, browser automation).

| Tool or connector | What it is for | Status | Notes |
|---|---|---|---|
|  |  |  |  |

## CLI tools

Command-line tools Claude may call (git, gh, node, python, ffmpeg and the like).

| Tool or connector | What it is for | Status | Notes |
|---|---|---|---|
|  |  |  |  |

## Accounts and subscriptions

Services the user has an account with, including perks bundled with another subscription.

| Tool or connector | What it is for | Status | Notes |
|---|---|---|---|
|  |  |  |  |

## Paid or metered APIs

Anything that spends money or credits per call. Each one also gets a pattern in
`.claude/metered.json` so the metered-credit guard blocks it until the user approves the spend.

| Tool or connector | What it is for | Status | Budget | Notes |
|---|---|---|---|---|
|  |  |  |  |  |

## Recommended connections

Nothing here is required. Each row says what it unlocks, so you can pick by what you want Claude to
do. `/setup` checks which of these you already have, recommends the two or three that fit your
answers, and adds the ones you connect to the tables above. Connectors are added in your Claude
connector settings (claude.ai, then Settings, then Connectors) and show up in the next Claude Code
session. Type `/mcp` in Claude Code to see what is connected.

### Start here (free, the biggest gain)

| Connection | What it unlocks | How |
|---|---|---|
| Mail (Gmail, or Outlook through Microsoft 365) | `/setup` reads your sent mail for people, recurring work and your writing voice. `/cadence` shows unread mail. `/inbox-janitor` labels the inbox | Claude connector settings |
| Calendar (Google Calendar, or Microsoft 365) | `/cadence` shows today and flags clashes. `/deadline` puts hand-ins on the calendar with reminders. `/setup` reads your weekly rhythm | Claude connector settings |
| Cloud drive (Google Drive, or OneDrive through Microsoft 365) | `/setup` reads the plans and documents you point at. Claude files finished work where you keep it | Claude connector settings |
| GitHub CLI (`gh`) | The private backup of this folder, and the check that keeps the backup hook from pushing to a public repo | Install from cli.github.com, then `gh auth login` |
| Obsidian | Reading and browsing the brain as linked pages and a graph | `node scripts/doctor.mjs` prints the install command |

### Add when you need it

| Connection | What it unlocks | How |
|---|---|---|
| The app your work lives in (Notion, Slack, Linear, Asana, HubSpot and others) | Claude reads and updates work where it already is, and `/setup` can harvest it | Claude connector settings, if a connector exists for it |
| A web search or scraping connector | Research legs (the `researcher` agent), `/ingest` on articles, fact checks before a decision | Claude connector settings, or `claude mcp add` |
| A browser driver (the Playwright MCP server) | Anything behind a login that has no connector: portals, admin panels, forms | `claude mcp add playwright -- npx @playwright/mcp@latest` |
| `yt-dlp` and `ffmpeg` | `/ingest` on videos: captions and frames | Your package manager (`winget`, `brew`, `apt`) |
| A model from outside the Claude family (for example the Codex CLI) | `/second-opinion` and the outside seat on `/jury` | That vendor's CLI and login |
| An automation hub (Zapier or similar) | Apps that have no connector of their own | Claude connector settings |

### Before you connect anything paid

Write the monthly ceiling in the "Paid or metered APIs" table and add a pattern to
`.claude/metered.json`. The guard then blocks every call to it until you approve the spend in the
conversation.
