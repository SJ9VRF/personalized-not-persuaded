# Experiment Journal

**Provenance note.** EXP-001 through EXP-012 are a retrospective reconstruction from the frozen result files and design documents in this release. They are not presented as contemporaneous notes written at the moment each experiment ran. Each machine-readable experiment record links to its source artifacts and reproduction command. New work after the Git import is recorded incrementally.

These are the experiments that materially changed the current research story. The numbering is a research journal for this release, not a claim about historical commit dates.

## EXP-001 — Naive personalization baseline

**Hypothesis**  
Using all personally relevant context should improve personalization without badly damaging epistemic behavior.

**Setup**  
Apply the naive policy on the frozen ProvenanceBench splits and score exact three-license match, evidence uptake, leakage, and starvation.

**Result**  
On domain OOD (N=912), exact match was **0.368**, evidence uptake **1.000**, and unsupported leakage **0.857**.

**Interpretation**  
The policy is responsive, but it treats personal relevance too much like evidentiary authority.

**Next decision**  
Keep it as the lower-bound personalization baseline; do not use it as the core method.

---

## EXP-002 — Fixed firewall

**Hypothesis**  
A hard firewall that blocks personal context from the evidence channel should prevent contamination while remaining usable.

**Setup**  
Evaluate a fixed firewall on the same frozen splits.

**Result**  
On domain OOD, leakage fell to **0.000**, but evidence uptake also fell to **0.000** and exact match was **0.526**.

**Interpretation**  
Safety-by-blocking creates the opposite failure: legitimate evidence starvation.

**Next decision**  
Retain the firewall as a diagnostic baseline, not as the final architecture.

---

## EXP-003 — Provenance-only rule

**Hypothesis**  
Source provenance alone may be sufficient to decide evidentiary standing.

**Setup**  
Use a narrow explicit provenance rule and compare it to naive personalization and the fixed firewall.

**Result**  
Domain-OOD exact match improved to **0.684**, with evidence uptake **0.800** and leakage **0.071**. Compositional exact match was **0.600**.

**Interpretation**  
Provenance is important, but provenance alone does not encode task relevance, freshness, or confidence.

**Next decision**  
Learn task-conditioned standing rather than relying only on source type.

---

## EXP-004 — Learned three-head PLP router

**Hypothesis**  
A learned router can infer presentation, personalization, and evidence standing jointly and generalize beyond the training distribution.

**Setup**  
Train three license heads with validation-only thresholds; evaluate ID, domain-OOD, compositional, and matched provenance splits.

**Result**  
The learned router reached **1.000** ID exact match, but only **0.842** domain-OOD and **0.400** compositional exact match. OOD leakage was **0.143**.

**Interpretation**  
The learned formulation fits the ordinary held-out task but is brittle under structured shift.

**Next decision**  
Keep the learned router, but add a small set of auditable validity constraints rather than hiding the failure with a larger classifier.

---

## EXP-005 — Hybrid validity gates

**Hypothesis**  
A learned router plus narrow constraints for stale, low-confidence, and task-irrelevant context can reduce leakage without collapsing back into a fixed firewall.

**Setup**  
Apply the three validity gates after the learned heads and rerun the frozen splits.

**Result**  
Hybrid PLP reached **0.947 [0.933, 0.962]** domain-OOD exact match and **0.800 [0.771, 0.828]** compositional exact match. OOD leakage fell to **0.000**, while evidence uptake remained **0.800**.

**Interpretation**  
The hybrid repair fixes much of the shift failure, but it remains conservative: some valid evidence is still missed.

**Next decision**  
Treat evidence starvation as the dominant remaining failure rather than claiming the routing problem is solved.

---

## EXP-006 — Matched provenance intervention

**Hypothesis**  
If provenance is causally important, changing only provenance while holding task, scope, confidence, currentness, relevance, and surface text fixed should change the correct standing decision.

**Setup**  
Evaluate 400 matched pairs / 800 examples with only provenance metadata changed.

**Result**  
No-provenance exact match was **0.500**; Learned PLP and Hybrid PLP were **0.750**; the narrow provenance-only rule was **1.000**.

**Interpretation**  
Provenance is causally necessary on this controlled test, but the learned router does not transfer perfectly to delexicalized provenance changes.

**Next decision**  
Keep the paired intervention as a required causal diagnostic rather than relying only on standard held-out accuracy.

---

## EXP-007 — Calibration under distribution shift

**Hypothesis**  
If the evidence head generalizes, its confidence should remain reasonably calibrated under domain and compositional shift.

**Setup**  
Measure evidence-head expected calibration error (ECE) on the frozen splits.

**Result**  
ECE increased from **0.011** on ID to **0.157** on domain OOD and **0.486** on the compositional split.

**Interpretation**  
The model becomes miscalibrated exactly where standing decisions become harder. Accuracy alone understated this failure.

**Next decision**  
Report calibration beside exact match and keep uncertainty-aware evaluation in the core evidence set.

---

## EXP-008 — Multi-seed stability

**Hypothesis**  
The large compositional failure might mainly be optimizer or initialization variance.

**Setup**  
Retrain/evaluate Learned and Hybrid PLP across **10 seeds (0–9)**.

**Result**  
The reported metrics were stable across seeds; the same split-specific failure pattern repeated.

**Interpretation**  
The dominant problem is not random initialization. It is the representation / split structure.

**Next decision**  
Spend effort on better interventions and data construction, not on cherry-picking seeds.

---

## EXP-009 — Conflicting-source authority subtest

**Hypothesis**  
Conflict resolution between multiple evidence sources should be measured separately from whether a single signal has evidentiary standing.

**Setup**  
Evaluate an explicit source-authority ranking on controlled conflict groups.

**Result**  
The current ranking rule reaches **1.000** on the controlled in-domain and held-out conflict groups.

**Interpretation**  
This is a specification-level success for a distinct subproblem; folding it into the main license metric would overstate the learned router.

**Next decision**  
Keep authority selection separate from standing classification in both the paper and the code.

---

## EXP-010 — Trial-level failure mining

**Hypothesis**  
The remaining Hybrid PLP failures would include a mixture of unsupported leakage and evidence starvation.

**Setup**  
Run the frozen task/trial/grader evaluation over **2,600 trials** and mine failed state-verification events.

**Result**  
There were **392** licensing failures, and all **392** were classified as **evidence starvation** in the current frozen run.

**Interpretation**  
The hybrid method has become conservative. The next data intervention should target missed valid evidence, not stronger blocking.

**Next decision**  
Build a targeted correction curriculum around starvation failures.

---

## EXP-011 — Failure-driven correction mixture

**Hypothesis**  
Failures should be converted into targeted training examples without discarding already-correct behavior.

**Setup**  
Convert the 392 starvation failures into correction examples and pair them with an equal number of stability anchors sampled from successful cases.

**Result**  
The resulting post-training seed contains **392 failure corrections + 392 stability anchors = 784 examples**.

**Interpretation**  
The eval-to-data loop is executable, but this is a data artifact, not evidence that SFT / preference optimization / RL has already improved a language model.

**Next decision**  
Use this mixture in a future real-model intervention and rerun the identical frozen evaluation surface.

---

## EXP-012 — Research-candidate gate

**Hypothesis**  
The current controlled router is mature enough to be treated as a research candidate while remaining below a production-launch claim.

**Setup**  
Gate ID, OOD, compositional, leakage, uptake, and trial-weighted state score against fixed thresholds.

**Result**  
All research-candidate checks pass; the trial-weighted state score is **0.9246**. The gate explicitly says it is **not** a production launch approval.

**Interpretation**  
The controlled system is reproducible enough for the next research stage, but external-model and human evidence are still required.

**Next decision**  
Freeze the controlled protocol and move the next scientific risk to real-model generation and independent human judgment.
