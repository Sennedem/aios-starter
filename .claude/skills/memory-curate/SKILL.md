---
name: memory-curate
description: Curate the hand-written Claude Code memory layer for this project. Clusters related memories, de-dupes, merges superseded ones, re-ranks, fixes the MEMORY.md index and flags contradictions, so recall stays sharp as the memory set grows. Draft-first; never deletes or merges without approval. Use when memory feels bloated or stale, after a burst of new memories, or when the user says "curate my memory", "clean up memory", "/memory-curate". The janitor runs it as part of every local run.
---

# /memory-curate: memory layer curator

Automated learning adds memories but never prunes them, so over time `MEMORY.md` and the per-fact files collect duplicates, stale facts, contradictions and index drift. This skill does the gardening: cluster, de-dupe, merge superseded, re-rank, fix the index, flag conflicts.

**Autonomy: draft-first.** Produce a curation diff for the user's review. Never delete or merge a memory without their explicit OK: memory loss is irreversible and a wrong merge buries a real fact. Re-ordering the index and fixing obvious index/file mismatches may be applied once shown; content merges and deletes always wait for approval.

**Scope:** the Claude Code memory directory for this project (the per-fact `*.md` files and the `MEMORY.md` index). If the directory or `MEMORY.md` does not exist yet, say "no memory store yet, nothing to curate" and stop. Do not edit the brain here: that is `/audit`'s and `/onboard`'s job. This skill may flag brain staleness it notices.

## Step 0: Load

1. `references/curation-checklist.md`: the heuristics. Apply them.
2. `references/learnings.md`: the user's accumulated corrections. They override the defaults.
3. The whole store: `MEMORY.md` plus every per-fact file. Read the files, not just the index lines.
4. Note the schema so edits stay valid: frontmatter `name`, `description`, `metadata.type` (user, feedback, project, reference); the body carries the fact, with **Why:** and **How to apply:** for feedback and project memories; `[[name]]` links between memories. One fact per file, one index line per file.

## Step 1: Analyze (build the map)

- **Duplicates and overlaps:** two or more files covering the same fact, or one file holding two facts that should split.
- **Superseded or stale:** facts contradicted by a newer memory, or dated facts now out of date (convert relative dates; check against `brain/context/priorities.md`).
- **Contradictions:** pairs that cannot both be true. Recent generally wins; flag, don't auto-resolve.
- **Index drift:** index lines with no file, files with no index line, index hooks that no longer match the file.
- **Weak links:** `[[name]]` pointers to memories that do not exist.
- **Rank:** which memories are load-bearing and which are rarely relevant, for ordering.

## Step 2: Propose the curation diff (nothing applied)

Group by action, highest value first, short enough to approve in one read:

- **MERGE:** files X and Y into one (show the merged result and which index lines collapse).
- **UPDATE:** refresh a stale fact (before and after).
- **SPLIT:** one file holding two facts becomes two files.
- **DELETE:** a wrong or obsolete memory, with why it is safe to drop.
- **FIX-INDEX:** add, remove or repair `MEMORY.md` lines; reorder or group.
- **FLAG:** contradictions or brain staleness for the user to decide (no edit proposed).

## Step 3: Approve, then apply

- The user approves all, some or none (item by item for MERGE and DELETE). No merge or delete proceeds without an explicit yes.
- Apply approved edits with valid frontmatter and one fact per file. When merging, keep a one-line provenance note and re-point any `[[links]]`. Update every affected `MEMORY.md` line so index and files stay one-to-one.
- Re-check links afterwards: nothing may point at a file you just merged or renamed.

## Step 4: Capture feedback

When the user reacts ("don't merge those two, they're distinct", "keep stale ones, just mark them"), append a dated Rule / Why / Before and After entry to `references/learnings.md`. Do not skip it.

## Guardrails

- When unsure whether two memories are the same, FLAG; don't merge.
- A curated store that breaks the schema is worse than a messy one.
- Run after a burst of new memories or about monthly. Cheap to skip, expensive to over-curate.
