"""The blocking lint gate.

Every outbox entry is linted at send time, signature included. A mail that fails
does not send: it moves to `outbox/held/` with the reasons, and the digest lists
it. `approve.py` runs the same check before anything reaches the outbox, so a
failing draft is fixed in chat instead of discovered by the Action.

Two kinds of check, and the second matters more:

1. Style tells (ban list): phrases that make a cold mail read as machine-written
   or salesy. English by default; add phrases for the language you write in
   under `extra_banned_phrases` in outreach.config.json.
2. Structural checks, language-independent. They catch generation failures (an
   unreplaced {{company}}, an empty body, a truncated draft, a name that did not
   merge) rather than matters of taste. Those are the realistic risk: a template
   artefact reaching a real person.

Keep the English list in sync with the writing skill's ban list when it changes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import config
import signature

BANNED_EN = [
    "delve", "leverage", "unlock", "harness the power", "robust", "seamless",
    "cutting-edge", "game-changer", "game-changing", "revolutionize", "transformative",
    "elevate your", "empower", "unleash", "tapestry", "realm", "synergy", "holistic",
    "paradigm", "moving forward", "circle back", "touch base", "myriad", "plethora",
    "in today's", "the world of", "a testament to", "at the end of the day",
    "i hope this email finds you well", "i hope this finds you well", "i just wanted to",
    "i wanted to reach out", "let's dive in", "in a nutshell", "the bottom line is",
    "without further ado", "don't hesitate to reach out",
]

# Template artefacts that mean generation broke.
PLACEHOLDERS = [
    r"\{\{.*?\}\}", r"\{[a-z_]+\}", r"\[[A-Z_]{2,}\]",
    r"\bTODO\b", r"\bTBD\b", r"\bXXX\b", r"\bLOREM\b",
    r"<[a-z_]+>", r"\bINSERT\b", r"\bPLACEHOLDER\b",
]

MIN_BODY_CHARS = 200   # shorter than this on a cold touch is almost always a truncated draft
MAX_BODY_CHARS = 1800  # replies drop hard past ~200 words
MAX_EM_DASHES = 0      # zero dashes in prose: the strongest single machine-writing tell
URL_RE = re.compile(r"https?://|www\.", re.I)
EM_DASH = "\u2014"
SPACED_EN_DASH = re.compile(" \u2013 ")
SALUTATIONS = r"hi|hello|hey|dear|hallo|beste|bonjour|hola|ciao|ola"


@dataclass
class LintResult:
    passed: bool
    failures: list[str]

    @property
    def summary(self) -> str:
        return "pass" if self.passed else "; ".join(self.failures)[:200]


def check(subject: str, body: str, touch: str = "1") -> LintResult:
    """Run every gate. Returns all failures, not just the first, so a held mail
    is fixable in one pass.

    `touch`: "1" = first cold mail (link-free), "2", "3"... = follow-ups,
    "reply" = an answer to someone who wrote back (links fine, no minimum length).
    """
    failures: list[str] = []
    touch = str(touch).strip()

    # A reply carries the previous mail quoted underneath. Gating on the whole
    # blob lets that quote spend THIS mail's budget (a dash in the quoted mail
    # would hold a clean reply) and pads a too-short reply past the minimum.
    # Every gate below judges only the copy above the quote.
    body = signature.split_quote(body)[0].rstrip() or body
    low = f"{subject}\n{body}".lower()

    if not subject.strip():
        failures.append("empty subject")
    if not body.strip():
        failures.append("empty body")

    for pattern in PLACEHOLDERS:
        found = re.search(pattern, f"{subject}\n{body}")
        if found:
            failures.append(f"unreplaced placeholder: {found.group(0)!r}")

    n = len(body.strip())
    if 0 < n < MIN_BODY_CHARS and touch != "reply":
        failures.append(f"body suspiciously short ({n} chars, min {MIN_BODY_CHARS}): likely truncated")
    if n > MAX_BODY_CHARS:
        failures.append(f"body too long ({n} chars, max {MAX_BODY_CHARS})")

    # A first cold mail is link-free: better inbox placement, and the reply to
    # "can I send you an example?" is the engagement signal. Links go in touch 2+.
    if touch == "1" and URL_RE.search(body):
        failures.append("touch 1 must be link-free (move the link to the reply after a yes)")

    if re.search(rf"\b(?:{SALUTATIONS})\s*[,\.]", body, re.I):
        failures.append("empty salutation: the name did not merge")

    dashes = body.count(EM_DASH) + len(SPACED_EN_DASH.findall(body))
    if dashes > MAX_EM_DASHES:
        failures.append(f"{dashes} dash(es) used as punctuation (max {MAX_EM_DASHES})")

    for phrase in BANNED_EN + config.load().extra_banned_phrases:
        if phrase and phrase in low:
            failures.append(f"ban-list: {phrase!r}")

    if re.search(r"it'?s not just .{1,60}(?:\u2014|-|,|it'?s)", low):
        failures.append("ban-list pattern: \"it's not just X, it's Y\"")

    return LintResult(passed=not failures, failures=failures)
