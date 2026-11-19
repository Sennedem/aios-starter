# Outreach engine

Sends the cold e-mails you approve from your own Gmail, through GitHub Actions in your own private repository. Free, runs with no session open, and built so that a dead engine is hard to miss. Part of the `outreach` pack; the `/outreach` skill drives it. First-time setup: [SETUP-GMAIL.md](SETUP-GMAIL.md).

## How one batch flows

```
/outreach drafts in chat ──> tmp/outreach/drafts-*.json   (gitignored: never pushed, never sent)
        │  approve.py (check only): lint every draft, nothing written
        │  you review the drafts in chat and say "send"
        ▼
approve.py --send ──> outbox/<date>-<project>-NN-<company>.json   (stamped approved_at)
        │  git push (or the session-end backup push)
        ▼
send-file.yml ──> send_file.py: approval check, lint again with signature, daily caps,
        │          send through the Gmail API, move to outbox/sent/, tracker row
        ▼
outreach.yml (daily) ──> run.py: replies and bounces on outbox/sent threads,
                         auto-pause, digest e-mail, heartbeat.md
```

The one rule the layout exists for: **anything in `outbox/` is sent on the next push, and the backup hook pushes at the end of every session.** So drafts never go in `outbox/`. Only `approve.py --send`, run after your go, writes there, and `send_file.py` holds any entry without the approval stamp.

The Action cannot choose a recipient or write a word of copy. It sends exactly what an approved entry says, plus your signature. That boundary is the safety property; keep it.

## Files

| File | Role |
|---|---|
| `outreach.config.json` | Sender, aliases, signature, caps, timezone, digest address, `paused` kill switch. Committed (the Action needs it), no secrets |
| `config.py` | Loads and validates the config; outbox paths |
| `approve.py` | Lints a drafts file; with `--send`, writes the outbox entries. The only writer of `outbox/` |
| `send_file.py` | Sends approved entries. Run by `.github/workflows/send-file.yml` |
| `lint.py` | The blocking gate: ban list, placeholders, length, link-free first touch, zero dashes |
| `signature.py` | Appends your signature at send time (the Gmail API never adds one) |
| `send_queue.py` | Daily caps (new first, follow-ups on top, per-domain) and the tracker table |
| `monitor.py` | Reply and bounce detection from live Gmail |
| `alert.py` | The digest e-mail, only when there is news |
| `run.py` | The daily monitor. Run by `.github/workflows/outreach.yml`; writes `heartbeat.md` |
| `gmail_auth.py` | OAuth refresh and a thin Gmail REST client; raises on any error |
| `get_refresh_token.py` | One-time Gmail login, writes the token to `.env` |
| `set_github_secrets.py` | Copies the three secrets from `.env` to GitHub (refuses a public repo) |
| `dotenv.py` | Reads and writes the gitignored `.env` |
| `test_engine.py` | Checks everything that needs no Gmail login |

## Running it by hand

```
python scripts/outreach/test_engine.py                       # no login needed
python scripts/outreach/approve.py tmp/outreach/drafts-....json        # lint only
python scripts/outreach/approve.py tmp/outreach/drafts-....json --send # after the go
```

`send_file.py` and `run.py` need the three Gmail values in `.env` (or the environment) and `pip install requests`. Normally only the Actions run them.

## Caps

| Key | Default | Means |
|---|---|---|
| `max_new_per_day` | 10 | first mails to new contacts |
| `max_followups_per_day` | 10 | touch 2+, on top of the new ones |
| `max_total_per_day` | 20 | ceiling over both |
| `max_per_domain_per_day` | 1 | never several mails to one company on one day |

"Per day" is a day in the `timezone` from the config. Entries over a cap stay in `outbox/` and go out on the next weekday run. A brand-new Gmail address should start around 5 a day.

## Outbox entry fields

`to`, `company`, `subject`, `body`, `touch` (`"1"`, `"2"`, ... or `"reply"`), `approved`, `approved_at`, and optionally `tracker`, `send_on`, `from` (an alias from `send_as`), `cc`, `signature: false`, `reply_thread_id` and `reply_to_message_id` (follow-ups and replies thread into the original conversation), `attachments`. The full annotated format is at the top of `send_file.py`.

Attachments: the starter's `.gitignore` excludes PDFs, images and office files, so an attachment in `outbox/` is not committed and the Action reports it missing. Add `!outbox/**` to `.gitignore` if you need attachments. A first cold mail should never carry one.

## The failure model

A lane that can only report a problem by successfully sending a message goes quiet when it breaks, and quiet looks exactly like healthy. Three guards:

1. **Heartbeat:** `run.py` writes `heartbeat.md` on every run, failures included. `/outreach` reads it before staging anything and warns when it is more than 36 hours old.
2. **Red job:** any Gmail error raises and the run fails. Turn on GitHub's failed-workflow e-mails (SETUP-GMAIL.md, step 10).
3. **Auto-pause:** one spam or reputation bounce, or more than two bounces, sets `paused: true`.

Kill switch: `paused: true` in `outreach.config.json`, pushed. Or disable the workflows in the Actions tab.

## Removing the pack

`node scripts/packs.mjs remove outreach` deletes the skill, this folder and both workflows. Remove the three `GMAIL_*` secrets in GitHub (Settings, Secrets and variables, Actions) and the app at https://myaccount.google.com/permissions.
