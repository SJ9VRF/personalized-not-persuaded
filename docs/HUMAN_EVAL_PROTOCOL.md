# Blinded Human Validation Protocol

## Goal
Validate the three license dimensions independently of the benchmark generator and model. Raters decide whether a user-context signal is allowed to affect:

1. presentation,
2. personalization,
3. epistemic evidence for the stated task.

## Materials

- `datasets/human_eval/blinded_license_packet.csv` — 552 blinded items
- `datasets/human_eval/heldout_answer_key.csv` — frozen contract labels; do not expose to raters
- `scripts/aggregate_human_eval.py` — agreement and contract-comparison analysis

## Collection

1. Give each rater an independently randomized copy of the blinded packet.
2. Fill `rater_id` with a stable anonymous identifier.
3. Keep method/model identity and the held-out answer key hidden.
4. Obtain three independent judgments per item.
5. Fill the three `rater_*_license` columns with 0/1, plus optional confidence and notes.
6. Preserve disagreement; do not adjudicate during collection.

## Primary analysis

The aggregation script reports, for each license dimension:

- nominal Krippendorff-style alpha on items with complete multi-rater labels;
- majority-label agreement with the frozen contract labels;
- a bootstrap 95% confidence interval for majority-vs-contract accuracy.

Run:

```bash
python scripts/aggregate_human_eval.py completed_annotations.csv
```

## Predeclared subgroup analysis

Report disagreement and accuracy by:

- provenance class;
- task kind;
- scope;
- ordinary held-out vs domain-OOD vs compositional split.

## Interpretation rule

If disagreement is concentrated in a provenance/task family, revise or qualify the benchmark contract before using that family to compare models. Human disagreement is evidence about construct ambiguity, not annotator failure.

No human-validation result is included in the repository until completed annotations are supplied.
