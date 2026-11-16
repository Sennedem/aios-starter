---
type: log
status: active
updated: 2026-11-16
domain: meta
parent: "[[audits/README|Audits]]"
tags: [janitor, lint]
---

# Brain janitor, 2026-11-16

Deterministic lint by `scripts/brain-janitor.mjs` (repo-only run). Overwritten on every run; `/audit` quotes these counts instead of re-deriving them. Scope: 17 brain pages, 0 projects, 21 skills.

## Summary

| Check | Count |
|---|---|
| broken | 0 |
| ambiguous | 0 |
| orphans | 0 |
| notInIndex | 0 |
| wikiNotInIndex | 0 |
| fmMissing | 0 |
| fmEnum | 0 |
| stale | 0 |
| drift | 0 |
| markers | 0 |
| dupIngest | 0 |
| tasks | 0 |
| cadence | 3 |
| skills | 0 |
| agents | 0 |
| local | 0 |
| **structural defects** (broken + ambiguous + orphans + index gaps + frontmatter + drift + dup ingests + skill/agent frontmatter) | **0** |

## Broken wikilinks

- none

## Ambiguous bare links (two files share the basename)

- none

## Orphans (content layer and wiki pages with no inbound link from a navigation page)

- none

_Unlinked pages elsewhere in the brain (informational, 0): none_

## Content pages missing from the brain/README.md index

- none

## Wiki pages missing from the wiki/README.md index

- none

## Frontmatter missing (parent / updated / none)

- none

## Frontmatter enum violations

- none

## Stale content pages (updated: more than 21 days ago, oldest first)

- none

## Frontmatter drift (updated: older than the git last commit)

- none

## Open / TBD markers (content layer)

- none

## Duplicate wiki ingests (same source URL)

- none

## OS: tasks.yaml past deadline, not done

- none

## OS: cadence rows due today, overdue or never run

- Morning check: never run (no last run, no next due)
- Weekly audit: never run (no last run, no next due)
- Weekly janitor: never run (no last run, no next due)

## OS: skill frontmatter and script references

- none

## OS: agent frontmatter

- none

_Judgment checks (missing pages for recurring entities, contradictions between pages) are not scripted; `/audit` still does those._
