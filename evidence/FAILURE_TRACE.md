# One failure, end to end

This page traces one frozen failure through the actual evaluation and data-building pipeline. It is not a hypothetical example.

## Case

`PI-0000-1` comes from `datasets/provenance/provenance_intervention_test.csv`. The context is **tool-verified**, current, high-confidence, relevant, and scoped to a factual-world task. The frozen contract therefore gives it evidence standing.

## What the system did

Hybrid PLP predicted `presentation=0, personalization=0, evidence=0`. The evidence grader expected `1`, so the trial failed with weighted score **0.5**. The validity gates did not block the signal; the miss came from the learned standing prediction.

## How the failure was classified

The miner labels it `evidence:starvation`: a valid evidence source was under-used, not an unsupported source over-used.

## What changed downstream

The case becomes `CURR-PI-0000-1`, a targeted correction whose supervision changes only the evidence channel to `1` while preserving the already-correct presentation and personalization channels. The correction is then inserted into the 784-example post-training mixture alongside stability anchors.

## What this does *not* prove

The trace proves the **eval -> failure classification -> correction-data** path is executable. It does not prove that SFT, preference optimization, or RL on this example improves an external language model; that experiment remains future work.

## Raw links

- Benchmark row: `datasets/provenance/provenance_intervention_test.csv` (`PI-0000-1`)
- Trial trajectory: `results/trial_trajectories.jsonl` (`TRIAL-HYBRID-PI-0000-1`)
- Error table: `results/provenancebench_errors.csv` (`PI-0000-1`)
- Correction: `datasets/post_training/failure_curriculum.jsonl` (`CURR-PI-0000-1`)
- Training mixture: `datasets/post_training/training_mixture.jsonl` (same correction record)
- Machine-readable trace: `artifacts/evidence/qualitative_cases/PI-0000-1_failure_trace.json`
