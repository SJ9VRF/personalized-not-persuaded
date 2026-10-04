# Senior Research Audit

**Project:** Personalized, Not Persuaded  
**Paper:** *Learning When Personal Context Counts as Evidence*  
**Author:** Aura Yavary

## Verified
- 26/26 unit tests pass.
- ProvenanceBench headline results regenerate from code.
- Domain-OOD, compositional, conflict, and matched provenance interventions are included.
- Claim ledger matches generated result artifacts.
- Result-consistency audit verifies the public benchmark tables against `results/provenancebench_method_summary.csv`.
- Superseded ProvenanceBench reports are isolated under `archive/legacy_reports/` rather than the active reviewer path.
- Public surfaces use the current title and avoid stale prototype framing.
- The browser demo is labeled as a contract explorer; learned-router results come from the executable benchmark.
- The eval-to-training loop regenerates trial trajectories, a 392-example failure curriculum, and a balanced 784-example training mixture.
- Research-candidate gate passes on the controlled benchmark.

## Evidence boundary
- Human annotations are prepared but not collected in this release.
- End-to-end language-model generation experiments are not reported.
- The post-training mixture is prepared, but model updating has not been run.
- Results support a controlled routing/evaluation claim, not an empirical frontier-model SOTA claim.

## Senior-review conclusion
The repository now has one coherent research story: personal context can be useful without automatically counting as evidence. The main path exposes the paper, learned method, benchmark, causal provenance intervention, failure analysis, and eval-to-training loop. Older supporting experiments remain in the repository for reproducibility but are not part of the reviewer path.

## Homepage / hiring-manager surface

The flagship `index.html` implements the required 14-section project-page contract. It includes a 60-second summary, a baseline→method executive result table (success / recovery / measured router-only latency / external API cost), recorded frozen evaluation trajectories, scaling and safety boundaries, a complete artifact inventory, and a 2026 BibTeX citation for Aura Yavary. The public GitHub state is represented honestly: no repository URL is invented; the exact GitHub-ready source snapshot is shipped instead.

Environment-specific homepage runtime measurements are stored in `results/homepage_runtime_summary.json` and regenerated only with `make homepage`; they are intentionally outside the deterministic paper pipeline.
