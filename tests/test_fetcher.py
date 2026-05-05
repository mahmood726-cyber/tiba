"""tiba.yaml fetcher tests — mocks `gh api` subprocess."""
import base64
import subprocess
from unittest.mock import patch

import pytest

from tiba.generator.discover import RepoRef
from tiba.generator.fetcher import FetchResult, fetch_tiba_yaml


SAMPLE_MANIFEST = """\
schema_version: 1
layer: discovery
status: operational
owning_repo: mahmood726-cyber/pactr-hiddenness-atlas
pages_url: https://mahmood726-cyber.github.io/pactr-hiddenness-atlas/
headline_metric:
  label: x
  value: y
  source: z
contact:
  steward: mahmood726-cyber
last_verified: "2026-05-05"
"""


def _mock_gh_response(content: str) -> subprocess.CompletedProcess:
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    return subprocess.CompletedProcess(
        args=["gh", "api"], returncode=0, stdout=encoded, stderr=""
    )


def test_fetch_returns_parsed_manifest_on_success() -> None:
    ref = RepoRef("mahmood726-cyber", "pactr-hiddenness-atlas")
    with patch("subprocess.run", return_value=_mock_gh_response(SAMPLE_MANIFEST)):
        result = fetch_tiba_yaml(ref)
    assert isinstance(result, FetchResult)
    assert result.found is True
    assert result.manifest["layer"] == "discovery"
    assert result.error is None


def test_fetch_returns_not_found_when_gh_404s() -> None:
    ref = RepoRef("mahmood726-cyber", "no-tiba-yaml-here")
    err = subprocess.CalledProcessError(
        returncode=1, cmd=["gh", "api"], stderr="HTTP 404"
    )
    with patch("subprocess.run", side_effect=err):
        result = fetch_tiba_yaml(ref)
    assert result.found is False
    assert result.manifest is None
    assert "404" in (result.error or "")


def test_fetch_returns_error_on_invalid_yaml() -> None:
    ref = RepoRef("owner", "repo")
    invalid = "not: valid: yaml: ::"
    with patch("subprocess.run", return_value=_mock_gh_response(invalid)):
        result = fetch_tiba_yaml(ref)
    assert result.found is False
    assert result.error is not None
