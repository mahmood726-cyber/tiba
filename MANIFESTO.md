# Tiba — Manifesto

> *Tiba* (Swahili: healing, medicine).

## Vision

Pan-African, African-led, living-evidence ecosystem that **discovers, synthesises, verifies, teaches, and publishes meta-analyses at sub-week cadence**, anchored at Makerere, free at point of use.

The infrastructure for evidence synthesis was built for the global North. Most African-registered trials never reach the synthesis pipeline because the discovery layer can't see them (NCT-bridge methodology has 6.2% sensitivity for PACTR-published African evidence). Tiba names that gap, then composes existing tools — discovery, quality gates, equity scoreboard, publishing, training — into a buildable framework that closes it.

## Scope

**v0.1.0 is a framework declaration**, not the working pipeline. v0.1.0 names the moonshot, anchors it in already-shipped evidence (PACTR Hiddenness Atlas + ARAC), publishes the architecture, and stands up a federation marker so future Africa-tagged repos compose under one banner.

The working pipeline is v0.2+ and beyond:

- **v0.2** Workforce activation — Makerere cohort under Tiba banner, next academic term
- **v0.3** Living updates — adapt CardioSynth pattern on one African-priority condition
- **v0.4** Verification UI primitive — generalise RapidMeta one-trial-at-a-time pattern as reusable

## Governance

Lightweight stewardship. mahmood726-cyber as v0.1.0 steward. After Makerere PI nomination (v0.2), governance becomes co-stewardship.

Affiliated repos retain **full local autonomy.** Tiba imposes the manifest schema (`tiba.yaml`), not project rules, file layouts, or coding conventions. The framework composes; it does not control.

## How to affiliate

1. Decide which Tiba layer your project belongs to: `discovery` · `quality-gate` · `equity` · `publishing` · `training` · `workforce` · `living-updates` · `verification-ui`.
2. Drop a [`tiba.yaml`](schema/tiba.yaml.schema.json) at your repo root, declaring `layer`, `status` (`operational` or `roadmap`), `pages_url`, `headline_metric`, and a `last_verified` date.
3. Push. The Tiba CI generator auto-discovers your repo on the next index rebuild and renders a card on [the index page](https://mahmood726-cyber.github.io/tiba/) — but only if your declared `pages_url` returns HTTP 200.

## Trademark posture

**Tiba is not affiliated with the Cochrane Collaboration.** "Cochrane", "Cochrane Review", "Cochrane Library", and related marks are registered trademarks of The Cochrane Collaboration. Tiba uses freely-available systematic-review methodology (PRISMA, GRADE, RoB-2, the published handbook) but is independent of that organisation. Tiba copy must never adopt those marks as a Tiba product or service name; a pre-push guard ([`scripts/pre_push_cochrane_guard.py`](scripts/pre_push_cochrane_guard.py)) blocks accidental drift.

---

*Spec:* [`docs/superpowers/specs/2026-05-05-tiba-design.md`](docs/superpowers/specs/2026-05-05-tiba-design.md)
*Implementation plan:* [`docs/superpowers/plans/2026-05-05-tiba-v0.1.0.md`](docs/superpowers/plans/2026-05-05-tiba-v0.1.0.md)
