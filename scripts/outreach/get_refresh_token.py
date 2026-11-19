"""One-time OAuth helper: produce a Gmail refresh token for the send Action.

    python scripts/outreach/get_refresh_token.py

Before running: put GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET in the .env file at
the repo root (SETUP-GMAIL.md, step 5). This script opens your browser, you
approve access for your own Gmail account, and the refresh token is written
straight into .env. It is never printed: a token in a terminal is a token in
scrollback.

Uses a Desktop-app client with a loopback redirect, the flow Google supports
today (the old copy-this-code flow is retired).
"""

from __future__ import annotations

import http.server
import secrets
import socket
import threading
import urllib.parse
import webbrowser

import requests

import dotenv

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
# gmail.send to send; gmail.modify to read replies and bounces for the daily
# monitor and to label a reply once it has been reported.
SCOPES = "https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.modify"

_received: dict[str, str] = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (stdlib naming)
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _received.update({k: v[0] for k, v in params.items()})
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        ok = "code" in _received
        self.wfile.write(
            (
                "<h2>Done. You can close this tab and go back to the terminal.</h2>"
                if ok
                else "<h2>Authorisation failed</h2><p>Go back to the terminal for details.</p>"
            ).encode()
        )

    def log_message(self, *args: object) -> None:
        pass  # keep the console clean


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def main() -> None:
    print("Gmail refresh-token setup\n" + "=" * 40)

    # Credentials come from the gitignored vault, not from a prompt: it keeps
    # them out of shell history and out of any chat transcript.
    env = dotenv.load()
    client_id = env.get("GMAIL_CLIENT_ID", "").strip()
    client_secret = env.get("GMAIL_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        raise SystemExit(
            f"GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be filled in {dotenv.ENV_PATH}.\n"
            "Get them from Google Cloud console > Google Auth Platform > Clients >\n"
            "your Desktop client (SETUP-GMAIL.md, steps 4 and 5)."
        )
    print(f"Using client {client_id[:18]}... from {dotenv.ENV_PATH.name}")

    port = free_port()
    redirect_uri = f"http://127.0.0.1:{port}"
    state = secrets.token_urlsafe(16)

    query = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": SCOPES,
            "access_type": "offline",  # required to get a refresh token at all
            "prompt": "consent",       # forces a fresh refresh token on re-runs
            "state": state,
        }
    )
    url = f"{AUTH_URL}?{query}"

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.handle_request, daemon=True).start()

    print(f"\nOpening your browser. If it does not open, paste this into it:\n\n{url}\n")
    webbrowser.open(url)
    print("Waiting for you to approve in the browser (up to 5 minutes)...")

    for _ in range(300):
        if _received:
            break
        threading.Event().wait(1)

    if not _received:
        raise SystemExit("No answer from the browser within 5 minutes. Run the script again.")
    if _received.get("state") != state:
        raise SystemExit("State mismatch: aborting rather than trusting the response.")
    code = _received.get("code")
    if not code:
        raise SystemExit(f"No authorisation code returned: {_received.get('error', 'unknown error')}")

    resp = requests.post(
        TOKEN_URL,
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise SystemExit(f"Token exchange failed ({resp.status_code}): {resp.text[:300]}")

    token = resp.json().get("refresh_token")
    if not token:
        raise SystemExit(
            "No refresh_token in the response. Google only returns one on first consent: "
            "remove the app at https://myaccount.google.com/permissions and run this again."
        )

    dotenv.set_key("GMAIL_REFRESH_TOKEN", token)

    print("\n" + "=" * 40)
    print(f"Refresh token obtained and written to {dotenv.ENV_PATH}")
    print(f"(length {len(token)}, not printed on purpose)")
    print("=" * 40)
    print(
        "\nNext: copy all three values into your GitHub repository secrets, either by hand\n"
        "(SETUP-GMAIL.md, step 7a) or with\n  python scripts/outreach/set_github_secrets.py"
    )


if __name__ == "__main__":
    main()
