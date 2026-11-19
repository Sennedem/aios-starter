"""The digest e-mail: replies, bounces, held mail and a paused engine, the same day.

It only sends when there is something to say. A daily "nothing happened" mail
trains you to ignore it, which is how a dead engine hides in a full inbox. A
silent engine is caught by the heartbeat instead (run.py).

Goes to `alert_to` in outreach.config.json, or to the sender when that is empty.
"""

from __future__ import annotations

import textwrap

from gmail_auth import Gmail


def build(findings: dict, held: list[dict], sent: list[dict], paused: bool) -> tuple[str, str] | None:
    replies = findings.get("replies", [])
    bounces = findings.get("bounces", [])
    if not (replies or bounces or held or paused):
        return None

    # The subject alone should say whether to open it.
    if replies:
        headline = f"{len(replies)} REPLY" + ("" if len(replies) == 1 else "S")
    elif paused:
        headline = "ENGINE PAUSED"
    elif bounces:
        headline = f"{len(bounces)} bounce(s)"
    else:
        headline = f"{len(held)} held by lint"
    subject = f"Outreach: {headline}"

    parts: list[str] = []
    if paused:
        parts.append(
            "ENGINE IS PAUSED\n"
            "Nothing will send until paused is set back to false in scripts/outreach/outreach.config.json.\n"
            "Read the bounces below first: send again only once you know why it paused.\n"
        )
    if replies:
        parts.append("REPLIES: these need you\n" + "=" * 40)
        for r in replies:
            parts.append(
                f"\n{r['company']}\nFrom:    {r['from']}\nSubject: {r['subject']}\nDate:    {r['date']}\n\n"
                f"{textwrap.fill(r['snippet'], 78)}\n"
            )
    if bounces:
        parts.append("\nBOUNCES\n" + "=" * 40)
        for b in bounces:
            flag = "  [SPAM SIGNAL: engine pauses]" if b.get("spam_signal") else ""
            parts.append(
                f"\n{b.get('scope', 'other')} ({b.get('to') or 'address not stated'}){flag}\n"
                f"{b['subject']}\n{textwrap.fill(b['snippet'], 78)}\n"
            )
    if held:
        parts.append("\nHELD: did not send (see outbox/held/)\n" + "=" * 40)
        for h in held:
            parts.append(f"\n{h.get('company', '?')} <{h.get('to', '?')}>\n  " + "\n  ".join(h.get("why", [])) + "\n")
    if sent:
        parts.append(f"\nSENT IN THE LAST DAY: {len(sent)}\n" + "=" * 40)
        for s in sent:
            parts.append(f"  {s.get('company', '?')} <{s.get('to', '?')}> touch {s.get('touch', '1')}: {s.get('subject', '')}")
    return subject, "\n".join(parts)


def run(to: str, findings: dict, held: list[dict], sent: list[dict], paused: bool, gmail: Gmail) -> bool:
    built = build(findings, held, sent, paused)
    if not built:
        print("Nothing to report: no digest sent.")
        return False
    subject, body = built
    gmail.send_new(to, subject, body)
    print(f"Digest sent: {subject}")
    return True
