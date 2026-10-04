# ProvenanceBench Statistical Report

Bootstrap intervals resample benchmark items with 5,000 replicates. Paired exact tests compare Hybrid PLP against the provenance-only baseline on exact three-license match. These intervals characterize benchmark-item uncertainty, not model-seed or human-rater uncertainty.

## test

| Method | Exact match (95% CI) | Evidence uptake (95% CI) | Unsupported leakage (95% CI) |
|---|---:|---:|---:|
| naive | 0.643 [0.565, 0.714] | 1.000 [1.000, 1.000] | 0.273 [0.197, 0.348] |
| firewall | 0.571 [0.494, 0.643] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| provenance_only | 0.786 [0.720, 0.845] | 0.667 [0.528, 0.833] | 0.000 [0.000, 0.000] |
| learned_plp | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |
| hybrid_plp | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |

Paired exact test vs provenance-only: hybrid-only correct=36, baseline-only correct=0, p=2.91e-11.

## ood_test

| Method | Exact match (95% CI) | Evidence uptake (95% CI) | Unsupported leakage (95% CI) |
|---|---:|---:|---:|
| naive | 0.579 [0.547, 0.610] | 1.000 [1.000, 1.000] | 0.429 [0.391, 0.464] |
| firewall | 0.579 [0.547, 0.612] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| provenance_only | 0.684 [0.654, 0.715] | 0.800 [0.750, 0.850] | 0.214 [0.185, 0.246] |
| learned_plp | 0.842 [0.818, 0.864] | 1.000 [1.000, 1.000] | 0.214 [0.183, 0.246] |
| hybrid_plp | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |

Paired exact test vs provenance-only: hybrid-only correct=288, baseline-only correct=0, p=4.02e-87.

## compositional_test

| Method | Exact match (95% CI) | Evidence uptake (95% CI) | Unsupported leakage (95% CI) |
|---|---:|---:|---:|
| naive | 0.400 [0.362, 0.436] | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] |
| firewall | 0.600 [0.565, 0.636] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| provenance_only | 0.400 [0.365, 0.436] | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] |
| learned_plp | 0.400 [0.364, 0.435] | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] |
| hybrid_plp | 1.000 [1.000, 1.000] | 1.000 [1.000, 1.000] | 0.000 [0.000, 0.000] |

Paired exact test vs provenance-only: hybrid-only correct=432, baseline-only correct=0, p=1.8e-130.

