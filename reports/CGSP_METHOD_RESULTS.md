> **Supporting predecessor artifact.** The current paper result is the learned ProvenanceBench study in `reports/PROVENANCEBENCH_EXECUTABLE.md`; this file documents an earlier controlled reference design.

# CGSP Method Results

**Method:** Contract-Guided Selective Personalization (CGSP)

CGSP implements a hard factorization of user context. Allowed channels (style, response preferences, goals, constraints) may change presentation; protected beliefs and non-evidentiary memories cannot enter the response-construction path.

## Exact paired contract result

- Contracts: **820**
- Allowed Personalization Gain: **0.3627**
- Protected Epistemic Drift: **0.0000**
- Protected Epistemic Invariance: **1.0000**
- Contract Score: **0.3627**
- Contract Pass Rate: **100.0%**

For comparison, the behavior-aware proxy passes **90.2%** and naive personalization passes **70.7%** in the same controlled fixture.

## Interpretation boundary

The result establishes that the *implementation obeys the intended contract in the local proxy world*. It does not establish SOTA performance on frontier models. The falsifiable next experiment is to apply the same factorized contract as a training/steering regularizer to real models and evaluate with blinded human labels.
