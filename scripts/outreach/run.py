"""The daily monitor: what `.github/workflows/outreach.yml` calls. It never sends outreach.

1. Scan Gmail for replies and bounces on every thread in `outbox/sent/`.
2. Auto-pause (paused: true in outreach.config.json) on a spam or reputation
   signal, or more than 2 bounces. The send Action respects the flag.
3. E-mail you a digest when there is something to say.
4. Write `heartbeat.md` on every path, success or failure.

The heartbeat is the guard that survives everything else being misconfigured.
A lane that can only report a problem by successfully sending a message goes
quiet when it breaks, and quiet looks exactly like healthy. Here silence is the
alarm: /outreach reads the heartbeat before it stages anything, and says so when
the last run is more than 36 hours old or ended in an error.
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

import alert
import config
import monitor
import send_file
from gmail_auth import Gmail, GmailError

HEARTBEAT = Path(__file__).resolve().parent / "heartbeat.md"


def write_heartbeat(status: str, replies: int = 0, bounces: int = 0, held: int = 0,
                    sent_last_day: int = 0, note: str = "") -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    # One line: the file is read as `key: value`, and Gmail's error bodies are
    # multi-line, which would swallow the keys after the note.
    note = " ".join(note.split())[:300]
    HEARTBEAT.write_text(
        "# Outreach engine heartbeat\n\n"
        "Written by the daily monitor on every run, success or failure. If last_run is\n"
        "more than 36 hours old, the monitor is not running: check the Actions tab.\n\n"
        f"last_run: {now}\nstatus: {status}\nsent_last_day: {sent_last_day}\n"
        f"replies: {replies}\nbounces: {bounces}\nheld: {held}\nnote: {note}\n",
        encoding="utf-8",
    )
    print(f"heartbeat: {status} at {now}")


def _entries(folder: Path) -> list[dict]:
    out = []
    for p in sorted(folder.glob("*.json")):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
    return out


def recent(entries: list[dict], key: str, hours: int = 26) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    out = []
    for e in entries:
        try:
            when = datetime.fromisoformat(str(e.get(key, "")).split()[0])
        except ValueError:
            continue
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        if when >= cutoff:
            out.append(e)
    return out


def main() -> int:
    settings = config.load()
    if not settings.sender and not os.environ.get("GMAIL_REFRESH_TOKEN"):
        # The pack is installed but not set up: stay green and quiet, so a user
        # who never turned outreach on gets no daily failure e-mails from GitHub.
        print("Outreach is not set up (no sender, no Gmail token): nothing to monitor.")
        return 0
    try:
        config.validate(settings)
        gmail = Gmail(settings.sender)
        findings = monitor.scan(gmail, send_file.sent_rows())

        paused = settings.paused
        if findings["should_pause"] and not paused:
            config.save_paused(True)
            paused = True
            print("PAUSED on a bounce or spam signal.")

        held = [{"company": e.get("company", "?"), "to": e.get("to", "?"), "why": e.get("held_reason", [])}
                for e in recent(_entries(config.HELD), "held_at")]
        sent = recent(_entries(config.SENT), "sent_at")

        note = ""
        if alert.run(settings.digest_to, findings, held, sent, paused, gmail):
            try:
                monitor.mark_alerted(gmail, findings["replies"])
            except GmailError as exc:
                # A failed label only means the reply alerts once more.
                note = f"alerted-label failed: {exc}"
                print(f"WARN: {note}", file=sys.stderr)

        write_heartbeat("ok", replies=len(findings["replies"]), bounces=len(findings["bounces"]),
                        held=len(held), sent_last_day=len(sent), note=("paused " if paused else "") + note)
        return 0
    except (GmailError, config.ConfigError) as exc:
        write_heartbeat("error", note=str(exc)[:300])
        print(f"FATAL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 (the job must go red on anything)
        write_heartbeat("error", note=f"{type(exc).__name__}: {exc}"[:300])
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
