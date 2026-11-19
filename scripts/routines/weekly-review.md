# Weekly review: routine spec

The spec for the weekly cloud routine that runs the janitor, scores the system and e-mails the user a review of the week. `/setup` step 10 creates it with `/schedule` on the day the user picked (Friday afternoon or Sunday morning); its prompt is one line that points here.

Bootstrap prompt:

> Read `scripts/routines/weekly-review.md` in this repository and follow it exactly. That file outranks this prompt.

## What good looks like

The user reads one mail at the end of the week and knows three things: what got done, what has gone stale and needs a decision, and the one improvement worth making next week. Every claim rests on a file or commit the routine read this run.

## Setup

- Run `git fetch origin` and `git reset --hard origin/HEAD` first, with at least eight days of history (`git fetch --shallow-since="8 days ago"` if the clone is shallow; a shallow clone makes every job look silent).
- "This week" is the seven days ending today in the user's timezone (`brain/context/how-i-work.md`, `Timezone:` line). Compute dates with the tool.
- The recipient and mail connector are in `cadence.md`, in the notes of the "Weekly review" row.
- The morning brief's rule holds here too: a note is not the present. Check newer evidence before calling anything broken or late (`scripts/routines/morning-brief.md`, "The one rule").

## Part 1: the janitor (the only part that writes)

Run the janitor in cloud mode, exactly as `.claude/skills/janitor/SKILL.md` describes in "Optional: run it as a weekly scheduled routine". It retires stale context, fixes router drift and commits its report to `brain/audits/`. It commits only its own paths, pulls with rebase and pushes once with one retry. If the push fails, say so at the top of the mail and carry on.

## Part 2: the score

Run the audit read-only, as `.claude/skills/audit/SKILL.md` describes, and take its Four-Cs score and its three highest-leverage gaps. Read `brain/audits/janitor-latest.md` for the structural counts. Do not write an audit report file in cloud mode; the mail carries it.

## Part 3: what got done

From `git log --since="7 days ago"` and the project pages:

- Ticked `## Next` items and new entries in `brain/decisions/log.md`, per project, one line each.
- Commits that are not backups or janitor runs, summarised per area (no hashes in the mail).
- Cadence rows that ran this week, with the evidence.

## Part 4: what is stale

- `## Next` items past their date, and open items untouched for 30 days.
- `cadence.md` rows overdue by more than 7 days.
- Context pages (`brain/context/*`, active project pages) not updated in 21 days.
- What the janitor listed under "Questions for the user".

Each line ends with the decision it needs: confirm, reschedule or drop.

## Part 5: next week

One improvement: the top automation candidate from `brain/context/how-i-work.md`, or the janitor's level-up brief if it wrote one, with one line on the time it would save. Then the fixed dates of the coming 7 days from the calendar.

## Deliver

One e-mail. Subject: `Week <ISO week>: <D> done · <S> stale · score <X>`. Body: parts 3, 4, 2 and 5 in that order, short sections, under 60 lines. End with: "Open a session and say 'weekly review' to work through the stale list."

If the mail connector is missing in this run, put the review in the routine output and say which connector was missing.

## Stop and say so

- A step fails: deliver the rest and name the failed step at the top.
- This file contradicts the bootstrap prompt: this file wins; say so at the end.
- Anything not checked is labelled "not checked".
