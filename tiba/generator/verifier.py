# tiba/generator/verifier.py
"""Schema validation + HTTP-200 gate for fetched manifests (spec R2)."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests
from jsonschema import Draft202012Validator

from .fetcher import FetchResult


HEAD_TIMEOUT_SECONDS = 5


@dataclass(frozen=True)
class VerifiedManifest:
    fetch: FetchResult
    schema_errors: list[str] = field(default_factory=list)
    pages_status: int | None = None
    pages_error: str | None = None

    @property
    def renderable(self) -> bool:
        if not self.fetch.found:
            return False
        if self.schema_errors:
            return False
        m = self.fetch.manifest or {}
        if m.get("status") == "operational" and self.pages_status != 200:
            return False
        return True

    @property
    def fetch_error(self) -> str | None:
        return self.fetch.error


def _check_pages_url(url: str) -> tuple[int | None, str | None]:
    try:
        r = requests.head(url, timeout=HEAD_TIMEOUT_SECONDS, allow_redirects=True)
        return r.status_code, None
    except requests.RequestException as e:
        return None, str(e)


def verify_all(
    fetch_results: list[FetchResult], schema_path: Path
) -> list[VerifiedManifest]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    verified: list[VerifiedManifest] = []
    for fr in fetch_results:
        if not fr.found or fr.manifest is None:
            verified.append(VerifiedManifest(fetch=fr))
            continue

        errors = [e.message for e in validator.iter_errors(fr.manifest)]
        if errors:
            verified.append(VerifiedManifest(fetch=fr, schema_errors=errors))
            continue

        if fr.manifest.get("status") == "operational":
            status, err = _check_pages_url(fr.manifest["pages_url"])
            verified.append(
                VerifiedManifest(fetch=fr, pages_status=status, pages_error=err)
            )
        else:
            verified.append(VerifiedManifest(fetch=fr))
    return verified
