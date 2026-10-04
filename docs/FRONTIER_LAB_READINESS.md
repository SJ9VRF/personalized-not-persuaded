# Frontier-Lab Readiness

This project is intentionally organized to demonstrate research behaviors that matter in frontier model teams rather than only a polished paper artifact.

## Evaluation craftsmanship

- frozen benchmark and claim ledger;
- domain-OOD, compositional, conflict, and causal provenance-intervention splits;
- task/trial/grader/trajectory representation;
- state verification rather than output-only scoring;
- bootstrap uncertainty, paired significance tests, calibration diagnostics, and multi-seed evaluation.

## Model-behavior debugging

- failure taxonomy separates unsupported influence leakage from evidence starvation;
- error exports preserve the exact source example and predicted license vector;
- the main negative result is retained rather than hidden: learned routing fails under compositional shift and Hybrid PLP still starves some licensed evidence.

## Post-training interface

- failure mining produces correction examples;
- stability anchors protect already-correct decisions;
- the post-training mixture is generated deterministically from frozen outputs;
- the repository distinguishes “data prepared for training” from “training completed.”

## Research-to-product boundary

- a research-candidate gate is executable;
- production launch requirements are documented separately;
- generation compliance, human validity, latency/cost, adversarial provenance, and broader safety regressions remain explicit external gates.

## Research ownership

`docs/RESEARCH_AGENDA.md` records the next experiments and kill criteria. `docs/DESIGN_DECISIONS.md` records rejected approaches and why the current architecture exists. Together they make the project inspectable as an evolving research program rather than a one-shot benchmark result.
