---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, tool, google, cli, gmail, drive, claude-code]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]"]
---

# Google Workspace CLI (`gws`)

One command-line tool for Drive, Gmail, Calendar, Docs, Sheets, Chat, Admin and more, with agent skills bundled. Item 2 of [[wiki/sources/nateherk-6-best-github-repos-for-claude|Nate Herk's repo list]].

- **Repo:** https://github.com/googleworkspace/cli, npm `@googleworkspace/cli`, published under the `googleworkspace` GitHub org. The README ships many `SKILL.md` files, one per API plus helpers and about 50 recipes. Nate said "over 40"; the README text says both "40+" and "100+".
- **Install (per the README):** `npx skills add https://github.com/googleworkspace/cli` for all skills, or a single skill path such as `.../skills/gws-gmail`. The CLI itself installs through npm or `nix run github:googleworkspace/cli`. Helper commands look like `gws gmail +triage`, `gws calendar +agenda` and `gws drive +upload`.

## What Nate said (creator-claimed)

- **[01:30-02:15]** It works in Claude Code, Codex or any agent, unlike the built-in Claude Google connector, which he says only works in the desktop app and "doesn't cover everything". Setup takes minutes: a Google Cloud project for the login, then per-app access grants. His pitch: small businesses run on Google, so reports, invoices and follow-ups become automatable.

## Security note

This is OAuth access to a whole Google account from a local CLI (a CLI with skills, not an MCP). Create the Cloud project and consent screen under the account that should own them long term, such as your business account rather than a throwaway. Grant only the apps you need; the Gmail send scope is the dangerous one.

If mail, calendar and drive connectors already cover what you do, this adds little. It earns its place for headless work the connectors don't reach, such as formatting Sheets and Docs.
