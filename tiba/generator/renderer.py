# tiba/generator/renderer.py
"""Render the index.html using Jinja2 against verified+grouped manifests."""
from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .verifier import VerifiedManifest


def render_index(
    *,
    operational: dict[str, list[VerifiedManifest]],
    roadmap: dict[str, list[VerifiedManifest]],
    template_dir: Path,
    version: str,
    generated_at: str,
) -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("index.html.j2")
    return template.render(
        operational=operational,
        roadmap=roadmap,
        version=version,
        generated_at=generated_at,
    )
