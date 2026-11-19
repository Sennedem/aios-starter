"""approve.py: turn a reviewed drafts file into outbox entries. The ONLY writer of outbox/.

    python scripts/outreach/approve.py tmp/outreach/drafts-<date>-<slug>.json          # check only
    python scripts/outreach/approve.py tmp/outreach/drafts-<date>-<slug>.json --send   # after the user said send

Why this script exists: anything in `outbox/` is sent by the GitHub Action on the
next push, and the session-end backup hook pushes everything. A draft that sat
in the outbox "for review" would go out the moment the session closed. So drafts
live in `tmp/outreach/` (gitignored, never pushed), and only this script, run
with `--send` after the user's explicit go, writes outbox entries. The Action
holds any entry that lacks the approval stamp written here.

Without `--send` it writes nothing: it prints the lint verdict per draft, which
is how Claude checks a batch while the user is still reviewing it.

Drafts file:
    {
      "project": "<slug>",                       # brain/projects/<slug>/
      "drafts": [
        {
          "to": "sam@acme.com",
          "company": "Acme",
          "subject": "question about acme",
          "body": "Hi Sam,\\n\\n...\\n\\nBest regards,",
          "touch": "1",                          # "1", "2"... or "reply"
          "tier": "CONFIRMED",                   # CONFIRMED | PATTERN | GUESS | FORM
          "hook_source": "https://acme.com/about",   # where the personal line came from
          "send_on": "2026-05-05",               # optional
          "reply_thread_id": "...", "reply_to_message_id": "..."   # follow-ups/replies
        }
      ]
    }

All or nothing: if any draft fails, nothing is written, so the batch the user
approved is exactly the batch that goes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import parseaddr
from pathlib import Path

import config
import lint
import send_file

SENDABLE_TIERS = {"CONFIRMED", "PATTERN"}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "x"


def already_contacted() -> set[str]:
    """Addresses that already got (or are queued for) a first touch."""
    seen = set()
    for folder in (config.OUTBOX, config.SENT):
        for p in folder.glob("*.json"):
            try:
                e = json.loads(p.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if send_file.touch_of(e) == "1":
                seen.add(parseaddr(e.get("to", ""))[1].lower())
    return seen


def check_draft(d: dict, settings: config.Settings, contacted: set[str], allow_guess: bool) -> list[str]:
    problems = [f"missing {k}" for k in ("to", "subject", "body") if not str(d.get(k, "")).strip()]
    if problems:
        return problems
    address = parseaddr(d["to"])[1].lower()
    touch = send_file.touch_of(d)
    if "@" not in address:
        problems.append(f"not an e-mail address: {d['to']!r}")
    tier = str(d.get("tier", "")).upper()
    if touch != "reply" and tier not in SENDABLE_TIERS and not allow_guess:
        problems.append(f"address tier {tier or 'missing'}: only CONFIRMED or PATTERN addresses are sent; "
                        "verify it first (or list it as a manual contact)")
    if touch == "1" and address in contacted:
        problems.append("this address already got a first mail; send a follow-up (touch 2) instead")
    if touch != "1" and touch != "reply" and not d.get("reply_thread_id"):
        problems.append("a follow-up needs reply_thread_id (and reply_to_message_id) so it lands in the same thread")
    if d.get("send_on") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d["send_on"])):
        problems.append("send_on must be YYYY-MM-DD")
    try:
        _, subject, body = send_file.build(d, settings, resolve_reply=False)
    except Exception as exc:  # noqa: BLE001 (report any build problem as a draft problem)
        return problems + [f"cannot build the mail: {exc}"]
    verdict = lint.check(subject, body, touch)
    return problems + verdict.failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("drafts", help="path to the drafts JSON (normally under tmp/outreach/)")
    parser.add_argument("--send", action="store_true", help="the user said send: write the outbox entries")
    parser.add_argument("--allow-guess", action="store_true",
                        help="the user verified GUESS-tier addresses themselves and said send anyway")
    args = parser.parse_args()

    settings = config.load()
    config.validate(settings)
    data = json.loads(Path(args.drafts).read_text(encoding="utf-8"))
    project = slug(str(data.get("project", "")))
    drafts = data.get("drafts") or []
    if not drafts:
        print("no drafts in the file")
        return 1

    contacted = already_contacted()
    batch_seen: set[str] = set()
    failed = 0
    for i, d in enumerate(drafts, 1):
        problems = check_draft(d, settings, contacted | batch_seen, args.allow_guess)
        if send_file.touch_of(d) == "1":
            batch_seen.add(parseaddr(d.get("to", ""))[1].lower())
        label = f"{i:02d} {d.get('company') or '?'} <{d.get('to', '?')}>"
        if problems:
            failed += 1
            print(f"FAIL {label}\n     " + "\n     ".join(problems))
        else:
            print(f"ok   {label}")

    if failed:
        print(f"\n{failed} of {len(drafts)} draft(s) need fixing. Nothing was written.")
        return 1
    if not args.send:
        print(f"\nAll {len(drafts)} pass. Nothing written: rerun with --send once the user says send.")
        return 0

    config.OUTBOX.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    day = settings.today()
    written = []
    for i, d in enumerate(drafts, 1):
        entry = {k: v for k, v in d.items() if k not in ("tier",)}
        entry["touch"] = send_file.touch_of(d)
        entry["approved"] = True
        entry["approved_at"] = stamp
        if project != "x":
            entry.setdefault("tracker", f"brain/projects/{project}/outreach-tracker.md")
        name = f"{day}-{project}-{i:02d}-{slug(d.get('company') or parseaddr(d['to'])[1])}.json"
        (config.OUTBOX / name).write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written.append(name)
    print(f"\nWrote {len(written)} outbox entr(y/ies):\n  " + "\n  ".join(written))
    print("Next: commit and push outbox/ so the send Action runs now (the session-end backup would also push it).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except config.ConfigError as exc:
        print(f"Not set up yet: {exc}", file=sys.stderr)
        sys.exit(2)
