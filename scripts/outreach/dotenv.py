"""Minimal .env reader/writer for the gitignored key vault at the repo root.

No python-dotenv dependency: the vault is plain `KEY="value"` lines, and adding a
package to parse that is not worth the supply-chain surface.

Values are never printed by anything that imports this.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


def load(path: Path | None = None) -> dict[str, str]:
    """Read the vault into a dict AND into os.environ, without clobbering
    anything already set: GitHub Actions secrets must win over a local file."""
    path = path or ENV_PATH
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, raw = line.partition("=")
        key = key.strip()
        value = raw.strip().strip('"').strip("'")
        if not value:
            continue
        values[key] = value
        os.environ.setdefault(key, value)
    return values


def set_key(key: str, value: str, path: Path | None = None) -> None:
    """Write a single key, replacing it in place if present.

    Rewrites the whole file but keeps every other key and comment: this vault
    holds all your API keys, and a clumsy write here is expensive.
    """
    path = path or ENV_PATH
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    line = f'{key}="{value}"'
    pattern = re.compile(rf"^{re.escape(key)}=.*$", re.MULTILINE)

    if pattern.search(text):
        text = pattern.sub(lambda _m: line, text)
    else:
        text = text.rstrip("\n") + f"\n{line}\n"
    path.write_text(text, encoding="utf-8")
