---
name: janitor
description: Weekly curator for the whole AIOS. Reads every Claude Code session since the last run and writes the new durable facts, decisions and preferences into the right brain and OS files, retires stale context (passed deadlines, superseded sections, rotting tasks, overdue cadence rows), fixes router drift between CLAUDE.md and the skills, and does the housekeeping nothing else owns (tmp retention, dead scripts, silent scheduled jobs, failed backups). Autonomous with evidence, one commit per run. Use for "/janitor", "clean up the AIOS", "update stale context", "sweep my sessions into the brain", "what's out of date", or when the weekly cadence row is due. Not for mail (/inbox-janitor), not the read-only Four-Cs score (/audit), not memory merges (/memory-curate).
---

# /janitor: the curator

`scripts/brain-janitor.mjs` finds structural defects, `/audit` scores, and this skill fixes. It turns the week's sessions into curated context and retires what has gone stale. This file is the whole spec.

State lives in `state.json` next to this file. `lastRun` is the harvest watermark: only a run that harvested sessions advances it. A fresh clone ships `lastRun: null`, which means "harvest the last 14 days".

**Autonomy: act, with evidence.** Every change is applied directly and lands in one commit; the user reviews the report or the diff. The guardrails exist because a wrong fact in the brain is worse than a missing one.

## Guardrails

1. **Evidence or nothing.** A fact from a session is written only with a quote showing something was decided or done (a commit, a "done", the user stating a fact or a choice). Plans, ideas, options Claude offered, and things the user merely asked about are never written.
2. **Contradictions are questions.** A session that contradicts a curated file, or two sessions that disagree, go under *Questions for the user* and change nothing. The user's firsthand account outranks what a document implies.
3. **Retire, don't delete.** Superseded content moves under a `## Superseded (retired <date> by /janitor)` heading at the bottom of the same file, or the page gets `status: archived`. Dead scripts move to `scripts/_retired/`. Only `tmp/` retention deletes.
4. **Never touch:** session transcripts, `.env`, other repos, any cloud folder beyond listing an inbox, the history in `brain/decisions/log.md` (append only), `brain/wiki/raw/`. Never send, post, or run another skill's job.
5. **Memory store** (the Claude Code memory directory for this project): fix index integrity directly (missing or dangling `MEMORY.md` lines); a new durable fact about the user becomes a new memory file. Merging or deleting existing memories is `/memory-curate`'s job, run as step 5b, approval-gated.
6. **Hand edits win.** Edit surgically, never regenerate a file.
7. **Correction loop.** If the user reverts or corrects a janitor change, log it in `references/learnings.md` with the date and turn it into a rule here. Two corrections of the same kind demote that change type to "propose only" (listed under Questions, not applied).

## Procedure (one run)

1. **Load state.** Read `state.json`. If it is missing or unreadable, recreate it from the starter shape (`{"lastRun": null, "lastReport": null, "lastMemoryCurate": null, "runs": []}`) and say so. Read `references/learnings.md` and `references/allowlist.md`.
2. **Structural baseline.** Run `node scripts/brain-janitor.mjs` and read the report it writes (`brain/audits/janitor-latest.md` unless it prints another path). Do not re-lint by hand. If the script is missing or fails, say so at the top of the report and continue.
3. **Stale scan.** Run `git fetch` first if the repo has a remote (a stale origin makes scheduled jobs look silent; if the fetch fails, put that at the top of *Flagged* and mark the scheduled-job check unverified). Then check, by reading the files:
   - a backup failure note left in `tmp/` by the backup hook;
   - scheduled jobs listed in `cadence.md` or `connections.md` with no commit or output since their last expected run;
   - `cadence.md` rows overdue by more than 7 days;
   - dated claims in the brain whose date has passed ("by 2026-03-01", "until", "pending", "days out");
   - OS-layer files (`CLAUDE.md`, `connections.md`, `cadence.md`, `otherworlds/*`) not reviewed in 21 days;
   - skills in `.claude/skills/` that `CLAUDE.md` does not mention, and names in `CLAUDE.md` that are not skills (skip anything in `references/allowlist.md`);
   - `tasks.yaml` enum spellings and todos untouched for more than 30 days;
   - `tmp/` files older than 14 days; scripts nothing references.
4. **Session harvest.** List the session transcripts in the Claude Code projects directory for this repo (`~/.claude/projects/<this repo's path with separators replaced by dashes>/*.jsonl`) modified after the watermark. Exclude the current session. If there are none, skip to step 6.
5. **Distil (delegated, parallel).** Split the transcripts into batches of about five and launch one **harvester** agent per batch in a single message. Brief (fill in the file list, change nothing else):

   > Read these Claude Code session transcripts: <paths>. Each is a session between the user and Claude. Return ONE markdown table, columns: `fact | quote (25 words max, verbatim) | session file | turn | kind (fact / decision / preference / task-done / task-new / correction) | area (project slug, finance, aios, user)`.
   > - **Each step:** for each transcript, scan the user's lines, Claude's closing replies and any commits. Expected signal: 0 to 8 rows per session.
   > - **Count only** things decided, done, or stated as fact by the user. **Skip** options Claude offered, unconfirmed plans, questions, debugging chatter, and anything only Claude asserted without the user's yes or a commit.
   > - **Likeliest failure:** restating a proposal as a decision. Countermove: if the quote is Claude's and the user never confirmed it, drop it.
   > - **What good looks like:** "Invoices are booked on invoice basis | 'yes, book them when the invoice goes out' | <file> | 41 | decision | finance": specific, with a quote anyone can re-find.
   > - **Stop when** every transcript is covered; list any you could not read. Do not open other files. Mark anything ambiguous with `?` in the kind column instead of guessing.

   Done-condition (check it yourself): every transcript appears in some table or in a "could not read" list, and every row has a quote.

   **Reconcile (main session).** For each row, open the target file below and (a) drop the row if the fact is already there, (b) drop it if a later session overrides it, (c) send it to *Questions* if it contradicts the file, (d) otherwise write it. Spot-check at least 3 quotes against the transcript before writing.

   | Kind / area | Target |
   |---|---|
   | project fact or decision | `brain/projects/<slug>/CONTEXT.md` (a decision also gets appended to `brain/decisions/log.md`) |
   | the big picture of the user's work | `brain/context/work.md` |
   | shift in what matters | `brain/context/priorities.md` |
   | how the user likes to work | `brain/context/how-i-work.md` |
   | new tool, connector or credential state | `connections.md` |
   | user preference or correction | a memory file + its `MEMORY.md` line |
   | task done / new task | `tasks.yaml` |
   | recurring work started or stopped | `cadence.md` |

5b. **Memory curate.** Run `/memory-curate` steps 0 to 2 exactly as its `SKILL.md` says, counting the memories step 5 just wrote. Nothing in its diff is applied autonomously: present it after the janitor report and apply only what the user approves. If the diff is empty, say "memory store: nothing to curate". Record the date as `lastMemoryCurate`.
6. **Retire stale context**, one decision per finding:
   - *Dated claim passed*: if the outcome is known (session evidence or a later line in the same file), rewrite the line to the outcome or retire it under Superseded; if unknown, ask under Questions ("launch target 2026-03-01: what happened?").
   - *OS-layer file older than 21 days*: re-read it against current reality; fix what is wrong and set `updated:`; if nothing is wrong, still set `updated:` and say "reviewed, no change".
   - *Skills missing from CLAUDE.md*: add a Commands line for live ones; propose retiring dead ones under Questions (skills are never moved autonomously).
   - *tasks.yaml*: fix enum spellings; a todo rotting more than 30 days is marked `done` (with evidence) or set to `status: blocked` with `note: stale since <date>, confirm or drop`. Never deleted.
   - *Cadence overdue more than 7 days*: a one-off row whose event passed and evidence shows done is deleted (the ledger is a to-do list, not history); a recurring row keeps its date and goes under *Flagged* (the janitor does not run other skills).
   - *tmp/ older than 14 days* and not referenced: delete. Referenced: keep.
   - *Dead scripts*: move to `scripts/_retired/` and say so.
   - *Backup failure or silent scheduled job*: never fix credentials or schedules; put it at the top of *Flagged* with the one action the user must take.
   - Then the judgment checks no scan can do: `CLAUDE.md` claims against reality (which repos and folders live where); `priorities.md` still describing a finished period; "pending" items with no date.
7. **Report, state, commit.**
   - Write `brain/audits/janitor-<YYYY-MM-DD>.md` (frontmatter `type: log`, `status: active`, `domain: meta`, `updated: <date>`, `parent: "[[README]]"`) with exactly these sections: **Flagged: needs the user** (5 lines max, most urgent first), **Questions for the user**, **Changed** (table: file, what, evidence), **Harvest** (sessions read, rows in, rows written, rows dropped as duplicate), **Scan counts**.
   - Update `state.json`: `lastRun` = the run's start time (ISO, UTC) if the harvest ran, `lastReport`, append to `runs` (date, mode, sessions, changes, questions).
   - Commit only the paths you touched, as one commit: `git add <paths> && git commit -m "chore: janitor <YYYY-MM-DD>"`. If the repo has no git or no remote, say the change is local only.
   - Roll the janitor row in `cadence.md`: last run today, next due in 7 days. If the row does not exist, add it.
   - In chat: the Flagged lines, the counts and the report path. Nothing else.

## Verification (before claiming the run done)

- `git show --stat HEAD` matches the *Changed* table one-to-one; open two changed files and read the edit in context.
- Re-check each stale finding you claimed fixed: it is gone; what remains is in Questions or Flagged.
- `state.json` advanced; listing transcripts newer than the new watermark returns only this session.
- Say what was verified and how; anything not verified is labelled so.

## Dry run

`/janitor --dry` runs steps 1 to 5 and writes the report with **Changed** as *Would change*, edits nothing else, and does not advance `state.json`. Make the first run on a new install a dry run.

## Optional: run it as a weekly scheduled routine

The janitor can be scheduled as a weekly cloud routine (the built-in `/schedule` skill). A cloud runner has no session transcripts, no memory directory and no local `tmp/`, so a scheduled run:

- does steps 1, 2, 3, 6 and 7 only, skips the harvest (4, 5, 5b) and never touches `lastRun` (it writes `lastCloudRun` and appends a run with `"mode": "cloud"`);
- ignores the backup, `tmp/` and memory checks, which describe the local machine;
- fetches enough history before scanning (a shallow clone makes every job look silent);
- for each `cadence.md` row that names an automated job, sets `Last run` only when a commit or output file proves the run, quoting the evidence in the cell; rows only the user can run are never marked as run;
- may also write a `/level-up` candidate brief (`brain/audits/level-up-<YYYY-MM-DD>.md`, sections Candidate, Why this one, Scope, Runners-up, To ship) using level-up phases 1 and 2; it never builds;
- commits only its own paths, pulls with rebase, pushes once with one retry.

Keep the routine prompt to one line that points at this file, so the spec cannot drift from the prompt.
