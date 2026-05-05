"""Group verified manifests by layer in canonical order (spec §4)."""
from __future__ import annotations

from collections import OrderedDict

from .verifier import VerifiedManifest

OPERATIONAL_LAYER_ORDER: tuple[str, ...] = (
    "discovery",
    "quality-gate",
    "equity",
    "publishing",
    "training",
)
ROADMAP_LAYER_ORDER: tuple[str, ...] = (
    "workforce",
    "living-updates",
    "verification-ui",
)


def group_by_layer(
    verified: list[VerifiedManifest],
) -> tuple[dict[str, list[VerifiedManifest]], dict[str, list[VerifiedManifest]]]:
    operational: OrderedDict[str, list[VerifiedManifest]] = OrderedDict(
        (k, []) for k in OPERATIONAL_LAYER_ORDER
    )
    roadmap: OrderedDict[str, list[VerifiedManifest]] = OrderedDict(
        (k, []) for k in ROADMAP_LAYER_ORDER
    )
    for v in verified:
        if not v.renderable:
            continue
        layer = (v.fetch.manifest or {}).get("layer")
        if layer in operational:
            operational[layer].append(v)
        elif layer in roadmap:
            roadmap[layer].append(v)
    # drop empty layers from output
    return (
        {k: vs for k, vs in operational.items() if vs},
        {k: vs for k, vs in roadmap.items() if vs},
    )
