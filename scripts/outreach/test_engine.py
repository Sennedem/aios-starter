"""Verification suite for everything that needs no Gmail credential.

Covers: daily caps and idempotence, the lint gate, the signature (MIME rewrite,
replies, idempotence), the outbox send pipeline with a fake Gmail (approval
guard, send_on, caps, held mail, tracker), approve.py (the only outbox writer),
and reply/bounce classification.

Stdlib only. Run from anywhere:
    python scripts/outreach/test_engine.py
It also runs under pytest (`python -m pytest scripts/outreach/test_engine.py`).
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from email import message_from_bytes
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# requests only exists in the Action's runtime. Stub it so the engine imports
# locally; nothing in this suite makes a network call.
if "requests" not in sys.modules:
    import types as _types

    _stub = _types.ModuleType("requests")
    _stub.post = _stub.get = lambda *a, **k: None
    _stub.RequestException = type("RequestException", (Exception,), {})
    sys.modules["requests"] = _stub

import config  # noqa: E402

SETTINGS = {
    "sender": "alex@example.com",
    "send_as": ["hello@example.com"],
    "timezone": "UTC",
    "caps": {"max_new_per_day": 3, "max_followups_per_day": 2, "max_total_per_day": 4, "max_per_domain_per_day": 1},
    "signature": {
        "name": "Alex Example",
        "role": "Founder, Example Studio",
        "closing": "Best regards,",
        "photo_url": "https://example.com/alex.png",
        "links": [
            {"label": "example.com", "url": "https://example.com"},
            {"label": "Book a call", "url": "https://cal.example.com/alex"},
        ],
    },
}
config.use(SETTINGS)

import approve  # noqa: E402
import lint  # noqa: E402
import monitor  # noqa: E402
import send_file  # noqa: E402
import send_queue as q  # noqa: E402
import signature  # noqa: E402

PASS, FAIL = "PASS", "FAIL"
results: list[tuple[str, str, str]] = []


def check(name: str, condition: object, detail: str = "") -> None:
    results.append((PASS if condition else FAIL, name, detail))


def write_queue(front: str, rows: list[str]) -> Path:
    path = Path(tempfile.mkdtemp()) / "queue.md"
    head = "| " + " | ".join(q.COLUMNS) + " |\n|" + "|".join(["---"] * len(q.COLUMNS)) + "|"
    path.write_text(f"---\n{front}\n---\n\n{head}\n" + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def row(to: str, company: str, status: str = "staged", sent_at: str = "", touch: str = "1") -> str:
    return f"| t-{company} | d-{company} | {to} | {company} | {touch} | 2026-05-04 |  | {status} | {sent_at} |"


# --- caps: nothing sends when nothing is staged --------------------------------

cfg, rows = q.load(write_queue("paused: false\nmax_per_day: 3", [
    row("a@x.com", "A", status="held"),
    row("b@y.com", "B", status="sent", sent_at="2026-05-04T06:30:00+00:00"),
    row("c@z.com", "C", status="closed"),
]))
check("no staged rows -> zero eligible", len(q.eligible(cfg, rows, today="2026-05-04")) == 0)

cfg, rows = q.load(write_queue("paused: true\nmax_per_day: 10", [row("a@x.com", "A"), row("b@y.com", "B")]))
check("paused: true -> zero eligible", len(q.eligible(cfg, rows, today="2026-05-04")) == 0)

cfg, rows = q.load(write_queue("paused: false\nmax_per_day: 10\nmax_per_domain_per_day: 1", [
    row(f"p{i}@{d}", f"C{i}{d}") for d in ("x.com", "y.com", "z.com") for i in range(5)
]))
picked = q.eligible(cfg, rows, today="2026-05-04")
check("15 rows / 3 domains, 1 per domain -> exactly 3", len(picked) == 3, f"got {len(picked)}")
check("picked domains unique", len({r.domain for r in picked}) == 3)

cfg, rows = q.load(write_queue("paused: false\nmax_per_day: 2", [row("a@x.com", "A"), row("b@y.com", "B"), row("c@z.com", "C")]))
check("max_per_day: 2 -> exactly 2", len(q.eligible(cfg, rows, today="2026-05-04")) == 2)

cfg, rows = q.load(write_queue("paused: false\nmax_per_day: 3", [
    row("a@x.com", "A", status="sent", sent_at="2026-05-04T06:30:00+00:00"),
    row("b@y.com", "B", status="sent", sent_at="2026-05-04T06:30:00+00:00"),
    row("c@z.com", "C", status="sent", sent_at="2026-05-04T06:30:00+00:00"),
    row("d@w.com", "D"),
]))
check("cap already spent today -> zero (scheduled run fired twice)", len(q.eligible(cfg, rows, today="2026-05-04")) == 0)
check("next day the cap resets", len(q.eligible(cfg, rows, today="2026-05-05")) == 1)

cfg, rows = q.load(write_queue("paused: false\nmax_per_day: 5", [
    row("a@x.com", "A", status="sent", sent_at="2026-05-04T06:30:00+00:00"),
    row("b@x.com", "B"),
    row("c@y.com", "C"),
]))
check("domain already hit today is skipped",
      [r.company for r in q.eligible(cfg, rows, today="2026-05-04")] == ["C"])

# --- caps: follow-ups are extras, never the daily number ------------------------

SPLIT = "paused: false\nmax_new_per_day: 8\nmax_followups_per_day: 6\nmax_total_per_day: 14\nmax_per_domain_per_day: 1"

check("touch 1 is fresh", q.is_fresh("1"))
check("touch 2 is a follow-up", not q.is_fresh("2"))
check("blank touch counts as fresh", q.is_fresh("") and q.is_fresh("  "))
check("garbled touch (or 'reply') counts as fresh", q.is_fresh("x") and q.is_fresh("reply"))

cfg, rows = q.load(write_queue(SPLIT, [
    row(f"s{i}@sent{i}.com", f"S{i}", status="sent", sent_at="2026-05-04T10:00:00+00:00", touch="2") for i in range(5)
] + [row(f"n{i}@fresh{i}.com", f"N{i}") for i in range(8)] + [row(f"f{i}@old{i}.com", f"F{i}", touch="2") for i in range(2)]))
picked = q.eligible(cfg, rows, today="2026-05-04")
n_fresh = sum(1 for r in picked if q.is_fresh(r.touch))
check("5 follow-ups already sent -> all 8 fresh still send", n_fresh == 8, f"got {n_fresh}")
check("follow-up budget spent down to 1 left", len(picked) - n_fresh == 1)
check("fresh rows are picked before follow-ups", all(q.is_fresh(r.touch) for r in picked[:n_fresh]))

cfg, rows = q.load(write_queue(
    "paused: false\nmax_new_per_day: 8\nmax_followups_per_day: 6\nmax_total_per_day: 10",
    [row(f"f{i}@old{i}.com", f"F{i}", touch="2") for i in range(6)] + [row(f"n{i}@fresh{i}.com", f"N{i}") for i in range(8)],
))
picked = q.eligible(cfg, rows, today="2026-05-04")
n_fresh = sum(1 for r in picked if q.is_fresh(r.touch))
check("ceiling 10 with follow-ups listed first -> 8 fresh + 2 follow-up", (n_fresh, len(picked)) == (8, 10))

cfg, rows = q.load(write_queue("paused: false\nmax_per_day: 8",
                               [row(f"f{i}@old{i}.com", f"F{i}", touch="2") for i in range(10)]
                               + [row(f"n{i}@fresh{i}.com", f"N{i}") for i in range(10)]))
picked = q.eligible(cfg, rows, today="2026-05-04")
check("max_per_day alias caps the total", len(picked) == 8)
check("max_per_day alias picks fresh first", all(q.is_fresh(r.touch) for r in picked))

cfg, _ = q.load(write_queue("paused: false", [row("a@x.com", "A")]))
check("no cap keys -> defaults, total == new + follow-up",
      cfg.max_total_per_day == cfg.max_new_per_day + cfg.max_followups_per_day > 0)

cfg, rows = q.load(write_queue(SPLIT, [row("follow@same.com", "Follow", touch="2"), row("fresh@same.com", "Fresh")]))
check("same domain, one fresh one follow-up -> the fresh one wins",
      [r.company for r in q.eligible(cfg, rows, today="2026-05-04")] == ["Fresh"])

_from_cfg = q.Config.from_settings(config.load())
check("caps come from outreach.config.json",
      (_from_cfg.max_new_per_day, _from_cfg.max_followups_per_day, _from_cfg.max_total_per_day) == (3, 2, 4))

check("sent_at: bare isoformat parses", q._day("2026-05-04T09:48:00+00:00") == "2026-05-04")
check("sent_at: trailing note does not crash", q._day("2026-05-04T09:48:00+00:00 (resent)") == "2026-05-04")

# --- tracker -------------------------------------------------------------------

_tracker = Path(tempfile.mkdtemp()) / "brain" / "projects" / "demo" / "outreach-tracker.md"
q.upsert(_tracker, q.Row("t1", "d1", "sam@acme.com", "Acme", "1", "2026-05-04", "pass", "sent", "2026-05-04T08:00:00+00:00"))
q.upsert(_tracker, q.Row("t2", "d2", "kim@beta.com", "Beta | Co", "1", "2026-05-04", "pass", "sent", ""))
q.upsert(_tracker, q.Row("t1", "d1", "sam@acme.com", "Acme", "1", "2026-05-04", "pass", "replied", ""))
_, _trows = q.load(_tracker)
check("tracker: created on first upsert", _tracker.exists())
check("tracker: upsert updates in place", [r.status for r in _trows] == ["replied", "sent"], str([r.status for r in _trows]))
check("tracker: a pipe in a company name cannot break the table", _trows[1].company == "Beta / Co")

# --- lint ----------------------------------------------------------------------

GOOD = (
    "Hi Sam,\n\n"
    "Your site says every new order is copied by hand from the inbox into the stock sheet. "
    "That takes time each week and goes wrong as soon as it gets busy.\n\n"
    "I build small systems that keep that kind of list up to date by themselves. "
    "Would it help if I sent you a short example of how that would look for Acme?\n\n"
    "If this is not relevant, one word back is enough and you will not hear from me again.\n\n"
    "Best regards,\nAlex"
)

check("clean draft passes", lint.check("stock sheet", GOOD, "1").passed, lint.check("stock sheet", GOOD, "1").summary)
cases = [
    ("unreplaced {{ }} placeholder", "Subject", GOOD.replace("Sam", "{{first_name}}"), "1"),
    ("bracket placeholder", "Subject", GOOD.replace("Acme", "[COMPANY]"), "1"),
    ("empty salutation", "Subject", GOOD.replace("Hi Sam,", "Hi ,"), "1"),
    ("empty subject", "", GOOD, "1"),
    ("empty body", "Subject", "", "1"),
    ("truncated body", "Subject", "Hi Sam, I saw that", "1"),
    ("link in touch 1", "Subject", GOOD + "\n\nSee https://example.com", "1"),
    ("ban-list phrase", "Subject", GOOD.replace("That takes time", "A seamless fix takes time"), "1"),
    ("AI opener", "Subject", "I hope this email finds you well.\n\n" + GOOD, "1"),
    ("em dash", "Subject", GOOD.replace("by hand from", "by hand \u2014 from"), "1"),
    ("spaced en dash", "Subject", GOOD.replace("by hand from", "by hand \u2013 from"), "1"),
    ("not-just pattern", "Subject", GOOD + "\n\nIt's not just a tool, it's a system.", "1"),
]
for name, subject, body, touch in cases:
    check(f"lint blocks: {name}", not lint.check(subject, body, touch).passed)

check("link allowed at touch 2", lint.check("Subject", GOOD + "\n\nSee https://example.com", "2").passed)
check("a short reply is not held as truncated", lint.check("Re: x", "Hi Sam,\n\nHere it is: https://example.com/demo\n\nBest regards,", "reply").passed)

config.use({**SETTINGS, "extra_banned_phrases": ["synergie"]})
check("extra_banned_phrases from the config are enforced", not lint.check("x", GOOD + " Synergie.", "1").passed)
config.use(SETTINGS)

# --- signature -----------------------------------------------------------------

signed1 = signature.sign_text(GOOD, "1")
signed2 = signature.sign_text(GOOD, "2")
check("touch 1 body gains the signature block", "Founder, Example Studio" in signed1)
check("no duplicated name after the sign-off", signed1.count("Alex") == 1, f"got {signed1.count('Alex')}")
check("closing kept exactly once", signed1.count("Best regards,") == 1)
check("signing is idempotent", signature.sign_text(signed1, "1") == signed1)
check("touch 1 signature is link-free", not lint.URL_RE.search(signed1))
check("signed touch 1 still passes lint", lint.check("stock sheet", signed1, "1").passed, lint.check("stock sheet", signed1, "1").summary)
check("touch 2 signature carries the links", "https://cal.example.com/alex" in signed2)
check("signed touch 2 passes lint", lint.check("Subject", signed2, "2").passed)
check("re-signing touch 2 does not stack the link row", signature.sign_text(signed2, "2") == signed2)
check("linked signature would be blocked at touch 1", not lint.check("Subject", signed2, "1").passed)
check("strip_signoff leaves the argument alone", "I build small systems" in signature.strip_signoff(GOOD))
check("strip_signoff drops only the sign-off",
      signature.strip_signoff(GOOD).rstrip().endswith("you will not hear from me again."))

RAW = (
    b"From: alex@example.com\r\nTo: sam@acme.com\r\nSubject: Re: stock sheet\r\n"
    b"In-Reply-To: <abc@mail.gmail.com>\r\nReferences: <abc@mail.gmail.com>\r\n"
    b'Content-Type: multipart/alternative; boundary="B"\r\n\r\n'
    b"--B\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n" + GOOD.encode()
    + b"\r\n--B\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    b"<div><p>Hi Sam,</p><p>Best regards,</p></div>\r\n--B--\r\n"
)
new_raw, new_body = signature.apply(RAW, "2")


def html_of(raw: bytes) -> str:
    for part in message_from_bytes(raw).walk():
        if part.get_content_type() == "text/html":
            return part.get_payload(decode=True).decode("utf-8", "replace")
    return ""


rebuilt = new_raw.decode("utf-8", "replace")
check("threading headers survive the rewrite", "<abc@mail.gmail.com>" in rebuilt)
check("recipient survives the rewrite", "sam@acme.com" in rebuilt)
check("plain part is signed", "Founder, Example Studio" in new_body)
check("html part carries the photo", "example.com/alex.png" in html_of(new_raw))
check("html part carries the touch-2 links", "cal.example.com/alex" in html_of(new_raw))
check("html signature is fenced for re-runs", signature.HTML_OPEN in html_of(new_raw))
check("re-applying does not stack the html block", html_of(signature.apply(new_raw, "2")[0]).count(signature.HTML_OPEN) == 1)
check("an upstream-typed signature is left alone", signature.sign_html("<div>Founder, Example Studio</div>", "2") is None)

HTML_TEXTLIKE = '<html><body><div dir="auto">Hi Sam,<br/><br/>Here is the text.<br/><br/>Best regards,<br/>Alex</div></body></html>'
signed_html = signature.sign_html(HTML_TEXTLIKE, "1")
check("html sign-off is not duplicated", signed_html.lower().count("best regards") == 1)
check("html body copy survives the strip", "Here is the text." in signed_html)
check("html strip keeps the document closed", signed_html.rstrip().endswith("</body></html>"))
check("mid-body 'regards' is not stripped",
      "regards" in signature.strip_signoff_html("<p>With regards to your order, a question.</p><p>One more line.</p>"))
check("html block escapes the ampersand",
      "&amp;" in (config.use({**SETTINGS, "signature": {**SETTINGS["signature"], "role": "Ops & Sales"}}) or signature.html_block("1")))
config.use(SETTINGS)
check("touch 1 html block is link-free", "href" not in signature.html_block("1"))
check("touch 1 carries the photo", "alex.png" in signature.html_block("1"))
config.use({**SETTINGS, "signature": {**SETTINGS["signature"], "photo_url": ""}})
check("no photo configured -> no img tag", "<img" not in signature.html_block("1"))
config.use(SETTINGS)

_, text_only = signature.apply(
    b"From: a@b.com\r\nTo: c@d.com\r\nSubject: x\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    b"<div><p>Hi Sam, here is the text.</p></div>\r\n", "1")
check("html-only message yields text for lint", "here is the text" in text_only)

# A plain-text-only message (how the Gmail connector and EmailMessage build
# them) must gain an html part, or the photo never ships.
_plain_only = (
    b"From: alex@example.com\r\nTo: kim@beta.com\r\nSubject: job codes\r\nIn-Reply-To: <abc@mail.gmail.com>\r\n"
    b"Content-Type: text/plain; charset=utf-8\r\n\r\nHi Kim,\r\n\r\nYour site maps each of the 93 job codes by hand.\r\n\r\nBest regards,\r\n"
)
_signed, _lintable = signature.apply(_plain_only, "1")
_parts = {p.get_content_type(): (p.get_payload(decode=True) or b"").decode("utf-8", "replace")
          for p in message_from_bytes(_signed).walk() if p.get_content_maintype() != "multipart"}
check("plain-only message gains an html part", "text/html" in _parts)
check("plain-only message ships the photo", "alex.png" in _parts.get("text/html", ""))
check("plain-only touch 1 stays link-free", "cal.example.com" not in _parts.get("text/html", ""))
check("html twin preserves the copy", "93 job codes" in _parts.get("text/html", ""))
check("html twin keeps the recipient and threading",
      message_from_bytes(_signed)["To"] == "kim@beta.com" and message_from_bytes(_signed)["In-Reply-To"] == "<abc@mail.gmail.com>")

_reply = (
    "Hi Chris,\n\nQuick follow-up. Your team checks insurance coverage by hand for every client before a "
    "session is booked, which is the step that does not scale.\n\nWould it help if I sent you a short example?\n\n"
    "Best regards,\n\nOn Thu, May 01, 2026 10:49 AM, Alex Example <alex@example.com> wrote:\n\n"
    "> Hi Chris,\n> the original first mail\n> Alex Example\n"
)
_signed_reply = signature.sign_text(_reply, "2")
check("reply signature sits above the quote", 0 < _signed_reply.find("Founder, Example Studio") < _signed_reply.find("On Thu, May 01"))
check("reply keeps the quoted thread", "> the original first mail" in _signed_reply)
check("reply signing is idempotent", signature.sign_text(_signed_reply, "2") == _signed_reply)

_html_reply = (
    '<div dir="auto">Hi Chris,<br><br>Quick follow-up.<br><br>Best regards,</div>'
    '<div class="gmail_extra"><blockquote class="gmail_quote"><div>original<br>Alex Example<br>'
    "Founder, Example Studio</div></blockquote></div>"
)
_signed_html = signature.sign_html(_html_reply, "2")
check("html reply is signed, not skipped (guard looks above the quote)", _signed_html is not None)
check("html reply block sits above the quote",
      _signed_html is not None and 0 < _signed_html.find("alex.png") < _signed_html.find("gmail_extra"))

_own = (
    "Hi Pat,\n\nQuick follow-up. Your partner search runs by hand: every introduction is matched manually "
    "before it reaches a client, which is the part that scales badly.\n\nWould it help if I sent you a short "
    "example of how this works in practice?\n\nBest regards,"
)
_quoted = "\n\nOn Thu, May 01, 2026 10:49 AM, Alex Example <alex@example.com> wrote:\n\n> One line \u2014 with a dash.\n"
check("an attached quote does not spend the dash budget", lint.check("Re: x", _own + _quoted, "2").passed)
check("a dash in our OWN copy is still blocked",
      not lint.check("Re: x", _own.replace("scales badly", "scales badly \u2014 truly") + _quoted, "2").passed)
check("prose containing 'wrote:' is not treated as a quote",
      "prompted this email" in signature.sign_text(
          "Hi Jo,\n\nOne of your reviewers wrote: a wrong code delays every claim.\nThat line is what prompted this email.\n\nBest regards,", "1"))

# --- outbox: building one mail -------------------------------------------------


def _payloads(raw: bytes) -> bytes:
    """Decoded part bodies (MIME base64-encodes them; searching wire bytes fails silently)."""
    return b"".join(p.get_payload(decode=True) or b"" for p in message_from_bytes(raw).walk()
                    if p.get_content_maintype() != "multipart")


_s = config.load()
_mail, _, _ = send_file.build({"to": "sam@acme.com", "subject": "x", "body": GOOD, "touch": "1"}, _s, resolve_reply=False)
check("outbox: signature added by default", b"Founder, Example Studio" in _payloads(_mail))
check("outbox: touch 1 ships the photo with no link", b"alex.png" in _payloads(_mail) and b"cal.example.com" not in _payloads(_mail))
_plain, _, _ = send_file.build({"to": "sam@acme.com", "subject": "x", "body": "Hi,\n\nNote.\n", "signature": False}, _s, resolve_reply=False)
check("outbox: signature false leaves the body alone", b"Founder" not in _payloads(_plain))
check("outbox: from alias in send_as accepted", send_file.resolve_sender(_s, {"from": "hello@example.com"}) == "hello@example.com")
try:
    send_file.resolve_sender(_s, {"from": "someone@else.com"})
    _raised = False
except send_file.GmailError:
    _raised = True
check("outbox: an unlisted From is refused", _raised)

# --- outbox: the send pipeline with a fake Gmail ---------------------------------


class _FakeSender:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send_raw(self, raw_b64: str, thread_id: str = "") -> dict:
        self.sent.append((raw_b64, thread_id))
        return {"id": f"m{len(self.sent)}", "threadId": thread_id or f"t{len(self.sent)}"}

    def get_message(self, message_id: str) -> dict:
        return {"payload": {"headers": [{"name": "Message-ID", "value": "<orig@mail.gmail.com>"}]}}

    def profile_email(self) -> str:
        return "alex@example.com"


def _sandbox() -> Path:
    root = Path(tempfile.mkdtemp())
    config.OUTBOX, config.SENT, config.HELD = root / "outbox", root / "outbox" / "sent", root / "outbox" / "held"
    config.OUTBOX.mkdir(parents=True)
    send_file.ROOT = root
    return root


def _entry(to: str, company: str, touch: str = "1", **extra: object) -> dict:
    body = GOOD.replace("Sam", company)
    e = {"to": to, "company": company, "subject": f"question about {company.lower()}", "body": body,
         "touch": touch, "approved": True, "approved_at": "2026-05-04T09:00:00+00:00",
         "tracker": "brain/projects/demo/outreach-tracker.md"}
    e.update(extra)
    return e


def _put(name: str, entry: dict) -> None:
    (config.OUTBOX / f"{name}.json").write_text(json.dumps(entry), encoding="utf-8")


_root = _sandbox()
_put("01-a", _entry("a@one.com", "One"))
_put("02-b", _entry("b@two.com", "Two"))
_put("03-c", _entry("c@one.com", "Three"))                       # same domain as 01: waits
_put("04-d", _entry("d@four.com", "Four", send_on="2099-01-01"))  # future: waits
_unapproved = _entry("e@five.com", "Five")
del _unapproved["approved_at"]
_put("05-e", _unapproved)                                         # never approved: held
_put("06-f", _entry("f@six.com", "Six"))
_put("07-g", _entry("g@seven.com", "Seven"))                     # over the 3-new cap: waits

_to_send, _held = send_file.plan(config.load(), "2026-05-04")
check("plan: unapproved entry is held, never sent", [p.stem for p, _, _ in _held] == ["05-e"])
check("plan: future send_on waits", "04-d" not in {p.stem for p, _ in _to_send})
check("plan: one per domain per day", "03-c" not in {p.stem for p, _ in _to_send})
check("plan: new-contact cap (3) respected", [p.stem for p, _ in _to_send] == ["01-a", "02-b", "06-f"],
      str([p.stem for p, _ in _to_send]))

_fake = _FakeSender()
for _p, _e, _r in _held:
    send_file.hold(_p, _e, _r)
with redirect_stdout(io.StringIO()):
    for _p, _e in _to_send:
        send_file.send_one(_fake, config.load(), _p, _e)
check("send: three mails went out", len(_fake.sent) == 3)
check("send: sent entries moved to outbox/sent with ids",
      all(json.loads((config.SENT / f"{n}.json").read_text())["message_id"] for n in ("01-a", "02-b", "06-f")))
check("send: unapproved entry parked in outbox/held with a reason",
      "not approved" in json.loads((config.HELD / "05-e.json").read_text())["held_reason"][0])
check("send: waiting entries stay in the outbox", sorted(p.stem for p in config.OUTBOX.glob("*.json")) == ["03-c", "04-d", "07-g"])
_, _trows = q.load(_root / "brain" / "projects" / "demo" / "outreach-tracker.md")
check("send: tracker gained one sent row per mail", [r.status for r in _trows] == ["sent"] * 3)
_wire = message_from_bytes(__import__("base64").urlsafe_b64decode(_fake.sent[0][0]))
check("send: the wire mail is signed and addressed right",
      _wire["To"] == "a@one.com" and b"Founder, Example Studio" in _payloads(_wire.as_bytes()))

_again, _ = send_file.plan(config.load(), q._day(json.loads((config.SENT / "01-a.json").read_text())["sent_at"]))
check("rerun the same day: the new cap is already spent -> nothing more", _again == [], str([p.stem for p, _ in _again]))

_bad = _entry("h@eight.com", "Eight")
_bad["body"] = _bad["body"].replace("That takes time", "A seamless fix takes time")
_put("08-h", _bad)
with redirect_stdout(io.StringIO()):
    _ok = send_file.send_one(_fake, config.load(), config.OUTBOX / "08-h.json", _bad)
check("send: a lint failure at send time is held, not sent", not _ok and (config.HELD / "08-h.json").exists() and len(_fake.sent) == 3)

_put("09-r", _entry("a@one.com", "One", touch="2", reply_thread_id="t1", reply_to_message_id="m1"))
with redirect_stdout(io.StringIO()):
    send_file.send_one(_fake, config.load(), config.OUTBOX / "09-r.json", json.loads((config.OUTBOX / "09-r.json").read_text()))
_fu = message_from_bytes(__import__("base64").urlsafe_b64decode(_fake.sent[-1][0]))
check("follow-up threads into the original conversation",
      _fake.sent[-1][1] == "t1" and _fu["In-Reply-To"] == "<orig@mail.gmail.com>")

check("tracker path must stay under brain/projects", send_file.tracker_path({"tracker": "../../etc/x.md"}) is None
      and send_file.tracker_path({"tracker": "outbox/x.json"}) is None)

# --- approve.py: the only writer of outbox/ --------------------------------------

_sandbox()


def _drafts(*drafts: dict) -> Path:
    p = Path(tempfile.mkdtemp()) / "drafts.json"
    p.write_text(json.dumps({"project": "Demo Project", "drafts": list(drafts)}), encoding="utf-8")
    return p


def _run_approve(path: Path, *flags: str) -> tuple[int, str]:
    old = sys.argv
    sys.argv = ["approve.py", str(path), *flags]
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            code = approve.main()
    finally:
        sys.argv = old
    return code, buf.getvalue()


def _d(to: str, company: str, tier: str = "CONFIRMED", **extra: object) -> dict:
    d = {"to": to, "company": company, "subject": f"question about {company.lower()}",
         "body": GOOD.replace("Sam", company), "touch": "1", "tier": tier}
    d.update(extra)
    return d


_good_batch = _drafts(_d("sam@acme.com", "Acme"), _d("kim@beta.com", "Beta", tier="PATTERN"))
_code, _out = _run_approve(_good_batch)
check("approve: check-only passes and writes nothing", _code == 0 and not list(config.OUTBOX.glob("*.json")), _out)

_code, _out = _run_approve(_drafts(_d("sam@acme.com", "Acme"), _d("lee@gamma.com", "Gamma", tier="GUESS")), "--send")
check("approve: a GUESS address blocks the whole batch", _code == 1 and not list(config.OUTBOX.glob("*.json")), _out)

_code, _out = _run_approve(_drafts(_d("sam@acme.com", "Acme", body="Hi Sam, short")), "--send")
check("approve: a lint failure blocks the batch", _code == 1 and not list(config.OUTBOX.glob("*.json")))

_code, _out = _run_approve(_drafts(_d("sam@acme.com", "Acme", touch="2")), "--send")
check("approve: a follow-up without its thread id is refused", _code == 1 and "reply_thread_id" in _out)

_code, _out = _run_approve(_good_batch, "--send")
_written = [json.loads(p.read_text()) for p in sorted(config.OUTBOX.glob("*.json"))]
check("approve --send: one entry per draft", _code == 0 and len(_written) == 2, _out)
check("approve --send: entries carry the approval stamp",
      all(e["approved"] is True and e["approved_at"] for e in _written))
check("approve --send: tracker points into the project folder",
      _written[0]["tracker"] == "brain/projects/demo-project/outreach-tracker.md")
check("approve --send: the address tier is not shipped", "tier" not in _written[0])
check("approve --send: entries pass the send-time plan", len(send_file.plan(config.load(), "2026-05-04")[0]) == 2)

_code, _out = _run_approve(_drafts(_d("sam@acme.com", "Acme")), "--send")
check("approve: a second first-touch to the same address is refused", _code == 1 and "already got a first mail" in _out)

# --- config --------------------------------------------------------------------

try:
    config.validate(config.from_dict({}))
    _cfg_raised = ""
except config.ConfigError as exc:
    _cfg_raised = str(exc)
check("config: an empty config refuses to send, naming the fields",
      "sender" in _cfg_raised and "signature.name" in _cfg_raised)
check("config: shipped outreach.config.json parses",
      config.load(config.CONFIG_PATH).caps["max_per_domain_per_day"] == 1)
check("config: unknown timezone falls back to UTC", config.from_dict({"timezone": "Mars/Base"}).tz() is not None)

# --- bounce scope and reply sweep --------------------------------------------------

_rdeny = ("Delivery Status Notification (Failure) Message blocked Your message to lee@gamma.com has been blocked. "
          "The response from the remote server was: 550 5.7.1 RDENY 74.125.228.140: The receiver denied your mail.")
_reputation = ("Delivery Status Notification (Failure) 550 5.7.1 this message is likely suspicious due to the "
               "very low reputation of the sending domain. Message blocked.")
_unknown = ("Delivery Status Notification (Failure) Address not found Your message wasn't delivered to "
            "nobody@example.com because the address couldn't be found.")
check("scope: RDENY is recipient-deny", monitor.classify(_rdeny) == monitor.SCOPE_RECIPIENT)
check("scope: reputation text is spam", monitor.classify(_reputation) == monitor.SCOPE_SPAM)
check("scope: address-not-found is other", monitor.classify(_unknown) == monitor.SCOPE_OTHER)
check("scope: bounced address parsed", monitor.bounced_address(_rdeny) == "lee@gamma.com")
check("scope: 'wasn't delivered to' address parsed", monitor.bounced_address(_unknown) == "nobody@example.com")


def _bounce(blob: str) -> dict:
    scope = monitor.classify(blob)
    return {"subject": "", "snippet": blob[:300], "scope": scope, "to": monitor.bounced_address(blob),
            "spam_signal": scope == monitor.SCOPE_SPAM}


check("pause: one recipient-deny alone does NOT pause", not monitor.decide_pause([_bounce(_rdeny)]))
check("pause: one reputation signal pauses", monitor.decide_pause([_bounce(_reputation)]))
check("pause: three bounces of any kind pause", monitor.decide_pause([_bounce(_rdeny)] * 3))
check("pause: two other bounces do not pause", not monitor.decide_pause([_bounce(_unknown)] * 2))
check("delay notice is not a bounce", monitor.is_delay_notice("Delivery Status Notification (Delay)"))
check("mailer-daemon inside a tracked thread is not a reply", monitor.is_bounce_sender("Mail Delivery Subsystem <mailer-daemon@googlemail.com>"))
check("a human sender is a reply", not monitor.is_bounce_sender("Sam <sam@acme.com>"))


def _msg(ts: int, *labels: str) -> dict:
    return {"internalDate": str(ts), "labelIds": list(labels)}


check("answered: our reply after theirs -> not waiting",
      monitor.already_answered({"messages": [_msg(1, "SENT"), _msg(2, "INBOX"), _msg(3, "SENT")]}))
check("answered: their message is newest -> waiting", not monitor.already_answered({"messages": [_msg(1, "SENT"), _msg(2, "INBOX")]}))
check("answered: an unsent draft is not an answer",
      not monitor.already_answered({"messages": [_msg(1, "SENT"), _msg(2, "INBOX"), _msg(3, "DRAFT")]}))
check("answered: empty thread -> waiting", not monitor.already_answered({}))


class _FakeMonitorGmail:
    def __init__(self, labels: dict[str, list[str]]) -> None:
        self.labels = labels

    def search(self, query: str, max_results: int = 100) -> list[dict]:
        return [{"id": mid, "threadId": "t-acme"} for mid in self.labels] if query.startswith("in:inbox") else []

    def get_thread(self, thread_id: str) -> dict:
        return {"messages": [_msg(1, "SENT")] + [_msg(2, *ls) for ls in self.labels.values()]}

    def get_message(self, message_id: str) -> dict:
        return {"labelIds": self.labels[message_id], "snippet": "No thanks",
                "payload": {"headers": [{"name": "From", "value": "sam@acme.com"}]}}

    def label_id(self, name: str) -> str:
        return "L-alerted"

    def add_label(self, message_id: str, label_id: str) -> dict:
        self.labels[message_id] = self.labels[message_id] + [label_id]
        return {}


_mrows = [q.Row("t-acme", "d1", "sam@acme.com", "Acme", "1", "", "pass", "sent", "2026-05-04T08:00:00+00:00")]
_fm = _FakeMonitorGmail({"m-no": ["INBOX"]})
_first = monitor.scan(_fm, _mrows)
check("alert once: first run reports the reply", len(_first["replies"]) == 1 and _first["replies"][0]["company"] == "Acme")
monitor.mark_alerted(_fm, _first["replies"])
check("alert once: second run is silent", monitor.scan(_fm, _mrows)["replies"] == [])
_fm.labels["m-new"] = ["INBOX"]
check("alert once: a NEW message in the same thread still alerts",
      [r["message_id"] for r in monitor.scan(_fm, _mrows)["replies"]] == ["m-new"])
check("monitor: an untracked thread is never read", monitor.scan(_FakeMonitorGmail({"m": ["INBOX"]}), [])["replies"] == [])

# --- report --------------------------------------------------------------------


def test_engine() -> None:
    """pytest entry point: the checks above ran at import; fail if any failed."""
    failed = [f"{n} {d}" for s, n, d in results if s == FAIL]
    assert not failed, failed


if __name__ == "__main__":
    width = max(len(n) for _, n, _ in results)
    for status, name, detail in results:
        print(f"[{status}] {name.ljust(width)}" + (f"  {detail}" if detail and status == FAIL else ""))
    failed = [r for r in results if r[0] == FAIL]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
