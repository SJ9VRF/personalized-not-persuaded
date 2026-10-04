# Evidence Layer

This directory is the research-process layer behind **Personalized, Not Persuaded**. It is deliberately separate from the polished project page.

The goal is not to make the project look messy. It is to make the scientific path inspectable: what was tried, what failed, what changed, what the current numbers actually say, and which claims remain untested.

## Read in this order

1. [Experiment Journal](EXPERIMENT_JOURNAL.md) — the sequence of experiments that materially changed the project.
2. [What Didn't Work](FAILED_EXPERIMENTS.md) — failed or rejected hypotheses and why they were rejected.
3. [Decision Log](DECISION_LOG.md) — material technical choices with alternatives and trade-offs.
4. [Real Eval Tables](REAL_EVAL_TABLES.md) — canonical tables with N, confidence intervals, seeds, and scope.
5. [Unexpected Findings](UNEXPECTED_FINDINGS.md) — observations that changed the research direction.
6. [Git History](GIT_HISTORY.md) — what the repository history can and cannot prove.

## Raw evidence

The machine-readable evidence is under [`artifacts/evidence/`](../artifacts/evidence/):

- `experiment_logs/` — one JSON record per logged experiment;
- `eval_runs/` — copies of canonical result files used in the evidence pages;
- `failure_examples/` — raw and representative failure cases;
- `plots/` — plots regenerated from canonical results;
- `configs/` — the frozen evaluation settings summarized for review;
- `qualitative_cases/` — recorded success/failure trajectories;
- `ablations/` — focused ablation tables;
- `git/` — a real git bundle and log created from the repository history beginning with the verified snapshot import.

The evidence layer makes no claim that external-model generations or independent human labels have been collected. Those remain separate, explicit next experiments.
