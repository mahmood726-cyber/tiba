---
title: "Tiba: a buildable framework for African-led living evidence synthesis"
short_title: "Tiba framework"
authors:
  - name: "Mahmood Ahmad"
    affiliation: "Makerere University, Uganda; Tiba steward"
    orcid: "TBD-pre-publication"
    corresponding: true
    email: "mahmood726@gmail.com"
    role: "First/corresponding author; Uganda PI for v0.1.0"
target_venue: "BMJ Methods or JCE (TBD at draft-2 — spec §10 D2); Zenodo preprint at v0.1.0"
format_constraints:
  word_count_target: 4500
  word_count_min: 4000
  word_count_max: 6000
  references: "Vancouver (default; reformat if target journal differs)"
keywords: ["evidence synthesis", "African research", "framework", "PACTR", "living evidence", "Tiba"]
date: 2026-05-06
status: draft-1
---

# Tiba: a buildable framework for African-led living evidence synthesis

**Mahmood Ahmad**, Makerere University, Uganda; Tiba steward  
Corresponding author: mahmood726@gmail.com  
Date: 2026-05-06 | Status: draft-1

---

## Abstract

**Background.** African clinical trials are systematically hidden from evidence synthesis infrastructure. The dominant discovery methodology — bridging registrations through ClinicalTrials.gov (NCT-bridge) — has 6.2% sensitivity for trials registered on the Pan-African Clinical Trials Registry (PACTR), the primary registry for African research. Even within the visible corpus, 14.3% of Cochrane meta-analyses on a 7,545-MA benchmark cannot be reproduced at the primary-estimand level. The tools to address these problems already exist but remain unconnected.

**Objective.** To present Tiba, a named, buildable framework that composes existing evidence-synthesis tools — discovery, quality gates, equity scoreboard, publishing, training — into a coherent African-led ecosystem, and to document the v0.1.0 operational state and roadmap.

**Methods.** Tiba is a framework declaration, not a novel research finding. Each of its eight architecture layers maps to a pre-existing, version-controlled repository with its own acceptance-tested codebase and live GitHub Pages deployment. A lightweight federation contract (`tiba.yaml`) and a JSON Schema allow affiliated repositories to self-declare their layer, status, and headline metric. A CI generator renders a live index page at https://mahmood726-cyber.github.io/tiba/ from these manifests, suppressing any card whose declared Pages URL returns a non-200 response.

**Results.** At v0.1.0, four of the five operational layers are seeded: Discovery (PACTR Hiddenness Atlas; NCT-bridge sensitivity 6.2%), Quality gates (Repro-Floor Atlas; 14.3% non-reproducibility on n=7,545 MAs), Equity scoreboard (African Representation Atlas of Cochrane, ARAC; inter-classifier kappa 1.000 on n=9 evaluable trials), and Training (Synthesis Courses; 26 courses x 12 languages, anchored at Makerere University with 190 students per week). The Publishing rail (E156 workbook) is not yet a federated GitHub repository and is designated a v0.2 task. Three roadmap layers — Workforce activation (v0.2), Living updates (v0.3), and Verification UI primitive (v0.4) — are named in the architecture but have explicit pre-conditions before any code is written.

**Conclusion.** Tiba demonstrates that a structurally coherent African-led living-evidence framework can be assembled from existing tools without inventing new methods. The v0.2 milestone commits to activating the Makerere PhD cohort under the Tiba banner, adding Makerere co-principal investigators, and completing the human inter-rater reliability audit that ARAC's v0.1.1 calibration defers. Tiba is not affiliated with the Cochrane Collaboration.

---

## 1. Introduction

The infrastructure of evidence synthesis was built for, and largely by, the global North. Its discovery layer — the apparatus that finds, screens, and ingests trials into systematic reviews and meta-analyses — depends on the assumption that registered trials are registered on ClinicalTrials.gov (NCT). That assumption does not hold in sub-Saharan Africa.

The Pan-African Clinical Trials Registry (PACTR) is the primary registry for trials conducted across Africa and is one of the registries recognised by the World Health Organisation's International Clinical Trials Registry Platform (ICTRP).[1,2] African investigators register on PACTR because it is purpose-built for the region, its forms accommodate context-specific study designs, and its registration fees are structured for lower-income research environments. Yet the dominant search methodology used by Cochrane systematic reviews and the majority of published meta-analyses — which queries PubMed, EMBASE, and CENTRAL using NCT identifiers as cross-reference keys — cannot bridge from a PACTR registration to a published trial report.

The PACTR Hiddenness Atlas quantified this gap empirically.[3] In a preregistered, blinded audit of 30 PACTR-registered trials with peer-reviewed publications, a human auditor identified 16 trials as findable via standard bibliographic search. An automated NCT-bridge algorithm found 1. The resulting sensitivity estimate of 6.2% (Wilson 95% CI 0.3%–30.2%) is not a rounding error — it is a structural property of a discovery system that was never designed for non-NCT registries.

The consequences compound. If a trial cannot be found, it cannot be included in a meta-analysis. If it cannot be included, any synthesised treatment effect is estimated on a non-representative sample of the evidence base. For African populations, whose disease burden, care pathways, and treatment responses may differ systematically from populations enrolled in Northern trials, exclusion of African evidence is not a minor nuisance — it is a validity threat to the evidence that informs their care.

The problem is not limited to what is hidden. Among the trials that are visible — those indexed in the Pairwise70 Cochrane dataset of 595 reviews and 7,545 individual meta-analyses — a second integrity problem exists at the synthesis level itself. The Repro-Floor Atlas demonstrates that 14.3% of those meta-analyses cannot be reproduced at the primary-estimand level (|delta| > 0.005 on the pooled effect) under a reference implementation using the declared statistical method.[4] Non-reproducibility is not distributed uniformly: continuous outcomes (25.0%) and generic inverse-variance analyses (27.0%) fail at twice the rate of binary outcomes (12.9%). A synthesis infrastructure that routinely imports non-reproducible computations is not a reliable foundation on which to build African-specific analyses.

Alongside these two empirical anchors, a third observation bears directly on the feasibility of improvement. The African Representation Atlas of Cochrane (ARAC) shows that automated LLM-based geographic classification of trial populations, calibrated against a blinded second-judge LLM, reaches a Tier-P inter-classifier agreement of kappa = 1.000 on the n=9 evaluable calibration trials.[5] This result requires careful interpretation — the evaluable subset is small, the comparison is LLM-versus-LLM not human gold standard, and upstream data-linkage errors affected 7 of 30 calibration trials — but it demonstrates that automated equity assessment at scale is not technically intractable. Human validation is the next precondition, not the primary technical barrier.

This paper presents **Tiba** (Swahili: *healing, medicine*), a named, buildable framework that responds to these three observations by composing existing tools into a coherent ecosystem. Tiba is not a new method, a new software system, or an organisation. It is a composition: a named architecture in which eight existing or planned layers fit together under a lightweight federation contract, with a CI-rendered index page that makes the composition legible and the integrity of each layer continuously verifiable. Every layer that is operational today already exists as a version-controlled, acceptance-tested GitHub repository with a live Pages deployment. Every layer that is on the roadmap has explicit pre-conditions before any code is written.

The paper proceeds as follows. Section 2 provides background on PACTR, the NCT-bridge methodology, and the reproducibility evidence that motivates the framework. Section 3 describes the eight-layer architecture in detail. Section 4 documents the federation contract that binds affiliated repositories. Section 5 reports the v0.1.0 operational state. Section 6 outlines the v0.2+ roadmap with concrete pre-conditions. Section 7 enumerates limitations with honesty about what v0.1.0 is not. Section 8 concludes with the framing thesis: composition, not invention.

---

## 2. Background

### 2.1 Trial registration and the NCT-bridge problem

The International Clinical Trials Registry Platform, maintained by the World Health Organisation, establishes standards for primary registries and acts as a portal across 17 member registries.[1] ClinicalTrials.gov, operated by the United States National Library of Medicine, is the largest single registry by volume and the de facto anchor of most systematic review search strategies.[6] Its NCT numbering system has become a near-universal cross-reference key: search filters in PubMed, registration-to-publication linkage algorithms in systematic review tools, and meta-data fields in EMBASE and CENTRAL all treat the NCT number as the canonical trial identifier.

PACTR was established in 2007 under the auspices of the South African Medical Research Council in response to advocacy for an Africa-specific registry that would reduce the friction of registration for African investigators.[7] By 2026, PACTR hosts registrations from over 40 African countries. Its structure differs from ClinicalTrials.gov in granularity, required fields, and the governance model for retrospective registration — all designed to accommodate the resource environment in which African trials operate.

The consequence of the dual-registry landscape is a linkage gap. Systematic reviews that source their search from PubMed and EMBASE using NCT-bridge methodology will retrieve a trial only if (a) the trial has an NCT registration that matches a publication's metadata, or (b) the publication is indexed with a free-text mention of an NCT number that the algorithm can extract. A trial with only a PACTR registration — or a publication whose abstract does not mention any registry number — is invisible to this pathway. The PACTR Hiddenness Atlas documents the magnitude of that invisibility: 6.2% sensitivity in a blinded n=30 audit.[3]

### 2.2 Reproducibility as a second integrity layer

Even if the discovery problem were solved, there is a second integrity problem within the visible corpus. Cochrane meta-analyses are among the most methodologically rigorous evidence products in medicine; their individual review protocols are pre-registered, their data-extraction processes dual-verified, and their statistical methods declared in advance. Yet, as the Repro-Floor Atlas demonstrates, 14.3% of analyses on a Pairwise70 benchmark cannot be reproduced to within |delta| = 0.005 of the published pooled effect.[4] The failures are not random: they concentrate in analyses that use generic inverse-variance methods and continuous outcomes, precisely the domains where heterogeneous software implementations produce the largest numerical divergence.

Reproducibility is a necessary but not sufficient condition for trustworthiness. An analysis that cannot be reproduced has no stable foundation on which to build. Any African-specific extension of Cochrane infrastructure — whether adding African trials to existing meta-analyses or conducting new African-population syntheses — must be built on a reproducible computational base.

### 2.3 Methodology baseline

The methodology that Tiba draws upon is described in the Cochrane Handbook for Systematic Reviews of Interventions, version 6.5 (2024),[8] the PRISMA 2020 statement,[9] the Grading of Recommendations Assessment, Development and Evaluation (GRADE) framework,[10] and Cochrane's Risk of Bias tool version 2.[11] The standard meta-analysis reference methods include the DerSimonian-Laird estimator[23] and the Hartung-Knapp-Sidik-Jonkman variance correction.[24,25] The textbook-level treatment of these methods is Borenstein et al.[26] These are openly licensed methodological standards; using them does not imply any affiliation with the Cochrane Collaboration.

---

## 3. The eight-layer Tiba architecture

Tiba's architecture is organised into two tiers: five operational layers, seeded or in active deployment at v0.1.0, and three roadmap layers whose pre-conditions are explicit.

**Figure 1** *(SVG to be produced at draft-2)*: Eight-layer architecture diagram. Operational layers rendered as solid boxes with owning repo name; roadmap layers as dashed outlines with pre-condition text and milestone target. Arrows indicate data flow: Discovery feeds Quality gates; Quality gates and Equity scoreboard feed Publishing rail; Training rail and Workforce activation operate in parallel; Living updates feeds back into Quality gates; Verification UI serves both Equity and Workforce.

---

### 3.1 Discovery (operational)

**Owning repository:** `mahmood726-cyber/pactr-hiddenness-atlas`  
**Pages:** https://mahmood726-cyber.github.io/pactr-hiddenness-atlas/

The Discovery layer addresses the fundamental question: what African evidence exists and how much of it is currently invisible to mainstream synthesis? The PACTR Hiddenness Atlas answers this by implementing a preregistered, blinded, n=30 audit of PACTR-registered trials with peer-reviewed publications.[3] The headline metric — NCT-bridge sensitivity 6.2% (Wilson 95% CI 0.3%–30.2%) — was derived by comparing an automated algorithm's performance against a blinded human auditor on the same 30 trials. The algorithm identified 1 trial; the auditor identified 16. This is not an algorithm defect that can be patched: it reflects the structural absence of NCT identifiers in PACTR-registered trial publications. The result was preregistered using OpenTimestamps-anchored Bitcoin blockchain attestation (three calendar OTS confirmations: spec, sample, instrument).[12]

The v0.2 Discovery roadmap extends the Atlas by implementing PACTR-ID direct retrieval via the EuropePMC API, bypassing the NCT-bridge entirely. This is a known technical pathway — EuropePMC indexes PACTR IDs in its trial-registration metadata — and represents the single highest-priority sensitivity improvement identified in the Atlas's gap analysis.

---

### 3.2 Quality gates (operational)

**Primary owning repository:** `mahmood726-cyber/repro-floor-atlas`  
**Supporting repositories:** `mahmood726-cyber/pi-atlas`, `mahmood726-cyber/responder-floor-atlas`, `mahmood726-cyber/trial-truthfulness-atlas`, `mahmood726-cyber/cochrane-modern-re`

The Quality gates layer provides five complementary lenses on the integrity of the visible corpus, each calibrated against the Pairwise70 dataset of 595 Cochrane reviews and 7,545 meta-analyses.[13]

The **Repro-Floor Atlas** is the primary quality-gate instrument.[4] Across all 7,545 MAs, 14.3% fail reproduction at |delta| > 0.005 on the pooled effect; failure rates by outcome type are 12.9% (binary), 25.0% (continuous), and 27.0% (generic inverse-variance). The non-reproducible subset is approximately twice as sensitive to statistical method choice, meaning that downstream re-analyses of this subset face compounded uncertainty.

The **Prediction Interval Atlas** (PI Atlas) quantifies the calibration of Cochrane prediction intervals across the Pairwise70 corpus — a year-long computational study currently in pre-registration, with compute on dedicated hardware and a six-week check-in routine from June 2026. The prediction interval methodology follows Viechtbauer's Q-profile approach[21] and the IntHout et al. advocacy for routine PI reporting.[22]

The **Responder Floor Atlas** demonstrates that empirical implied minimally important differences exceed published canonical thresholds by 1.28- to 3.81-fold across the four reviews examined (clustered bootstrap 95% CI; 2,013 trial-arm observations).[14] The atlas also notes that treatment rankings — often summarised as SUCRA values in network meta-analyses — require the complementary POTH (Probability of Treatment being Optimal for the Hierarchy) statistic[20] to convey rank uncertainty; the Responder Floor findings carry the same interpretive discipline. This finding directly informs the equity assessment question: if the threshold used to declare treatment success is miscalibrated for the Northern populations in which it was derived, applying that threshold to African-population subgroups compounds the bias.

The **Trial Truthfulness Atlas** implements five integrity flags per trial (NCT-bridge linkage, outcome drift via a locally-running LLM, N drift, direction concordance, and FDAAA results-posting compliance) on a fixture corpus of five cardiology trials, with AACT-linked extension to full sweep at v0.2.[15]

The **cochrane-modern-re** repository quantifies the impact of switching from DerSimonian-Laird estimation to REML with HKSJ correction on Pairwise70 MAs, finding that 8.2% of Tier-1 MAs flip statistical significance under the methodological update — a calibration check relevant to any new African meta-analysis choosing its estimator.[16]

Together, these five instruments constitute a quality-gate layer that characterises the error floor of the evidence base before any African-specific contribution enters it.

---

### 3.3 Equity scoreboard (operational)

**Owning repository:** `mahmood726-cyber/arac`  
**Pages:** https://mahmood726-cyber.github.io/arac/

The Equity scoreboard quantifies the geographic distribution of trial populations in Cochrane reviews, using the African Representation Atlas of Cochrane (ARAC).[5] ARAC implements five Representation Gap Score (RGS) metrics: trial-origin gap, population-enrolled gap, authorship gap, language-of-publication gap, and registry-type gap.

At v0.1.1, ARAC reports a calibration result on the LLM-based geographic classifier: Tier-P inter-classifier kappa = 1.000 on n=9 evaluable calibration trials (opus production classifier vs sonnet blinded judge). The evaluable subset is small because 7 of the 30 calibration trials were affected by upstream Pairwise70 PMID linkage errors (documented as R9 in the ARAC specification) and 14 further trials had geography-silent abstracts that both classifiers could not resolve. The sensitivity proxy — the fraction of geography-informative trials correctly classified — was 100% (Wilson 95% CI 34.2%–100%).

These results are encouraging but require two caveats. First, the comparison is LLM-versus-LLM, not LLM-versus-human gold standard. Second, the underlying R9 PMID errors in Pairwise70 — which are an upstream data-quality issue, not an ARAC defect — inflate the "Insufficient" classification rate beyond what would be observed on a corrected dataset.

The production RGS atlas — the population-level estimate of African-trial representation across all 595 Pairwise70 reviews — is deferred to v0.2. Producing it requires approximately $30 of LLM API usage for the full-corpus batch classification run. This is a deliberate authorisation gate: the classification architecture is validated, the batch is ready to run, but authorisation is required before the compute is executed. The v0.1.0 equity scoreboard ships the validation evidence, not the production headline number.

The ARAC verification UI (a RapidMeta one-trial-at-a-time interface accessible at the federation index) allows a human reviewer to inspect, confirm, or override any single-trial classification with a timestamped audit trail and JSON export. This UI is the precursor to the v0.4 Verification UI primitive layer.

---

### 3.4 Publishing rail (operational)

**Primary instrument:** E156 micro-paper format (workbook at `C:\E156\rewrite-workbook.txt`)  
**Imprint:** Synthēsis-Africa (to be established as an imprint of Synthēsis journal)

The Publishing rail closes the loop between evidence generation and dissemination. Its primary instrument is the E156 format: a seven-sentence, at-most-156-word structured micro-paper with one named primary estimand.[17] The format enforces clarity at the point of writing — each sentence has a declared function (question, dataset, method, result, robustness, interpretation, boundary) and a word budget — and the resulting papers are short enough to submit and review in sub-week turnaround cycles.

As of v0.1.0, the E156 workbook contains 558+ entries representing the aggregate output of applying this format across the portfolio. The sub-week cadence is documented by commit timestamps across the portfolio history. Synthēsis, the open-access methods journal that hosts the E156 Methods Note series, has validated that the format meets its Methods Note criteria (up to 400 words, Vancouver references, OJS submission workflow).

The Publishing rail is not yet a federated GitHub repository — the workbook is maintained as a local text file. Migrating it to a version-controlled, Pages-rendered entry in the federation is a v0.2 task. For v0.1.0, the rail is operational in the sense that it is actively producing disseminated output; it is roadmap in the sense of federation formalisation.

---

### 3.5 Training rail (operational)

**Owning repository:** `mahmood726-cyber/synthesis-courses`  
**Pages:** https://mahmood726-cyber.github.io/synthesis-courses/

The Training rail operationalises the principle that any evidence ecosystem is only as strong as the workforce trained to use it. Synthesis Courses delivers 26 interactive, browser-based evidence-synthesis courses in 12 languages, hosted via GitHub Pages since 2026-04-20.[18] The courses cover systematic review fundamentals, meta-analysis methods, risk of bias assessment, GRADE, and interpretation of pooled effects.

The courses are anchored institutionally at Makerere University, where a 190-student-per-week teaching cohort uses them as the primary instructional resource. This is not an outreach programme — it reflects the reality that Mahmood Ahmad is an insider at the institution, and the course adoption is organic rather than imposed. The presence of 190 students per week engaging with evidence-synthesis methods in a resource-constrained African setting provides both the training pipeline for the v0.2 Workforce activation layer and the proof-of-concept that the training rail is functional at meaningful scale.

The multilingual design (12 languages, with interfaces including English, French, Arabic, and Swahili) directly addresses the language-of-publication gap that ARAC identifies as one of its five RGS metrics. African research published in French or Portuguese is doubly hidden: invisible to NCT-bridge discovery and linguistically excluded from English-language training materials.

---

### 3.6 Workforce activation (roadmap, v0.2)

The Workforce activation layer formalises the Makerere PhD cohort under the Tiba banner. The v0.2 milestone commits to three concrete pre-conditions before any cohort work begins. First, 2-3 additional Makerere co-principal investigators must be nominated, expanding the African-PI roster beyond the single-insider model of v0.1.0 and formalising plural African leadership. Second, the cohort must enrol Tiba-tagged reviews in the next academic term, using the existing course infrastructure as the methodological foundation. Third, ARAC's v0.1.1 calibration must be extended to include a human inter-rater reliability audit — the Makerere PhD students provide the human annotators whose classifications establish the gold-standard sensitivity estimate that LLM-versus-LLM comparison cannot.

The Workforce activation layer follows the principle established in `feedback_makerere_student_workload.md`: cohort projects are verification-not-extraction. Students confirm algorithmically pre-classified decisions in the RapidMeta one-trial-at-a-time interface rather than performing raw data extraction from scratch. This constraint is intentional: it ensures that student effort is methodologically reliable (structured confirmation is more reproducible than free-form extraction), educationally productive (engagement with real evidence products), and tractable within the time constraints of a taught PhD programme.

---

### 3.7 Living updates (roadmap, v0.3)

The Living updates layer extends the CardioSynth pattern — a portfolio of 57 continuously-updated living meta-analysis apps for cardiology, each updating on a weekly cadence from new trial data — to a single African-priority clinical condition chosen at the v0.3 specification stage. The specific condition is deliberately deferred: selecting it requires engagement with the newly-nominated Makerere co-principal investigators, because African-priority condition identification is a substantive scientific decision that must not be made unilaterally by the framework steward.

The technical pattern for living updates is proven. CardioSynth's architecture demonstrates that rolling meta-analyses can be maintained at sub-week update cadence from a single-developer repository using browser-based JavaScript meta-analysis engines, no server-side infrastructure, and GitHub Pages for distribution. Adapting this pattern to one African-priority condition is a matter of configuration and data curation, not novel engineering.

---

### 3.8 Verification UI primitive (roadmap, v0.4)

The Verification UI primitive generalises the RapidMeta one-trial-at-a-time pattern into a reusable Tiba component that any affiliated repository can embed. At v0.1.1, ARAC already ships a working instance of this pattern: the verification UI allows a single reviewer to inspect one trial record, see its algorithmically-assigned geographic classification with evidence text, confirm or override the classification, and export a timestamped audit log in JSON. The v0.4 task is to extract this pattern into a shared library — decoupled from the ARAC-specific data model — so that any Tiba-affiliated project requiring human-in-the-loop verification can adopt it without reimplementing from scratch.

The timing of v0.4 is conditional on v0.2 and v0.3 providing sufficient real-world usage to identify the generalisable API boundaries. Building a reusable primitive before its use cases are empirically characterised risks premature abstraction.

---

## 4. Federation contract (`tiba.yaml`)

The mechanism that binds affiliated repositories into a coherent framework — without imposing any project-internal constraints — is the `tiba.yaml` federation manifest.

### 4.1 Schema design

The manifest is governed by a JSON Schema at `schema/tiba.yaml.schema.json` in the Tiba meta-repository.[19] The schema uses the JSON Schema draft 2020-12 specification. Eight fields are required:

- `schema_version` (integer, constant 1): enables forward-compatible schema evolution without breaking existing manifests.
- `layer` (closed enum): one of eight values matching the Tiba layer architecture exactly. New layers require a Tiba Request for Comments (RFC) document to be committed to `docs/rfcs/` in the meta-repository before the schema is updated. This prevents marketing-driven layer proliferation — a lesson drawn from past experience with agent-authored systems that acquire indefinitely expanding capability claims.
- `status` (enum: `operational` | `roadmap`): declared by the repo maintainer. Operationally important: the CI index generator only renders a layer card if `status: operational` AND the declared `pages_url` returns HTTP 200 within five seconds. A repository that declares itself operational but whose Pages site is unreachable renders as "verification failed" with the `last_verified` date.
- `owning_repo` (string, pattern `<owner>/<repo>`): the GitHub repository identity.
- `pages_url` (URI, must begin with `https://`): the live Pages deployment. The HTTP-200 gate is the R2 mitigation in the risk register.
- `headline_metric` (object): `label`, `value`, `source` (required), plus optional `ci_or_qualifier`. This forces every affiliated repository to declare a single verifiable summary number — resisting the temptation to claim broad impact without a computable anchor.
- `contact` (object): `steward` (required) and optional `cohort` (null, `makerere`, or `saarc`). The cohort field links to the Workforce activation layer without requiring any shared infrastructure.
- `last_verified` (date, YYYY-MM-DD): provides a staleness signal. The CI generator emits a warning in the index page for any manifest with `last_verified` more than 90 days in the past.

### 4.2 Affiliation process

Affiliation is deliberately frictionless. A repository maintainer who wishes to join the federation completes three steps: (1) decide which of the eight layer values applies; (2) create a `tiba.yaml` file at the repository root populated according to the schema; (3) push. No pull request to the Tiba meta-repository is required for repositories owned by `mahmood726-cyber`. For external repositories, a pull request adding the repo to `federation.yaml` in the meta-repository triggers the CI generator to discover the new manifest on the next build cycle.

The v0.1.0 federation uses a curated `federation.yaml` file that lists affiliated repositories explicitly. The v0.2 enhancement replaces this with the GitHub Search API to auto-discover any repository on the user's GitHub account that contains a `tiba.yaml` — removing the manual curation step.

### 4.3 Canonical manifest example

The canonical YAML for the PACTR Hiddenness Atlas, which seeds the Discovery layer, is:

```yaml
schema_version: 1
layer: discovery
status: operational
owning_repo: mahmood726-cyber/pactr-hiddenness-atlas
pages_url: https://mahmood726-cyber.github.io/pactr-hiddenness-atlas/
headline_metric:
  label: "NCT-bridge sensitivity for PACTR-registered publications"
  value: "6.2%"
  ci_or_qualifier: "Wilson 95% CI 0.3%–30.2%; n=30 blinded audit"
  source: "pactr-hiddenness-atlas v0.1.0"
contact:
  steward: mahmood726-cyber
  cohort: null
last_verified: 2026-05-05
```

### 4.4 Trademark guard

A pre-push script (`scripts/pre_push_cochrane_guard.py`) enforces the trademark posture described in §1 and the Manifesto. The script uses a regular expression to detect the string "cochrane" (case-insensitive) in any committed file outside the `docs/papers/` directory tree. Files in `docs/papers/` are allowlisted because academic-citation use of "Cochrane Handbook" or "Cochrane Collaboration" in references and running text is legitimate and necessary. The script exits non-zero if a violation is detected, blocking the push. The allowlist is explicit in the script source to prevent silent expansion.

---

## 5. Operational evidence

At v0.1.0, four repositories are enumerated in `federation.yaml` and confirmed operational. The fifth operational-tier layer (Publishing rail) is active but not yet a federated repository.

### 5.1 PACTR Hiddenness Atlas — Discovery layer

**Repository:** `mahmood726-cyber/pactr-hiddenness-atlas`  
**Version:** v0.1.0 (tag confirmed; last commit `76e933f`)  
**Pages:** https://mahmood726-cyber.github.io/pactr-hiddenness-atlas/ (HTTP 200 confirmed)  
**Test suite:** 97 tests, 0 Sentinel BLOCK  
**Headline:** NCT-bridge sensitivity = 6.2% (1/30 algorithm vs 16/30 human auditor); atlas.csv byte-for-byte pinned; three OTS calendar confirmations (spec, sample, instrument)

This repository is the primary empirical anchor for the Tiba framework. Its v0.1.0 preregistration was stamped using OpenTimestamps Bitcoin blockchain attestation on all three substantive documents (specification, sample list, audit instrument) before any data collection. The blinding was enforced procedurally: the automated algorithm was run to completion before the human auditor conducted the review, and the auditor's classifications were finalised before the two were compared. The Spot-check 0/30 algorithm-vs-auditor agreement is the finding — not a failure of the study.

### 5.2 ARAC — Equity scoreboard layer

**Repository:** `mahmood726-cyber/arac`  
**Version:** v0.1.1 (tags: prereg-v0.1.1.0, prereg-v0.1.1.1-amend-1, prereg-v0.1.1.2-amend-2, v0.1.1)  
**Pages:** https://mahmood726-cyber.github.io/arac/ (HTTP 200 confirmed)  
**Test suite:** 110 tests, 1 skip, 0 Sentinel BLOCK  
**Headline:** Tier-P inter-classifier kappa = 1.000 on n=9 evaluable trials; R9 caveat (7 trials affected by upstream Pairwise70 PMID errors); production RGS atlas deferred pending $30 LLM batch authorisation

The ARAC v0.1.1 calibration result (kappa = 1.000, sensitivity proxy 100%, Wilson 95% CI 34.2%–100%) demonstrates methodological consistency between two independently-prompted LLM classifiers. The small evaluable sample (n=9) reflects upstream data quality, not a design weakness: the Pairwise70 PMID linkage errors that excluded 7 trials are documented in the ARAC specification as R9 and are a known limitation of the Pairwise70 dataset. The implication for interpretation is that the production RGS atlas — when authorised and run — will operate on a partially-imperfect input; any resulting "Insufficient" classifications should be interpreted with this in mind.

### 5.3 Repro-Floor Atlas — Quality gates layer (representative)

**Repository:** `mahmood726-cyber/repro-floor-atlas`  
**Version:** v0.1.0 (tag confirmed; commit `42eb4b5`)  
**Pages:** https://mahmood726-cyber.github.io/repro-floor-atlas/ (HTTP 200 confirmed)  
**Test suite:** 102 tests, 0 Sentinel BLOCK  
**Headline:** 14.3% non-reproducible MAs at |delta|>0.005 (n=7,545 MAs / 595 reviews; binary 12.9%, continuous 25.0%, GIV 27.0%)

This repository serves as the representative Quality gates seed in the federation. All five quality-gate instruments have their own repositories, but the Repro-Floor Atlas provides the most directly actionable figure for the African-synthesis motivation: before any African-specific analysis is added, the existing infrastructure's reproducibility floor must be understood.

### 5.4 Synthesis Courses — Training layer

**Repository:** `mahmood726-cyber/synthesis-courses`  
**Pages:** https://mahmood726-cyber.github.io/synthesis-courses/ (HTTP 200 confirmed; live since 2026-04-20)  
**Scale:** 26 interactive courses × 12 languages; 335 files, 63.7 MB  
**Institutional anchor:** Makerere University, 190 students/week  
**Headline:** training rail operational at meaningful scale before v0.2 workforce activation

### 5.5 Publishing rail — operational but not yet federated

The E156 workbook, with 558+ entries as of v0.1.0, demonstrates sub-week publication cadence. However, the workbook is maintained as a local text file at `C:\E156\rewrite-workbook.txt` and has not been migrated to a version-controlled, Pages-rendered GitHub repository. Migrating this to a federated entry is a v0.2 task. For the purposes of the federation index, the Publishing rail does not appear as a live card at v0.1.0 — a deliberate choice to maintain the HTTP-200 gate's integrity rather than list a layer that cannot be programmatically verified.

---

## 6. Roadmap (v0.2+)

### 6.1 v0.2 — Workforce activation (target: next Makerere academic term)

The v0.2 milestone has three mandatory pre-conditions, all of which must be satisfied before any v0.2 code is written:

1. **Co-PI nominations.** 2-3 additional Makerere University faculty or senior PhD supervisors must agree to serve as named co-principal investigators on the Tiba framework. This is not an administrative formality — it transforms Tiba from a single-insider framework into a genuinely plural African-led enterprise. The criteria for co-PI nomination are: active research role at Makerere or a peer African institution, engagement with at least one Tiba-affiliated layer (training, equity, or discovery), and willingness to take responsibility for the accuracy of any affiliated repo's data within their domain.

2. **Cohort enrolment.** The Makerere PhD cohort must formally enrol Tiba-tagged reviews as part of its coursework in the next academic term. Enrolment means that student verifications are committed to ARAC's verification UI with student identifiers, timestamped audit logs, and supervisor sign-off — not informal participation.

3. **ARAC human IRR audit.** The inter-rater reliability audit that ARAC v0.1.1 defers must be completed with Makerere PhD students as human annotators. This audit will produce the human gold-standard sensitivity estimate that ARAC's v0.1.1 calibration cannot provide (because LLM-versus-LLM is not a gold standard). The audit will also determine whether the Pairwise70 R9 PMID errors systematically bias the RGS atlas results or affect them only marginally.

Once these three pre-conditions are met, v0.2 will also migrate the E156 workbook to a federated GitHub repository, completing the fifth operational layer.

### 6.2 v0.3 — Living updates (target: one African-priority condition)

The v0.3 milestone adapts the CardioSynth rolling-MA pattern to one African-priority clinical condition. Condition selection requires engagement with the v0.2 co-principal investigators — it is a substantive scientific decision that must reflect African epidemiological priorities, not the framework steward's preferences.

### 6.3 v0.4 — Verification UI primitive

The v0.4 milestone extracts the RapidMeta one-trial-at-a-time verification pattern into a reusable Tiba component. Timing is conditional on v0.2 and v0.3 providing sufficient empirical usage to characterise the generalisable API.

---

## 7. Limitations

The following limitations apply to v0.1.0 and should be understood by any reader or reviewer before the framework is cited or adopted.

**Tiba v0.1.0 is a framework declaration, not a working pipeline.** The eight layers are named, the federation contract is specified, and the operational layers are seeded — but no trial has been discovered, synthesised, and published end-to-end through Tiba as an integrated pipeline. That capability is v0.2+ work and depends on co-PI nomination and cohort enrolment.

**Tiba is not a funded programme.** All v0.1.0 work was conducted without dedicated external funding, using open-source tools, free-tier GitHub infrastructure, and academic affiliation. The $30 LLM API cost required to run the ARAC production RGS atlas is itself a binding authorisation gate — a figure that illustrates both the low marginal cost of the infrastructure and the deliberate governance discipline applied to incremental resource use.

**Tiba is not yet a multi-PI consortium.** At v0.1.0, Mahmood Ahmad is the sole Uganda/Makerere PI and the sole Tiba steward. The plural African leadership that the framework's vision requires is an explicit v0.2 deliverable, not a current reality. Papers and presentations that cite this framework should note the single-PI limitation at v0.1.0.

**Federation generator uses curated discovery at v0.1.0.** The `federation.yaml` file that drives index generation is manually maintained. Auto-discovery via the GitHub Search API is a v0.2 enhancement. Any repo that commits a `tiba.yaml` but is not listed in `federation.yaml` will not appear on the index page until `federation.yaml` is updated.

**ARAC's production RGS atlas is deferred.** The v0.1.1 equity scoreboard ships the calibration evidence, not the headline population-level representation number. Readers should not cite ARAC as evidence of a specific African-trial representation percentage in Cochrane reviews because that computation has not been authorised or run.

**ARAC's calibration is LLM-versus-LLM, not LLM-versus-human.** The kappa = 1.000 result on n=9 evaluable trials demonstrates internal consistency between two independently-prompted LLM classifiers. It does not demonstrate that either classifier agrees with human geographic classification of the same trials. Human gold-standard validation is the primary deliverable of the v0.2 IRR audit.

**Upstream Pairwise70 PMID errors affect ARAC calibration.** The R9 documentation in the ARAC specification records that 7 of 30 calibration trials were excluded because of PMID linkage errors in the Pairwise70 dataset. These are upstream errors that ARAC cannot correct, but they mean that the calibration sample is not a simple random sample of Pairwise70 trials — it is the subset for which linkage was successful.

**Four of five operational layers are seeded.** The Publishing rail (E156 workbook) is not yet a federated GitHub repository. The federation index at v0.1.0 does not render a Publishing rail card.

---

## 8. Conclusion

Tiba's thesis is composition, not invention. The tools required to build a pan-African, African-led, living-evidence ecosystem already exist. The PACTR Hiddenness Atlas provides a quantified account of the discovery gap. The five Pairwise70 atlases provide a reproducibility floor beneath which any new synthesis must not descend. ARAC provides an equity scoreboard against which African-population representation can be tracked. Synthesis Courses provides a training infrastructure that is already running at scale at Makerere. The E156 format and Synthēsis-Africa imprint provide a publishing rail that can disseminate findings in sub-week cycles.

What was missing was a name for how these pieces fit together — a framework document, a federation contract, and a CI-rendered index that makes the composition legible and its integrity continuously verifiable. Tiba v0.1.0 provides that.

The moonshot framing is deliberate. An African-led living-evidence ecosystem that discovers PACTR-registered trials invisible to current infrastructure, synthesises them to reproducible standards, scores their equity representation, trains a PhD-level workforce to verify the results, and publishes them in a format readable in days rather than months — that is not a marginal improvement. It is a structural change to who participates in evidence synthesis and whose health questions get answered.

The v0.2 commitment is concrete: nominate 2-3 Makerere co-principal investigators, enrol the PhD cohort under the Tiba banner in the next academic term, and complete the ARAC human IRR audit that transforms a promising calibration result into a validated gold-standard sensitivity estimate. The pathway from v0.1.0 to a working multi-PI consortium is defined, its pre-conditions are explicit, and its first milestone is within one academic term.

**Tiba is not affiliated with the Cochrane Collaboration.**

---

## References

1. World Health Organization. International Clinical Trials Registry Platform (ICTRP). Geneva: WHO; 2023. Available from: https://www.who.int/clinical-trials-registry-platform. DOI: TBD-pre-publication

2. Pan African Clinical Trials Registry. About PACTR. Cape Town: South African Medical Research Council; 2024. Available from: https://pactr.samrc.ac.za. DOI: TBD-pre-publication

3. Ahmad M. PACTR Hiddenness Atlas v0.1.0: NCT-bridge sensitivity for PACTR-registered African publications. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/pactr-hiddenness-atlas. DOI: TBD-pre-publication

4. Ahmad M. Repro-Floor Atlas v0.1.0: reproducibility of Cochrane meta-analyses at the primary-estimand level. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/repro-floor-atlas. DOI: TBD-pre-publication

5. Ahmad M. African Representation Atlas of Cochrane (ARAC) v0.1.1: geographic equity in Cochrane meta-analyses. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/arac. DOI: TBD-pre-publication

6. Zarin DA, Tse T, Williams RJ, Califf RM, Ide NC. The ClinicalTrials.gov results database — update and key issues. N Engl J Med. 2011;364(9):852–60. DOI: 10.1056/NEJMsa1012065

7. Nchinda TC. Research capacity strengthening in the South. Soc Sci Med. 2002;54(11):1699–711. DOI: 10.1016/S0277-9536(01)00338-1

8. Higgins JPT, Thomas J, Chandler J, Cumpston M, Li T, Page MJ, Welch VA (editors). Cochrane Handbook for Systematic Reviews of Interventions, version 6.5. Cochrane; 2024. Available from: https://training.cochrane.org/handbook. DOI: 10.1002/9781119536604

9. Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71. DOI: 10.1136/bmj.n71

10. Guyatt GH, Oxman AD, Vist GE, Kunz R, Falck-Ytter Y, Alonso-Coello P, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924–6. DOI: 10.1136/bmj.39489.470347.AD

11. Sterne JAC, Savovic J, Page MJ, Elbers RG, Blencowe NS, Boutron I, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898. DOI: 10.1136/bmj.l4898

12. OpenTimestamps. Bitcoin calendar attestation service. Available from: https://opentimestamps.org. DOI: TBD-pre-publication

13. Pairwise70 dataset. Cochrane meta-analyses benchmark (595 reviews, 7,545 MAs). DOI: TBD-pre-publication

14. Ahmad M. Responder Floor Atlas v0.3.0: empirical implied minimally important differences in Cochrane meta-analyses. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/responder-floor-atlas. DOI: TBD-pre-publication

15. Ahmad M. Trial Truthfulness Atlas v0.1.0: trial integrity flags for Cochrane-linked cardiology trials. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/trial-truthfulness-atlas. DOI: TBD-pre-publication

16. Ahmad M. cochrane-modern-re: DL-to-REML heterogeneity estimator flip-rate on Pairwise70. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/cochrane-modern-re. DOI: TBD-pre-publication

17. Ahmad M. E156 specification v0.2: seven-sentence, 156-word evidence micro-paper format. Synthēsis; 2026. DOI: TBD-pre-publication

18. Ahmad M. Synthesis Courses: 26 interactive evidence-synthesis courses in 12 languages. GitHub Pages; 2026. Available from: https://mahmood726-cyber.github.io/synthesis-courses. DOI: TBD-pre-publication

19. Ahmad M. Tiba meta-repository v0.1.0: federation schema and index generator for African-led living evidence synthesis. GitHub; 2026. Available from: https://github.com/mahmood726-cyber/tiba. DOI: TBD-pre-publication

20. Wigle J, Salanti G, Rücker G, Schmid C, Nikolakopoulou A. Probability of treatment being optimal for the hierarchy in network meta-analysis. Stat Med. 2025. DOI: TBD-pre-publication

21. Viechtbauer W. Confidence intervals for the amount of heterogeneity in meta-analysis. Stat Med. 2007;26(1):37–52. DOI: 10.1002/sim.2514

22. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. BMJ Open. 2016;6(7):e010247. DOI: 10.1136/bmjopen-2015-010247

23. DerSimonian R, Laird N. Meta-analysis in clinical trials. Control Clin Trials. 1986;7(3):177–88. DOI: 10.1016/0197-2456(86)90046-2

24. Hartung J, Knapp G. A refined method for the meta-analysis of controlled clinical trials with binary outcome. Stat Med. 2001;20(24):3875–89. DOI: 10.1002/sim.1009

25. Sidik K, Jonkman JN. A simple confidence interval for meta-analysis. Stat Med. 2002;21(21):3153–9. DOI: 10.1002/sim.1262

26. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. Chichester: Wiley; 2009. DOI: 10.1002/9780470743386


---

## Appendix A: `tiba.yaml` schema (full JSON)

The following is the complete JSON Schema (`schema/tiba.yaml.schema.json`) as committed in the Tiba meta-repository at v0.1.0. Included here for reviewer convenience.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/mahmood726-cyber/tiba/blob/main/schema/tiba.yaml.schema.json",
  "title": "Tiba Federation Manifest",
  "description": "Manifest dropped at the root of any repo affiliated with the Tiba framework.",
  "type": "object",
  "required": [
    "schema_version",
    "layer",
    "status",
    "owning_repo",
    "pages_url",
    "headline_metric",
    "contact",
    "last_verified"
  ],
  "additionalProperties": false,
  "properties": {
    "schema_version": { "type": "integer", "const": 1 },
    "layer": {
      "type": "string",
      "enum": [
        "discovery",
        "quality-gate",
        "equity",
        "publishing",
        "training",
        "workforce",
        "living-updates",
        "verification-ui"
      ]
    },
    "status": { "type": "string", "enum": ["operational", "roadmap"] },
    "owning_repo": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
    },
    "pages_url": {
      "type": "string",
      "format": "uri",
      "pattern": "^https://"
    },
    "headline_metric": {
      "type": "object",
      "required": ["label", "value", "source"],
      "additionalProperties": false,
      "properties": {
        "label": { "type": "string", "minLength": 1, "maxLength": 200 },
        "value": { "type": "string", "minLength": 1, "maxLength": 100 },
        "ci_or_qualifier": { "type": "string", "maxLength": 200 },
        "source": { "type": "string", "minLength": 1, "maxLength": 200 }
      }
    },
    "contact": {
      "type": "object",
      "required": ["steward"],
      "additionalProperties": false,
      "properties": {
        "steward": { "type": "string", "minLength": 1 },
        "cohort": {
          "anyOf": [
            { "type": "null" },
            { "type": "string", "enum": ["makerere", "saarc"] }
          ]
        }
      }
    },
    "last_verified": {
      "type": "string",
      "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
    }
  }
}
```

---

## Appendix B: Acceptance criteria for v0.1.0 ship (from spec §7)

The following ten criteria must all be true before the v0.1.0 tag is applied. Reproduced from `docs/superpowers/specs/2026-05-05-tiba-design.md` §7 for reviewer convenience.

| # | Criterion | Verification |
|---|---|---|
| (a) | Diagnostic paper drafted to draft-1 (≤400w body) | Word-count check; structure matches Synthēsis Methods Note template |
| (b) | Constructive companion drafted to draft-1 (4–6kw) | Word-count check; all 8 layers present in architecture section |
| (c) | Index page Pages-live at `mahmood726-cyber.github.io/tiba/` | HTTP 200 + visual smoke test |
| (d) | `MANIFESTO.md` committed | File exists in `main`, ≤1 page rendered |
| (e) | `tiba.yaml` JSON schema committed at `schema/tiba.yaml.schema.json` | Schema validates against a sample manifest |
| (f) | Sentinel: 0 BLOCK on the meta-repo | `python -m sentinel scan --repo C:\Projects\tiba` |
| (g) | ≥3 of the 5 operational repos have committed `tiba.yaml` | CI federation scan returns ≥3 manifests |
| (h) | Makerere PI(s) nominated and added to author list | Edit to `docs/papers/*/draft.md` author block |
| (i) | E156 workbook entry created (both papers as one entry under "framework") | Entry visible in `C:\E156\rewrite-workbook.txt` |
| (j) | Crossref/Zenodo DOI plan documented | Note in `docs/papers/README.md` saying "DOI at publication" |

---

## Appendix C: Calibration provenance — OTS proofs and git tags

The following OpenTimestamps attestations and git tags constitute the preregistration record for the empirical anchors cited in this paper.

### PACTR Hiddenness Atlas (Discovery layer)

| Document | OTS calendar | Status |
|---|---|---|
| Specification | Bitcoin blockchain anchor | Confirmed — 3 calendars |
| Sample list (30 PACTR trials) | Bitcoin blockchain anchor | Confirmed — 3 calendars |
| Audit instrument (blinded scoring sheet) | Bitcoin blockchain anchor | Confirmed — 3 calendars |

Tags: `prereg-v0.0.1`, `prereg-v0.1.0-amend-1`, `v0.1.0`

### ARAC (Equity scoreboard layer)

| Document | OTS calendar | Status |
|---|---|---|
| Specification (Amendment 2 re-stamped) | Bitcoin blockchain anchor | Confirmed |
| Sample list (Amendment 1 re-stamped) | Bitcoin blockchain anchor | Confirmed |
| Audit instrument | Bitcoin blockchain anchor | Confirmed |

Tags: `prereg-v0.1.1.0`, `prereg-v0.1.1.1-amend-1`, `prereg-v0.1.1.2-amend-2`, `v0.1.1`

### Tiba meta-repository

| Document | Commit | Tag |
|---|---|---|
| Design spec (this framework) | `826fe75` (D1 resolved) | — |
| Papers scaffold + DOI plan | `056b6e3` | — |
| v0.1.0 release | TBD at acceptance criteria completion | `v0.1.0` |

All OTS proofs are stored in their respective repository roots as `.ots` files alongside the attested documents. Bitcoin blockchain confirmation (3+ calendar services) is the attestation standard used across this portfolio. Verification: `ots verify <file>.ots`.

---

*End of draft-1. Word count target: 4,000–6,000 body words. Sections 1–8 constitute the body; Abstract, References, and Appendices are excluded from the word-count target.*

*Next steps: draft-2 will add the Figure 1 SVG architecture diagram, resolve D2 (journal target), and add Makerere co-PI author entries to the frontmatter.*
