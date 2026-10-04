# Project Homepage Completion Checklist

The flagship homepage is `index.html`; `site/index.html` is a standalone mirror.

| Required section | Implemented content |
|---|---|
| 1. Hero | Project name; one-sentence problem; main result; Paper / Code / Demo / Benchmark / Video buttons |
| 2. Why this problem matters | Problem, difficulty, why naive personalization and fixed firewalls fail |
| 3. Core idea | PLP in 2–3 sentences; explicit novelty boundary; three influence licenses |
| 4. Architecture | Main pipeline diagram plus failure-to-data-to-retraining/recovery loop |
| 5. My contribution | Design ownership, implementation ownership, key technical decision |
| 6. Experiments | Datasets/tasks, baselines, ablations, setup, frozen protocol, human-eval path |
| 7. Results | Clean baseline→method table with success, recovery, evidence uptake, leakage, latency, cost |
| 8. Failure analysis | Concrete benchmark failures, causes, and PLP recovery behavior |
| 9. Interactive demo | Recorded frozen Hybrid PLP trials (success + real OOD failure) plus a separate browser contract explorer |
| 10. Scaling | Model size, task horizon, tool count, cost/latency, robustness, data scale |
| 11. Safety / limitations | Known failures, irreversible actions, permission boundaries, human escalation |
| 12. Technical deep dive | Engineering report, training objective, eval methodology, real-model adapter |
| 13. Artifacts | Paper, GitHub status, exact source snapshot, benchmark, dataset, demo, video, technical report, blog |
| 14. Citation | Aura Yavary, 2026, and BibTeX |

## Author

Aura Yavary

## Automated enforcement

This 14-section contract is enforced by `scripts/homepage_contract_audit.py` and runs as part of `make audit` / `make verify`. The release fails if a required section, Hero CTA, executive results field, recorded trajectory, scaling/safety item, artifact link, author, year, or BibTeX block is missing.

## Evidence layer below the polished story

The homepage also contains an unnumbered **Inside the research process** layer between Failure Analysis and Interactive Demo. It is intentionally outside the 14-section numbering so the required project-page structure stays stable.

Required evidence links:

- Experiment Journal
- What didn't work
- Decision Log
- Unexpected Findings
- Real Eval Tables
- Full Evidence Layer
- Reproduce results

Current release counts are 12 logged experiments, 6 failed/revised research ideas, 8 material decisions, and 5 unexpected findings. `scripts/evidence_layer_audit.py` verifies these against the evidence files and raw artifact tree.
