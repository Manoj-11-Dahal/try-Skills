# Skill Similarity and Deduplication Audit

**Date:** 2026-09-29  
**Deduplication scope:** 3,291 skills at the time of that audit. The catalog subsequently grew to 3,300 after nine independently authored MCP-focused additions.

## Method and limits

The earlier task-specific 85% screen was recorded as returning 70 candidate pairs, with a maximum score of 88.75%. Its complete pair table was not saved to the workspace, so it cannot be cross-walked edge-by-edge now. Six edges across five related clusters were manually compared against their task-specific procedures and guardrails; those 11 source skills were combined into five workflows. The broader scans that produced 13,128 substantive-section pairs and 310 title/trigger pairs were rejected as template-sensitive and were not used as merge lists.

For a reproducible follow-up, a fresh screen was run over the 3,294-skill catalog after the first five consolidations. It used TF-IDF cosine over character-within-word n-grams (lengths 3–5, sublinear term frequency) on each skill slug plus its frontmatter description. At 85% it returned 21 pairs. These are triage candidates, not automatic duplicates: paired task procedures and artifacts were inspected before decisions. Two pairs were consolidated; the other 19 were retained as distinct tasks. This follow-up profile is not represented as an exact reproduction of the unsaved earlier 70-pair list.

After those two merges, a rescan found a complementary site-readiness/validation pair, which was also consolidated. The final 3,291-skill rescan returned eight pairs at or above 85%; all eight were checked against their actual task procedures and retained as distinct.

## Consolidations

| Consolidated skill | Absorbed source skills | Candidate score |
|---|---|---:|
| `gh-aw-agent-context-lifecycle-review` | `gh-aw-agent-context-file-selection`; `gh-aw-context-retention-and-data-minimization` | 88.34% (earlier task-specific screen) |
| `browser-iframe-origin-data-boundary-review` | `browser-cross-origin-frame-data-boundary`; `browser-iframe-target-origin-validation` | 85.14% (earlier task-specific screen) |
| `medical-imaging-dicom-transfer-preflight` | `medical-imaging-dicom-routing-target-safety-check`; `medical-imaging-dicom-sop-class-compatibility-check` | 85.09% (earlier task-specific screen) |
| `security-assessment-scope-authorization-register` | `security-assessment-authorization-packet`; `security-scope-exclusion-register` | 85.64% (earlier task-specific screen) |
| `security-evidence-lifecycle-governance` | `security-control-evidence-collection-plan`; `security-evidence-retention-and-disposal-plan`; `security-log-retention-and-access-review` | 85.49% and 87.88% (earlier task-specific screen) |
| `medical-imaging-model-update-impact-and-release-gate` | `medical-imaging-model-update-impact-assessment`; `medical-imaging-update-validation-and-rollout-gate` | 86.97% (follow-up screen) |
| `medical-imaging-reader-model-interaction-evaluation` | `medical-imaging-human-ai-team-evaluation-design`; `medical-imaging-reader-workstation-usability-evaluation` | 85.02% (follow-up screen) |
| `medical-imaging-external-site-validation-readiness` | `medical-imaging-clinical-site-activation-readiness`; `medical-imaging-external-site-validation-protocol` | 85.03% (final follow-up) |

The consolidated imaging-update workflow separates change-impact analysis from the evidence/release gate. The reader–model workflow has explicit branches for human–AI performance evaluation and workstation usability. The external-site workflow keeps local activation prerequisites distinct from the independent validation design while giving them one coherent readiness-to-protocol path.

## First follow-up candidates retained as distinct

These are the 19 non-merged pairs from the 21-pair follow-up run before the final rescan. The two omitted pairs from that run are the model-update impact/release-gate and reader–model/workstation-usability consolidations listed above.

| Pair | Score | Reason retained |
|---|---:|---|
| `medical-imaging-human-ai-team-evaluation-design` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 89.72% | Reader–model interaction outcomes versus technical lineage and output-integrity record. |
| `medical-imaging-model-update-impact-assessment` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 88.37% | Change-impact analysis versus run-level provenance logging. |
| `medical-imaging-prediction-provenance-and-model-version-log` ↔ `medical-imaging-update-validation-and-rollout-gate` | 87.99% | Capturing which model produced an output versus deciding whether an update meets release criteria. |
| `medical-imaging-model-card-limitations-review` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 87.84% | Documenting limitations and non-use cases versus recording execution provenance. |
| `medical-imaging-intended-use-and-target-population-card` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 87.63% | Defining population and intended-use boundaries versus per-output lineage. |
| `medical-imaging-external-site-validation-protocol` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 87.62% | Designing independent-site validation versus recording model-run lineage. |
| `medical-imaging-external-site-validation-protocol` ↔ `medical-imaging-human-ai-team-evaluation-design` | 86.89% | Estimating external-site generalizability versus evaluating reader–model workflow effects. |
| `medical-imaging-evaluation-claim-to-evidence-trace` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 86.51% | Tracing performance claims to evidence versus logging model-output provenance. |
| `medical-imaging-external-site-validation-protocol` ↔ `medical-imaging-update-validation-and-rollout-gate` | 86.51% | Independent-site evaluation design versus a release decision across predefined gates. |
| `medical-imaging-human-ai-team-evaluation-design` ↔ `medical-imaging-intended-use-and-target-population-card` | 86.45% | Measuring reader–model interaction versus specifying intended use and population. |
| `medical-imaging-clinical-site-activation-readiness` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 85.52% | Site startup/governance readiness versus model-output traceability. |
| `medical-imaging-evaluation-claim-to-evidence-trace` ↔ `medical-imaging-intended-use-and-target-population-card` | 85.52% | Auditing claim support versus defining population and excluded settings. |
| `medical-imaging-prediction-provenance-and-model-version-log` ↔ `medical-imaging-reader-workstation-usability-evaluation` | 85.48% | Recording technical lineage versus testing interface clarity and reader errors. |
| `medical-imaging-human-ai-team-evaluation-design` ↔ `medical-imaging-update-validation-and-rollout-gate` | 85.45% | Human-factor study design versus technical update release control. |
| `medical-imaging-confidence-interval-and-sample-plan` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 85.25% | Statistical sample/uncertainty design versus output provenance capture. |
| `medical-imaging-intended-use-and-target-population-card` ↔ `medical-imaging-update-validation-and-rollout-gate` | 85.24% | Setting intended-use boundaries versus testing an update against release criteria. |
| `security-evidence-hash-integrity-check` ↔ `security-scope-expiry-and-renewal-check` | 85.22% | Verifying artifact integrity versus revalidating authorization after scope/time changes. |
| `medical-imaging-model-change-scope-envelope` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 85.05% | Defining permitted change boundaries and triggers versus recording model execution history. |
| `gh-aw-checkout-ref-trust-boundary` ↔ `gh-aw-instruction-file-change-protection` | 85.03% | Establishing trusted/untrusted checkout revisions versus protecting privileged instruction files from unreviewed changes. |

## Final catalog candidates retained as distinct

| Pair | Score | Reason retained |
|---|---:|---|
| `medical-imaging-model-card-limitations-review` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 87.95% | Limitations/non-use documentation versus per-output provenance. |
| `medical-imaging-intended-use-and-target-population-card` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 87.73% | Intended-use and population scope versus execution lineage. |
| `medical-imaging-evaluation-claim-to-evidence-trace` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 86.67% | Evidence support for claims versus model-output traceability. |
| `medical-imaging-evaluation-claim-to-evidence-trace` ↔ `medical-imaging-intended-use-and-target-population-card` | 85.68% | Claim-to-evidence audit versus intended-use definition. |
| `medical-imaging-confidence-interval-and-sample-plan` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 85.41% | Statistical sample/uncertainty design versus provenance capture. |
| `security-evidence-hash-integrity-check` ↔ `security-scope-expiry-and-renewal-check` | 85.24% | Artifact integrity verification versus authorization validity. |
| `medical-imaging-model-change-scope-envelope` ↔ `medical-imaging-prediction-provenance-and-model-version-log` | 85.19% | Permitted change boundaries versus execution history. |
| `gh-aw-checkout-ref-trust-boundary` ↔ `gh-aw-instruction-file-change-protection` | 85.04% | Checkout revision trust versus instruction-file change control. |

## Outcome and validation

- Skills before consolidation: **3,300**
- Source folders consolidated: **17** into **8**
- Net folder reduction: **9**
- Skills after consolidation: **3,291**
- Final category counts: AI/agent systems 197; software/development 306; cloud/security 259; data analytics 236; business operations 936; science/health/research 413; engineering/industry 596; creative/media/design 147; education/public service 201.
- The catalog retains exactly nine subject categories and has no separate Other category.
- The original 70-edge candidate table was not retained, so this report does not claim one-to-one disposition of every edge from that earlier screen. The reproducible follow-up and final-catalog candidates are recorded above.
- Post-merge validation passed: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_skills.py` validated all 3,291 skills; the repository unit suite passed all 7 tests. The INDEX has 3,291 unique resolving skill links, and the category totals plus README/banner counts agree.

## Subsequent MCP additions

Nine MCP-specific skills were added after the deduplication pass; the current catalog contains 3,300 skills. The new skills are independently authored and their research sources and rationale are recorded in `references/source-notes.md`. Revalidation after the additions passed for all 3,300 skills; all 7 unit tests passed, and all 3,300 INDEX links resolve.


## Expansion deduplication screen: batches 34–44 (2026-09-29)

The 3,300-skill catalog received 1,100 new candidate skills across 11 topic-led packs. Each batch was checked sequentially against every existing INDEX entry for exact name collisions and with the repository preflight's lexical overlap coefficient (0.55 review cutoff). The `backend-ops-schema-migration` stream was replaced with connection-pool saturation after a flag against `database-migration-safety`; `stem-lab-course-outcomes` was replaced with lab-station access after flags against curriculum workflows. The final preflight for each of the 11 batches had zero exact collisions and zero remaining 0.55 lexical flags.

A separate catalog-wide screen used TF-IDF cosine on `slug + frontmatter description`, with character-within-word 3–5-grams and sublinear term frequency (the same family of screen used in the earlier follow-up). Across 1,100 new and 3,300 prior skills, it returned **zero** new-versus-existing pairs at or above 0.85 and **zero** new-versus-new pairs at or above 0.85. At a review threshold of 0.80, the sole within-new pair was 0.8156: `omics-data-enrichment-universe-scope-intake-gate` ↔ `omics-data-enrichment-universe-source-provenance-ledger`. Manual review retained both: intake defines the research object, permitted data, owner, and stopping boundary; provenance maps analytical claims and inputs to their exact source/reference versions. Their deliverables and acceptance checks differ.

These similarity results reduce duplicate risk but do not prove semantic uniqueness. The 11 packs deliberately reuse a bounded procedure scaffold while varying the domain, trigger, data/evidence boundary, artifact, feedback measure, and authority guard. The original-URL/topic rationale and selected source/license notes are in `source-notes.md` and `skills-txt-source-audit.md`.

Post-expansion checks: 4,400 skill files; 4,400 unique resolving INDEX links; all repository validator checks passed; all 7 unit tests passed. The new-pack distribution is 100 each for `agent-telemetry-`, `backend-ops-`, `container-assurance-`, `ml-data-ops-`, `growth-evidence-`, `omics-data-`, `pcb-design-`, `edge-fleet-`, `blender-production-`, `premiere-production-`, and `stem-lab-`.


## Multi-skill catalog expansion: batches 45–55 (2026-09-29)

The AAS catalog supplied topic discovery only; 1,100 new local skills were independently authored. All 11 batches passed preflight with zero exact-name collisions and zero 0.55 overlap-coefficient flags against the then-current INDEX.

A catalog-wide TF-IDF cosine screen used `slug + frontmatter description`, character-within-word 3–5-grams, and sublinear term frequency. Results for the 1,100 new skills against the 4,400 prior skills: **zero** new-versus-prior pairs at or above 0.85; **zero** new-versus-new pairs at or above 0.85. Four within-new pairs scored at or above 0.80 and were manually retained as distinct workflows:

- `aas-devrel-tutorial-prerequisites-scope-intake-gate` ↔ `aas-devrel-tutorial-prerequisites-source-provenance-ledger` (0.8152): scope/acceptance boundary versus evidence/version provenance.
- `aas-devrel-tutorial-prerequisites-approval-evidence-packet` ↔ `aas-devrel-tutorial-prerequisites-scope-intake-gate` (0.8038): decision-ready approval evidence versus task intake and acceptance definition.
- `aas-devtools-workspace-bootstrap-scope-intake-gate` ↔ `aas-devtools-workspace-bootstrap-source-provenance-ledger` (0.8032): fresh-workspace requirements versus evidence for environment versions and bootstrap claims.
- `aas-agent-coordination-review-adjudication-scope-intake-gate` ↔ `aas-agent-coordination-review-adjudication-source-provenance-ledger` (0.8019): adjudication scope and authority versus provenance of reviewer evidence.

The earlier 0.45 dry-run on the same metric produced 350,249 pair edges and a 3,100-skill connected component, largely because the catalog shares a bounded-workflow scaffold. That threshold is not used for automatic merging: a similarity edge is a review signal, not proof of duplicate intent. No skills were merged or removed during this catalog expansion.

Post-expansion checks: `validate_skills.py` passed for 5,500 skills; all 7 unit tests passed; all 5,500 INDEX links resolve uniquely. Category counts and repo totals are synchronized.
