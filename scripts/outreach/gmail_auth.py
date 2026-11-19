"""Gmail API auth + thin REST client.

Plain `requests` instead of google-api-python-client: one dependency, no vendored
discovery documents, and the whole surface needed is a handful of endpoints.

Credentials come from the environment (GitHub Actions secrets, or the gitignored
.env locally), never from a file in the repo.

Auth model: a long-lived OAuth *refresh* token is exchanged for a short-lived
access token on every run. Whether the refresh token lasts depends on how the
OAuth app was set up; SETUP-GMAIL.md picks the setting that does not expire
after seven days.
"""

from __future__ import annotations

import base64
import os
from email.message import EmailMessage
from typing import Any

import requests

import config
import dotenv

# Local runs read the gitignored vault; in GitHub Actions the real environment
# already holds the secrets and load() will not overwrite them.
dotenv.load()

TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://gmail.googleapis.com/gmail/v1/users/me"
TIMEOUT = 30


class GmailError(RuntimeError):
    """Any non-2xx from Google. Raised so the Action exits non-zero and goes red.

    Load-bearing: a send lane that swallows a quota or auth failure goes quiet,
    and quiet looks exactly like healthy. Nothing here is caught and
    logged-but-continued.
    """

    def __init__(self, message: str, status: int = 0) -> None:
        super().__init__(message)
        self.status = status


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise GmailError(
            f"Missing required environment variable {name}. "
            "Set it as a GitHub Actions secret, or in the gitignored .env for local runs "
            "(scripts/outreach/SETUP-GMAIL.md)."
        )
    return value


class Gmail:
    def __init__(self, sender: str | None = None) -> None:
        self.sender = sender if sender is not None else config.load().sender
        self._token = self._access_token()

    def _access_token(self) -> str:
        resp = requests.post(
            TOKEN_URL,
            data={
                "client_id": _require_env("GMAIL_CLIENT_ID"),
                "client_secret": _require_env("GMAIL_CLIENT_SECRET"),
                "refresh_token": _require_env("GMAIL_REFRESH_TOKEN"),
                "grant_type": "refresh_token",
            },
            timeout=TIMEOUT,
        )
        if resp.status_code != 200:
            # The single most likely real-world failure: a revoked or expired
            # refresh token. Say so plainly rather than leaking a raw 400.
            raise GmailError(
                f"Token refresh failed ({resp.status_code}): {resp.text[:400]}. "
                "If this says invalid_grant, the refresh token was revoked or expired. "
                "Re-run get_refresh_token.py and update the GMAIL_REFRESH_TOKEN secret "
                "(SETUP-GMAIL.md, step 6 explains the seven-day trap)."
            )
        return resp.json()["access_token"]

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    def _get(self, path: str, **params: Any) -> dict:
        resp = requests.get(f"{API}{path}", headers=self._headers(), params=params, timeout=TIMEOUT)
        if resp.status_code != 200:
            raise GmailError(f"GET {path} failed ({resp.status_code}): {resp.text[:400]}", resp.status_code)
        return resp.json()

    def _post(self, path: str, payload: dict) -> dict:
        resp = requests.post(f"{API}{path}", headers=self._headers(), json=payload, timeout=TIMEOUT)
        if resp.status_code not in (200, 201):
            raise GmailError(f"POST {path} failed ({resp.status_code}): {resp.text[:400]}", resp.status_code)
        return resp.json()

    # ---- reads -------------------------------------------------------------

    def profile_email(self) -> str:
        """The address of the account the refresh token belongs to."""
        return str(self._get("/profile").get("emailAddress", "")).lower()

    def search(self, query: str, max_results: int = 100) -> list[dict]:
        """Return message stubs ({id, threadId}) matching a Gmail search query."""
        out: list[dict] = []
        page: str | None = None
        while True:
            params: dict[str, Any] = {"q": query, "maxResults": min(max_results, 100)}
            if page:
                params["pageToken"] = page
            data = self._get("/messages", **params)
            out.extend(data.get("messages", []) or [])
            page = data.get("nextPageToken")
            if not page or len(out) >= max_results:
                break
        return out[:max_results]

    def get_message(self, message_id: str) -> dict:
        return self._get(f"/messages/{message_id}", format="metadata")

    def get_thread(self, thread_id: str) -> dict:
        """Thread with its messages; minimal = labelIds + internalDate."""
        return self._get(f"/threads/{thread_id}", format="minimal")

    # ---- writes ------------------------------------------------------------

    def send_raw(self, raw_b64: str, thread_id: str = "") -> dict:
        """Send one fully built message. The only send path for outreach."""
        payload: dict[str, Any] = {"raw": raw_b64}
        if thread_id:
            payload["threadId"] = thread_id
        return self._post("/messages/send", payload)

    def label_id(self, name: str) -> str:
        """Id of a user label, created on first use."""
        for label in self._get("/labels").get("labels", []) or []:
            if label.get("name") == name:
                return label["id"]
        return self._post("/labels", {"name": name})["id"]

    def add_label(self, message_id: str, label_id: str) -> dict:
        """Tag one message. Used only to mark a reply as already alerted."""
        return self._post(f"/messages/{message_id}/modify", {"addLabelIds": [label_id]})

    def send_new(self, to: str, subject: str, body: str) -> dict:
        """Compose and send. Used ONLY for the digest to the user themselves."""
        msg = EmailMessage()
        msg["To"] = to
        msg["From"] = self.sender
        msg["Subject"] = subject
        msg.set_content(body)
        return self.send_raw(base64.urlsafe_b64encode(msg.as_bytes()).decode())


def header(message: dict, name: str) -> str:
    """Pull a header value out of a Gmail message payload, case-insensitively."""
    headers = message.get("payload", {}).get("headers", []) or []
    lowered = name.lower()
    for h in headers:
        if h.get("name", "").lower() == lowered:
            return h.get("value", "")
    return ""
