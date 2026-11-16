---
type: reference
updated:
---

# Cadence: recurring work

The catch-up ledger. Read it at session start: surface any row whose `Next due` is today or
earlier, or that has never run, and offer to run it. After running an item, set its `Last run`
to today and move `Next due` forward by its `Interval`.

Dates are absolute (`YYYY-MM-DD`) in the user's local timezone. A row with no last run and no
next due counts as due now. The janitor (`scripts/brain-janitor.mjs`) and the dashboard both read
this table by its column names, so keep the header row as it is.

| Item | Command | Interval | Last run | Next due | Notes |
|---|---|---|---|---|---|
| Morning check | `/cadence` | daily |  |  | Ledger, today's calendar if a calendar connector exists, clashes in the week ahead. |
| Weekly audit | `/audit` | weekly |  |  | Scores the system on the Four Cs and writes a report to `brain/audits/`. |
| Weekly janitor | `/janitor` | weekly |  |  | Sweeps sessions into the brain, retires stale context, fixes drift. Run after the audit. |
