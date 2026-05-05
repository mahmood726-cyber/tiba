"""Schema-validation tests for tiba.yaml federation manifest."""
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator


@pytest.fixture
def schema(repo_root: Path) -> dict:
    schema_path = repo_root / "schema" / "tiba.yaml.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_schema_itself_is_valid_draft_2020_12(schema: dict) -> None:
    Draft202012Validator.check_schema(schema)


def test_valid_fixture_passes(schema: dict, fixtures_dir: Path) -> None:
    manifest = _load_yaml(fixtures_dir / "valid_tiba.yaml")
    Draft202012Validator(schema).validate(manifest)


def test_missing_layer_fails(schema: dict, fixtures_dir: Path) -> None:
    manifest = _load_yaml(fixtures_dir / "invalid_tiba_missing_layer.yaml")
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    assert errors, "expected validation errors for missing layer"
    assert any("'layer' is a required property" in e.message for e in errors)


def test_bad_layer_enum_fails(schema: dict, fixtures_dir: Path) -> None:
    manifest = _load_yaml(fixtures_dir / "invalid_tiba_bad_layer_enum.yaml")
    errors = list(Draft202012Validator(schema).iter_errors(manifest))
    assert errors, "expected validation errors for bad layer enum"
    assert any("is not one of" in e.message for e in errors)


def test_pages_url_must_be_https(schema: dict) -> None:
    bad = {
        "schema_version": 1,
        "layer": "discovery",
        "status": "operational",
        "owning_repo": "owner/repo",
        "pages_url": "http://example.org/",
        "headline_metric": {"label": "x", "value": "y", "source": "z"},
        "contact": {"steward": "user"},
        "last_verified": "2026-05-05",
    }
    errors = list(Draft202012Validator(schema).iter_errors(bad))
    assert errors


def test_owning_repo_pattern_enforced(schema: dict) -> None:
    bad = {
        "schema_version": 1,
        "layer": "discovery",
        "status": "operational",
        "owning_repo": "not-a-valid-repo-spec",
        "pages_url": "https://example.org/",
        "headline_metric": {"label": "x", "value": "y", "source": "z"},
        "contact": {"steward": "user"},
        "last_verified": "2026-05-05",
    }
    errors = list(Draft202012Validator(schema).iter_errors(bad))
    assert errors
