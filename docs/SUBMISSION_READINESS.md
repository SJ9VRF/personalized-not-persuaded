# Submission Readiness

## Completed in the repository

- Three-head **learned PLP router** with validation-only threshold selection.
- **Hybrid PLP** with explicit stale / low-confidence / irrelevant validity gates.
- **ProvenanceBench**: 4,800 examples across ordinary held-out, domain-OOD, compositional, and conflict regimes.
- **Paired provenance intervention**: 400 matched pairs / 800 examples with identical surface text and validity metadata.
- Naive, firewall, provenance-only, learned, hybrid, and oracle baselines.
- Separate conflict-source evaluation.
- 5,000-resample item-bootstrap intervals and paired exact tests.
- Calibration tables and exported error cases.
- Ten-seed linear-router stability check.
- 552-item blinded human-validation packet + separate answer key + aggregation script.
- Provider-neutral generation-adapter harness and oracle-license decomposition.
- LaTeX manuscript + rendered PDF + benchmark card + technical report.
- Automated tests and submission artifact audit.

## What remains external by definition

These cannot be truthfully completed without outside participation or model access:

1. **Independent human judgments** and inter-rater agreement.
2. **End-to-end open/frontier model generations** under predicted vs oracle licenses.
3. **Head-to-head external implementations** of FPPS, CCS, and Resist-and-Update on comparable generator backbones.
4. Natural deployed-memory histories where provenance itself must be inferred rather than supplied.

The repository contains frozen protocols and executable hooks for these experiments. They are not claimed as completed.

## Current claim boundary

The package supports a controlled methods/benchmark claim:

> Multi-channel provenance licensing is learnable under ordinary held-out evaluation, standard accuracy hides meaningful domain/compositional failures, narrow validity gates reduce unsupported leakage, and matched provenance interventions are necessary to verify causal source sensitivity.

It does not support a claim that PLP improves a frontier language model end-to-end.

## Main-track blocker

For a strong general-model paper, the remaining blocker is **external behavioral evidence**, not another local metric. The next unit of work should therefore be real generators + blinded human evaluation, not additional synthetic feature expansion.
