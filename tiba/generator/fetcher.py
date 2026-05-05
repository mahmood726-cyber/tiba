# tiba/generator/fetcher.py
"""Fetch tiba.yaml from a federation repo via `gh api` (subprocess)."""
from __future__ import annotations

import base64
import datetime as _dt
import subprocess
from dataclasses import dataclass
from typing import Any

import yaml

from .discover import RepoRef


@dataclass(frozen=True)
class FetchResult:
    ref: RepoRef
    found: bool
    manifest: dict[str, Any] | None
    error: str | None


def fetch_tiba_yaml(ref: RepoRef) -> FetchResult:
    """Try to fetch tiba.yaml from the repo root via gh api.

    Returns FetchResult with found=True iff the file exists and parses as YAML.
    """
    cmd = [
        "gh", "api",
        f"/repos/{ref.owner}/{ref.repo}/contents/tiba.yaml",
        "--jq", ".content",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return FetchResult(ref=ref, found=False, manifest=None, error=str(e.stderr or e))
    except FileNotFoundError:
        return FetchResult(
            ref=ref, found=False, manifest=None, error="gh CLI not installed"
        )

    raw_b64 = proc.stdout.strip().replace("\n", "")
    if not raw_b64:
        return FetchResult(ref=ref, found=False, manifest=None, error="empty response")

    try:
        decoded = base64.b64decode(raw_b64).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as e:
        return FetchResult(ref=ref, found=False, manifest=None, error=f"decode: {e}")

    try:
        parsed = yaml.safe_load(decoded)
    except yaml.YAMLError as e:
        return FetchResult(ref=ref, found=False, manifest=None, error=f"yaml: {e}")

    if not isinstance(parsed, dict):
        return FetchResult(
            ref=ref, found=False, manifest=None, error="manifest is not a mapping"
        )

    # Normalize PyYAML date coercion: unquoted YYYY-MM-DD parses as datetime.date,
    # which then fails the schema's `type: string` constraint. Coerce to ISO string.
    for k, v in list(parsed.items()):
        if isinstance(v, _dt.date) and not isinstance(v, _dt.datetime):
            parsed[k] = v.isoformat()

    return FetchResult(ref=ref, found=True, manifest=parsed, error=None)
