"""Reply and bounce detection, from live Gmail.

Replies are derived from Gmail, never from the tracker: the tracker is a lagging
record. The threads watched are the ones in `outbox/sent/`, so only mail this
engine sent is tracked; your other mail is never read for this.

Bounce scope:
- A recipient-set block ("the receiver denied your mail", RDENY) is one person
  opting out with their own mail client. It counts toward the daily bounce
  threshold but does not pause the engine by itself.
- A reputation or spam signal ("low reputation", "policy violation", 554) pauses
  the engine on one strike: a deliverability problem compounds with every
  further send.
- A "(Delay)" notice is not a bounce; Gmail is still retrying.
- Only bounces inside tracked threads count, so an unrelated bounce elsewhere in
  the mailbox can never pause outreach.

Alert once per reply: each reported reply gets a Gmail label after the digest
went out, and later scans skip labelled messages. A new message in the same
thread has no label, so it still alerts.
"""

from __future__ import annotations

import re
from datetime import date, timedelta

import send_queue as q
from gmail_auth import Gmail, header

BOUNCE_SENDERS = ("mailer-daemon", "postmaster")
ALERTED_LABEL = "Outreach/Alerted"
BOUNCE_PAUSE_THRESHOLD = 3  # more than 2 bounces in the window pauses the engine
SPAM_SIGNALS = ("blocked", "spam", "rejected", "policy violation", "reputation", "554", "550 5.7")
# Checked BEFORE the spam keywords: these say the recipient refused us, not that
# a filter judged us. They also contain "blocked" and "550 5.7".
RECIPIENT_DENY_SIGNALS = ("rdeny", "receiver denied your mail", "the receiver denied")

SCOPE_RECIPIENT = "recipient-deny"
SCOPE_SPAM = "spam"
SCOPE_OTHER = "other"

_TO_PATTERNS = (
    re.compile(r"final-recipient:\s*rfc822;\s*<?([^\s<>]+@[^\s<>]+)>?", re.I),
    re.compile(r"your message to\s+<?([^\s<>]+@[^\s<>]+)>?", re.I),
    re.compile(r"wasn't delivered to\s+<?([^\s<>]+@[^\s<>]+)>?", re.I),
)


def classify(blob: str) -> str:
    """Scope a bounce from its subject + snippet. Recipient denials first."""
    low = blob.lower()
    if any(s in low for s in RECIPIENT_DENY_SIGNALS):
        return SCOPE_RECIPIENT
    if any(s in low for s in SPAM_SIGNALS):
        return SCOPE_SPAM
    return SCOPE_OTHER


def bounced_address(blob: str) -> str:
    """Best effort: the address the bounce is about, or "" if not stated."""
    for pattern in _TO_PATTERNS:
        match = pattern.search(blob)
        if match:
            return match.group(1).strip().rstrip(".,:;").lower()
    return ""


def is_bounce_sender(from_header: str) -> bool:
    """A delivery-failure notice lands inside the recipient's thread, so the
    reply sweep sees it as an inbound message. It is not a reply."""
    return any(s in from_header.lower() for s in BOUNCE_SENDERS)


def is_delay_notice(subject: str) -> bool:
    """A "(Delay)" DSN means Gmail is still retrying; only "(Failure)" is a bounce."""
    return "(delay)" in subject.lower()


def already_answered(thread: dict) -> bool:
    """True when our own sent message is the newest one in the thread (drafts skipped)."""
    msgs = [m for m in thread.get("messages", []) if "DRAFT" not in m.get("labelIds", [])]
    if not msgs:
        return False
    newest = max(msgs, key=lambda m: int(m.get("internalDate", 0)))
    return "SENT" in newest.get("labelIds", [])


def already_alerted(msg: dict, alerted_label_id: str) -> bool:
    return bool(alerted_label_id) and alerted_label_id in msg.get("labelIds", [])


def mark_alerted(gmail: Gmail, replies: list[dict]) -> None:
    """Label every reported reply. Call only AFTER the digest went out:
    labelling first and then failing to send would swallow the reply."""
    if not replies:
        return
    label = gmail.label_id(ALERTED_LABEL)
    for r in replies:
        gmail.add_label(r["message_id"], label)


def decide_pause(bounces: list[dict]) -> bool:
    """One spam/reputation signal, or more than 2 bounces in the window, pauses."""
    return len(bounces) >= BOUNCE_PAUSE_THRESHOLD or any(b["spam_signal"] for b in bounces)


def _lookback(days: int = 3) -> str:
    """Gmail's after: filter is date-granular; 3 days covers a weekend plus a missed run."""
    return (date.today() - timedelta(days=days)).strftime("%Y/%m/%d")


def scan(gmail: Gmail, rows: list[q.Row], days: int = 3) -> dict:
    tracked = {r.thread_id for r in rows if r.thread_id}
    since = _lookback(days)

    replies = []
    answered: dict[str, bool] = {}
    alerted_label: str | None = None
    for stub in gmail.search(f"in:inbox -from:me after:{since}", max_results=100):
        thread_id = stub.get("threadId")
        if thread_id not in tracked:
            continue
        if thread_id not in answered:
            answered[thread_id] = already_answered(gmail.get_thread(thread_id))
        if answered[thread_id]:
            continue  # the user replied after their last message; nothing is waiting
        msg = gmail.get_message(stub["id"])
        if alerted_label is None:
            alerted_label = gmail.label_id(ALERTED_LABEL)
        if already_alerted(msg, alerted_label):
            continue
        sender_header = header(msg, "From")
        if is_bounce_sender(sender_header):
            continue  # counted in the bounce sweep below, never as a reply
        match = next((r for r in rows if r.thread_id == thread_id), None)
        replies.append({
            "company": match.company if match else "(untracked thread)",
            "from": sender_header,
            "subject": header(msg, "Subject"),
            "date": header(msg, "Date"),
            "snippet": msg.get("snippet", "")[:300],
            "thread_id": thread_id,
            "message_id": stub["id"],
        })

    bounces = []
    for sender in BOUNCE_SENDERS:
        for stub in gmail.search(f"from:{sender} after:{since}", max_results=50):
            if stub.get("threadId") not in tracked:
                continue
            msg = gmail.get_message(stub["id"])
            subject = header(msg, "Subject")
            if is_delay_notice(subject):
                continue
            snippet = msg.get("snippet", "")
            blob = f"{subject} {snippet}"
            scope = classify(blob)
            bounces.append({
                "subject": subject,
                "snippet": snippet[:300],
                "scope": scope,
                "to": bounced_address(blob),
                "spam_signal": scope == SCOPE_SPAM,
            })

    return {"replies": replies, "bounces": bounces, "should_pause": decide_pause(bounces)}
