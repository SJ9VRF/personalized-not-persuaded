# Final Checklist

- [x] Project name: **Personalized, Not Persuaded**
- [x] Paper subtitle: **Learning When Personal Context Counts as Evidence**
- [x] Author: **Aura Yavary**
- [x] README, homepage, paper, citation metadata, and reviewer guide use the same title
- [x] Learned PLP and Hybrid PLP are executable
- [x] ProvenanceBench: 4,800 examples
- [x] Matched provenance intervention: 800 examples / 400 pairs
- [x] ID, domain-OOD, compositional, and conflict evaluations
- [x] Calibration, bootstrap CIs, paired tests, and multi-seed evaluation
- [x] Human-validation packet + aggregation code
- [x] Provider-neutral generation adapter + oracle-license condition
- [x] Trial/trajectory/state-verification evaluation
- [x] Failure curriculum + stability-anchor training mixture
- [x] Research-candidate gate + regression gates
- [x] Claim ledger + claim audit
- [x] Public benchmark tables checked against canonical result CSV
- [x] Superseded result reports moved out of the active reviewer path
- [x] Public-surface audit
- [x] CI runs method, statistics, research gate, regression, submission, claim, result-consistency, and public-surface audits
- [x] 26/26 unit tests pass
- [x] Paper PDF rendered from current source
- [x] PDF contains no project CreationDate/ModDate metadata
- [x] No public claim of completed human study, frontier-model generation gain, or post-training run

## Flagship project homepage

- [x] Independent project homepage with exactly 14 required sections.
- [x] Hero includes project name, one-sentence problem, main result, and Paper / Code / Demo / Benchmark / Video actions.
- [x] 60-second summary exposes problem, contribution, main result, and working status.
- [x] Architecture includes evaluation → failure → correction data → future SFT/preference/RL → frozen re-evaluation loop.
- [x] Results include baseline→method success, recovery, measured router latency, and external API cost, plus research metrics.
- [x] Demo includes recorded frozen Hybrid PLP success and real OOD failure trajectories; contract explorer is explicitly separate.
- [x] Scaling and safety cover model size, task horizon, tool count, latency/cost, robustness, irreversible actions, permission boundaries, and human escalation.
- [x] Artifacts include Paper, GitHub status, exact source snapshot, Benchmark, Dataset, Demo, Video, Technical report, and Blog post.
- [x] Citation lists Aura Yavary, year 2026, and BibTeX.

## Evidence layer

- [x] 12 logged experiments with hypothesis / setup / result / interpretation / next decision.
- [x] Dedicated “What didn't work” page with six real rejected/revised ideas.
- [x] Decision log with eight material choices, alternatives, evidence, trade-offs, and outcomes.
- [x] Real eval tables include N, bootstrap CIs, seeds, calibration, and trial-level failure counts.
- [x] Five unexpected findings are documented separately from headline results.
- [x] Raw evidence tree includes experiment logs, eval runs, failure examples, plots, configs, qualitative trajectories, and ablations.
- [x] Homepage contains an unnumbered “Inside the research process” layer beneath the polished story.
- [x] Evidence layer has its own builder and audit and is part of `make verify`.
- [x] Git history begins honestly at the verified snapshot; no backdated history is invented.
