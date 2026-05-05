# tiba/generator/discover.py
"""Federation discovery — reads curated federation.yaml.

v0.2 will add GitHub Search API auto-discovery; for v0.1.0 the federation
is a hand-curated list to keep the generator dependency-free of network
calls during discovery.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class RepoRef:
    owner: str
    repo: str

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.repo}"


def load_federation(path: Path) -> list[RepoRef]:
    if not path.is_file():
        raise FileNotFoundError(f"federation manifest not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    schema_version = data.get("schema_version")
    if schema_version != 1:
        raise ValueError(
            f"unsupported federation schema_version: {schema_version!r} (expected 1)"
        )
    repos_raw = data.get("repos") or []
    return [RepoRef(owner=r["owner"], repo=r["repo"]) for r in repos_raw]
