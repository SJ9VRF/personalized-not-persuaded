# Personalized, Not Persuaded

**Why personal AI needs an evidence firewall that is smarter than a firewall**  
**Aura Yavary**

A personal assistant should remember that you like concise answers. It should remember that your flight is tomorrow. It may remember that you strongly believe a company is dishonest. Those three memories are all personal context — but they should not have the same power over the model.

That is the core idea behind **Personalized, Not Persuaded**.

The difficult part of personalization is not simply learning more about a user. The difficult part is deciding **how each piece of user context is allowed to influence the system**.

A style preference should change presentation. A goal can change what the assistant prioritizes. A tool-verified calendar event can be legitimate evidence about the user's schedule. But an unsupported remembered belief should not quietly become evidence about the external world.

I call this distinction **Provenance-Licensed Personalization (PLP)**.

PLP asks three separate questions for every user-context signal:

1. May this change presentation?
2. May this change personalization or planning?
3. May this change the evidentiary state of the answer?

The answer depends on the signal's scope, provenance, confidence, currentness, and the task being performed.

A naive personalized system has a dangerous failure mode: because a statement is explicit and personal, it can feel authoritative. In the controlled benchmark in this project, the naive policy accepts all useful licensed evidence, but also leaks unsupported context into evidentiary decisions. A fixed firewall solves the leakage problem by blocking too much — it also starves the system of legitimate personal or verified evidence. PLP separates these two failure modes.

The project is intentionally built as an auditable research testbed. It contains behavior scenarios, paired counterfactual contracts, provenance tests, long-horizon stress measurements, failure mining, ablations, reward-model diagnostics, a real-model adapter, and a human-evaluation protocol.

The current PLP implementation is deterministic. That is a feature for this stage of the work: the licensing behavior can be inspected line-by-line and the benchmark can test whether the formulation itself is coherent. It is not the final research destination. The next step is to learn the licensing policy from data and evaluate it on external models under a frozen benchmark.

The larger thesis is simple:

> Personal context should have **permissioned influence**.

A good personal AI should know you well enough to adapt — and know enough about evidence to avoid being persuaded merely because a belief came from you.
