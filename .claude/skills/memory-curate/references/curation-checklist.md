# Curation checklist: heuristics for /memory-curate

Distillation, ranking and contradiction handling for a plain-markdown memory store. Apply in steps 1 and 2.

## Clustering and de-dupe

- Group memories by shared topic, `metadata.type`, overlapping title words and shared `[[links]]`.
- A cluster of near-identical facts is a MERGE candidate: keep the strongest framing, union the detail, keep one provenance line.
- One file asserting two unrelated facts is a SPLIT candidate.
- Merge only when the facts are the same claim. Two facts that co-occur but are distinct (for example "sends mail from the work address" and "no messaging apps for clients") stay separate. When unsure, FLAG.

## Staleness

- Convert relative dates to absolute. A fact pinned to "this term" or "currently" is a staleness candidate: check it against `brain/context/priorities.md`.
- A project memory whose project shipped, paused or changed status gets an UPDATE or a DELETE with a reason.
- Prefer UPDATE when a fact is merely out of date; DELETE only when it is wrong or fully obsolete.

## Contradiction (recent wins, but flag)

- Find pairs that cannot both hold (an old "project X is active" against a newer "project X is paused").
- The newer one usually wins, but FLAG it for the user and never silently delete the loser. On approval, update or merge so the store reflects the current truth, with a provenance note on what was superseded.

## Index integrity (MEMORY.md and files, one-to-one)

- Every per-fact file has exactly one `MEMORY.md` line; every line points at a real file. Repair both directions.
- Each index line's hook must still match its file. Refresh a one-liner that has become misleading.
- Load-bearing memories (active feedback, current priorities) go near the top; pure reference entries can sit lower. Re-ordering is low risk and may be applied once shown.

## Ranking (judgment, no access counters)

- Rank by how often a memory is load-bearing for real work, how current it is, and its type (active feedback and project above stable reference).
- Use rank only to order the index and to pick merge priority. Never delete a memory for being low-rank: a rarely used fact can be the one that matters.

## Output discipline

- The step 2 diff must be skim-approvable: grouped by action, highest value first, before and after for content changes, one-line reason per DELETE.
- Never present a change as done before approval. A wrong cut in long-term memory is silent and permanent.
