# Tiba — Papers

This directory holds the v0.1.0 framework papers.

## Documents

| Path | Audience | Format | Word target | Status |
|---|---|---|---|---|
| [`diagnostic/draft.md`](diagnostic/draft.md) | Synthēsis | Methods Note | ≤400 words | Draft (v0.1.0 deliverable) |
| [`constructive/draft.md`](constructive/draft.md) | BMJ Methods / JCE / Zenodo preprint | Long-form | 4,000–6,000 words | Draft (v0.1.0 deliverable) |

## Authorship

- **First / corresponding author (both papers):** Mahmood Ahmad (mahmood726-cyber).
- **Uganda / Makerere PI (v0.1.0):** Mahmood Ahmad (insider at Makerere University; serves as the Uganda PI for the v0.1.0 framework declaration; resolves D1 of the spec).
- **Additional Makerere co-PIs (v0.2):** explicitly carved out for v0.2 — broaden the African-PI roster beyond a single insider before any production-pipeline (Workforce activation layer) work.
- **Acknowledged:** ARAC contributors, PACTR Hiddenness Atlas contributors, Synthesis Courses contributors whose material is referenced.
- **COI:** none. Mahmood left the Synthēsis editorial board on 2026-04-20 (per `feedback_e156_authorship.md`).

## DOI plan (per Synthēsis policy)

Per `reference_synthesis_journal.md`: DOIs are minted **at publication**, not pre-publication. Plan:

1. **Constructive paper preprint → Zenodo.** When draft-1 is complete, deposit on Zenodo to obtain a preprint DOI. Cite the preprint DOI in the diagnostic Methods Note.
2. **Diagnostic Methods Note → Synthēsis OJS.** Submit via the 5-step OJS wizard (`reference_synthesis_journal.md`). DOI minted on acceptance.
3. **Constructive paper → BMJ Methods or JCE.** Decision at draft-2 (spec §10 D2). DOI minted on acceptance.
4. **Crossref deposit** for both papers post-acceptance via the journal's standard pipeline. No manual Crossref deposit by the author.

## Citation hygiene

Per `lessons.md` "LLM citation misattribution":

- Cap context at ≤10 sources per section in any LLM-assisted drafting.
- **DOI-resolve every citation programmatically** before push (use Crossref REST API directly).
- The diagnostic Methods Note will use Vancouver style per Synthēsis spec; the constructive paper will use whichever style the chosen target journal mandates (default Vancouver until D2 is resolved).

## Trademark posture in papers

The trademark guard (`scripts/pre_push_cochrane_guard.py`) **allowlists** `docs/papers/**` for academic-citation context. You may cite the Cochrane Handbook, Cochrane reviews, or other Cochrane Collaboration publications in this directory. **Do not** use "Cochrane" as a Tiba product or service name anywhere — including in figure captions, headers, or running text.
