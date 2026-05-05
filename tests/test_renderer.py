# tests/test_renderer.py
"""Renderer tests — render template against in-memory verified manifests."""
from pathlib import Path

import pytest

from tiba.generator.discover import RepoRef
from tiba.generator.fetcher import FetchResult
from tiba.generator.layers import group_by_layer
from tiba.generator.renderer import render_index
from tiba.generator.verifier import VerifiedManifest


def _verified(layer: str, status: str, slug: str = "o/r") -> VerifiedManifest:
    owner, repo = slug.split("/")
    return VerifiedManifest(
        fetch=FetchResult(
            ref=RepoRef(owner, repo),
            found=True,
            manifest={
                "schema_version": 1,
                "layer": layer,
                "status": status,
                "owning_repo": slug,
                "pages_url": "https://example.org/",
                "headline_metric": {
                    "label": "test metric",
                    "value": "42%",
                    "ci_or_qualifier": "[40, 44]",
                    "source": "test source",
                },
                "contact": {"steward": "u"},
                "last_verified": "2026-05-05",
            },
            error=None,
        ),
        pages_status=200 if status == "operational" else None,
    )


@pytest.fixture
def template_dir(repo_root: Path) -> Path:
    return repo_root / "site" / "templates"


def test_render_includes_owning_repo(template_dir: Path) -> None:
    items = [_verified("discovery", "operational", "owner/repo")]
    operational, roadmap = group_by_layer(items)
    html = render_index(
        operational=operational,
        roadmap=roadmap,
        template_dir=template_dir,
        version="0.1.0",
        generated_at="2026-05-05T00:00:00Z",
    )
    assert "owner/repo" in html
    assert "test metric" in html
    assert "42%" in html


def test_render_groups_into_operational_and_roadmap_sections(template_dir: Path) -> None:
    items = [
        _verified("discovery", "operational", "owner/disc"),
        _verified("workforce", "roadmap", "owner/wf"),
    ]
    operational, roadmap = group_by_layer(items)
    html = render_index(
        operational=operational, roadmap=roadmap, template_dir=template_dir,
        version="0.1.0", generated_at="2026-05-05T00:00:00Z",
    )
    assert html.index("Operational") < html.index("Roadmap")


def test_render_includes_trademark_disclaimer(template_dir: Path) -> None:
    operational, roadmap = group_by_layer([])
    html = render_index(
        operational=operational, roadmap=roadmap, template_dir=template_dir,
        version="0.1.0", generated_at="2026-05-05T00:00:00Z",
    )
    assert "Not affiliated with the Cochrane Collaboration" in html
