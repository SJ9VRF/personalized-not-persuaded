# Decision Log

Format: **Decision → Alternatives → Evidence → Trade-off → Outcome**.

## D-001 — Model standing, not trusted/untrusted memory

**Decision**  
Represent whether a signal may affect presentation, personalization, and evidence separately for the current task.

**Alternatives**  
One global trust bit; retrieve/don't-retrieve; fixed memory firewall.

**Evidence**  
The fixed firewall removed leakage but drove evidence uptake to 0.000; naive personalization achieved 1.000 uptake with 0.857 OOD leakage.

**Trade-off**  
More explicit state and evaluation complexity in exchange for distinguishing legitimate personal evidence from unsupported belief.

**Outcome**  
Three-channel standing became the central problem formulation.

---

## D-002 — Keep three independent license heads

**Decision**  
Predict presentation, personalization, and evidence standing independently.

**Alternatives**  
A single “use context” classifier; one scalar trust score.

**Evidence**  
Several benchmark cases require style/personalization to change while evidentiary state must remain unchanged.

**Trade-off**  
Three outputs are harder to evaluate, but they expose cross-channel leakage that a single score would hide.

**Outcome**  
Exact three-license match plus channel-specific metrics are canonical.

---

## D-003 — Hybrid learned router + narrow validity gates

**Decision**  
Use learned PLP for standing prediction, then enforce three explicit gates for stale, low-confidence, and task-irrelevant context.

**Alternatives**  
Pure learned router; fully deterministic rule system; larger learned model.

**Evidence**  
Pure learned PLP was 1.000 ID but 0.400 compositional and 0.143 OOD leakage. Hybrid PLP reached 0.800 compositional and 0.000 OOD leakage.

**Trade-off**  
The hybrid system is less “pure” statistically, but easier to audit and safer under the measured shifts. It remains somewhat conservative.

**Outcome**  
Hybrid PLP is the current method; learned-only remains an ablation.

---

## D-004 — Add a matched provenance intervention

**Decision**  
Hold task, scope, confidence, freshness, relevance, and surface text fixed while changing only provenance.

**Alternatives**  
Rely on ID/OOD accuracy and feature ablations.

**Evidence**  
The no-provenance model looked strong on some ordinary splits but fell to 0.500 on the paired intervention.

**Trade-off**  
The paired test is intentionally narrow and synthetic, but it isolates the causal role of provenance much better than aggregate accuracy.

**Outcome**  
The 800-example paired intervention is required in `make paper`.

---

## D-005 — Report leakage and starvation separately

**Decision**  
Treat unsupported influence leakage and evidence starvation as distinct failure axes.

**Alternatives**  
One aggregate accuracy or “safety” score.

**Evidence**  
Naive personalization and the firewall fail in opposite directions; a single score obscures why.

**Trade-off**  
More metrics to read, but the failure mechanism is visible.

**Outcome**  
Exact match is accompanied by uptake, leakage, starvation, and calibration.

---

## D-006 — Keep oracle and simple baselines

**Decision**  
Retain naive, firewall, provenance-only, and oracle conditions even when they are not competitive end systems.

**Alternatives**  
Compare only learned variants.

**Evidence**  
The oracle separates “can correct standing solve the routing task?” from “can the model infer standing?”; the firewall exposes starvation; provenance-only isolates source information.

**Trade-off**  
The table is larger, but each baseline answers a different diagnostic question.

**Outcome**  
All four remain in the canonical result surface.

---

## D-007 — Use grouped / structured splits, not random rows

**Decision**  
Freeze ID, domain-OOD, compositional, conflict, and paired provenance splits; group semantically related reward-model variants.

**Alternatives**  
Random row split everywhere.

**Evidence**  
Random rows can leak near-duplicate scenario variants and ordinary held-out performance substantially overstates compositional robustness.

**Trade-off**  
Harder metrics and lower apparent performance, but more meaningful generalization evidence.

**Outcome**  
Structured splits are part of `make paper` and the evidence layer.

---

## D-008 — Do not train on every mined failure yet

**Decision**  
Build a balanced correction mixture with stability anchors, but do not claim post-training improvement until a real model intervention is run.

**Alternatives**  
Train on all failure examples immediately; claim the curriculum itself as a performance result.

**Evidence**  
The current failure miner finds 392 starvation cases. Overweighting them without anchors could repair one failure class while regressing already-correct decisions.

**Trade-off**  
The project stops short of a stronger end-to-end claim, but the evidence boundary stays clean.

**Outcome**  
The repo exports 392 corrections + 392 stability anchors and labels them as *training input*, not training evidence.
