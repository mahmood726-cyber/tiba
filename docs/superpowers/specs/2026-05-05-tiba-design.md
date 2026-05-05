# Tiba — v0.1.0 Design Spec

**Date:** 2026-05-05
**Status:** Brainstorm output, awaiting user review
**Authors:** mahmood726-cyber (driver). Makerere co-authors TBD — locked at draft-2.
**Successor doc:** Implementation plan (writing-plans skill, next step).

---

## 1. Identity

**Name:** Tiba (Swahili: *healing / medicine*).
**Publishing imprint:** Synthēsis-Africa.
**One-line vision:** Pan-African, African-led, living-evidence ecosystem that discovers, synthesises, verifies, teaches, and publishes meta-analyses at sub-week cadence, anchored at Makerere, free at point of use.
**Trademark posture:** "Cochrane" is a registered trademark of the Cochrane Collaboration. Their methodology (systematic reviews, GRADE, RoB-2, PRISMA) is open and freely usable. Tiba copy MUST NOT use "Cochrane", "Cochrane Review", "Cochrane Library", or any derivative as a Tiba product/service name. Sentinel pre-push regex enforces (see §8).

---

## 2. Scope of v0.1.0

Tiba v0.1.0 is **a framework declaration**, not the working pipeline. The working pipeline is v0.2+ (Makerere cohort activation) and beyond. v0.1.0 names the moonshot, anchors it in already-shipped evidence (PACTR Hiddenness Atlas + ARAC), publishes the architecture, and stands up a federation marker so future Africa-tagged repos compose under one banner.

**Primary audience:** methods/journal community (Synthēsis, BMJ Methods, JCE, Cochrane methods group, RSM).
**Secondary audiences (downstream):** funders (B), Makerere cohort (A), portfolio anchor (D) — all gated on v0.1.0 shipping first.

---

## 3. Deliverables (4)

### 3.1 Diagnostic paper — Synthēsis Methods Note (≤400 words)
- **Claim:** *African evidence is hidden from existing synthesis infrastructure.*
- **Empirical anchor:** PACTR Hiddenness Atlas headline (NCT-bridge methodology has 6.2% sensitivity for PACTR-registered African publications; algorithm 1/30 vs blinded auditor 16/30) + ARAC's 5 RGS metrics on Cochrane African representation.
- **Target:** Synthēsis Methods Note. Format per `reference_synthesis_journal.md`: ≤400w body, .docx A4 1.5spc, 11-pt Calibri / 12-pt TNR, Vancouver refs, OJS 5-step wizard.
- **Closing sentence:** points to the constructive companion paper for the proposed response.

### 3.2 Constructive companion paper (longer-form preprint)
- **Claim:** *Here is a buildable blueprint for African-led living evidence synthesis.*
- **Format:** 4–6k words, longer-form preprint. Targeted at BMJ Methods or JCE; preprint on Zenodo first.
- **Content:** the 8-layer architecture (§4), per-layer pointer to operationalising repo, two-tier maturity table, governance model.
- **DOI:** Zenodo at preprint, Crossref at journal acceptance. (Per Synthēsis policy: DOI minted at publication, not pre-publication.)

### 3.3 Index page
- **Location:** `tiba` meta-repo, GitHub Pages (`mahmood726-cyber.github.io/tiba/`).
- **Generator:** CI-driven. On push to `main`, GitHub Actions scans the federation (every repo on the user's GitHub account that contains a `tiba.yaml`), pulls the YAML manifests, and renders `index.html`.
- **Visual:** 8-layer architecture diagram (operational layers solid, roadmap layers dashed). Per-layer card with: layer name, owning repo link, headline metric, status badge (operational | roadmap), Pages URL (rendered only if HTTP 200 — see §8 mitigation).
- **Headline:** ARAC equity scoreboard (top 1–2 RGS numbers).
- **Self-contained:** no external CDN dependencies (per `rules.md` HTML-apps section).

### 3.4 Manifesto + governance
- **Manifesto:** 1 page, 4 sections — Vision / Scope / Governance / How-to-affiliate. Committed at `tiba/MANIFESTO.md`.
- **Governance:** lightweight. Mahmood as steward; named Makerere PIs as co-stewards (TBD draft-2); affiliated repos retain full local autonomy.
- **How-to-affiliate:** drop a `tiba.yaml` in your repo root with the schema in §5. PR adds your repo to the federation list (or just push — the CI generator auto-discovers if your repo is in the user's GitHub account).

---

## 4. Architecture — two-tier 5+3

### 4.1 Operational today (MVP-in for v0.1.0)
| Layer | Owning repo | Headline today |
|---|---|---|
| **Discovery** | `pactr-hiddenness-atlas` | NCT-bridge sensitivity 6.2% for PACTR-published African evidence (16/30 blinded vs 1/30 algorithm) |
| **Quality gates** | `repro-floor-atlas`, `pi-atlas`, `responder-floor-atlas`, `trial-truthfulness-atlas`, `cochrane-modern-re` | 5 Pairwise70 atlases shipped, all Pages-live |
| **Equity scoreboard** | `arac` | 5 RGS metrics on Cochrane African representation, dashboard + verification UI live |
| **Publishing rail** | `E156` workbook + `Synthēsis-Africa` (imprint, hosted by Synthēsis) | 558+ workbook entries, 7-sentence ≤156w E156 format, sub-week cadence |
| **Training rail** | `synthesis-courses` | 26 interactive evidence-synthesis courses × 12 languages, Pages-live since 2026-04-20 |

### 4.2 Roadmap (named in architecture, deferred)
| Layer | Milestone | Pre-condition |
|---|---|---|
| **Workforce activation** | v0.2 | Makerere PIs nominated; cohort enrols Tiba-tagged reviews next academic term |
| **Living updates** | v0.3 | Pick one African-priority condition (TBD); adapt CardioSynth's 57-app rolling-MA pattern |
| **Verification UI primitive** | v0.4 | Generalise RapidMeta one-trial-at-a-time pattern as a Tiba-reusable primitive across domains |

The constructive paper (§3.2) presents all 8 layers in one architecture figure, with operational vs roadmap visually distinct.

---

## 5. Repo structure & federation

### 5.1 Meta-repo
- **Local path:** `C:\Projects\tiba\`
- **Remote:** `github.com/mahmood726-cyber/tiba`
- **Top-level layout:**
  ```
  tiba/
    README.md                    # one-page intro, links to index page + papers
    MANIFESTO.md                 # the 1-page manifesto (§3.4)
    LICENSE                      # MIT (matches portfolio default)
    .gitignore
    .github/workflows/index.yml  # CI generator for index page
    docs/
      superpowers/specs/         # this design doc + writing-plans output
      papers/
        diagnostic/              # Synthēsis Methods Note draft + .docx
        constructive/            # longer-form preprint draft
    site/
      generator/                 # script that scans federation and renders index.html
      index.html                 # generated artifact (committed)
      assets/
    schema/
      tiba.yaml.schema.json      # JSON schema for tiba.yaml federation manifest
  ```

### 5.2 Federation manifest — `tiba.yaml`
Each affiliated repo drops this file at its root.

```yaml
# tiba.yaml — federation manifest for Tiba (the framework)
# Schema: https://github.com/mahmood726-cyber/tiba/blob/main/schema/tiba.yaml.schema.json
schema_version: 1
layer: discovery | quality-gate | equity | publishing | training | workforce | living-updates | verification-ui
status: operational | roadmap
owning_repo: <github-org>/<repo>
pages_url: https://<owner>.github.io/<repo>/
headline_metric:
  label: "NCT-bridge sensitivity for PACTR pubs"
  value: "6.2%"
  ci_or_qualifier: "[3.4%, 10.4%], n=30 blinded audit"
  source: "pactr-hiddenness-atlas v0.1.0"
contact:
  steward: mahmood726-cyber
  cohort: null   # or "makerere" / "saarc"
last_verified: 2026-05-05  # YYYY-MM-DD; CI uses this for staleness warnings
```

### 5.3 Layer enum is closed
The `layer` field is a closed enum of 8 values matching §4. New layers require a Tiba RFC (added to `docs/rfcs/` in the meta-repo). This prevents marketing-driven layer drift.

---

## 6. Authorship & governance

- **First / corresponding author (both papers):** mahmood726-cyber (Mahmood). Tiba is *not* an E156 micro-paper; the E156 middle-author-only rule (`feedback_e156_authorship.md`) does not apply.
- **Co-authors:** Makerere PI(s), **TBD — locked at draft-2.** Spec ships with this blank; ship of v0.1.0 (per acceptance criterion h, §7) gated on the blank being filled.
- **Acknowledged:** ARAC contributors, PACTR Hiddenness Atlas contributors, any Synthesis Courses contributors whose material is referenced.
- **Synthēsis editorial COI:** clean. Mahmood left the Synthēsis editorial board on 2026-04-20 (per `feedback_e156_authorship.md`).
- **Steward model:** Mahmood as v0.1.0 steward. After Makerere PI nomination (v0.2), governance becomes co-stewardship. Affiliated repos retain full local autonomy — Tiba imposes the manifest schema, not project rules.

---

## 7. Acceptance criteria for v0.1.0 ship

All ten must be true before v0.1.0 is tagged.

| # | Criterion | Verification |
|---|---|---|
| (a) | Diagnostic paper drafted to draft-1 (≤400w body) | Word-count check; structure matches Synthēsis Methods Note template |
| (b) | Constructive companion drafted to draft-1 (4–6k w) | Word-count check; all 8 layers present in architecture figure |
| (c) | Index page Pages-live at `mahmood726-cyber.github.io/tiba/` | HTTP 200 + visual smoke test |
| (d) | `MANIFESTO.md` committed | File exists in `main`, ≤1 page rendered |
| (e) | `tiba.yaml` JSON schema committed at `schema/tiba.yaml.schema.json` | Schema validates against a sample manifest |
| (f) | Sentinel: 0 BLOCK on the meta-repo | `python -m sentinel scan --repo C:\Projects\tiba` |
| (g) | ≥3 of the 5 operational repos have committed `tiba.yaml` | CI federation scan returns ≥3 manifests |
| (h) | Makerere PI(s) nominated and added to author list | Edit to `docs/papers/*/draft.md` author block |
| (i) | E156 workbook entry created (both papers as one entry under "framework") | Entry visible in `C:\E156\rewrite-workbook.txt` |
| (j) | Crossref/Zenodo DOI plan documented | Note in `docs/papers/README.md` saying "DOI at publication" |

---

## 8. Risks & mitigations

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | "Cochrane" slips into Tiba copy by accident | P0 (legal) | Sentinel pre-push regex on `cochrane` (case-insensitive) on the `tiba` repo. Allowlist: references in academic-citation context (Vancouver-format inside `docs/papers/` only). Fail-closed everywhere else. |
| R2 | Index page claims a layer is operational when its Pages site is dead | P1 | CI generator only renders a layer card if (i) `tiba.yaml` declares `status: operational` AND (ii) the declared `pages_url` returns HTTP 200 within 5s. Otherwise renders as "verification failed" with last-success date from `last_verified`. |
| R3 | Marketing-vs-implementation drift in papers | P1 | No-Marketing Rule (`lessons.md`). Spec self-review checks every claim against the operational tier. "Global", "Full", "Complete", "Integrated" require explicit citation to today's implementation. |
| R4 | Authorship friction stalls draft-2 | P1 | Acceptance criterion (h) gates v0.1.0 ship on PI nomination. Spec writing not blocked. |
| R5 | Scope creep into Makerere v0.2 work | P2 | v0.1.0 explicitly excludes any code that is "for the Makerere pilot". If found in scope review, defer. |
| R6 | Federation generator drift (a tiba.yaml is added to a repo whose Pages is broken) | P2 | R2 mitigation handles render-time. Plus: weekly CI cron scans federation and opens a GitHub issue per failing manifest. |
| R7 | LLM citation misattribution in the constructive paper's references | P1 | Per `lessons.md`: DOI-resolve every citation programmatically before push. Cap context at ≤10 sources per section. |
| R8 | Trademark complaint from a third party despite §1 posture | P2 | MANIFESTO.md includes explicit "not affiliated with the Cochrane Collaboration" disclaimer. README.md repeats it. |

---

## 9. Out of scope for v0.1.0 (explicit non-goals)

- Any new code for Makerere cohort enrolment (v0.2)
- Any new living-MA app (v0.3 — CardioSynth pattern is referenced, not extended)
- Any verification-UI primitive extraction work (v0.4)
- Any funder pitch deck or grant application (downstream)
- Any new student cohort beyond Makerere + SAARC (already in portfolio)
- Any retroactive renaming of existing repos to add a "tiba-" prefix (federation works without renames)

---

## 10. Open decisions (resolve before writing-plans)

| # | Decision | Default if not resolved |
|---|---|---|
| D1 | Makerere PI nominations | Spec ships with blank; user resolves before draft-2 |
| D2 | Constructive paper target journal: BMJ Methods vs JCE vs preprint-only | Default: Zenodo preprint at v0.1.0; journal target chosen at draft-2 |
| D3 | Site generator language: Python vs Node | Default: Python (matches portfolio default and existing toolchain) |
| D4 | African-priority condition for v0.3 living-MA pilot | Defer to v0.3 spec |
| D5 | Whether to include SAARC cohort under Tiba banner or keep as sibling framework | Default: sibling for now; Tiba is Africa-only by name |

---

## 11. References to existing portfolio

- PACTR Hiddenness Atlas — `C:\Projects\pactr-hiddenness-atlas\` + `github.com/mahmood726-cyber/pactr-hiddenness-atlas` (v0.1.0, shipped 2026-05-05)
- ARAC — `C:\Projects\arac\` + `github.com/mahmood726-cyber/arac` (v0.9.0)
- 5 Pairwise70 atlases — see `MEMORY.md` "Active Projects (top 8)" section
- Synthesis Courses — `github.com/mahmood726-cyber/synthesis-courses` (Pages-live)
- E156 workbook — `C:\E156\rewrite-workbook.txt`
- Synthēsis journal submission spec — `reference_synthesis_journal.md`
- Brainstorming methodology — `feedback_research_methodology.md` (brainstorm → spec → plan → TDD → audit, validated by DossierGap, ARAC, PACTR Hiddenness Atlas)

---

## 12. Successor

Next step is the **writing-plans** skill — produces the implementation plan that turns these acceptance criteria into ordered, TDD-able tasks. Plan target: ≤25 tasks, all paper-drafting tasks gated on the Makerere PI blank (D1) being filled.
