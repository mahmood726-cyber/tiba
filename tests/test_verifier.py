# tests/test_verifier.py
"""HTTP-200 verifier tests — mocks requests."""
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from tiba.generator.discover import RepoRef
from tiba.generator.fetcher import FetchResult
from tiba.generator.verifier import VerifiedManifest, verify_all


def _result(layer: str, status: str, pages_url: str) -> FetchResult:
    return FetchResult(
        ref=RepoRef("o", "r"),
        found=True,
        manifest={
            "schema_version": 1,
            "layer": layer,
            "status": status,
            "owning_repo": "o/r",
            "pages_url": pages_url,
            "headline_metric": {"label": "x", "value": "y", "source": "z"},
            "contact": {"steward": "user"},
            "last_verified": "2026-05-05",
        },
        error=None,
    )


def _schema_path(repo_root: Path) -> Path:
    return repo_root / "schema" / "tiba.yaml.schema.json"


def test_operational_with_http_200_is_renderable(repo_root: Path) -> None:
    fetch_results = [_result("discovery", "operational", "https://example.org/")]
    mock_resp = MagicMock(status_code=200)
    with patch("requests.head", return_value=mock_resp):
        verified = verify_all(fetch_results, schema_path=_schema_path(repo_root))
    assert len(verified) == 1
    assert verified[0].renderable is True
    assert verified[0].pages_status == 200


def test_roadmap_status_is_renderable_without_http_check(repo_root: Path) -> None:
    fetch_results = [_result("workforce", "roadmap", "https://example.org/")]
    with patch("requests.head") as mock_head:
        verified = verify_all(fetch_results, schema_path=_schema_path(repo_root))
        mock_head.assert_not_called()
    assert verified[0].renderable is True
    assert verified[0].pages_status is None


def test_operational_with_http_404_is_not_renderable(repo_root: Path) -> None:
    fetch_results = [_result("discovery", "operational", "https://example.org/")]
    mock_resp = MagicMock(status_code=404)
    with patch("requests.head", return_value=mock_resp):
        verified = verify_all(fetch_results, schema_path=_schema_path(repo_root))
    assert verified[0].renderable is False
    assert verified[0].pages_status == 404


def test_invalid_schema_is_not_renderable(repo_root: Path) -> None:
    bad = FetchResult(
        ref=RepoRef("o", "r"),
        found=True,
        manifest={"schema_version": 1, "layer": "not-an-enum"},  # missing required fields
        error=None,
    )
    verified = verify_all([bad], schema_path=_schema_path(repo_root))
    assert verified[0].renderable is False
    assert verified[0].schema_errors


def test_fetch_failure_passes_through(repo_root: Path) -> None:
    failed = FetchResult(
        ref=RepoRef("o", "r"), found=False, manifest=None, error="HTTP 404"
    )
    verified = verify_all([failed], schema_path=_schema_path(repo_root))
    assert verified[0].renderable is False
    assert verified[0].fetch_error == "HTTP 404"
