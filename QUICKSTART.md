# Quickstart

## Reproduce the current paper

```bash
python -m pip install -r requirements.txt
make paper
pytest -q
```

`make paper` is the canonical path for the current research claim. It regenerates the matched provenance intervention, learned/hybrid PLP results, strict statistics, multi-seed analysis, trial evaluation, failure curriculum, research gate, and claim-consistency audits.

## Run the broader research history

```bash
make reproduce
```

This extended pipeline also runs earlier BehaviorBench, counterfactual-contract, reward-proxy, long-horizon, and diagnostic experiments. Those artifacts are retained for research history and regression coverage; they are not required to establish the main paper result.

## Review order

1. `RESULTS_CARD.md`
2. `paper/PAPER_DRAFT.md`
3. `reports/PROVENANCEBENCH_EXECUTABLE.md`
4. `reports/PROVENANCEBENCH_STRICT_STATS.md`
5. `docs/DESIGN_DECISIONS.md`
6. `docs/THREATS_TO_VALIDITY.md`
7. `behavior_lab/methods/learned_plp.py`

## External experiments not bundled as completed results

- independent human annotation
- end-to-end language-model generation study
- frontier/open-model head-to-head comparison

The repository contains frozen protocols and adapters for these experiments, but it does not present them as completed evidence.

## Verify the complete release

Run the same contract used by CI:

```bash
make verify
```

This runs unit tests, Python compilation, the canonical paper pipeline, and all release audits.

## Re-measure homepage runtime/demo assets

`make homepage` regenerates the environment-specific router latency summary and the recorded demo examples. It is intentionally separate from `make paper` because latency is machine-dependent.
