---
name: cadence
description: Morning start-of-day check. Surfaces what is due from the cadence ledger (recurring AIOS work), today's calendar (meetings, deadlines, appointments), a clash sweep of the week ahead, and unread mail, then offers to run whatever is due. Calendar and mail steps run only when a connector exists. Use for "/cadence", "what's due today", "morning check", "start my day".
---

# /cadence: the morning check

One command to start the day: what recurring work is due, and what is on the calendar. It works best when a recurring "run /cadence" calendar nudge triggers it; a habit alone slips.

Use the real current date in the user's timezone (from `brain/context/how-i-work.md`; if none is recorded, the system clock's zone).

## Steps

### 1. What's due (the ledger)

- Read `cadence.md`. If it is missing or has no rows, say so and offer to add the first recurring jobs (each row needs an item, a command, an interval, a last-run date and a next-due date).
- For each row, compare the next-due date with today and group:
  - **🔴 Overdue:** next due before today
  - **🟡 Due today**
  - **⚪ Coming up:** within about 7 days
- One line each: *item, command, due date*.
- Offer to run any overdue or due item. After running one, set its last-run date to today and roll its next-due date forward by the interval (edit `cadence.md`).

### 2. Today on the calendar

- Needs a calendar connector (check `connections.md` and the available tools). None: skip this step and say "no calendar connected".
- List today's events on the primary calendar as *time, title*, in the user's timezone. Call out anything that is a deadline, hand-in or appointment.

### 3. Unread mail

- Needs a mail connector. None: skip and say so.
- Search `in:inbox is:unread` (about 25 threads, minimal view). Give the count, then *sender, subject* newest first. Call out anything that reads action-required or time-sensitive (a reply owed, a deadline, a bill, a real person rather than a newsletter).
- If the inbox is noisy, filter out promotions, social and updates, and report the filtered count in one line so nothing is hidden silently.
- Offer to act: draft replies through the `writing` skill (drafts first, shown inline, never auto-sent), or run `/inbox-janitor` to label the pile.

### 4. Week-ahead clash sweep

- Calendar connector only. Pull the next 7 days and flag any overlapping events in one line. Never let a silent double-booking stand.

### 5. One-line summary

Close with: *"N due, M events today, U unread, K clashes."* Then act on whatever the user picks.

## Notes

- Don't create or move any event without flagging clashes in that window first. New deadlines go through `/deadline`.
- This makes the session-start catch-up an on-demand, complete morning check.
