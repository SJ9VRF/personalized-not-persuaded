# ProvenanceBench — strict statistical report

All intervals are 5,000-resample item bootstraps. Paired exact tests compare Hybrid PLP with the provenance-only baseline. These quantify benchmark-item uncertainty, not model-seed or human-rater uncertainty.

## test

- Hybrid exact: **1.000** (95% CI 1.000–1.000)
- Learned exact: **1.000**
- Provenance-only exact: **0.714**
- Paired discordant cases (Hybrid-only / baseline-only): **48 / 0**, exact p=7.11e-15
- Evidence-head ECE: **0.011**

## ood_test

- Hybrid exact: **0.947** (95% CI 0.933–0.962)
- Learned exact: **0.842**
- Provenance-only exact: **0.684**
- Paired discordant cases (Hybrid-only / baseline-only): **288 / 48**, exact p=2.27e-15
- Evidence-head ECE: **0.157**

## compositional_test

- Hybrid exact: **0.800** (95% CI 0.771–0.828)
- Learned exact: **0.400**
- Provenance-only exact: **0.600**
- Paired discordant cases (Hybrid-only / baseline-only): **288 / 144**, exact p=3.81e-12
- Evidence-head ECE: **0.486**

## provenance_intervention

- Hybrid exact: **0.750** (95% CI 0.719–0.780)
- Learned exact: **0.750**
- Provenance-only exact: **1.000**
- Paired discordant cases (Hybrid-only / baseline-only): **0 / 200**, exact p=2.4e-15
- Evidence-head ECE: **0.253**
