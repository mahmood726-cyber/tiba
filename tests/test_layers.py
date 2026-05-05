"""Layer-grouping helper tests."""
from tiba.generator.discover import RepoRef
from tiba.generator.fetcher import FetchResult
from tiba.generator.layers import OPERATIONAL_LAYER_ORDER, ROADMAP_LAYER_ORDER, group_by_layer
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
                "headline_metric": {"label": "x", "value": "y", "source": "z"},
                "contact": {"steward": "u"},
                "last_verified": "2026-05-05",
            },
            error=None,
        ),
        pages_status=200 if status == "operational" else None,
    )


def test_grouping_returns_operational_first() -> None:
    items = [
        _verified("training", "operational", "o/training"),
        _verified("workforce", "roadmap", "o/workforce"),
        _verified("discovery", "operational", "o/discovery"),
    ]
    operational, roadmap = group_by_layer(items)
    operational_layers = list(operational.keys())
    assert operational_layers.index("discovery") < operational_layers.index("training")


def test_grouping_preserves_canonical_order() -> None:
    items = [_verified(layer, "operational") for layer in OPERATIONAL_LAYER_ORDER[::-1]]
    operational, _ = group_by_layer(items)
    assert list(operational.keys()) == list(OPERATIONAL_LAYER_ORDER)


def test_unrenderable_items_dropped_from_operational_group() -> None:
    bad = VerifiedManifest(
        fetch=FetchResult(
            ref=RepoRef("o", "r"),
            found=True,
            manifest={
                "schema_version": 1,
                "layer": "discovery",
                "status": "operational",
                "owning_repo": "o/r",
                "pages_url": "https://example.org/",
                "headline_metric": {"label": "x", "value": "y", "source": "z"},
                "contact": {"steward": "u"},
                "last_verified": "2026-05-05",
            },
            error=None,
        ),
        pages_status=404,
    )
    operational, _ = group_by_layer([bad])
    assert operational == {}
