# Closest-Work Matrix

**Project:** Personalized, Not Persuaded  
**Author:** Aura Yavary

This matrix is intentionally conservative. It is meant to prevent novelty inflation, not to create it.

| Work | What it already covers | What this project must *not* claim | Remaining distinction used here |
|---|---|---|---|
| FPPS / PFQABench | Factuality-preserving personalization; detects personalization-induced factual distortion and steers representations | First work on personalization + factuality | Explicit signal-level standing across presentation / personalization / evidence, including legitimate user-specific evidence uptake |
| Resist and Update | Causal contract: resist forbidden influence, update to licensed evidence; counterfactual report coordinates | First resist/update or causal-contract formulation | Persistent personal context, heterogeneous memory/tool provenance, task-conditioned standing, and leakage-vs-starvation in personalization |
| Interaction Context Often Increases Sycophancy | Shows richer interaction context and memory profiles can increase sycophancy | First to connect personalization and sycophancy | Intervention / routing objective rather than observational characterization |
| QUMem | Query-conditioned user-state inference with typed memories, temporal validity, and source evidence | First query-conditioned provenance-aware personalization system | Decides what retrieved personal context is *allowed to influence*, not primarily how to retrieve or infer user state |
| MemORAI | Provenance-enriched memory graph and query-adaptive retrieval | First provenance-aware memory retrieval method | Influence permission after retrieval; three distinct behavioral channels |
| Agent Zero Memory | Provenance-aware long-term memory, citation lock, multi-store retrieval | First provenance/citation discipline for personal memory | Task-conditioned standing can permit personalization without permitting epistemic update; includes evidence-starvation objective |
| Veracium | Source-aware memory quarantine and provenance-preserving user memory | First product system to quarantine third-party claims | Learned / evaluated standing rather than fixed storage quarantine |
| PACMI | Provenance-aware invalidation of stale dependent memories | First provenance + temporal update handling | Standing at use time across behavior channels rather than dependency invalidation alone |
| NLSI standing instructions | Selects which persistent user instructions apply to a current dialogue | First task-conditioned selection of persistent preferences | Separates applicability from evidentiary authority and tests factual influence explicitly |

## Strongest novelty statement

The safest current statement is:

> **We study the evidentiary standing of personal context: for a given task, which user-context signals may affect presentation, personalization, or the epistemic answer? We operationalize standing as a three-channel license vector and evaluate both unsupported influence leakage and evidence starvation with matched provenance interventions.**

## What would be required for a stronger claim

To claim empirical state of the art, the project still needs head-to-head evaluation on real language models against the strongest comparable methods, including at least an FPPS-style baseline and a Resist-and-Update-style baseline, plus independent human validation. Until then, the project is **frontier-aligned and plausibly novel in formulation**, not empirically proven SOTA.
