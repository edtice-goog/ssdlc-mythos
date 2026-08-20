# AI Roles in the Architecture

**Status:** Draft
**Purpose:** Companion document for Deck 5 in the SSDLC in the Mythos Era series. Reads the four-deck
series and corrects the conclusion that AI is a single thing with a single home in the pipeline.
Three placements, three accountability boundaries.

---

## Why This Deck Exists

The four-deck series develops a framework without ever asking where AI sits in it. A reader who
finishes the series with the late-stage deep-analysis role in mind has drawn the most available
conclusion and the wrong one.

AI's role is not uniform across the pipeline. The stage-cost gradient, the property requirements, and
the calibration loop each justify a different placement, and each placement comes with a different
accountability boundary. Confusing them is how organizations over-trust AI in roles it cannot bear, or
waste it in roles where it would compose well.

## The Principle

Three simultaneous placements, not three steps in a maturity model.

1. **Deep analysis** — release-candidate cadence. Frontier models, multi-agent harnesses, exhaustive
   analysis.
2. **Continuous oversight** — across the calibration loop. Watches for conditions that should trigger
   human review.
3. **Contextual triage** — post-merge and PR stages. Uses accumulated enrichment as context for triage
   decisions.

An organization can and should run all three at once. They are justified by different arguments, they
cost different things, and none of them is decision authority.

## Deep Analysis

Expensive on all three criteria, and placed accordingly: hours to days of elapsed time, high compute and
tokens, and substantial overhead in triage, integration, and calibration.

The placement principle puts deep analysis at release-candidate cadence. It does not belong at PR
cadence or in the inner loop — not because it cannot run there, but because its costs do not fit any
earlier stage's budget pair.

**Why this only works with inward enrichment flow.** Without it, late-stage cost stays late-stage cost
forever: one bite at the apple per release candidate. With it, expensive analysis pays for itself
across every subsequent earlier-stage run, because its findings become cheap lookups upstream.

Two honest caveats. Non-determinism is the operator's engineering problem, not the vendor's to wave
away. And containment of the model against its own runtime is a real design decision that has to be
made deliberately rather than deferred.

## Continuous Oversight

Here non-determinism is a feature rather than a bug, because the conditions worth surfacing are the
ones nobody wrote a rule for.

The portfolio loop carries the periodic-revisit obligations the architecture accumulates. Most of them
fire on conditions, not on a schedule. A human-only oversight model misses them by definition — a
human reviewer attends to one part of the architecture at a time, on the cadence calibration sets, and
anything that becomes visible between scheduled reviews is invisible.

**AI surfaces, humans decide.** The calibration call is human. The AI's role is to flag conditions
worth a human look — including the call to do nothing.

**Traceability, not reproducibility.** What did the model see, what made it flag, what did the human
decide. Bit-for-bit reproducibility is the wrong bar for oversight, and pursuing it fights the tool.

**Continuous cadence, periodic review.** Continuous AI observation lets periodic human review be
triggered by signal rather than by schedule. Same pattern as inward enrichment: pay once, benefit
continuously.

The selection criterion that matters most here is signal quality at the recommendation surface —
precision balanced with explanatory value. A precise but uninterpretable signal is worse than a
noisier but explainable one, because the second can be argued with and the first can only be obeyed or
ignored.

`07-agentic-oversight.md` develops this role in full.

## Contextual Triage

The asymmetry is context, not intelligence. AI does not reason better than human triagers. It can hold
the entire enrichment database in working context, and a human cannot.

**Example: a fuzzer crash.** A human triager knows the library is widely used. An AI triager also
knows, in the same operation: the library was attributed as a memory-safe wrapper around an unsafe
core; this entry point was verified reachable from external input last quarter; a similar finding was
triaged as an upstream duplicate six weeks ago.

Two architectural requirements follow.

**Cite the enrichment used.** A triage decision that names its inputs is auditable, contestable, and
distinguishable from a coin flip. One that does not is a verdict without a record.

**Triage decisions become enrichment.** Which earlier enrichments turned out to be operationally
load-bearing is exactly the signal the calibration loop needs, and it is produced for free as a
by-product of triage.

Human triage authority on production-affecting findings does not change. The information feeding the
decision changes.

## Boundaries

What AI is not doing, and what still needs human accountability.

**Not replacing the backbone.** Coverity, Black Duck, signing, and pen testing remain the system of
record.

**Not making calibration decisions.** Continuous oversight surfaces signal. Humans decide what to recalibrate and
when — especially the call to *not* recalibrate when signal is present but disruptive.

**Not eliminating triage authority.** Findings affecting production stay with the human triager who
can be held accountable for the outcome.

Three things stay human without qualification: tool selection, which trades off organizational
concerns AI has no visibility into; calibration decisions; and sandbox-escape governance, meaning
containment, breach response, and reporting obligations.

## Carrying Forward

The three roles are placements justified by the same framework the four-deck series develops. They are
not exhaustive. The durable claim is the principle — AI's role decomposes into placements with
distinct accountability boundaries — not the specific inventory of three.

Three claims for the calibration loop to test:

1. **Does the deep-analysis / contextual-triage split hold as latency drops?** If frontier-model latency falls by
   an order of magnitude, contextual triage may begin to overlap with deep analysis at the release-candidate
   boundary.
2. **Does continuous oversight produce useful signal, or degrade to ignored noise?** If the latter,
   either the tool, the cadence, or the human integration is wrong. All three are recoverable; none
   without measurement.
3. **Does triage attribution produce the compounding-value loop?** The claim is testable. If it does
   not hold, the architectural emphasis on attribution is doing less work than expected.
