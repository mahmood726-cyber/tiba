"""Smoke test: verifies test harness wiring and repo layout invariants."""
from pathlib import Path


def test_repo_root_has_pyproject(repo_root: Path) -> None:
    assert (repo_root / "pyproject.toml").is_file()


def test_repo_root_has_license(repo_root: Path) -> None:
    assert (repo_root / "LICENSE").is_file()


def test_repo_root_has_spec() -> None:
    spec = Path(__file__).parent.parent / "docs" / "superpowers" / "specs" / "2026-05-05-tiba-design.md"
    assert spec.is_file()
