# Tool Selection

**Status:** Draft
**Purpose:** Companion document for Deck 4 in the SSDLC in the Mythos Era series. Picks specific
tools against the upstream specification. The most replaceable decision in the sequence — by design.

---

## Why This Deck Exists

Tool selection is where most SSDLC conversations start, and starting there is the failure. This deck
exists to put the decision back in its place: last, downstream of three other decisions, and
deliberately easy to redo.

The design intent is reversibility. Specific tools turn over; the specification they answered to
should not. An organization that can change tools without re-deriving its requirements has bought
itself the ability to track a moving marketplace. An organization that cannot has bought a vendor
relationship and called it an architecture.

## The Principle

Selection is downstream. The hard work was upstream.

If selection is the first real decision the team makes, the resulting toolset will be wrong for
reasons unrelated to the tools. The selection conversation produces good answers only when there is
something to argue against, and classification, placement, and property requirements are that
something.

**The diagnostic.** If the selection meeting cannot answer *which required control does this tool
implement, at which stage, against which property requirements* — the upstream work was skipped. Stop
and go back. Tool comparison without the specification is a vendor demo, not a decision.

## Selection Inputs

Three artifacts feed the procurement conversation.

1. **From classification** — the set of controls required for this application, given its exposure and
   its shape.
2. **From placement** — for each required control, the stage it runs at and the elapsed-time and resource
   budget it must fit.
3. **From tool properties** — the interface requirements any candidate must satisfy to participate in
   the feedback architecture.

Selection is matching products to this specification. The specification was the work; the matching is
mechanics.

## Two Selection Profiles

Backbone and augmentation get picked on different criteria, and the most common procurement error is
applying one set to the other.

**Deterministic backbone — the system of record.** Judged on auditability, reproducibility,
regulatory recognition, stability across versions, and vendor longevity. These tools are the ground
truth against which everything else is calibrated, and the qualities that make them boring are the
qualities that make them load-bearing.

**AI augmentation — the force multiplier.** Judged on yield per dollar at the placed stage,
integration with the backbone, quality of attributed enrichment, calibration cost over time, and the
clarity of its non-determinism boundaries.

Selecting AI augmentation against backbone criteria yields tools that audit well and find nothing new.
Selecting backbone against augmentation criteria yields exciting demos and no system of record.

## Multi-Vendor Reconciliation

Real pipelines have multiple tools per stage. Selection has to address reconciliation rather than
assume it away — two tools that each find the right things still produce a broken pipeline if their
findings cannot be reconciled.

**Which findings does each tool own?** Decided up front. Overlap is fine; ambiguity about authority is
not.

**How are disagreements resolved?** Either by a named arbiter, by deterministic precedence, or by
surfacing the conflict to a human. All three are valid. Silence is not.

**How does reconciliation appear in audit trails?** Which tool said what, when, with what attribution,
and how the conflict was settled. This is the system-of-record layer doing its job.

## Selection as a Calibration Target

Every upstream decision drifts. Classification shifts as applications evolve. Placement shifts as cost
curves change. Property requirements evolve as the marketplace matures. Selection has to drift with
them, which makes it a standing item for the portfolio loop rather than a project that completes.

The calibration-loop questions for selection:

- Are the tools still implementing the controls classification requires, or have requirements drifted
  past them?
- Are tools still placed at stages whose budgets they fit, or have cost curves moved them?
- Do the tools still meet property requirements, or has the bar risen as the ecosystem matured?
- Which findings are best produced by which tool now — has the answer changed since the last review?

## The Full Sequence

Each upstream decision constrains the next. Each is independently re-runnable.

1. **Classification** — what are we protecting, and what shape is the project.
2. **Placement** — where does each required control run.
3. **Tool Properties** — what attributes do tools need to participate.
4. **Tool Selection** — which specific products fit the specification, today.

Tools change. Process discipline does not.
