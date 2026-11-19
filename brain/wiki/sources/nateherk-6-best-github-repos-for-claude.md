---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, source, youtube, github, skills, claude-code, plugins]
related: ["[[wiki/tools/google-workspace-cli]]", "[[wiki/tools/apify-mcp-server]]", "[[wiki/tools/scroll-craft]]", "[[wiki/tools/humanizer]]", "[[wiki/tools/addy-osmani-agent-skills]]", "[[wiki/tools/playwright-cli]]", "[[wiki/concepts/token-saver-repos-vs-measured-savings]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]", "[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/concepts/stateless-wakeup-handoff-log]]"]
---

# Source: "I Tried 100+ Github Repos for Claude. These 6 Are the Best" (Nate Herk)

YouTube (10:36), Nate Herk | AI Automation, published 2026-10-11: https://www.youtube.com/watch?v=HhZdNYI4pJs. The captions garble names ("Haygen", "Superbase", "Appy Pie"); the repo identities below were checked by web search.

**Title mismatch:** the title says 6, the intro says "10 I cannot work without", and the video walks through 10 numbered items plus honourable mentions. Treat it as 10.

## The ten, with verified repos

1. **HeyGen's open-source HTML-to-video framework**, video rendered from HTML [00:25]. No page here.
2. **Google Workspace CLI** [01:28]: [[wiki/tools/google-workspace-cli]]
3. **Apify MCP server** [02:16]: [[wiki/tools/apify-mcp-server]]
4. **ScrollCraft** (Nate's own, disclosed) [03:08]: [[wiki/tools/scroll-craft]]
5. **Humanizer** [04:19]: [[wiki/tools/humanizer]]
6. **Agent Skills** (Addy Osmani), spec, plan and build commands [05:02]: [[wiki/tools/addy-osmani-agent-skills]]
7. **Expo official skills**, for mobile apps [06:24-07:00]: idea to a real iPhone app in an afternoon, even from Windows. Includes Expo's list of 20 things that make an app look AI-built, plus App Store rules. Tip: name the skills explicitly, because they don't always auto-load. Needs the $99 a year Apple developer account. No page (thin; repo not individually verified).
8. **Supabase and Stripe official skills** [07:01-07:40]: install only Stripe's "best practices" skill, not the full plugin (it may route every vendor decision through Stripe). Set the Supabase connector to read-only and log in as a test user to confirm you can't see other users' data. No page (thin; unverified).
9. **Playwright CLI** plus **Claude Security** (Anthropic's multi-agent security plugin) [07:40-08:35]: [[wiki/tools/playwright-cli]]
10. **Open SEO** [08:35-08:59]: real keyword data, rankings and backlinks; the free trial credits are small, and data sits on their server unless you self-host. Likely https://github.com/every-app/open-seo ("open source alternative to Semrush and Ahrefs"), but not confirmed as the one Nate means. DataForSEO is the usual data source and costs money.

Honourable mentions: token savers and Codeburn, covered in [[wiki/concepts/token-saver-repos-vs-measured-savings|token-saver repos vs measured savings]]; Superpowers ("still really good") and Matt Pocock's skills as a bonus [06:06-06:21].

## Nate's practical advice

- **[09:49-10:10]** Do not install all ten. Pick the one that fixes your current problem; if unsure, start with the Google CLI, Apify, ScrollCraft and Humanizer. If something breaks after installing several, you won't know which repo caused it.
- **[10:07-10:27]** The business loop: pull businesses with no website, build one from a sample page, clean the copy, send the link. "No one's going to pay you for a GitHub repo ... what you're selling is the thing you build around it."

## Overlap check before installing

| Repo | Skip it if you already have | What it adds anyway |
|---|---|---|
| Google Workspace CLI | Mail, calendar and drive connectors | Headless Sheets and Docs formatting |
| Apify MCP | Another scraper or search tool (Firecrawl, Exa, a browser MCP) | Ready-made scrapers for blocked sites; paid per result, terms-of-service risk |
| ScrollCraft | Frontend design skills | The checker's frame-by-frame scroll capture |
| Humanizer | A writing skill with its own ban list | A broad, maintained catalogue of AI tells |
| Agent Skills | Superpowers or plan mode | Little; two spec-and-plan systems compete for the same triggers |
| Playwright CLI | Playwright MCP | Fewer tokens in long browser sessions |

## Skeptic note

- The frame is "which repos help you land clients": a freelancer pitch, not a tooling evaluation. "Tried 100+" comes with no list, no criteria and no failures shown; the omitted repos are "in the description", not on screen.
- One of the ten is his own product, alongside his community. He discloses ownership (good) and ranks it fourth.
- The video demonstrates no output: every capability is asserted. Savings, speed and "10x" figures are his.
- Benchmarks (Caveman 8.5%, Ponytail 10%) are relayed from a JetBrains test he does not cite.
- Every item is third-party code running with Claude Code's permissions. His only security advice is Supabase read-only and Stripe skill-only; nothing on reading a plugin's hooks before installing it.

## Connections

- Confirms and extends [[wiki/sources/nateherk-fable-5-1-kills-website-slop|"Fable 5.1 kills website slop"]]: ScrollCraft is now a public repo.
- Echoes [[wiki/sources/nateherk-build-skills-not-agents|"Build skills, not agents"]]: skills as the unit of distribution, here packaged as GitHub repos and plugin marketplaces.
- The same verification instinct as [[wiki/concepts/prove-its-work|prove its work]] (Playwright, Claude Security).
- The spec-files fix for context rot matches [[wiki/concepts/stateless-wakeup-handoff-log|the stateless wake-up and handoff log]]: state in files, not chat.
