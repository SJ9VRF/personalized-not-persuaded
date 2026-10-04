# Technical Report — Personalized, Not Persuaded

**Aura Yavary**

## 1. Problem

A personal assistant consumes heterogeneous context: preferences, inferred habits, memories, tool outputs, third-party messages, and external records. Retrieval answers *what context is available*. PLP asks a different question: **what influence is each signal licensed to exert on this task?**

Two failure modes are symmetric:

- **unsupported influence leakage** — ungrounded or irrelevant context enters the evidentiary path;
- **evidence starvation** — current, relevant, grounded context is rejected.

## 2. License space

For each signal, PLP predicts three binary permissions:

- **presentation** — may alter wording or style;
- **personalization** — may affect user-specific ranking, planning, or choice;
- **evidence** — may change a factual or personal-state conclusion.

The prediction conditions on signal text, semantic scope, provenance, task, confidence, currentness, and relevance.

## 3. Learned router

`behavior_lab/methods/learned_plp.py` trains three independent class-balanced logistic heads over TF-IDF signal text, one-hot categorical metadata, and standardized continuous validity features. Each decision threshold is selected on validation only.

The design is intentionally simple: the scientific object is the licensing decomposition and its failure modes, not representational capacity.

## 4. Hybrid PLP

The pure learned router generalizes poorly to held-out combinations of trusted provenance with invalid context. Hybrid PLP applies three auditable negative gates after prediction:

```text
if stale OR low-confidence OR task-irrelevant:
    presentation = personalization = evidence = 0
```

These gates improve robustness but are asymmetric: they can veto an invalid positive, not create a licensed evidence permission the learned router missed.

## 5. ProvenanceBench

The primary benchmark contains **4,800 signal-level examples** across eight domains. Main-router splits:

- train: 1,680
- validation: 168
- ordinary held-out: 168
- domain-OOD: 912
- compositional: 720

Conflict-source rows are separated because source selection is a different subproblem from binary licensing.

A separate **400-pair / 800-example provenance intervention** holds task, scope, confidence, currentness, relevance, and surface text fixed while changing only source provenance.

## 6. Executable results

| Method | ID exact | Domain-OOD exact | Compositional exact | OOD uptake ↑ | OOD leakage ↓ |
|---|---:|---:|---:|---:|---:|
| Naive | 0.286 | 0.368 | 0.600 | 1.000 | 0.857 |
| Firewall | 0.571 | 0.526 | 0.400 | 0.000 | 0.000 |
| Provenance-only | 0.714 | 0.684 | 0.600 | 0.800 | 0.071 |
| Learned PLP | 1.000 | 0.842 | 0.400 | 0.800 | 0.143 |
| **Hybrid PLP** | **1.000** | **0.947** | **0.800** | **0.800** | **0.000** |
| Oracle | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |

Hybrid PLP item-bootstrap intervals are 0.947 [0.933, 0.962] on domain OOD and 0.800 [0.771, 0.828] on compositional shift.

## 7. Paired provenance intervention

On the matched intervention:

- strict learned no-provenance ablation: **0.500** exact match;
- Learned PLP: **0.750**;
- Hybrid PLP: **0.750**;
- provenance-only rule: **1.000**.

This result is deliberately mixed. It establishes causal provenance sensitivity while showing incomplete learned transfer when lexical source cues are removed.

## 8. Calibration

Evidence-head ECE:

- ordinary held-out: 0.011
- domain-OOD: 0.157
- compositional: 0.486
- provenance intervention: 0.253

Calibration degradation is therefore itself a useful shift signal.

## 9. Conflict resolution

The benchmark includes grouped conflicting sources. An explicit authority/freshness ranking reaches 1.000 on the current controlled conflict groups. This is reported separately and should not be interpreted as open-ended source reasoning.

## 10. Routing vs generation

A correct route does not guarantee a correct answer. The repository includes `scripts/evaluate_generation_adapter.py` so the same generator can be tested with:

- unrestricted context;
- predicted licenses;
- oracle licenses.

The oracle condition separates **router error** from **generation-compliance error**.

## 11. Human validation

A blinded 552-item packet and separate held-out answer key are included. The aggregation script computes nominal inter-rater agreement and majority-vs-contract agreement. No human judgment is claimed before labels are actually collected.

## 12. Multi-seed stability

Ten logistic-router solver seeds reproduce the same aggregate metrics. This rules out initialization noise for the bundled linear method, but it is not a substitute for neural-model seed variance.

## 13. Reproduction

```bash
python scripts/build_provenance_intervention.py
python scripts/run_provenancebench_learned.py
python scripts/provenancebench_stats_strict.py
python scripts/provenancebench_multiseed.py
pytest -q
python scripts/submission_audit.py
```

## 14. Scientific boundary

The current release supports a controlled licensing-method and benchmark claim. It does **not** establish:

- frontier-model SOTA;
- end-to-end generation improvement;
- human agreement with all contract labels;
- robustness to inferred or adversarially spoofed provenance.

Those are explicitly the next empirical layer rather than hidden assumptions.
