"""Daily caps for the send lane, and the per-project tracker table.

Named `send_queue`, not `queue`: a module called `queue` shadows the stdlib
module that `urllib3` (inside `requests`) imports.

Two jobs:

1. **Caps.** `eligible()` decides which pending outbox entries may go out on
   this run: a budget for first touches, a budget for follow-ups, one ceiling
   over both, and at most N mails per recipient domain per day. Fresh rows are
   picked first, so a backlog of follow-ups can never starve new contacts. A
   follow-up goes to someone already contacted; counting it against the daily
   number lets a day of pure follow-ups look like a day of outreach.
   Re-running on the same day is a no-op: mails already sent today count
   against their own budget and the ceiling, because a scheduled GitHub run can
   fire late or twice.

2. **The tracker.** A markdown table in the brain
   (`brain/projects/<slug>/outreach-tracker.md`) so the user and Claude can read
   what went out, to whom, and when. The send Action adds a row per sent mail.

Tracker format:

    ---
    type: tracker
    ---
    | thread_id | draft_id | to | company | touch | staged | lint | status | sent_at |
    |---|---|---|---|---|---|---|---|---|
    | 19f5... | 2026-05-04-acme-1 | sam@acme.com | Acme | 1 | 2026-05-04 | pass | sent | 2026-05-04T08:01:00+00:00 |

Status values: staged (approved, waiting to send), held (failed lint), sent,
replied, bounced, closed (deliberately dropped).

No YAML dependency on purpose: the frontmatter is a few scalars.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, tzinfo
from pathlib import Path

import config

COLUMNS = ["thread_id", "draft_id", "to", "company", "touch", "staged", "lint", "status", "sent_at"]
SENDABLE = "staged"
CAP_KEYS = ("max_new_per_day", "max_followups_per_day", "max_total_per_day", "max_per_domain_per_day")


def _day(iso: str, tz: tzinfo | None = None) -> str:
    """The calendar date of an ISO timestamp in the user's timezone (naive = UTC).

    A hand-annotated `sent_at` with a trailing note ("2026-05-04T08:01:00+00:00
    (resent)") must not crash the run, so only the leading token is parsed.
    """
    dt = datetime.fromisoformat(iso.split()[0])
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(tz or config.load().tz()).date().isoformat()


@dataclass
class Config:
    paused: bool = False
    max_per_day: int = 20           # legacy alias, kept == max_total_per_day
    max_new_per_day: int = 10       # touch 1: the real outreach number
    max_followups_per_day: int = 10  # touch 2+, on top of the fresh batch
    max_total_per_day: int = 20     # hard ceiling over both, for deliverability
    max_per_domain_per_day: int = 1
    raw: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_settings(cls, settings: config.Settings) -> "Config":
        cfg = cls(paused=settings.paused)
        seen = set()
        for key in CAP_KEYS:
            if key in settings.caps:
                setattr(cfg, key, int(settings.caps[key]))
                seen.add(key)
        _resolve_caps(cfg, seen)
        return cfg


@dataclass(frozen=True)
class Budgets:
    """What is still spendable today, per class and overall."""

    new: int
    followup: int
    total: int


def is_fresh(touch: str) -> bool:
    """True for a first-touch cold email.

    An unset or garbled `touch` (including "reply") counts as fresh on purpose:
    the failure we can afford is one first touch too few, never a mail spending
    budget it was not granted.
    """
    try:
        return int((touch or "").strip()) <= 1
    except ValueError:
        return True


def _resolve_caps(cfg: Config, seen: set[str]) -> None:
    """Reconcile the `max_per_day` alias with the split caps.

    A bare `max_per_day: 8` sets the ceiling AND both class budgets, so it never
    sends more than it said. An explicit split key always wins for its own
    dimension. With neither, the total is new + follow-up.
    """
    if "max_per_day" in seen:
        alias = cfg.max_per_day
        for key in ("max_total_per_day", "max_new_per_day", "max_followups_per_day"):
            if key not in seen:
                setattr(cfg, key, alias)
    elif "max_total_per_day" not in seen:
        cfg.max_total_per_day = cfg.max_new_per_day + cfg.max_followups_per_day
    cfg.max_per_day = cfg.max_total_per_day


@dataclass
class Row:
    thread_id: str = ""
    draft_id: str = ""
    to: str = ""
    company: str = ""
    touch: str = ""
    staged: str = ""
    lint: str = ""
    status: str = ""
    sent_at: str = ""

    @property
    def domain(self) -> str:
        return self.to.split("@")[-1].strip().strip(">").lower() if "@" in self.to else ""

    def as_cells(self) -> list[str]:
        return [(getattr(self, c) or "").replace("|", "/") for c in COLUMNS]


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    if value.lstrip("-").isdigit():
        return int(value)
    return value


def load(path: Path) -> tuple[Config, list[Row]]:
    """Read a tracker (or any table in this format). Frontmatter cap keys, if
    present, are honoured; the live send lane takes its caps from the config."""
    if not path.exists():
        raise FileNotFoundError(f"Tracker not found at {path}.")
    text = path.read_text(encoding="utf-8")

    cfg = Config()
    body = text
    if text.startswith("---"):
        _, front, body = text.split("---", 2)
        for line in front.splitlines():
            if ":" not in line or line.strip().startswith("#"):
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            parsed = _parse_scalar(value.split("#", 1)[0])
            cfg.raw[key] = value.strip()
            if hasattr(cfg, key) and key != "raw":
                setattr(cfg, key, parsed)
    _resolve_caps(cfg, set(cfg.raw))

    rows: list[Row] = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or cells[0] == "thread_id" or (set(cells[0]) <= {"-", ":"} and cells[0]):
            continue
        if not any(cells):
            continue
        cells += [""] * (len(COLUMNS) - len(cells))
        rows.append(Row(**dict(zip(COLUMNS, cells[: len(COLUMNS)]))))
    return cfg, rows


def save(cfg: Config, rows: list[Row], path: Path, title: str = "Outreach tracker") -> None:
    """Write the table back. Frontmatter keys are kept exactly as they were read."""
    front = dict(cfg.raw) or {"type": "tracker", "status": "active"}
    lines = ["---", *[f"{k}: {v}" for k, v in front.items()], "---", "", f"# {title}", ""]
    lines += [
        "Written by the outreach send Action after each mail, and by Claude when a reply or bounce comes in.",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    lines += ["| " + " | ".join(r.as_cells()) + " |" for r in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def upsert(path: Path, new: Row) -> None:
    """Add or update one row (matched on draft_id), creating the tracker if needed."""
    cfg, rows = load(path) if path.exists() else (Config(), [])
    for i, r in enumerate(rows):
        if r.draft_id and r.draft_id == new.draft_id:
            rows[i] = new
            break
    else:
        rows.append(new)
    save(cfg, rows, path)


def sent_today(rows: list[Row], today: str, tz: tzinfo | None = None) -> list[Row]:
    """Rows already dispatched on this calendar day (user's timezone)."""
    return [r for r in rows if r.status == "sent" and r.sent_at and _day(r.sent_at, tz) == today]


def remaining(cfg: Config, rows: list[Row], today: str | None = None, tz: tzinfo | None = None) -> Budgets:
    """Budget left today, per class and overall."""
    today = today or config.load().today()
    done = sent_today(rows, today, tz)
    fresh = sum(1 for r in done if is_fresh(r.touch))
    return Budgets(
        new=max(0, cfg.max_new_per_day - fresh),
        followup=max(0, cfg.max_followups_per_day - (len(done) - fresh)),
        total=max(0, cfg.max_total_per_day - len(done)),
    )


def eligible(cfg: Config, rows: list[Row], today: str | None = None, tz: tzinfo | None = None) -> list[Row]:
    """Rows that may send on this run, after every cap. Fresh rows first."""
    if cfg.paused:
        return []
    today = today or config.load().today()

    budgets = remaining(cfg, rows, today, tz)
    if budgets.total <= 0:
        return []

    domain_counts: dict[str, int] = {}
    for r in sent_today(rows, today, tz):
        domain_counts[r.domain] = domain_counts.get(r.domain, 0) + 1

    def take(candidates: list[Row], budget: int, room: int) -> list[Row]:
        limit = max(0, min(budget, room))
        picked: list[Row] = []
        for row in candidates:
            if len(picked) >= limit:
                break
            if row.status != SENDABLE or not row.draft_id or "@" not in row.to:
                continue
            if domain_counts.get(row.domain, 0) >= cfg.max_per_domain_per_day:
                continue
            domain_counts[row.domain] = domain_counts.get(row.domain, 0) + 1
            picked.append(row)
        return picked

    fresh = take([r for r in rows if is_fresh(r.touch)], budgets.new, budgets.total)
    follow = take([r for r in rows if not is_fresh(r.touch)], budgets.followup, budgets.total - len(fresh))
    return fresh + follow
