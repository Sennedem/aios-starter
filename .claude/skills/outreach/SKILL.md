---
name: outreach
description: Cold-email engine that turns a list of people or companies into verified addresses and personalised e-mails, sent from the user's own Gmail through a GitHub Action in their private repo. Drafts first, a blocking lint gate, deliverability-safe daily caps, follow-ups in the same thread, and a daily reply and bounce digest. Nothing is sent until the user says send. Use for lead outreach, interview requests, partner or supplier outreach, any batch of individual cold e-mails, or when the user says "/outreach", "e-mail these people", "write cold e-mails to this list", "reach out to these companies", "send a follow-up", "set up cold e-mail".
pack: outreach
---

# /outreach: cold-email engine

When the user has people to e-mail (leads, interview targets, partners, suppliers), run this end to end: verify each address, write one personal e-mail per contact, show the drafts, and send only after the user says send. Sending runs from their own Gmail through a GitHub Action in their own private repo, so it costs nothing and needs no session open.

All copy goes through the `writing` skill. The evidence behind the copy rules is [[references/cold-email-playbook]] (`brain/references/cold-email-playbook.md`): read it before the first batch for a project.

## Hard rules (never relax these)

1. **Drafts first. Nothing is sent without the user's explicit go**, given in this session, for this batch ("send", "go", "yes send them"). A go for one batch is not a go for the next. A follow-up batch needs its own go.
2. **Never stage a draft in `outbox/`.** Everything in `outbox/` is sent by the send Action on the next push, and the session-end backup hook pushes the whole repo. A draft parked there "for review" goes out the moment the session closes. Drafts live in `tmp/outreach/` (gitignored, never pushed). Only `scripts/outreach/approve.py --send`, run after the go, writes outbox entries, and the Action holds any entry without the approval stamp that script writes. Never write an outbox JSON by hand.
3. **The lint gate blocks.** `approve.py` lints every draft before it writes anything, and the Action lints again at send time with the signature attached. A failure is fixed in the draft, never waved through. Zero em dashes is part of the gate.
4. **Only verified addresses are sent** (CONFIRMED or PATTERN, Step 2). A GUESS address goes to the user as a manual check; `--allow-guess` only after they verified it themselves and said send anyway.
5. **Never send cold outreach any other way.** Not through the Gmail connector, not from a script you write in the session. The connector strips images and skips the lint gate and the caps. The connector is fine for reading (replies, the Sent folder).
6. **Every cold e-mail tells the truth about who sends it and carries a one-line opt-out.** An opt-out is honoured permanently: the address goes on the project's do-not-contact line and is never e-mailed again.

## Step 0: is the engine set up?

Check, in this order, and stop at the first gap:

1. `scripts/outreach/outreach.config.json` has a `sender` and `signature.name`. If not, run **First-time setup** below.
2. The Gmail connection exists: `.github/workflows/send-file.yml` is in the repo and the user has finished `scripts/outreach/SETUP-GMAIL.md` (ask; if they have not, walk them through it now, one step at a time, and wait for "done" after each). For its step 5, create `.env` from `.env.example` if it does not exist, make sure the three empty `GMAIL_` lines are in it, and open the file for them. Secrets are pasted into the file by the user, never into the chat; if one lands in the chat anyway, tell them to create a new client secret.
3. The backup repo is private. Outbox entries hold recipients and copy; a public repo would publish them. If it is public, stop and tell them how to make it private.
4. `scripts/outreach/heartbeat.md`: if `last_run` is older than 36 hours or `status: error`, the daily monitor is down. Say so and point to the Actions tab before you draft anything. "never" is fine on a fresh setup.

### First-time setup (once per user)

Ask these in one short batch, then fill `outreach.config.json` yourself (the user never edits JSON):

- The Gmail address they send from (`sender`). It must be the account they will connect in SETUP-GMAIL.md. Any extra "Send mail as" alias they have verified in Gmail settings goes in `send_as`.
- Their name and one-line role for the signature (`signature.name`, `signature.role`), and the closing they use (default "Best regards,").
- Optionally a photo URL (a square image at a public `https://` address). Recipients report a real face is what makes a cold mail read as human. Touch 1 carries the photo but never a link.
- Optionally links for follow-ups and replies (their site, a booking page). These never appear on a first mail.
- Their timezone (an IANA name such as `America/New_York` or `Europe/Berlin`), so "per day" means their day.
- Where the digest should go (`alert_to`; empty means the sender).
- If they write in a language other than English, a few stock phrases in that language that sound machine-written or salesy go in `extra_banned_phrases`.

Leave the caps at the defaults (10 new, 10 follow-ups, 20 total, 1 per recipient domain per day) unless they have a reason. A brand-new Gmail address should start lower (about 5 a day for the first two weeks).

### The legal check (before the first send, every new country)

Cold e-mail law differs by country. The usual differences: whether businesses may be e-mailed without prior consent (some countries allow it with an opt-out, some require consent even for businesses), whether consumers may be e-mailed at all, whether a published address counts as permission, and how the sender must identify themselves. Ask which country the user is in and which countries the recipients are in, and tell them to check the official rule for each (the national regulator's or government site) before the first send. Give no legal advice beyond that. Record their answer and the date in the project's `CONTEXT.md`. The hard rules above (true sender identity, opt-out line, honoured opt-outs, low volume) are the floor everywhere, never a substitute for the local rule.

## Step 1: the project and the list

- Read `references/learnings.md` (the user's earlier corrections; they override the defaults here).
- Every batch belongs to a project: `brain/projects/<slug>/`. Read its `CONTEXT.md` first (offer, audience, what was promised, earlier outreach). If no project fits, ask which one, or create it from `brain/templates/project-context.md`.
- The contact list lives in `brain/projects/<slug>/outreach-contacts.md`: one row per contact with name, role, company, language, the address with its tier, the hook with its source, and a status. The send record lives in `brain/projects/<slug>/outreach-tracker.md`, which the send Action writes after each mail.
- Ask up front only what is missing: the goal of the outreach (a call, an interview, a reply), the offer in one line, anything that must not be named (a client under NDA: generic web searches only, never the client name in a query, and zero hits for the name in every draft before staging).

## Step 2: verify addresses

For any address not already published and confirmed, research it. Fan out focused `researcher` agents, one per cluster of companies, each told to return a table. The highest-value find is one real published address per domain (team, contact or imprint page) to lock the name pattern; derive the rest from it.

Tag every address:
- **CONFIRMED**: published on a primary source. Sendable.
- **PATTERN**: derived from a named, confirmed address on the same domain. Sendable.
- **GUESS**: domain pattern only, no sample. Not sent; the user verifies it (LinkedIn, a phone call) first.
- **FORM / LinkedIn only**: no address. List the contact route as a manual to-do. Never invent an address.

A company with no address is still a tracked prospect in the contacts file; it never enters a batch.

## Step 3: write one e-mail per contact

Through the `writing` skill. The blueprint (evidence in the playbook):

- **50 to 125 words, three to five sentences, plain text.** Touch 1 has no links, images or attachments in the copy; the signature adds the photo.
- **Subject:** one to four words, lowercase, no sales language.
- **Body:** an observation about *them* that shows real research (never flattery), one line on who the sender is, the offer in one line, then a **permission ask, never a time ask** ("Would it help if I sent you a short example?"). The meeting ask comes after a yes. When the ask really is time (an interview request), a short time ask is fine.
- **The opt-out line** in every touch ("If this is not relevant, one word back is enough and you will not hear from me again.").
- **End the copy at the closing line.** Never type a signature: the engine adds the configured one at send time, and a typed one is detected and blocks the photo.
- **Language** follows the contact; never mix languages in one e-mail.
- **Hook plus source:** every personal line records where it came from (the page, post or review) in the contacts file. No untraceable claims.

Quality gates on every batch, before showing it:
1. **Verify pass (adversarial):** re-check each factual claim against its recorded source, trying to refute it. Kill overclaims (a dropped qualifier, an inflated number, a cause the source does not state). A wrong personal claim is worse than a generic line.
2. **Lint:** run `approve.py` without `--send` (Step 4). Every failure gets fixed before the user sees the batch.

## Step 4: drafts (nothing leaves the machine)

1. Write the batch to `tmp/outreach/drafts-<YYYY-MM-DD>-<slug>.json` in the format at the top of `scripts/outreach/approve.py` (`project`, then one object per draft with `to`, `company`, `subject`, `body`, `touch`, `tier`, `hook_source`).
2. Run `python scripts/outreach/approve.py tmp/outreach/drafts-<...>.json`. It writes nothing; it prints ok or the failures per draft. Fix and rerun until every draft passes.
3. **Show every draft in the chat**, in full: recipient, subject, body, the hook's source. Ask the user to review and say send, change, or drop per draft.
4. Update the contacts file: status `drafted`.

## Step 5: send (only after the explicit go)

1. Apply any changes the user asked for, rerun the check, and show the changed drafts again if the change was more than a typo.
2. Run `python scripts/outreach/approve.py tmp/outreach/drafts-<...>.json --send`. It is all or nothing: if one draft fails, nothing is written.
3. Commit and push the outbox so the send runs now: `git add outbox && git commit -m "outreach: <slug> batch <date>" && git push`. (The session-end backup would push it too, but the user wants to see it go.)
4. **Verify, do not assume.** After a minute or two: `git pull`, then check that each entry moved to `outbox/sent/` with a `message_id`, and read the Gmail Sent folder through the connector for at least one of them (photo present in a first mail, no link). Entries still in `outbox/` are waiting for their `send_on` day or the next day's cap; entries in `outbox/held/` failed and carry the reason. Report exactly that: sent N, waiting N, held N.
5. Contacts file: status `sent` with the date. The tracker was written by the Action.

### Deliverability-safe batching

- The daily caps in the config are enforced in code: new contacts first, follow-ups on top, one ceiling over both, at most one mail per recipient domain per day. Anything over the cap simply waits for the next weekday run of the send Action.
- To spread a big list on purpose, give drafts a `send_on` date. Prefer Tuesday to Thursday mornings in the recipients' timezone; a ready batch still beats a perfect slot.
- Write to the hands-on people before their bosses. Once one replies, mention it when you write to the boss later.

## Follow-ups

- Four working days after touch 1 with no reply, offer a touch 2. It is a reply in the same thread: set `touch: "2"` and copy `reply_thread_id` (the `thread_id`) and `reply_to_message_id` (the `message_id`) from that contact's entry in `outbox/sent/`. `approve.py` refuses a follow-up without them.
- Touch 2 gives one new reason (a result, an example) and bows out politely. At most two or three touches in total, fewer where the local rule is strict.
- Same rules as a first batch: drafts in chat, lint, the user's go, then `approve.py --send`.

## Replies

- Any human reply is answered **by the user**, personally. Draft the answer with the `writing` skill: substance first, then the example or link they said yes to. Never auto-reply.
- Send it through the same lane so the signature (with links now) is attached: a draft with `touch: "reply"` plus the two thread ids, the user's go, `approve.py --send`. Replies need no address tier.
- A "no" or "not now": status `closed` or a later date in the contacts file. A "stop" or any complaint: the do-not-contact line, permanently.

## The daily monitor and the kill switch

`.github/workflows/outreach.yml` runs once a day: it scans Gmail for replies and bounces on the threads in `outbox/sent/`, e-mails the user a digest when there is news, and writes `heartbeat.md`. One spam or reputation signal, or more than two bounces, sets `paused: true` in the config automatically. A recipient's own block counts as a bounce but does not pause by itself; a "no thanks" never pauses.

- **Kill switch:** set `paused: true` in `outreach.config.json` and push. Nothing sends until it is `false` again. Disabling the workflow in the Actions tab works too.
- **After a pause:** read the bounces with the user, fix the cause (a bad list, copy that reads as spam, too many per day), shrink the next batch, then unpause.
- When the digest reports replies, mark them in the contacts file and the tracker (`replied`), and offer the reply drafts.

## Corrections

When the user corrects a draft's tone, structure or targeting, log it in `references/learnings.md` (date, the correction, the rule it becomes) before the turn ends, and apply it to every later draft. Voice corrections also go to the `writing` skill's learnings.

## Files

| File | Job |
|---|---|
| `scripts/outreach/SETUP-GMAIL.md` | One-time Gmail and GitHub setup, click by click |
| `scripts/outreach/README.md` | How the engine works and how to run it by hand |
| `scripts/outreach/outreach.config.json` | Sender, signature, caps, timezone, kill switch |
| `scripts/outreach/approve.py` | Lints drafts; with `--send`, the only writer of `outbox/` |
| `scripts/outreach/send_file.py` | Sends approved entries (run by `send-file.yml`) |
| `scripts/outreach/run.py` | Daily replies, bounces, digest, heartbeat (run by `outreach.yml`) |
| `scripts/outreach/test_engine.py` | Checks the engine without a Gmail login |
