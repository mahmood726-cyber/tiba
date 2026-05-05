"""Integration test: orchestrator wires discover -> fetch -> verify -> render."""
import base64
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tiba.generator.build_index import build_index


VALID_MANIFEST = """\
schema_version: 1
layer: discovery
status: operational
owning_repo: mahmood726-cyber/pactr-hiddenness-atlas
pages_url: https://mahmood726-cyber.github.io/pactr-hiddenness-atlas/
headline_metric:
  label: "NCT-bridge sensitivity for PACTR pubs"
  value: "6.2%"
  ci_or_qualifier: "[3.4, 10.4]"
  source: "pactr-hiddenness-atlas v0.1.0"
contact:
  steward: mahmood726-cyber
last_verified: "2026-05-05"
"""


def test_build_index_produces_html(repo_root: Path, tmp_path: Path) -> None:
    federation = tmp_path / "federation.yaml"
    federation.write_text(
        "schema_version: 1\nrepos:\n  - {owner: mahmood726-cyber, repo: pactr-hiddenness-atlas}\n",
        encoding="utf-8",
    )

    encoded = base64.b64encode(VALID_MANIFEST.encode("utf-8")).decode("ascii")
    fake_gh = subprocess.CompletedProcess(args=["gh"], returncode=0, stdout=encoded, stderr="")
    fake_head = MagicMock(status_code=200)

    output = tmp_path / "index.html"
    with patch("subprocess.run", return_value=fake_gh), patch(
        "requests.head", return_value=fake_head
    ):
        build_index(
            federation_path=federation,
            schema_path=repo_root / "schema" / "tiba.yaml.schema.json",
            template_dir=repo_root / "site" / "templates",
            output_path=output,
            version="0.1.0",
        )

    html = output.read_text(encoding="utf-8")
    assert "pactr-hiddenness-atlas" in html
    assert "6.2%" in html
    assert "Operational" in html
    assert "Not affiliated with the Cochrane Collaboration" in html
