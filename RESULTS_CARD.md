# Results Card — Personalized, Not Persuaded

**Aura Yavary**

## Main result

The central result is a failure-and-repair story, not a perfect benchmark score.

A three-head learned PLP router fits the ordinary held-out licensing task, but degrades under domain and compositional shift. Hybrid PLP adds three narrow validity gates—stale, low-confidence, and task-irrelevant context cannot receive a license. Those gates remove measured unsupported leakage, but they do not recover every licensed-evidence positive missed by the learned router.

| Method | ID exact | Domain-OOD exact | Compositional exact | OOD evidence uptake ↑ | OOD leakage ↓ |
|---|---:|---:|---:|---:|---:|
| Naive personalization | 0.286 | 0.368 | 0.600 | 1.000 | 0.857 |
| Fixed firewall | 0.571 | 0.526 | 0.400 | 0.000 | 0.000 |
| Provenance-only | 0.714 | 0.684 | 0.600 | 0.800 | 0.071 |
| Learned PLP | **1.000** | 0.842 | 0.400 | 0.800 | 0.143 |
| **Hybrid PLP** | **1.000** | **0.947** | **0.800** | **0.800** | **0.000** |
| Oracle | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |

Item-bootstrap intervals for Hybrid PLP are **0.947 [0.933, 0.962]** on domain OOD and **0.800 [0.771, 0.828]** on the compositional split.

## Causal provenance intervention

Standard benchmark performance can still be confounded by correlations between task, scope, and source type. I therefore added **400 matched provenance pairs (800 examples)** in which task, scope, confidence, currentness, relevance, and surface text are fixed. Only provenance metadata changes.

| Method | Exact match ↑ | Evidence uptake ↑ | Unsupported leakage ↓ |
|---|---:|---:|---:|
| Naive | 0.500 | 1.000 | 1.000 |
| Firewall | 0.500 | 0.000 | 0.000 |
| Provenance-only | **1.000** | **1.000** | **0.000** |
| Learned PLP | 0.750 | 0.500 | 0.000 |
| Hybrid PLP | 0.750 | 0.500 | 0.000 |
| Learned without provenance cues | 0.500 | 1.000 | 1.000 |

The intervention shows two things at once: provenance is causally necessary for the matched task, and the learned router still transfers imperfectly to delexicalized source changes.

## Conflicting evidence

A separate authority-selection subtest chooses among multiple candidate sources for the same state. The current explicit ranking rule reaches **1.000** on both in-domain and held-out-domain conflict groups. This is intentionally reported as a separate subproblem rather than folded into license classification.

## Calibration and error analysis

The learned evidence head is well calibrated on the ordinary held-out split (ECE **0.011**) but degrades under domain shift (ECE **0.157**) and compositional shift (ECE **0.486**). This reinforces the main result: standard held-out accuracy substantially overstates robustness.

## Evidence still required for an end-to-end language-model claim

No human judgments or external model generations are claimed as completed. The repository includes:

- a **552-item blinded human-evaluation packet**;
- an aggregation script reporting Krippendorff-style nominal agreement and majority-vs-contract accuracy;
- a frozen generation-adapter harness;
- oracle-license conditions that separate **routing error** from **generation-compliance error**.

The current evidence supports a controlled routing and benchmark claim. End-to-end model quality remains an external experiment.
