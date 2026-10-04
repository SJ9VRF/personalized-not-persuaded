## v1.4.0
- Added Provenance-Licensed Personalization (PLP).
- Added provenance/task routing benchmark and tests.
- Narrowed novelty claim after a fresh literature audit.
- Retitled paper while retaining the public brand *Personalized, Not Persuaded*.

# Changelog

## v1.3.0 — Contract-Guided Selective Personalization
- Added **CGSP**, an executable factorized personalization method with allowed and protected user-context channels.
- Added hard non-interference tests for belief/memory interventions and positive adaptation tests for allowed channels.
- Added `docs/CGSP_METHOD.md` and `reports/CGSP_METHOD_RESULTS.md`.
- Expanded the frozen benchmark to compare four policies and 960 long-horizon stress measurements.
- CGSP reaches 100% Counterfactual Contract Pass Rate in the controlled proxy fixture (APG 0.3627, PED 0.0000); this is explicitly not a frontier-model claim.
- Retitled the paper **Personalized, Not Persuaded: Epistemically Stable Personalization via Counterfactual Contracts** after a terminology/novelty audit.

## v1.2.0 — Counterfactual Personalization Contracts
- Added exactly paired 4,920-scenario contract benchmark (820 contracts × P0–P5).
- Added APG/PED/PEI/CCI/Contract Score/Pass Rate.
- Added frontier gap audit and tightened novelty claims against adjacent work.
- Updated paper title to *Personalized, Not Persuaded: Counterfactual Contracts for Selective Personalization*.
- Added contract tests and release-audit requirements.

## v1.1.0 — Novelty/SOTA Reframe

- Renamed the flagship to **Personalized, Not Persuaded**.
- Reframed the central contribution as **factorized selective adaptation** rather than sycophancy detection.
- Added Counterfactual Epistemic Invariance (CEI), Epistemic Drift (ED), Personalization Gain (PG), and Selective Adaptation (SA).
- Added a nearest-work SOTA matrix and a defensible narrow novelty claim.
- Added matched-profile invariance analysis and generated proxy diagnostics.


## v1.0.2 — Presentation-grade portfolio release

- Added a standalone portfolio case-study homepage under `site/index.html`.
- Added a root Pages entrypoint and GitHub Pages deployment workflow.
- Added `REVIEWER_GUIDE.md` with 60-second, 5-minute, and 15-minute review paths.
- Promoted the homepage and Pages workflow to required release-audit artifacts.
- Updated package version to 1.0.2.

## v1.0.0

- Added BehaviorBench v1 with 1,200 validated scenarios.
- Added response-text-based evaluator and three executable proxy policies.
- Added bootstrap confidence intervals and profile/language/category breakdowns.
- Added synthetic long-horizon stress analysis, reward modeling, preference learning, reward-hacking sweeps, ablations, regression gates, and failure mining.
- Added human-evaluation protocol, offline annotation UI, and real-model adapter contract.
- Added dashboard, publication figures, paper draft, failure atlas, research talk, and demo script.
- Added CLI, Make targets, CI workflow, quickstart, artifact index, model/data cards, and reproducibility documentation.
- Final audit corrected translation provenance wording and documented all scientific boundaries.

## v1.0.1 — Audited complete-package release

- Restored full executable repository into the canonical release artifact.
- Added automated release-structure/link/scientific-boundary audit.
- Corrected translation-provenance wording in the paper.
- Re-ran pipeline, tests, and regression gates.

## v1.3.2 — Statistical + protocol-hardening release
- Added CGSP component ablations: allowed-channel removal, protected-gate removal, and style-only adaptation.
- Added 5,000-resample bootstrap confidence intervals and exact paired contract-effect analysis.
- Added frozen protocol SHA-256 manifest and protocol-version policy.
- Added explicit threats-to-validity and ethics/misuse documents.
- Fixed README long-horizon count (960 after CGSP) and a broken Markdown delimiter.
- Synced package version metadata.
