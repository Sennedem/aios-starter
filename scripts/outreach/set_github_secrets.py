"""Push the three Gmail credentials from .env into your repo's GitHub Actions secrets.

    python scripts/outreach/set_github_secrets.py            # the repo this folder belongs to
    python scripts/outreach/set_github_secrets.py --repo you/your-aios

Needs the GitHub CLI (`gh`), logged in with `gh auth login`. Values are piped to
gh through stdin: never echoed, never passed as a command-line argument (other
processes can read those), never logged.

Refuses to run against a public repository. The secrets themselves stay hidden
either way, but a public repo would publish your outbox (recipients, copy) and
your brain.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

import dotenv

KEYS = ("GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET", "GMAIL_REFRESH_TOKEN")


def _gh(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(["gh", *args], input=stdin, text=True, capture_output=True)
    except FileNotFoundError:
        raise SystemExit(
            "The GitHub CLI (gh) is not installed. Either install it (https://cli.github.com)\n"
            "and run `gh auth login`, or add the three secrets by hand (SETUP-GMAIL.md, step 7a)."
        )


def repo_visibility(repo: str | None) -> tuple[str, str]:
    args = ["repo", "view", "--json", "nameWithOwner,visibility"]
    if repo:
        args.insert(2, repo)
    result = _gh(args)
    if result.returncode != 0:
        raise SystemExit(f"Could not read the repository: {result.stderr.strip()}")
    data = json.loads(result.stdout)
    return data["nameWithOwner"], str(data.get("visibility", "")).upper()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", help="owner/name; defaults to the repo of the current folder")
    args = parser.parse_args()

    env = dotenv.load()
    missing = [k for k in KEYS if not env.get(k, "").strip()]
    if missing:
        print(f"Missing in {dotenv.ENV_PATH}: {', '.join(missing)}", file=sys.stderr)
        if "GMAIL_REFRESH_TOKEN" in missing:
            print("Run get_refresh_token.py first.", file=sys.stderr)
        return 1

    repo, visibility = repo_visibility(args.repo)
    if visibility != "PRIVATE":
        print(
            f"{repo} is {visibility.lower() or 'not private'}. Make it private first "
            "(GitHub > Settings > General > Danger Zone > Change visibility), then rerun.",
            file=sys.stderr,
        )
        return 1

    for key in KEYS:
        result = _gh(["secret", "set", key, "--repo", repo], stdin=env[key])
        if result.returncode != 0:
            print(f"FAILED {key}: {result.stderr.strip()}", file=sys.stderr)
            return 1
        print(f"  set {key} ({len(env[key])} chars)")

    print(f"\nAll three secrets set on {repo}.")
    print(f"Check with: gh secret list --repo {repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
