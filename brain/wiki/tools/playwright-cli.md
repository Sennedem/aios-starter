---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: coding
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, tool, testing, browser, playwright, claude-code]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]", "[[wiki/techniques/screenshot-scroll-verification]]", "[[wiki/concepts/prove-its-work]]"]
---

# Playwright CLI (Microsoft)

A command-line browser driver for coding agents, and the token-light sibling of Playwright MCP. Item 9 (with Claude Security) of [[wiki/sources/nateherk-6-best-github-repos-for-claude|Nate Herk's repo list]].

- **Repo:** https://github.com/microsoft/playwright-cli; docs at playwright.dev/docs/getting-started-cli. Install its skills with `playwright-cli install --skills`.
- A third-party benchmark quoted in a TestCollab blog reports about 114k tokens (MCP) against about 27k (CLI) for one task; secondary and not independently checked. The mechanism, per the README: data is saved to disk and the agent sees a file path instead of the full accessibility tree.

## What Nate said (creator-claimed)

- **[07:40-08:12]** Claude says "this works" without clicking the buttons. Playwright CLI opens a real browser, clicks through like a customer and writes re-runnable tests. Because it is a CLI and not an MCP, it doesn't dump the page into context, so it is lighter on tokens and faster.
- **[08:12-08:35]** He pairs it with Claude Security, Anthropic's security plugin: a team of agents hunts for holes, others try to disprove each finding, and you get a plain-English report with optional patches. Not verified independently here; no repo URL given.

## Security note

Maintained by Microsoft. It drives a real browser, so a logged-in profile exposes real accounts: apply the same rule as for Playwright MCP and require explicit approval before it touches a logged-in account.

If Playwright MCP is already wired for verification, the CLI wins mainly on token cost during long browser sessions.
