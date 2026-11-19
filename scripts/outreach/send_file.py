"""send_file.py: send approved outbox entries through your Gmail. Run by the send Action.

How a mail gets here: Claude drafts in chat (drafts live in tmp/outreach/, which
git ignores), you review them and say send, `approve.py --send` lints them and
writes one JSON entry per mail into `outbox/`, the push of that commit triggers
`.github/workflows/send-file.yml`, and this script sends.

Safety properties, in the order they matter:

1. It cannot send something you did not approve. An entry without the
   `approved_at` stamp that approve.py writes is moved to `outbox/held/` unsent.
2. It cannot choose a recipient or write a word of copy. It sends exactly what
   the entry says, plus your signature from outreach.config.json.
3. It cannot send an unlinted mail. Every entry is linted again at send time,
   signature included; a failure moves it to `outbox/held/`.
4. It cannot exceed the daily caps, and re-running is a no-op
   (send_queue.eligible). Entries over the cap, or with a future `send_on`
   date, stay in the outbox and go on the next scheduled run.
5. It cannot fail silently. A Gmail error turns the job red.

Outbox entry (`outbox/<name>.json`), as approve.py writes it:
    {
      "to": "sam@acme.com",
      "company": "Acme",
      "subject": "question about acme",
      "body": "plain text, ending at the closing line",
      "touch": "1",                      # "1" first cold mail, "2"+ follow-up, "reply"
      "approved": true,
      "approved_at": "2026-05-04T09:12:00+00:00",
      "tracker": "brain/projects/<slug>/outreach-tracker.md",   # optional
      "send_on": "2026-05-05",           # optional: not before this day (your timezone)
      "from": "alias@yourdomain.com",    # optional, must be sender or in send_as
      "cc": "...",                       # optional
      "signature": false,                # optional: skip the signature block
      "reply_thread_id": "1a06...",      # optional: Gmail threadId to reply into
      "reply_to_message_id": "1a06...",  # optional: the message being answered
      "attachments": [{"path": "outbox/file.pdf", "name": "file.pdf"}]  # optional
    }
After a successful send the entry gains "sent_at", "message_id", "thread_id" and
moves to `outbox/sent/`; an attachment is deleted from the tree (git history
keeps it). Entries that already carry "sent_at" are never sent again.
"""

from __future__ import annotations

import base64
import json
import mimetypes
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import parseaddr
from pathlib import Path

import config
import lint
import send_queue as q
import signature
from gmail_auth import Gmail, GmailError, header

ROOT = config.ROOT


def resolve_sender(settings: config.Settings, entry: dict) -> str:
    """The From address for one entry: its "from" if allowed, else the configured sender.

    Gmail silently rewrites an unverified From to the account's own address, so
    anything outside the configured list is refused instead of shipped wrong.
    """
    alias = (entry.get("from") or "").strip().lower()
    if not alias:
        return settings.sender
    if alias not in settings.allowed_from:
        raise GmailError(f"from {alias!r} is not your sender or a send_as alias in {config.CONFIG_PATH.name}")
    return alias


def reply_headers(gmail: Gmail | None, entry: dict) -> dict[str, str]:
    """In-Reply-To / References for a reply, read from the answered message.

    Fetched from Gmail at send time rather than typed into the entry: a hand-
    copied Message-ID arrives with a stray bracket and silently breaks threading.
    """
    source_id = entry.get("reply_to_message_id")
    if not source_id:
        return {}
    if gmail is None:
        raise GmailError("reply_to_message_id needs a Gmail client to resolve the Message-ID")
    source = gmail.get_message(source_id)
    message_id = header(source, "Message-ID")
    if not message_id:
        raise GmailError(f"message {source_id} has no Message-ID header; cannot thread the reply")
    references = header(source, "References")
    return {
        "In-Reply-To": message_id,
        "References": f"{references} {message_id}".strip() if references else message_id,
    }


def attachments(entry: dict) -> list[tuple[str, str | None]]:
    """(repo-relative path, filename) pairs from "attachment" and "attachments"."""
    pairs = [(entry["attachment"], entry.get("attachment_name"))] if entry.get("attachment") else []
    return pairs + [(a["path"], a.get("name")) for a in entry.get("attachments") or []]


def touch_of(entry: dict) -> str:
    return str(entry.get("touch") or "1").strip()


def build(entry: dict, settings: config.Settings, gmail: Gmail | None = None,
          resolve_reply: bool = True) -> tuple[bytes, str, str]:
    """Build one message. Returns (wire bytes, subject, signed plain body for lint)."""
    msg = EmailMessage()
    msg["To"] = entry["to"]
    if entry.get("cc"):
        msg["Cc"] = entry["cc"]
    msg["From"] = resolve_sender(settings, entry)
    msg["Subject"] = entry["subject"]
    if resolve_reply:
        for name, value in reply_headers(gmail, entry).items():
            msg[name] = value
    msg.set_content(entry["body"])
    for att, name in attachments(entry):
        path = ROOT / att
        if not path.exists():
            raise GmailError(f"attachment missing: {att}")
        ctype, _ = mimetypes.guess_type(str(path))
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        msg.add_attachment(path.read_bytes(), maintype=maintype, subtype=subtype, filename=name or path.name)

    if entry.get("signature") is False:
        return msg.as_bytes(), entry["subject"], entry["body"]
    raw, body = signature.apply(msg.as_bytes(), touch_of(entry))
    return raw, entry["subject"], body


def build_raw(entry: dict, settings: config.Settings, gmail: Gmail | None = None) -> str:
    raw, _, _ = build(entry, settings, gmail)
    return base64.urlsafe_b64encode(raw).decode()


def tracker_path(entry: dict) -> Path | None:
    """The entry's tracker, only if it is a markdown file under brain/projects/."""
    rel = str(entry.get("tracker") or "").replace("\\", "/").strip()
    if not rel or ".." in rel or not rel.startswith("brain/projects/") or not rel.endswith(".md"):
        return None
    return ROOT / rel


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hold(path: Path, entry: dict, reasons: list[str]) -> None:
    """Park an entry in outbox/held/ with its reasons. It never sends from there."""
    config.HELD.mkdir(parents=True, exist_ok=True)
    entry = {**entry, "held_at": _now(), "held_reason": reasons}
    (config.HELD / path.name).write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    path.unlink()
    print(f"HELD {path.name}: {'; '.join(reasons)[:200]}")


def sent_rows() -> list[q.Row]:
    rows = []
    for p in sorted(config.SENT.glob("*.json")):
        try:
            e = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        rows.append(q.Row(e.get("thread_id", ""), p.stem, parseaddr(e.get("to", ""))[1].lower(),
                          e.get("company", ""), touch_of(e), "", "pass", "sent", e.get("sent_at", "")))
    return rows


def plan(settings: config.Settings, today: str) -> tuple[list[tuple[Path, dict]], list[tuple[Path, dict]]]:
    """Split the outbox into (send now, held). Not-yet-due and over-cap entries are neither."""
    due: list[tuple[Path, dict]] = []
    held: list[tuple[Path, dict, list[str]]] = []
    for path in sorted(config.OUTBOX.glob("*.json")):
        try:
            entry = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            held.append((path, {}, [f"not valid JSON: {exc}"]))
            continue
        if entry.get("sent_at"):
            continue
        if entry.get("approved") is not True or not entry.get("approved_at"):
            held.append((path, entry, ["not approved: only approve.py --send may write outbox entries"]))
            continue
        missing = [k for k in ("to", "subject", "body") if not str(entry.get(k, "")).strip()]
        if missing:
            held.append((path, entry, [f"missing field(s): {', '.join(missing)}"]))
            continue
        if str(entry.get("send_on", "")) > today:
            continue
        due.append((path, entry))

    rows = sent_rows() + [
        q.Row("", p.stem, parseaddr(e["to"])[1].lower(), e.get("company", ""), touch_of(e), "", "", q.SENDABLE, "")
        for p, e in due
    ]
    picked = {r.draft_id for r in q.eligible(q.Config.from_settings(settings), rows, today, settings.tz())}
    return [(p, e) for p, e in due if p.stem in picked], [(p, e, r) for p, e, r in held]


def check_account(gmail: Gmail, settings: config.Settings) -> None:
    """Refuse to run when the token belongs to another account than the config says.

    `sender` is always the account itself; extra From addresses go in `send_as`.
    """
    account = gmail.profile_email()
    if account and settings.sender.lower() != account:
        raise GmailError(
            f"The Gmail token belongs to {account}, but {config.CONFIG_PATH.name} says sender is "
            f"{settings.sender}. Fix the sender, or redo get_refresh_token.py while logged in as the sender."
        )


def send_one(gmail: Gmail, settings: config.Settings, path: Path, entry: dict) -> bool:
    raw, subject, body = build(entry, settings, gmail)
    verdict = lint.check(subject, body, touch_of(entry))
    if not verdict.passed:
        hold(path, entry, verdict.failures)
        return False
    result = gmail.send_raw(base64.urlsafe_b64encode(raw).decode(), entry.get("reply_thread_id", ""))
    entry = {**entry, "sent_at": _now(), "message_id": result.get("id"), "thread_id": result.get("threadId")}
    config.SENT.mkdir(parents=True, exist_ok=True)
    (config.SENT / path.name).write_text(json.dumps(entry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    path.unlink()
    for att, _ in attachments(entry):
        if (ROOT / att).exists():
            (ROOT / att).unlink()
    tracker = tracker_path(entry)
    if tracker:
        q.upsert(tracker, q.Row(entry["thread_id"] or "", path.stem, parseaddr(entry["to"])[1].lower(),
                                entry.get("company", ""), touch_of(entry), entry["approved_at"][:10],
                                "pass", "sent", entry["sent_at"]))
    print(f"sent {path.name} -> {entry['to']} (message {entry['message_id']})")
    return True


def main() -> int:
    if not any(config.OUTBOX.glob("*.json")):
        print("outbox empty")
        return 0
    settings = config.load()
    config.validate(settings)
    if settings.paused:
        print(f"Paused (paused: true in {config.CONFIG_PATH.name}): sending nothing. Entries stay in the outbox.")
        return 0

    today = settings.today()
    to_send, held = plan(settings, today)
    for path, entry, reasons in held:
        hold(path, entry, reasons)
    waiting = len(list(config.OUTBOX.glob("*.json"))) - len(to_send)
    if not to_send:
        print(f"nothing due today ({waiting} waiting for a later day or the next cap window)")
        return 1 if held else 0

    gmail = Gmail(settings.sender)
    check_account(gmail, settings)
    failures = 0
    for path, entry in to_send:
        try:
            if not send_one(gmail, settings, path, entry):
                failures += 1
        except GmailError as exc:
            failures += 1
            print(f"FAILED {path.name}: {exc}")
    if waiting:
        print(f"{waiting} entr(y/ies) left for a later run (send_on date or daily cap)")
    return 1 if failures or held else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except config.ConfigError as exc:
        print(f"Not set up yet: {exc}", file=sys.stderr)
        sys.exit(2)
