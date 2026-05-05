"""Shared pytest fixtures for Tiba meta-repo tests."""
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).parent.parent
