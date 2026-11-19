"""The signature block the Gmail API will never add for you.

Gmail's signature is a compose-window feature: the web and mobile apps paste it
in, the server does not. Anything sent through the API arrives without it. So
the engine carries its own signature (from `outreach.config.json`) and appends
it at send time.

Two versions, and the split is deliberate:

- **Touch 1** (the first cold mail) carries the name, the role and, if you set
  one, a small photo. No links: a first cold mail stays link-free for
  deliverability, and lint blocks a link at touch 1. A face is not a link, and
  recipients report that a real photo is what makes a cold mail read as written
  by a person.
- **Touch 2+ and replies** land in a thread the recipient already has, where
  links are allowed. They get the links from the config as well.

Appending at send time is the load-bearing choice: the drafting step cannot
forget it, and the Claude Gmail connector strips <img> tags from drafts it
creates, so a photo only survives when the engine writes the MIME itself.
"""

from __future__ import annotations

import base64
import re
from email import message_from_bytes
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

# Our own HTML insertion is fenced, so re-applying replaces rather than stacks.
HTML_OPEN = "<!-- outreach-sig -->"
HTML_CLOSE = "<!-- /outreach-sig -->"
_FENCED_RE = re.compile(re.escape(HTML_OPEN) + ".*?" + re.escape(HTML_CLOSE), re.S)

# Closings that are sign-off remnants, not copy. Stripped before the canonical
# block goes on, so "Best regards,\nAlex" does not become "Alex\nAlex Example".
_COMMON_CLOSINGS = (
    "best regards", "kind regards", "warm regards", "regards", "best", "cheers",
    "sincerely", "all the best",
)
_MAX_STRIPPED_LINES = 6

# A reply carries the quoted thread BELOW the sign-off, so appending at the end
# of the body would bury the signature under the quote. Everything from the
# first quote marker down is held aside, signed above, re-attached untouched.
# Attribution lines in the languages Gmail most often writes them in.
_TEXT_QUOTE_RE = re.compile(
    r"^(?:"
    r"On\s.{0,160}?wrote:"
    r"|Am\s.{0,160}?schrieb.{0,80}?:"
    r"|Le\s.{0,160}?a\s+écrit\s*:"
    r"|El\s.{0,160}?escribió:"
    r"|Op\s.{0,160}?schreef.{0,80}?:"
    r"|-{2,}\s?Original Message"
    r"|_{5,}"
    r"|>.*"
    r")\s*$",
    re.M,
)

_HTML_QUOTE_MARKERS = (
    '<div class="gmail_extra"',
    '<blockquote class="gmail_quote"',
    '<div class="gmail_quote"',
    "<blockquote",
)


def _sig() -> config.Signature:
    return config.load().signature


def split_quote(body: str) -> tuple[str, str]:
    """(copy above the quoted thread, the quote itself); quote may be empty."""
    match = _TEXT_QUOTE_RE.search(body)
    if not match:
        return body, ""
    return body[: match.start()], body[match.start() :]


def split_quote_html(html: str) -> tuple[str, str]:
    lowered = html.lower()
    cut = len(html)
    for marker in _HTML_QUOTE_MARKERS:
        found = lowered.find(marker)
        if found != -1:
            cut = min(cut, found)
    return html[:cut], html[cut:]


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _is_first(touch: str) -> bool:
    return str(touch).strip() == "1"


def text_block(touch: str = "1") -> str:
    """The plain-text signature. Touch 1 stays URL-free by design."""
    sig = _sig()
    lines = [sig.closing, "", sig.name]
    if sig.role:
        lines.append(sig.role)
    links = sig.clean_links()
    if not _is_first(touch) and links:
        lines.append(" | ".join(f"{l['label']}: {l['url']}" if l["label"] else l["url"] for l in links))
    return "\n".join(lines)


def html_block(touch: str = "1") -> str:
    """The HTML signature: optional photo, name, role, and links from touch 2 on."""
    sig = _sig()
    font = "font-family:Arial,Helvetica,sans-serif;"
    rows = (
        f'<tr><td style="{font}font-size:16px;font-weight:bold;color:#111827;padding:0 0 2px 0;">'
        f"{_escape(sig.name)}</td></tr>"
    )
    if sig.role:
        rows += (
            f'<tr><td style="{font}font-size:12px;color:#4B5563;padding:0 0 8px 0;">'
            f"{_escape(sig.role)}</td></tr>"
        )
    links = sig.clean_links()
    if not _is_first(touch) and links:
        anchors = '<span style="color:#9CA3AF;">&nbsp;|&nbsp;</span>'.join(
            f'<a href="{_escape(l["url"])}" style="color:#1D4ED8;text-decoration:none;">'
            f'{_escape(l["label"] or l["url"])}</a>'
            for l in links
        )
        rows += f'<tr><td style="{font}font-size:12px;padding:0;">{anchors}</td></tr>'

    photo = ""
    if sig.photo_url:
        photo = (
            '<td valign="middle" style="padding:0 14px 0 0;">'
            f'<img src="{_escape(sig.photo_url)}" width="64" height="64" alt="{_escape(sig.name)}" '
            'style="display:block;width:64px;height:64px;border-radius:50%;"></td>'
        )
    body = (
        f'<p style="{font}font-size:14px;color:#111827">{_escape(sig.closing)}</p>'
        '<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"><tr>'
        f'{photo}<td valign="middle"><table cellpadding="0" cellspacing="0" border="0" '
        f'style="border-collapse:collapse;">{rows}</table></td></tr></table>'
    )
    return f"{HTML_OPEN}{body}{HTML_CLOSE}"


def _signoff_lines() -> set[str]:
    sig = _sig()
    names = {sig.name.lower(), sig.name.split(" ")[0].lower()} if sig.name else set()
    return {*_COMMON_CLOSINGS, sig.closing.lower().rstrip(",."), sig.role.lower(), *names} - {""}


def _is_link_row(line: str) -> bool:
    bare_urls = [l["url"].removeprefix("https://").removeprefix("http://").lower() for l in _sig().clean_links()]
    low = line.lower()
    return any(u and u in low for u in bare_urls)


def strip_signoff(body: str) -> str:
    """Drop a trailing sign-off so the canonical block replaces it.

    Bounded to a few lines: an unexpected shape must lose nothing but the last
    couple of lines, never eat into the argument of the email.
    """
    known = _signoff_lines()
    lines = body.rstrip().split("\n")
    for _ in range(_MAX_STRIPPED_LINES):
        while lines and not lines[-1].strip():
            lines.pop()
        if not lines:
            break
        last = lines[-1].strip().rstrip(",.!").lower()
        if last in known or _is_link_row(last):
            lines.pop()
            continue
        break
    return "\n".join(lines).rstrip()


def sign_text(body: str, touch: str = "1") -> str:
    """Idempotent: signing an already-signed body returns the same string.

    On a reply the block goes above the quoted thread, never below it.
    """
    head, quote = split_quote(body)
    signed = f"{strip_signoff(head)}\n\n{text_block(touch)}\n"
    if quote:
        return f"{signed}\n{quote}"
    return signed


def _html_signoff_re() -> re.Pattern:
    sig = _sig()
    closings = sorted({*_COMMON_CLOSINGS, sig.closing.lower().rstrip(",.")} - {""}, key=len, reverse=True)
    names = sorted({sig.name.lower(), sig.name.split(" ")[0].lower()} - {""}, key=len, reverse=True) if sig.name else []
    gap = r"(?:<br\s*/?>|<p[^>]*>|</p>|<div[^>]*>|&nbsp;|\s)*"
    name_part = (r"(?:" + "|".join(re.escape(n) for n in names) + r")?[,\.]?") if names else ""
    return re.compile(
        gap + r"(?:" + "|".join(re.escape(c) for c in closings) + r")[,\.!]?" + gap + name_part + gap
        # Only strip when nothing but closing tags follows: mid-body prose that
        # happens to contain "regards" must stay exactly where it is.
        + r"(?=(?:</(?:div|p|span|td|tr|table|tbody|body|html)>|\s)*$)",
        re.I,
    )


def strip_signoff_html(html: str) -> str:
    """Drop a trailing sign-off from an HTML body, tags left intact."""
    return _html_signoff_re().sub("", html, count=1)


def sign_html(html: str, touch: str = "1") -> str | None:
    """Append the HTML signature, or None if the draft already carries one.

    An unfenced signature means it was typed in upstream: leave it alone rather
    than print the name twice. The skill tells the drafting step not to do that.
    """
    stripped = _FENCED_RE.sub("", html)
    head, quote = split_quote_html(stripped)

    # The guard looks only ABOVE the quote. A reply quotes the previous touch,
    # signature and all, so testing the whole body would report "already
    # signed" for every reply and skip the block.
    sig = _sig()
    marker = sig.role or sig.name
    if marker and (marker in head or _escape(marker) in head):
        return None

    head = strip_signoff_html(head)
    block = html_block(touch)
    if quote:
        return head + block + quote
    for close in ("</body>", "</html>"):
        if close in head.lower():
            index = head.lower().rindex(close)
            return head[:index] + block + head[index:]
    return head + block


def _decode(part: Message) -> str:
    payload = part.get_payload(decode=True) or b""
    return payload.decode(part.get_content_charset() or "utf-8", "replace")


def _set(part: Message, text: str) -> None:
    del part["Content-Transfer-Encoding"]
    part.set_payload(text, charset="utf-8")


def _text_to_html(text: str) -> str:
    """A minimal HTML twin of a plain-text body."""
    return '<div dir="auto">' + _escape(text).replace("\n", "<br>") + "</div>"


def _with_html_twin(message: Message) -> Message:
    """Guarantee a text/html part, because the photo only lives in one.

    A message with an attachment (multipart/mixed) keeps it: the text/plain leaf
    is swapped in place for a multipart/alternative holding plain + html, which
    leaves every other part of the tree alone.
    """
    leaves = [p for p in message.walk() if p.get_content_maintype() != "multipart"]
    if any(p.get_content_type() == "text/html" for p in leaves):
        return message
    plain = next((p for p in leaves if p.get_content_type() == "text/plain"), None)
    if plain is None:
        return message

    twin = MIMEText(_text_to_html(_decode(plain)), "html", "utf-8")

    if message.get_content_type() == "multipart/alternative":
        message.attach(twin)
        return message

    if message.get_content_maintype() == "multipart":
        # Wrap the text leaf in an alternative rather than appending html as a
        # sibling of the attachment, which most clients show as a second body.
        for parent in message.walk():
            payload = parent.get_payload()
            if not isinstance(payload, list):
                continue
            for index, child in enumerate(payload):
                if child.get_content_type() == "text/plain":
                    alternative = MIMEMultipart("alternative")
                    alternative.attach(child)
                    alternative.attach(twin)
                    payload[index] = alternative
                    return message
        return message

    rebuilt = MIMEMultipart("alternative")
    for key, value in message.items():
        if key.lower().startswith("content-") or key.lower() == "mime-version":
            continue
        rebuilt[key] = value
    rebuilt.attach(MIMEText(_decode(plain), "plain", "utf-8"))
    rebuilt.attach(twin)
    return rebuilt


def apply(raw: bytes, touch: str = "1") -> tuple[bytes, str]:
    """Return (new raw MIME, the signed plain-text body used for linting).

    Every text/plain and text/html part is signed: a multipart/alternative whose
    halves disagree is how a recipient sees an unsigned mail in one client and a
    signed one in another.
    """
    message = _with_html_twin(message_from_bytes(raw))
    plain = ""

    for part in message.walk():
        content_type = part.get_content_type()
        if part.get_content_maintype() == "multipart":
            continue
        if content_type == "text/plain":
            signed = sign_text(_decode(part), touch)
            _set(part, signed)
            plain = plain or signed
        elif content_type == "text/html":
            signed = sign_html(_decode(part), touch)
            if signed is not None:
                _set(part, signed)

    if not plain:
        # HTML-only message: lint still needs text. Fall back to stripped HTML.
        for part in message.walk():
            if part.get_content_type() == "text/html":
                plain = html_to_text(_decode(part))
                break

    return message.as_bytes(), plain


def html_to_text(html: str) -> str:
    """Crude tag strip: enough for the lint gate, not a rendering engine."""
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&middot;", "·")
        .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    )
    return re.sub(r"\n{3,}", "\n\n", re.sub(r"[ \t]+", " ", text)).strip()


def b64(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode()
