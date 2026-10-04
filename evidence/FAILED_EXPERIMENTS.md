# What didn't work

These are not decorative “failure stories.” Each item changed the design, evaluation, or claim boundary.

## 1. Naive personalization leaked user belief into evidence

**What we expected**  
More personal context would improve usefulness while remaining mostly harmless to factual behavior.

**What happened**  
On domain OOD, evidence uptake was 1.000 but unsupported leakage was **0.857**.

**Why it failed**  
The policy treated relevance to the user as a proxy for evidentiary authority.

**What changed**  
Relevance and evidence standing became separate decisions.

---

## 2. A fixed firewall solved leakage by creating evidence starvation

**What we expected**  
Blocking personal memory from the evidence path would be a safe default.

**What happened**  
Leakage became 0.000, but evidence uptake also became **0.000**.

**Why it failed**  
The architecture could not distinguish unsupported user belief from legitimate current personal-state or tool evidence.

**What changed**  
The project moved from trusted/untrusted memory to task-conditioned standing.

---

## 3. Pure learned routing looked solved on ID and failed under composition

**What we expected**  
A three-head learned router that reached perfect ordinary held-out accuracy would transfer to structured combinations.

**What happened**  
ID exact match was **1.000**, while compositional exact match fell to **0.400** and domain-OOD leakage was **0.143**.

**Why it failed**  
The learned decision surface captured regularities in the training distribution but did not reliably enforce validity under structured shift.

**What changed**  
Hybrid PLP added three small auditable gates rather than increasing model capacity.

---

## 4. Standard held-out evaluation hid provenance shortcuts

**What we expected**  
Removing provenance cues should obviously degrade the ordinary benchmark if the model truly needed source information.

**What happened**  
The no-provenance variant remained deceptively strong on some ordinary splits because task/scope/content correlations still carried signal. On the matched intervention, it dropped to **0.500**.

**Why it failed**  
The benchmark contained correlated cues that allowed a model to infer the decision without observing provenance directly.

**What changed**  
A matched provenance intervention now holds everything fixed except source provenance and is required in the canonical paper pipeline.

---

## 5. Self-reported policy traits made evaluation circular

**What we expected**  
Exposing latent “quality” traits from a policy would make behavior diagnostics easier to instrument.

**What happened**  
The evaluator could partially inherit the policy's own claim that it was truthful or calibrated.

**Why it failed**  
The measurement was no longer independent of the system being measured.

**What changed**  
The response evaluator now receives response text and scenario metadata, not the policy's self-reported quality score.

---

## 6. Random row splits overstated a local reward-model diagnostic

**What we expected**  
A standard random row split would be sufficient for the synthetic reward-model diagnostic.

**What happened**  
Near-duplicate profile variants of the same scenario could leak across train and test.

**Why it failed**  
The split unit was smaller than the semantic scenario unit.

**What changed**  
Reward diagnostics use grouped scenario splits. This remains a local synthetic diagnostic and is not presented as human generalization evidence.

## What is intentionally *not* listed as a failure

The 784-example post-training mixture has **not** been used to claim a model improvement. No PPO/DPO/SFT result is invented here. The next training intervention is still an external experiment.
