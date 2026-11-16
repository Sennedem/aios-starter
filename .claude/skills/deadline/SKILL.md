---
name: deadline
description: Put a deliverable, hand-in or appointment on the user's calendar correctly: conflict-checked first, with the user's standard reminders attached in the same call. Use when a deadline needs to land on the calendar, or the user says "add <X> due <date>", "/deadline", "put this on my calendar", "remind me before <X>".
---

# /deadline: deliverable to calendar, done right

Turns "X is due <when>" into a conflict-checked event with the right reminders in one step, so the reminder math and the clash check never get skipped.

**Autonomy:** act-with-approval. The user names the deliverable and the date; the skill creates the event. It never invents deadlines.

**No calendar connector?** Check `connections.md` and the available tools. If none exists, say so, add the deadline as a task with a `deadline:` in `tasks.yaml` (so the dashboard counts it down), and stop.

## Step 0: Load the reminder defaults

Read the reminder defaults from `brain/context/how-i-work.md` (a line such as "Calendar reminders: popup at 07:00 on the day + 20 min before"). If none are recorded, ask once: "What reminders do you want on deadlines (for example a morning-of popup and one shortly before)?" Write the answer into `how-i-work.md` under a `Calendar reminders` line and bump its `updated:`, then use it from now on. Also take the user's timezone from that page.

## Step 1: Conflict check first (always)

Before creating anything, list events for the target window (and the surrounding day either side for all-day items) and surface any overlap. Never write over an existing slot silently: if it clashes, flag it and let the user choose.

## Step 2: Create the event with the standard reminders

Create the event on the primary calendar with reminders overridden to the user's defaults. Popup reminders are set in minutes before the start, so convert:

- **A time-of-day reminder** ("07:00 on the day"): minutes before = start time minus that time. For a 16:00 event and a 07:00 reminder that is 540; for 09:00 it is 120. If the event starts before the reminder time, drop that reminder and keep the rest.
- **A relative reminder** ("20 min before"): use it as is.
- **All-day deadline (date, no time):** calendars cannot fire a same-day morning popup on an all-day event (reminders count back from midnight). Default to a short timed marker on the due date at the morning reminder time, unless the user wants a true all-day block. Surface the choice; don't pick silently. If it stays all-day, use a day-before popup instead.
- Title = the deliverable; description = the source and context (what is due, for whom). Mark a deadline marker as free and an appointment as busy.

## Step 3: Confirm

Fetch the event back and report what was created (title, date and time, reminders) and any conflict found.

## Notes

- Batches are fine when the user lists several deadlines: conflict-check the whole window first, then create each.
- Recurring routines are not deadlines: they go in `cadence.md`, or on a hand-made recurring event.
