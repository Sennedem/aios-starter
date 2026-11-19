---
type: reference
status: active
updated: 2026-11-19
domain: meta
pack: core
parent: "[[references/README|References]]"
tags: [cadence, automation, routines]
---

# Automation and cadence: how recurring work runs

The durable answer to "can this system run a job on a rhythm, even with the laptop closed?" Read it before building any scheduler, so the constraints do not get relearned.

**Short version:** run the triage gate (section 4) before building anything. Deterministic steps go to a script on a scheduled GitHub Action; judgment steps go to a Claude cloud routine. Reflective weekly jobs need neither: a ledger plus a check at session start covers them for free. Laptop-closed sending uses an approved queue and a dumb scheduler that runs no model at all.

## 1. Why there is no server cron for everything

There are two kinds of scheduling, and neither does everything.

| | Runs with the laptop closed? | Sees the local repo folder? | Has the mail, calendar and drive connectors? |
|---|---|---|---|
| **In-session** (`/loop`, an open conversation, you being there) | No: it needs an open conversation | Yes | Yes |
| **Cloud** (GitHub Action, hosted runners, automation services) | Yes | Only through the GitHub repo (clone, commit, push) | No: connectors need interactive sign-in, so a cloud job calls the raw API with its own stored credential |
| **Claude cloud routine** (`/schedule`) | Yes | Through the GitHub repo | Yes, the connectors attached to the account |

The trap: a job that needs the live local files and a connector in one step ("decide who to follow up with from my notes, then send") cannot run headless as one step on a plain runner. Split it: an **in-session** step decides and writes an approved artifact; a **dumb cloud** step executes the artifact with its own credentials.

What makes the cloud path possible at all is that the system lives in a GitHub repo. A cloud runner can clone it, work, commit and push, so "no local files" stops being a blocker as long as the repo is pushed and the result may come back through git.

## 2. The default: a ledger and a check at session start

For reflective recurring work (a weekly audit, a weekly review, a monthly check):

- **State:** `cadence.md`, one row per recurring item with interval, last run and next due.
- **Trigger:** the session-start instruction in `CLAUDE.md` reads the ledger every time a session opens and surfaces anything due. After an item runs, roll its last run and next due forward.
- **Why it is enough:** if you open Claude most days, a due item surfaces within a day with no outside reminder. It is free, needs no infrastructure, and survives closed conversations.

A headless run of a reflective job is possible (a cloud routine that clones the repo, runs it, pushes the report), but an interview-style job that needs you present gains nothing from it.

## 3. Headless sending: an approved queue and a dumb scheduler

For anything that must happen with nothing open, such as sending batched e-mails on a schedule:

1. **In session, with you:** generate the messages and write an **approved, dated queue** with columns like `send_date | to | subject | body | status | sent_at`. Batching (a few per day, one per domain) is encoded in `send_date`. Only rows marked `approved` are eligible.
2. **A dumb cloud scheduler:** a daily job reads the queue, sends the rows due today through the raw mail API with its own credential, and marks them `sent`. It cannot invent a recipient; it can only send rows a human approved. That is what makes a headless sender safe.

The send job runs no model, so it costs nothing beyond the free runner.

Lessons that carry to any scheduled job:

- **Failure has to surface somewhere you look.** Some runners e-mail the owner when a trigger fails (Google Apps Script does by default); GitHub's failure mails are opt-in and go only to whoever last edited the schedule. Pick the runner with that in mind, or make the liveness check independent of the runner.
- **The vendor is rarely the real bug.** A lane that can only report trouble by sending a message goes silent when it dies, and silence looks healthy. Every scheduled job writes a **positive heartbeat** (a dated line in the repo saying "ran, did N things") that the morning check reads. Swapping one vendor for another without a heartbeat only moves the trap.
- **Deliverability before volume.** Any domain that sends needs SPF and DKIM. A DMARC policy of `p=none` only reports; move to `p=quarantine` before raising daily volume. The domain's reputation affects all your mail, not only the automated sends.

Some signals stay manual until a connector exists for them: social platform analytics, app store reviews, meeting recordings, some banks. Check `connections.md` before promising an automation that reads one of them.

## 4. Before building any new automation: the triage gate

**Step 1: classify every step as deterministic or judgment.** Write the flow as numbered steps (trigger, read, decide, draft, send). A step is deterministic when the same input always produces the same action (read a calendar, look up a row, send to a fixed address). A step needs judgment when its output genuinely varies with the content (draft a message, choose what to research, decide whether to act). See [[wiki/concepts/deterministic-vs-nondeterministic-automation]].

**Step 2: route by the number of judgment steps.**

| Judgment steps | Runs as | Credential | Cost |
|---|---|---|---|
| **0** | a script on a **GitHub Action** (push-triggered, cron as a backup) | its own API key or OAuth token in the repo's Actions secrets | free |
| **1 or 2** (draft, classify) | a **Claude cloud routine** that does the judgment step and hands the rest to a script | connectors + repo | your subscription |
| **a loop** (research, reconsider, research again) | an **in-session run**, or a cloud routine if it must run unattended | connectors + repo | your subscription |
| **1 or 2, inside a script** (the judgment must sit in the pipeline) | a **Claude API call** from the Action | an API key from its own workspace with a spend limit set | pay per token |

The most common mistake is the opposite of what it looks like: an agent wrapped around a flow that had no judgment in it. A morning-brief routine hosted on an agent drifted after a month and started messaging the wrong channels, because the agent reinterpreted its instruction on every run ([[wiki/concepts/routine-drift]]). A script cannot drift.

**Step 3: interview before building.** Have the agent ask what a script cannot guess: destination, timing and tolerance ("6:05 is fine"), scope (which calendar, which inbox), research boundaries, a cost cap per run. See [[wiki/techniques/interview-before-building-an-automation]]; the `/level-up` interview covers the same questions.

**Step 4: anything that wakes up repeatedly is designed to be stateless.** Every wake-up reads the spec file in the repo and the previous run's handoff, checks live state, acts, writes what changed and what comes next, and records irreversible actions as they happen. Continuity comes from shared records, not from the model remembering ([[wiki/concepts/stateless-wakeup-handoff-log]]). Keep the routine's prompt to a bootstrap that reads the spec file, because a prompt edited in a web form drifts while a file in the repo has history. Walk the failure modes before the first run ([[wiki/concepts/routine-failure-modes]]):

- **No prior record** on the first run: the run must not fail on an empty log.
- **A crash after an irreversible action** (an e-mail sent, an order placed): the record must exist before the next step, so a restart does not repeat it.
- **Two runs overlapping:** `concurrency` groups on Actions; a lock file or a single thread for routines.
- **Stale or missing state:** every routine that reads the repo forces a fresh fetch and resets to the remote main branch before reading, or it may act on an old checkout.
- **The host offline at fire time:** GitHub's scheduled triggers are best effort and can skip whole days, so push triggers come first and a positive heartbeat is what the morning check reads. See [[wiki/concepts/webhook-vs-cron-routines]].

**Step 5: verify in the destination, not only in the log.** A run that passed locally and "delivered" in the hosted log still has to be checked where it lands: the inbox, the channel, the sent folder. First hosted runs often report success and deliver nothing (a disabled setting, a duplicate guard that fired).

## In this system

`cadence.md` is the ledger and `/cadence` is the morning check. The morning and weekly e-mails run as cloud routines whose prompts only bootstrap `scripts/routines/morning-brief.md` and `scripts/routines/weekly-review.md`. `/level-up` is where a new automation gets designed through this gate.
