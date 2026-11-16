---
name: inbox-janitor
description: Label and tidy the user's Gmail inbox through a mail connector. Every unread thread gets exactly one category label from a small fixed set, noise is marked read, nothing is archived, deleted, replied to or drafted, and a five-line digest names what needs the user. Use for "/inbox-janitor", "clean my inbox", "label my mail", "what's in my inbox", or when a scheduled inbox run fires. Not for drafting replies (use the writing skill) and not for sending mail.
---

# /inbox-janitor: labels only, never drafts

Labels only makes a wrong label cheap to undo, so the skill can run unattended. Every label the user corrects becomes a rule in this file or a line in `references/sender-map.md`; the first week of runs is the trial.

**No mail connector?** Check `connections.md` and the available tools for a Gmail connector (tools such as `search_threads`, `label_thread`, `list_labels`). If there is none, stop and say: "No mail connector is connected, so I can't label your inbox. Connect Gmail in your Claude connector settings, record it in `connections.md`, and run `/inbox-janitor` again." Do not fall back to reading mail any other way. A different provider's connector works if it can list, label and mark read; map the steps onto its tools and note the mapping in `connections.md`.

## Hard rules

1. **Labels only.** Add labels, remove `UNREAD` on noise. Never archive, trash, spam-mark, star, reply, forward or draft.
2. **One category label per thread**, from the label set below.
3. **Never touch a thread the user already labelled by hand** (any user label outside the set). Their sort outranks the janitor's. If you labelled one by mistake, remove your label before the run ends.
4. **Read state:** `Notifications` and `Newsletters` are marked read. `Urgent` and `Primary` stay unread until the user reads them.
5. A thread already carrying the right category from an earlier run is left untouched.
6. Times in the digest and run log are the user's local time (timezone from `brain/context/how-i-work.md`, else the system clock), never UTC.

## The label set (a starter: edit it)

| Label | Goes here when | Read state |
|---|---|---|
| **Urgent** | a real person is waiting on the user: a reply to their outreach, a client, a customer, an invoice or payment demand with a date | unread |
| **Primary** | a real person wrote with no deadline: intros, questions, ongoing threads, anyone listed in `brain/context/network.md`; also automated mail that is business-impacting and needs action (an account suspended, a listing taken offline, an integration that must be reconnected) | unread |
| **Notifications** | machines: `noreply`, `no-reply`, `notification`, receipts, bank alerts, security alerts, form-submission copies, onboarding mail, the user's own scheduled self-digests | read |
| **Newsletters** | list mail (`list:` header, unsubscribe footer), digests, promotions, cold marketing pitches, anything in `category:promotions` | read |

Priority when two fit: Urgent, then Primary, then Notifications, then Newsletters.

To add a category (for example one for the user's own automated reports, or one per client), add a row here with its read state and place it in the priority order. Keep the set small: every extra label is a judgment call per thread.

## Procedure (one run)

1. Read `references/sender-map.md` (sender rules learned so far; they outrank the table above).
2. `list_labels` and resolve the ids of the label set. Create any that are missing, once, and record the ids in `references/sender-map.md` under "Label ids".
3. `search_threads` with `is:unread in:inbox` (page through if more than 50).
4. For each thread: classify on sender, subject and snippet. Open it (`get_thread`, plain text) only when the snippet is not enough.
5. Apply: `label_thread` with the one category id; for Notifications and Newsletters, remove `UNREAD` from each message.
6. Digest, five lines max: `Urgent N: <who, what>`, `Primary N: <who>`, `Notifications N marked read`, `Newsletters N marked read`, plus one line for anything odd. Name people, not thread ids.
7. Append a row to `references/run-log.md` (local date and time, unread in, counts per label, marked read, corrections).

## Verification

After applying, re-run `search_threads` with `is:unread in:inbox` and confirm only Urgent and Primary threads remain unread. Spot-check one labelled thread with `get_thread` and confirm the label id is on it. Report counts from the live read-back, not from the intended actions.

## Corrections

A label the user corrects is a rule change. Sender-specific fixes go into `references/sender-map.md` (`sender or pattern | label | why | date`); a fix that applies to a kind of mail goes into the label table or the hard rules here. Note the correction in the run log row.

## Optional: run it on a schedule

It can be scheduled (for example twice a day) as a cloud routine with the built-in `/schedule` skill. Keep the routine prompt to one line pointing at this file. A scheduled run does one pass, appends the run-log row, and commits only `references/run-log.md` and `references/sender-map.md`. If the user wants the digest delivered somewhere and a calendar connector exists, it can go in a short calendar event (no reminders, update an existing digest event in the same slot instead of duplicating it); otherwise the digest stays in the run log.
