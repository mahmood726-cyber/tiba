"""Tiba index-page orchestrator.

CLI:  python -m tiba.generator.build_index [--output site/index.html]
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from .discover import load_federation
from .fetcher import fetch_tiba_yaml
from .layers import group_by_layer
from .renderer import render_index
from .verifier import verify_all


def build_index(
    *,
    federation_path: Path,
    schema_path: Path,
    template_dir: Path,
    output_path: Path,
    version: str,
) -> Path:
    repos = load_federation(federation_path)
    fetched = [fetch_tiba_yaml(r) for r in repos]
    verified = verify_all(fetched, schema_path=schema_path)
    operational, roadmap = group_by_layer(verified)

    html = render_index(
        operational=operational,
        roadmap=roadmap,
        template_dir=template_dir,
        version=version,
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build Tiba federation index page")
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--output", type=Path, default=None)
    p.add_argument("--version", default="0.1.0")
    args = p.parse_args(argv)

    root: Path = args.repo_root
    output = args.output or (root / "site" / "index.html")

    out = build_index(
        federation_path=root / "federation.yaml",
        schema_path=root / "schema" / "tiba.yaml.schema.json",
        template_dir=root / "site" / "templates",
        output_path=output,
        version=args.version,
    )
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
