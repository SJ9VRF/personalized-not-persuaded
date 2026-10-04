# Unexpected Findings

## 1. Perfect ordinary held-out accuracy was not a robustness result

The learned router reached **1.000** exact match on the ordinary ID split. That initially looked like the routing problem might be nearly solved. It was not: domain OOD fell to **0.842** and compositional exact match to **0.400**.

**Why it mattered:** it shifted the project from optimizing a headline score to building structured-shift and causal diagnostics.

---

## 2. Removing provenance did not always hurt the ordinary benchmark

A no-provenance variant remained surprisingly strong on some ordinary splits because other fields correlated with source type. That could have led to the wrong conclusion that provenance was unimportant.

On the matched intervention, where only provenance changes, no-provenance exact match fell to **0.500**.

**Why it mattered:** it exposed a benchmark shortcut and motivated the paired provenance test.

---

## 3. The hybrid repair changed the *type* of error

Hybrid PLP drove measured OOD unsupported leakage to **0.000**, but it did not solve evidence uptake. The frozen trial run produced **392 failures**, all classified as **evidence starvation**.

**Why it mattered:** the next intervention should add evidence responsiveness, not stronger blocking.

---

## 4. Confidence failed before the final decision metric fully collapsed

Evidence-head ECE moved from **0.011** on ID to **0.157** on domain OOD and **0.486** on the compositional split.

**Why it mattered:** calibration is an earlier warning signal than aggregate exact-match alone and belongs in the core evaluation surface.

---

## 5. Ten seeds did not explain away the failure

The same split-specific metrics repeated across **10 seeds**.

**Why it mattered:** the failure is structural in this controlled setup, not a convenient bad initialization that can be removed by seed selection.
