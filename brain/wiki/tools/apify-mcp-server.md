---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=HhZdNYI4pJs
tags: [wiki, tool, scraping, mcp, apify, claude-code]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]"]
---

# Apify MCP server

An MCP connector to Apify's marketplace of ready-made scrapers (called "Actors"). Item 3 of [[wiki/sources/nateherk-6-best-github-repos-for-claude|Nate Herk's repo list]].

- **Repo:** https://github.com/apify/apify-mcp-server, maintained by Apify itself. As of November 2026 the latest release seen was v0.21.4 (2026-11-06), with 187 releases and about 174 open issues.
- **Install (per the README and docs):** `claude mcp add apify "https://mcp.apify.com" -t http` (hosted, OAuth), or locally over stdio with `npx -y @apify/actors-mcp-server` and an `APIFY_TOKEN`.

## What Nate said (creator-claimed)

- **[02:16-03:06]** Claude cannot reach sites like Instagram and Reddit on its own: they block it or render with JavaScript, so it gets an empty page. Apify gives it scrapers for Instagram, TikTok, Amazon and more. His example: find Chicago bakeries on Instagram with follower counts and no website in the bio, and get a spreadsheet back in minutes. The connector is open source, but the scrapers run on Apify's cloud and cost per result; the free plan is $5 of credit a month. He names Firecrawl as an alternative.

## Security note

There are two layers: the MCP itself (open source, Apify-maintained) and the third-party Actors it runs, which other people write and which bill per result. Scraping Instagram or TikTok can breach those platforms' terms, and collecting data on named business owners falls under privacy law such as the GDPR. With the hosted MCP, your queries pass through Apify's servers.

If you already have a scraper or search tool wired (Firecrawl, Exa, a browser MCP), check whether it covers the sites you need before adding this one.
