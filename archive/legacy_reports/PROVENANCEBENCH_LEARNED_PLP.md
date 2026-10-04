# ProvenanceBench: Learned PLP Evaluation

The learned router predicts three distinct licenses - presentation, personalization, and evidence - from signal text plus structured provenance metadata. Thresholds are selected on a validation split; reported test and OOD domains are untouched. A separate learned ranker resolves conflicting evidence sources.

## test

| Method | Exact license match ↑ | Evidence uptake ↑ | Unsupported leakage ↓ | Evidence starvation ↓ |
|---|---:|---:|---:|---:|
| naive | 0.643 | 1.000 | 0.273 | 0.000 |
| firewall | 0.571 | 0.000 | 0.000 | 1.000 |
| provenance_only | 0.786 | 0.667 | 0.000 | 0.333 |
| oracle | 1.000 | 1.000 | 0.000 | 0.000 |
| learned_plp | 1.000 | 1.000 | 0.000 | 0.000 |
| hybrid_plp | 1.000 | 1.000 | 0.000 | 0.000 |

## ood_test

| Method | Exact license match ↑ | Evidence uptake ↑ | Unsupported leakage ↓ | Evidence starvation ↓ |
|---|---:|---:|---:|---:|
| naive | 0.579 | 1.000 | 0.429 | 0.000 |
| firewall | 0.579 | 0.000 | 0.000 | 1.000 |
| provenance_only | 0.684 | 0.800 | 0.214 | 0.200 |
| oracle | 1.000 | 1.000 | 0.000 | 0.000 |
| learned_plp | 0.842 | 1.000 | 0.214 | 0.000 |
| hybrid_plp | 1.000 | 1.000 | 0.000 | 0.000 |

## compositional_test

| Method | Exact license match ↑ | Evidence uptake ↑ | Unsupported leakage ↓ | Evidence starvation ↓ |
|---|---:|---:|---:|---:|
| naive | 0.400 | 1.000 | 1.000 | 0.000 |
| firewall | 0.600 | 0.000 | 0.000 | 1.000 |
| provenance_only | 0.400 | 1.000 | 1.000 | 0.000 |
| oracle | 1.000 | 1.000 | 0.000 | 0.000 |
| learned_plp | 0.400 | 1.000 | 1.000 | 0.000 |
| hybrid_plp | 1.000 | 1.000 | 0.000 | 0.000 |

## Conflicting evidence

ID conflict selection accuracy: **1.000** over 48 groups.
OOD-domain conflict selection accuracy: **1.000** over 72 groups.

## Interpretation boundary

The pure learned router exposes a compositional-generalization failure. Hybrid PLP adds only three validity gates - stale, low-confidence, and task-irrelevant context cannot receive a license - while leaving the content/provenance decision learned. This is still a licensing result, not a full language-model generation result. The oracle row isolates the headroom if licensing were perfect; generator compliance remains a separate empirical question.
