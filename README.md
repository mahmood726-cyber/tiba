# Tiba

> Pan-African, African-led, living-evidence ecosystem.
> Swahili: *healing / medicine.*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](tests/)
[![Index](https://img.shields.io/badge/index-pages-success.svg)](https://mahmood726-cyber.github.io/tiba/)

**v0.1.0 — framework declaration.**
**Index page:** https://mahmood726-cyber.github.io/tiba/
**Manifesto:** [`MANIFESTO.md`](MANIFESTO.md)

## What is Tiba?

Tiba is a federation of African-led evidence-synthesis projects, organised under one architectural vocabulary so they compose into a single moonshot: a working living-evidence pipeline that an African research workforce can run, anchored at Makerere.

v0.1.0 is the **framework declaration** — the diagnostic + constructive papers that say what Tiba is, the [`tiba.yaml`](schema/tiba.yaml.schema.json) federation manifest that lets affiliated repos opt in, and the CI-generated [index page](https://mahmood726-cyber.github.io/tiba/) that renders the federation. The working pipeline (v0.2+) builds on this foundation.

## Architecture (8 layers, two-tier)

**Operational today (v0.1.0):**
| Layer | Owning repo |
|---|---|
| Discovery | [`pactr-hiddenness-atlas`](https://github.com/mahmood726-cyber/pactr-hiddenness-atlas) |
| Quality gates | [`repro-floor-atlas`](https://github.com/mahmood726-cyber/repro-floor-atlas), [`pi-atlas`](https://github.com/mahmood726-cyber/pi-atlas), [`responder-floor-atlas`](https://github.com/mahmood726-cyber/responder-floor-atlas), [`trial-truthfulness-atlas`](https://github.com/mahmood726-cyber/trial-truthfulness-atlas), [`cochrane-modern-re`](https://github.com/mahmood726-cyber/cochrane-modern-re) |
| Equity scoreboard | [`arac`](https://github.com/mahmood726-cyber/arac) |
| Publishing rail | E156 workbook + Synthēsis-Africa imprint |
| Training rail | [`synthesis-courses`](https://github.com/mahmood726-cyber/synthesis-courses) |

**Roadmap (v0.2+):** Workforce activation · Living updates · Verification UI primitive.

See [`MANIFESTO.md`](MANIFESTO.md) and [`docs/superpowers/specs/2026-05-05-tiba-design.md`](docs/superpowers/specs/2026-05-05-tiba-design.md) for the full architecture.

## Affiliating a repo

Drop a [`tiba.yaml`](schema/tiba.yaml.schema.json) at your repo root. See [`MANIFESTO.md`](MANIFESTO.md) §How-to-affiliate for the 3-step process. Schema is enforced by CI (Task 14 of the v0.1.0 plan); your repo will only render on the index page if its declared `pages_url` returns HTTP 200.

## Local development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m tiba.generator.build_index --output site/index.html
```

## Trademark

**Tiba is not affiliated with the Cochrane Collaboration.** "Cochrane" and related marks are registered trademarks of The Cochrane Collaboration. Tiba uses freely-available systematic-review methodology (PRISMA, GRADE, RoB-2) but is organisationally independent. See [`MANIFESTO.md`](MANIFESTO.md) §Trademark for the full posture.

## License

MIT — see [`LICENSE`](LICENSE).
