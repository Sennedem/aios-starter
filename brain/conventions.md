---
type: reference
status: active
updated: 2026-11-16
domain: meta
parent: "[[README|Brain]]"
---

# Wiki conventions

This vault is a linked Obsidian wiki that Claude maintains. Five rules keep it readable for you and cheap to search for Claude.

1. **Find pages through the index.** [[README]] lists every content page with a one-line summary. Claude reads it first instead of walking folders. A new page that is missing from the index is a lint error.

2. **Link with `[[wikilinks]]`.**
   - Use the path from the vault root with an alias: `[[projects/my-shop/CONTEXT|My Shop]]`.
   - Inside a markdown table, escape the alias pipe: `[[page\|Alias]]`.
   - Files outside the vault (the OS layer: `CLAUDE.md`, `cadence.md`, skills) are named with a plain path, never a wikilink.

3. **Frontmatter on every content page.**
   - `type`, the shape of the document: `context | project | index | reference | note | log | tracker | artifact`
   - `status`, where it is in its life: `active | paused | building | archived | draft | template`
   - `updated`, an ISO date. A hook bumps it when Claude edits the page.
   - Optional: `domain` (the project slug, or `wiki`, `meta`), `tags`, `related`.
   - `status` holds one enum value and nothing else. A remark goes in `status_note:`.

4. **Every content page has a `parent:`.** It is a wikilink to the nearest hub: a project's `CONTEXT`, a folder's `README`, or the brain [[README]]. Parents make each project show up as its own cluster in the graph view.

5. **Markdown only.** No code, no binaries, no exports. Images that notes use go in `attachments/`. Everything else lives where it belongs (a code repo, a cloud folder) and gets a pointer note in the OS folder `otherworlds/`.

`status: template` marks a page that `/setup` has not filled yet. The janitor script (`scripts/brain-janitor.mjs`) checks these rules and writes its findings to `audits/janitor-latest.md`.
