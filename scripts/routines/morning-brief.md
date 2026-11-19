# Morning brief: routine spec

The spec for the daily cloud routine that e-mails the user a morning brief. `/setup` step 10 creates the routine with `/schedule`; its prompt is one line that points here. Change the brief in this file, never in the prompt: a rule edited in a prompt box drifts, a rule in the repo is versioned.

Bootstrap prompt (what `/setup` gives the routine):

> Read `scripts/routines/morning-brief.md` in this repository and follow it exactly. That file outranks this prompt.

## What good looks like

The user reads the subject line on their phone before breakfast and trusts it. Every line in the brief is either something they must do today, or a fact checked this run with a named source. A short brief that is right beats a long one that is half stale. If nothing needs them, the brief says so in one line.

## The one rule everything else follows from

**A note is not the present.** A row's Notes in `cadence.md`, a project page and an unread alert each record what was true when they were written. Before you state that something *is* broken, blocked, overdue or disconnected:

1. Look for newer evidence in the repo (`git log -5 --format='%ad %s' --date=iso -- <path>`, the newest output file of the job in question).
2. If newer evidence contradicts the note, the note loses. Report the newer state.
3. If you cannot check it, write it as history with its date and source: "As of 10 Nov (cadence.md): ...; not re-checked." Never in the present tense, never in the subject line.

Evidence outranks notes. Did a scheduled job run? Read the newest file or commit it produces, not the ledger's Last run cell. Did the backup reach GitHub? The newest commit on `origin` and its date.

**Never read `tmp/`.** It is gitignored and machine-local. Anything in the runner's `tmp/` was written by a cloud run, not by the user's machine.

## Setup

- Read-only on the repo: never commit or push. The only write is the one e-mail.
- Run `git fetch origin` and `git reset --hard origin/HEAD` first, so you read today's repo and not a cached clone.
- "Today" is the date in the user's timezone, from `brain/context/how-i-work.md` (the `Timezone:` line). The routine may fire on the previous UTC day: compute the local date with the tool (`TZ=<zone> date +%F`), never by hand, and check the output is not quietly printing UTC.
- The recipient address and the mail connector (Gmail, or Outlook through Microsoft 365) are in `cadence.md`, in the notes of the "Morning brief" row.

## Part 1: due from the ledger

Read `cadence.md`. A row is due when its Next due is today or earlier.

- Skip rows marked done, paused or dormant.
- Rows that run themselves (a cloud routine, a scheduled Action): do not list them from the ledger date. Check their output and report only one that is really late.
- For every other due row, apply the rule above to its Notes before repeating a blocker from them.
- Format: `item, command, due date`. Overdue first, then due today, oldest first.

## Part 2: open tasks and deadlines

- For each `brain/projects/*/CONTEXT.md` with `status: active`, read the `## Next` section. List open lines (`- [ ]`) whose date is in the next 7 days or earlier, oldest first, as `project: task (date)`. Undated open tasks: one line with a count per project.
- Deadlines this week from the calendar go here too, once, not in both places.

## Part 3: today on the calendar

List today's events as `time, title`, in the user's timezone. Take every weekday name from the tool, never from memory.

Sort events into two kinds:

- **Soft:** the user's own planning blocks, reminders, anything marked free.
- **Hard:** everything with another person or a fixed place: classes, meetings, calls, appointments.

A **clash** is two hard events overlapping. Sweep today plus the next 7 days. Only hard-on-hard clashes are counted. A hard event on top of a soft block gets one line under "Squeezed", without a count.

## Part 4: unread mail

`in:inbox is:unread`, about 25 threads. Give the count, then `sender, subject, received`, skipping newsletters and automated reports.

- An automated alert older than 24 hours goes under "Old unread", never as news. An alert describes the moment it was sent: check it against the repo before repeating it.
- Mail from a real person, or anything with a deadline, is flagged as needing the user.

## Part 5: subject line

`Brief <weekday> <date>: N due · T tasks · M events · K clashes`. N counts part 1 rows, T the dated open tasks in part 2, M today's events, K hard-on-hard clashes.

## Deliver

One e-mail to the recipient in `cadence.md`, sent from their own account through the mail connector. Subject from part 5. Body: parts 1 to 4 as short plain sections, under 40 lines. End with one line: "Open a session to act on any of this."

If the mail connector is not available in this run, do not fail silently: put the brief in the routine's own output and say which connector was missing.

## Stop and say so

- A connector is unreachable: still deliver what you can, and name the part you could not build.
- This file contradicts the bootstrap prompt: this file wins; mention the conflict at the end of the brief.
- Anything you could not check is labelled "not checked".

## If the user says a line is wrong

They are the firsthand source. Do not defend the line. Say which file or mail it came from and its date, and which `cadence.md` row or project page is stale, so their next session fixes it. This routine cannot write to the repo.
