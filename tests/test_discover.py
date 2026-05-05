"""Federation-discovery tests."""
from pathlib import Path

import pytest

from tiba.generator.discover import RepoRef, load_federation


def test_load_federation_returns_list_of_repos(repo_root: Path) -> None:
    repos = load_federation(repo_root / "federation.yaml")
    assert len(repos) >= 4
    assert all(isinstance(r, RepoRef) for r in repos)


def test_federation_includes_pactr(repo_root: Path) -> None:
    repos = load_federation(repo_root / "federation.yaml")
    names = {(r.owner, r.repo) for r in repos}
    assert ("mahmood726-cyber", "pactr-hiddenness-atlas") in names


def test_federation_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_federation(tmp_path / "does-not-exist.yaml")


def test_federation_unknown_schema_version_raises(tmp_path: Path) -> None:
    f = tmp_path / "federation.yaml"
    f.write_text("schema_version: 99\nrepos: []\n", encoding="utf-8")
    with pytest.raises(ValueError, match="schema_version"):
        load_federation(f)
