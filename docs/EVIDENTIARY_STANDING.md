# Evidentiary Standing for Personal Context

**Project:** Personalized, Not Persuaded  
**Author:** Aura Yavary

## Core idea

Personal-agent context should not be treated as a single undifferentiated conditioning channel. A context item can be useful for *how* a model responds without being entitled to change *what the model treats as evidence*.

This project uses **evidentiary standing** to name that distinction.

For a context signal `c` and task `q`, define a standing vector:

```text
S(c, q) = [presentation, personalization, evidence]
```

Each component is a permission, not a confidence score:

- **presentation standing** — the signal may change wording, tone, format, or interaction style;
- **personalization standing** — the signal may change ranking, planning, recommendations, or user-specific choices;
- **evidentiary standing** — the signal may change the system's factual or personal-state conclusion.

Standing is **relational**. It depends on the current task, not only on the source type. The same memory item can have standing for one query and no standing for another.

## Why provenance alone is not enough

Provenance answers **where a signal came from**. Standing answers **what that signal is allowed to do here**.

A connected calendar event may be strong evidence for "When is my meeting?" but irrelevant to "Is this medical claim true?". A remembered preference may be decisive for restaurant ranking but carry no evidentiary standing for an external factual claim. A user's explicit correction may supersede a stale personal-state memory but should not automatically override an independently verified world fact.

The standing decision therefore conditions on:

```text
source provenance
× signal scope
× task
× relevance
× currentness
× confidence
× conflict / supersession state
```

## Dual failure modes

A useful system must avoid two symmetric errors:

1. **Unsupported influence leakage** — context without evidentiary standing changes the epistemic answer.
2. **Evidence starvation** — context with evidentiary standing is ignored.

A blanket firewall can eliminate leakage by starving the model of legitimate personal evidence. A naive personalization policy can maximize evidence uptake while letting unsupported user context contaminate factual conclusions. The research target is the region between those extremes.

## What is learned

The implementation keeps the original technical name **PLP (Provenance-Licensed Personalization)** for continuity. The learned three-head router estimates the standing vector. The hybrid variant adds auditable validity gates for stale, low-confidence, and task-irrelevant context.

This is intentionally a narrow method. It is not a new memory store, retrieval architecture, or full assistant policy.

## Falsifiable tests

The project treats the standing hypothesis as testable through matched interventions:

- hold task, content, relevance, confidence, and freshness fixed;
- change only source provenance;
- check whether evidentiary standing changes when it should;
- remove provenance and verify that performance falls toward ambiguity;
- separately measure leakage and starvation.

The current paired provenance intervention contains 400 matched pairs (800 examples). It is the cleanest test in the repository because it removes many benchmark shortcuts.

## Boundary of the claim

The project does **not** claim that it is the first provenance-aware memory system, the first factuality-preserving personalization method, or the first method to distinguish evidence from pressure. Those areas already contain strong prior work.

The defensible contribution is narrower:

> **We formulate persistent personal context as a task-conditioned standing problem: a context signal can be relevant to presentation or personalization without having evidentiary standing, and the permitted influence should be learned and evaluated under matched interventions.**

That formulation is what the paper, benchmark, failure taxonomy, and eval-to-training loop are organized around.
