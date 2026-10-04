# Personalized, Not Persuaded

**Aura Yavary**

### Learning When Personal Context Counts as Evidence

Personal assistants accumulate preferences, memories, tool outputs, inferred habits, and user assertions. Those signals are useful in different ways, but they are not epistemically interchangeable. A style preference may change how an answer is written. A calendar result may legitimately change a personal-state answer. A confident user belief about the external world should not become evidence merely because it was remembered.

This repository studies that distinction as **evidentiary standing** and operationalizes it with **Provenance-Licensed Personalization (PLP)**.

## Research question

> **What standing should a piece of personal context have for this task—what is it allowed to change?**

PLP represents that standing as three separate licenses for each context signal:

- **presentation** — may it change tone or form?
- **personalization** — may it affect ranking, planning, or user-specific choices?
- **evidence** — may it change the model's factual/personal-state conclusion?

The standing decision is conditioned on task, signal scope, provenance, confidence, currentness, relevance, and conflict state. Provenance tells us where context came from; standing tells us what that context is permitted to influence here.


## Why this is not just provenance-aware memory

Recent systems already track provenance, temporal validity, and query-conditioned personal memory. This project does **not** claim those ideas as new. Its unit of study is the **permission boundary after context is available**: a memory can be relevant and trustworthy enough to personalize a recommendation while still lacking standing to change an unrelated factual conclusion.

See `docs/EVIDENTIARY_STANDING.md`, `docs/CLOSEST_WORK_MATRIX.md`, and `docs/NOVELTY_AND_SOTA.md`.

## What changed during the research

The first design was a fixed firewall: user beliefs and memory could personalize behavior but never enter the epistemic path. That prevented unsupported influence, but it also rejected legitimate evidence such as a current connected-calendar record.

The next design learned the three licenses from data. It fit the ordinary held-out split, but failed under compositional and domain shift. In particular, source trust became a shortcut for evidence permission.

The current method, **Hybrid PLP**, keeps the learned router but adds three narrow validity gates: stale, low-confidence, or task-irrelevant context cannot receive a license. The gates improve robustness, but the executable results also expose a remaining limitation: a negative gate can reject bad evidence, yet cannot recover a positive evidence permission the learned router never predicted.

That asymmetry is part of the result, not hidden by the benchmark.

## Main controlled results

| Method | ID exact | Domain-OOD exact | Compositional exact | OOD uptake ↑ | OOD leakage ↓ |
|---|---:|---:|---:|---:|---:|
| Naive | 0.286 | 0.368 | 0.600 | 1.000 | 0.857 |
| Firewall | 0.571 | 0.526 | 0.400 | 0.000 | 0.000 |
| Provenance-only | 0.714 | 0.684 | 0.600 | 0.800 | 0.071 |
| Learned PLP | **1.000** | 0.842 | 0.400 | 0.800 | 0.143 |
| **Hybrid PLP** | **1.000** | **0.947** | **0.800** | **0.800** | **0.000** |
| Oracle | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |

See `reports/PROVENANCEBENCH_EXECUTABLE.md` and `reports/PROVENANCEBENCH_STRICT_STATS.md` for the regenerated results and uncertainty analysis.

## Paired provenance intervention

To verify that provenance itself matters causally, the repository includes **400 matched pairs (800 examples)** where task, scope, confidence, currentness, relevance, and surface text are identical. Only source provenance changes.

On this delexicalized test:

- removing provenance cues gives **0.500** exact match;
- Learned/Hybrid PLP reach **0.750**;
- the narrow provenance-only rule reaches **1.000**.

This is deliberately harder and more informative than reporting only standard held-out accuracy.

## ProvenanceBench

The main benchmark contains **4,800 signal-level examples** across ordinary held-out, domain-OOD, compositional, and conflicting-evidence regimes. A separate matched provenance-intervention set contains 800 additional examples.

Core files:

- `datasets/provenance/provenancebench.csv`
- `datasets/provenance/provenance_intervention_test.csv`
- `docs/BENCHMARK_CARD.md`
- `results/provenancebench_method_summary.csv`
- `results/provenancebench_calibration.csv`
- `results/provenancebench_errors.csv`

## Learned method

`behavior_lab/methods/learned_plp.py` implements a three-head classifier for presentation, personalization, and evidence licenses. Thresholds are chosen on validation only. The hybrid variant applies validity gates after prediction.

Reproduce the paper-facing evidence path with one command:

```bash
make paper
```

Verify the complete release contract (tests, compilation, paper pipeline, and audits) with:

```bash
make verify
```

That command regenerates the matched provenance intervention, learned/hybrid benchmark results, strict statistics, multi-seed study, trial evaluation, failure curriculum, research gate, and all public claim audits. The broader historical/proxy experiments remain available under `make reproduce`, but they are not required to support the paper claim.

## Separate routing from generation

Routing accuracy is not generation quality. Even a perfect license vector can fail if a downstream language model ignores it.

The repository therefore includes a provider-neutral generation harness:

```bash
python scripts/evaluate_generation_adapter.py path/to/adapter.py
```

An adapter exposes:

```python
generate(example: dict, licenses: dict) -> str
```

See `docs/GENERATION_EVAL_PROTOCOL.md`.

## Human validation

`datasets/human_eval/blinded_license_packet.csv` contains a blinded **552-item** validation packet. `scripts/aggregate_human_eval.py` aggregates completed annotations and reports nominal agreement plus majority-vs-contract accuracy. Human annotations are not included in this release.

## Paper

- `paper/PAPER_DRAFT.md`
- `paper/main.tex`
- `artifacts/personalized-not-persuaded-paper.pdf`

The paper makes a deliberately narrow claim: **provenance-conditioned multi-channel licensing is learnable in a controlled benchmark, standard held-out evaluation hides important shift failures, and explicit validity constraints improve—but do not solve—those failures.**

The current evidence is limited to controlled routing experiments; human validation and end-to-end generation studies are specified but not yet reported.

## Reviewer path

If you have five minutes:

1. `RESULTS_CARD.md`
2. `paper/PAPER_DRAFT.md`
3. `reports/PROVENANCEBENCH_EXECUTABLE.md`
4. `docs/DESIGN_DECISIONS.md`
5. `docs/THREATS_TO_VALIDITY.md`
6. `docs/SUBMISSION_READINESS.md`

For the full artifact map, see `ARTIFACT_INDEX.md`.

## Eval-to-training loop

The repository now includes an executable research loop rather than stopping at benchmark reporting:

```text
frozen tasks
→ trials + trajectories
→ state-verification graders
→ failure taxonomy
→ targeted correction data
→ stability anchors
→ research-candidate gate
→ re-evaluation
```

Run it with:

```bash
make research-gate
make curriculum
```

The current Hybrid PLP outputs generate **392 targeted correction examples**, all of them evidence-starvation failures, plus **392 stability anchors**. This makes the next intervention concrete: improve licensed evidence uptake without bringing unsupported influence leakage back.

See `docs/EVAL_TO_TRAINING_LOOP.md`, `docs/LAUNCH_GATES.md`, and `docs/RESEARCH_AGENDA.md`. The bundled mixture is the input to a future post-training experiment; this release stops before model updating.

## Evidence layer

The polished homepage is intentionally not the whole story. `evidence/` records the research process behind the current method:

- `evidence/EXPERIMENT_JOURNAL.md` — 12 logged experiments with hypothesis → setup → result → interpretation → next decision;
- `evidence/FAILED_EXPERIMENTS.md` — six rejected or revised research ideas;
- `evidence/DECISION_LOG.md` — eight material technical decisions with alternatives and trade-offs;
- `evidence/REAL_EVAL_TABLES.md` — N, confidence intervals, seeds, calibration, and trial-level failure counts;
- `evidence/UNEXPECTED_FINDINGS.md` — findings that changed the direction of the work;
- `artifacts/evidence/` — raw evaluation snapshots, failure examples, plots, configs, trajectories, ablations, and Git evidence.

Regenerate the raw layer with `make evidence`; `make verify` rebuilds it and fails if the evidence contract drifts from the canonical results.
