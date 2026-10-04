# Novelty & SOTA Audit

**Project:** Personalized, Not Persuaded  
**Paper title:** *Personalized, Not Persuaded: Learning When Personal Context Counts as Evidence*  
**Author:** Aura Yavary

## Verdict

### Is the broad problem novel?
No.

Personalization-induced sycophancy, factual distortion, query-conditioned personal memory, provenance-aware long-term memory, source-aware retrieval, and resist-vs-update behavior are all active research areas with strong recent work.

### Is the current project still research-interesting?
Yes, **if it is positioned narrowly**.

The strongest remaining contribution is not "provenance-aware personalization." It is **evidentiary standing**: learning and evaluating the task-conditioned permission of a personal-context item to influence three different behavioral channels.

### Is it empirically SOTA today?
No defensible claim yet.

The repository has strong controlled results, causal matched interventions, OOD tests, calibration analysis, failure mining, and an eval-to-training loop. It does not yet contain independent human labels or head-to-head end-to-end generations from frontier/open models against the strongest comparable methods. Therefore it should be described as **SOTA-aligned / frontier-relevant**, not as proven state of the art.

## Why the old claim was too broad

The following nearby directions already exist:

- factuality-preserving personalized steering;
- empirical work showing memory/personalization can increase sycophancy;
- query-conditioned personal memory with provenance and temporal validity;
- provenance-aware long-term memory and citation locks;
- provenance-aware memory invalidation;
- causal resist/update contracts separating pressure from evidence.

That means "personalization + provenance + factuality" is not enough to support novelty.

## Sharpened research gap

A personal agent may retrieve a context item correctly and still use it incorrectly.

Retrieval asks:

> Is this context relevant?

Provenance asks:

> Where did it come from?

Evidentiary standing asks:

> **What is this context allowed to change for this task?**

The project assigns separate standing for:

1. presentation;
2. personalization / decision policy;
3. epistemic answer.

The same item can have different standing across tasks. This separates *relevance*, *trust*, and *permitted influence* rather than collapsing them into one score.

## Nearest-work boundary

See `docs/CLOSEST_WORK_MATRIX.md` for the explicit comparison. The closest conceptual competitor is *Resist and Update*. The project's intended distinction is that the unit of analysis is persistent personal context—memories, preferences, user assertions, connected-tool outputs, inferred state, and third-party content—and the target is a task-conditioned standing vector across multiple behavioral channels.

QUMem, MemORAI, Agent Zero Memory, Veracium, and related systems substantially narrow the novelty available on the memory side: provenance-aware, typed, temporal, and query-conditioned memory is already a competitive area. The project therefore should not present its memory representation as the novelty.

## Evidence in the current repository

The repository contains:

- 4,800 signal-level ProvenanceBench examples;
- a separate 400-pair / 800-example matched provenance intervention;
- ID, domain-OOD, compositional, and conflict tests;
- learned three-head routing;
- hybrid validity gates;
- evidence-uptake vs unsupported-leakage decomposition;
- calibration and multi-seed analysis;
- failure-to-training-data loop and research gates.

The paired intervention is the strongest piece of causal evidence because surface text and task variables are held fixed while provenance changes.

## Defensible claim

Use this:

> **We formulate persistent personal context as an evidentiary-standing problem: a user-context signal can be relevant to presentation or personalized decision-making without being licensed to change the epistemic answer. We learn separate standing across presentation, personalization, and evidence channels, and evaluate both unsupported influence leakage and evidence starvation under matched interventions and distribution shift.**

Do not use these:

- "first provenance-aware personalized agent";
- "first personalization method that preserves factuality";
- "first counterfactual evidence contract";
- "state-of-the-art personalization method";
- "solves sycophancy".

## What would justify SOTA language later

A stronger empirical claim requires:

1. real-model generations across several model families;
2. independent human evaluation;
3. direct FPPS-style and Resist-and-Update-style baselines;
4. naturalistic long-context memory/tool traces;
5. robustness to provenance spoofing and conflicting trusted sources;
6. end-to-end evidence that the learned standing interface improves generation, not only routing.

Until those are run, the strongest accurate description is:

> **A novel, frontier-aligned formulation and controlled evaluation framework for task-conditioned evidentiary standing in personalized agents.**
