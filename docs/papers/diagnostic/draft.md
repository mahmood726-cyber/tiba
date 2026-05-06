---
title: "African evidence is hidden from existing synthesis infrastructure: a calibration study and a proposed framework (Tiba)"
short_title: "African evidence is hidden — Tiba framework"
authors:
  - name: "Mahmood Ahmad"
    affiliation: "Makerere University, Uganda; Tiba steward"
    orcid: "TBD-pre-publication"
    corresponding: true
    email: "mahmood726@gmail.com"
    role: "First/corresponding author; Uganda PI for v0.1.0"
target_journal: "Synthēsis (Methods Note, ≤400 words)"
format_constraints:
  word_count_max: 400
  page_setup: "A4, 1.5 line spacing, 11-pt Calibri body / 12-pt Times New Roman headings"
  references: "Vancouver"
keywords: ["systematic reviews", "African research", "PACTR", "evidence synthesis", "framework", "blinded audit"]
date: 2026-05-06
status: draft-1
---

## Body

African clinical trials are increasingly registered on the Pan-African Clinical Trials Registry (PACTR), not ClinicalTrials.gov (NCT). Existing evidence-synthesis infrastructure identifies trial publications by linking NCT registration numbers to journal articles — the NCT-bridge. Trials registered exclusively on PACTR carry no NCT identifier and are therefore structurally invisible to any synthesis tool relying on NCT-bridge linkage. This gap is not editorial bias: it is an architectural mismatch between the primary registry used by African trialists and the discovery mechanism used by systematic reviewers globally.

We conducted two pre-registered calibration studies. In the PACTR Hiddenness Atlas (v0.1.0), we assembled 30 PACTR-registered trials with confirmed peer-reviewed publications. A blinded human auditor independently searched EuropePMC; an automated algorithm applied the standard NCT-bridge. Both searches were completed before results were shared (pre-registered; Open Timestamps-stamped). In the African Representation Atlas of Cochrane (ARAC) Tier-P audit (v0.1.1), 30 Cochrane Pairwise70 trials were independently classified by two masked LLM-based classifiers following a pre-registered protocol with two documented amendments.

NCT-bridge sensitivity was 6.2% (1/30 algorithm vs 16/30 blinded auditor; Wilson 95% CI 0.2–30.2): the algorithm found one publication; the auditor found 16. For ARAC Tier-P: Cohen's κ = 1.000 on n_evaluable = 9 (perfect inter-classifier agreement); 21/30 trials were Insufficient — 7 because Pairwise70 PMID linkage errors caused both classifiers to retrieve the wrong record (an independently confirmed registry defect), and 14 because abstracts omitted participant geography. The ARAC κ estimate is LLM-vs-LLM consistency, not a human gold standard; a Makerere PhD-cohort human inter-rater reliability audit is planned for v0.2.

Tiba (Swahili: *healing*) is a federation of African-led evidence-synthesis projects sharing one architectural vocabulary. Version 0.1.0 operationalises four of five planned production layers: Discovery (PACTR Hiddenness Atlas), Quality gates (five Pairwise70 atlases), Equity scoreboard (ARAC), and Training (Synthesis Courses, 26 courses × 12 languages). The constructive companion paper details the full eight-layer architecture and governance model. Tiba is not affiliated with the Cochrane Collaboration.

## References

1. Ahmad M. PACTR Hiddenness Atlas v0.1.0. github.com/mahmood726-cyber/pactr-hiddenness-atlas. 2026.
2. Ahmad M. African Representation Atlas of Cochrane (ARAC) v0.1.1. github.com/mahmood726-cyber/arac. 2026.
3. Ahmad M. Tiba framework — constructive companion. Zenodo preprint, 2026 (DOI at deposit).
4. Pan-African Clinical Trials Registry. https://pactr.samrc.ac.za. Accessed 2026-05-06.
5. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021;372:n71.
6. Higgins JPT, Thomas J, eds. Cochrane Handbook for Systematic Reviews of Interventions v6.5. Cochrane, 2024.
7. Open Timestamps. https://opentimestamps.org. Accessed 2026-05-06.
8. Wilson EB. Probable inference, the law of succession, and statistical inference. J Am Stat Assoc 1927;22:209–212.
