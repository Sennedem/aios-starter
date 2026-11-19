"""The outreach engine's settings: who sends, how they sign, how much per day.

Two kinds of setting, kept in two places on purpose:

- Secrets (the three Gmail OAuth values) live in the gitignored `.env` on your
  machine and in GitHub Actions secrets. Never in this file. See SETUP-GMAIL.md.
- Everything else lives in `outreach.config.json` next to this file. It is
  committed, because the GitHub Action that sends your mail has no access to
  your `.env`. Nothing in it is secret: your address and your signature end up
  in every mail you send anyway. Your backup repo must be private regardless.

Fill the config once (the /outreach skill walks you through it). `validate()`
refuses to send while a required field is still empty, so a half-filled config
can never put a blank signature under a real e-mail.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone, tzinfo
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG_PATH = HERE / "outreach.config.json"

# The outbox is the ONLY folder the send Action reads. An entry lands here only
# when the user said "send" (approve.py writes it). Drafts live in tmp/outreach/,
# which is gitignored, so a session-end backup push can never turn a draft into
# a send.
OUTBOX = ROOT / "outbox"
SENT = OUTBOX / "sent"
HELD = OUTBOX / "held"
DRAFTS = ROOT / "tmp" / "outreach"

DEFAULT_CAPS = {
    "max_new_per_day": 10,
    "max_followups_per_day": 10,
    "max_total_per_day": 20,
    "max_per_domain_per_day": 1,
}


class ConfigError(ValueError):
    """A required setting is missing or malformed. The message says which."""


@dataclass
class Signature:
    name: str = ""
    role: str = ""
    closing: str = "Best regards,"
    photo_url: str = ""
    links: list[dict] = field(default_factory=list)  # [{"label": ..., "url": ...}], touch 2+ only

    def clean_links(self) -> list[dict]:
        return [
            {"label": str(l.get("label", "")).strip(), "url": str(l.get("url", "")).strip()}
            for l in self.links
            if isinstance(l, dict) and str(l.get("url", "")).strip()
        ]


@dataclass
class Settings:
    sender: str = ""
    send_as: list[str] = field(default_factory=list)
    alert_to: str = ""
    timezone: str = "UTC"
    paused: bool = False
    caps: dict = field(default_factory=lambda: dict(DEFAULT_CAPS))
    signature: Signature = field(default_factory=Signature)
    extra_banned_phrases: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    @property
    def allowed_from(self) -> frozenset[str]:
        """Addresses a mail may go out from: the account plus verified aliases."""
        return frozenset(a.strip().lower() for a in [self.sender, *self.send_as] if a.strip())

    @property
    def digest_to(self) -> str:
        return (self.alert_to or self.sender).strip()

    def tz(self) -> tzinfo:
        """The user's timezone, for the daily-cap day boundary. Falls back to UTC
        when the name is unknown (or the zone database is missing, as on some
        Windows Pythons): a wrong boundary shifts the cap by hours, never doubles it."""
        try:
            from zoneinfo import ZoneInfo

            return ZoneInfo(self.timezone or "UTC")
        except Exception:  # noqa: BLE001
            return timezone.utc

    def today(self) -> str:
        return datetime.now(self.tz()).date().isoformat()


def from_dict(data: dict) -> Settings:
    sig = data.get("signature") or {}
    caps = {**DEFAULT_CAPS, **{k: int(v) for k, v in (data.get("caps") or {}).items() if k in DEFAULT_CAPS}}
    return Settings(
        sender=str(data.get("sender", "")).strip(),
        send_as=[str(a) for a in data.get("send_as") or []],
        alert_to=str(data.get("alert_to", "")).strip(),
        timezone=str(data.get("timezone", "UTC")).strip() or "UTC",
        paused=bool(data.get("paused", False)),
        caps=caps,
        signature=Signature(
            name=str(sig.get("name", "")).strip(),
            role=str(sig.get("role", "")).strip(),
            closing=str(sig.get("closing", "Best regards,")).strip() or "Best regards,",
            photo_url=str(sig.get("photo_url", "")).strip(),
            links=list(sig.get("links") or []),
        ),
        extra_banned_phrases=[str(p).lower() for p in data.get("extra_banned_phrases") or [] if str(p).strip()],
        raw=dict(data),
    )


_override: Settings | None = None


def use(data: dict | Settings | None) -> None:
    """Swap in settings without touching the file. Tests use this; pass None to reset."""
    global _override
    _override = from_dict(data) if isinstance(data, dict) else data


def load(path: Path | None = None) -> Settings:
    if _override is not None and path is None:
        return _override
    path = path or CONFIG_PATH
    if not path.exists():
        return from_dict({})
    return from_dict(json.loads(path.read_text(encoding="utf-8")))


def save_paused(paused: bool, path: Path | None = None) -> None:
    """Flip the kill switch in the file, keeping every other key as the user wrote it."""
    path = path or CONFIG_PATH
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    data["paused"] = paused
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate(settings: Settings) -> None:
    """Raise ConfigError naming every empty required field, all at once."""
    missing = []
    if "@" not in settings.sender:
        missing.append("sender (the Gmail address you send from)")
    if not settings.signature.name:
        missing.append("signature.name")
    if settings.signature.photo_url and not settings.signature.photo_url.startswith("https://"):
        missing.append("signature.photo_url must start with https:// (or leave it empty)")
    if missing:
        raise ConfigError(
            f"{CONFIG_PATH.name} is not filled in yet: " + "; ".join(missing)
            + ". Run /outreach and ask it to set up the sender, or edit the file."
        )
