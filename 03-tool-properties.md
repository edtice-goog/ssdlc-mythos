# Tool Properties

**Status:** Draft
**Purpose:** Companion document for Deck 3 in the SSDLC in the Mythos Era series. Specifies what a
tool must do to fit the architecture, before any specific tool is named. The upstream specification
that procurement decisions answer to.

---

## Why This Deck Exists

This is the decision before tool selection, and the one most often skipped. When it is skipped, the
tool conversation has nothing to argue against, and it collapses into whichever demo was most
compelling.

The properties are also the durable half of the tooling question. Specific tools turn over — vendors
merge, products get deprecated, capability shifts. The specification a tool has to satisfy does not
turn over at the same rate. Writing it down is what makes the selection decision reversible.

## The Principle

Tools have to be participants, not islands.

A tool that finds problems but cannot publish what it learned, cannot consume what other tools
learned, and cannot be reconciled with the rest of the pipeline is a standalone analyzer. Standalone
analyzers do not compose into an SSDLC. They produce findings that a human has to carry between
systems by hand, which is exactly the cost the architecture is trying to remove.

Properties describe what the interface has to do. Implementation is vendor territory.

Explicitly out of scope for this deck: how enrichment freshness is managed, how conflicting attributed
sources reconcile, which trust mechanisms attribution chains use. These are real questions. Vendors
will differentiate on them and consumers will pick on them, but they sit one layer below the interface
described here.

## The Feedback Architecture

Findings flow outward. Enrichments flow inward.

**Findings flow outward** — later stages catch what earlier ones missed. This direction is the one
every pipeline already has, and it is why the pipeline has stages at all.

**Enrichments flow inward** — later-stage findings become cheap lookups at earlier stages. This
direction is the one most pipelines lack, and it is the one that changes the economics.

Without inward flow, expensive analysis at later stages stays expensive forever: one bite at the apple
per release candidate, every time. With it, expensive analysis pays for itself once and every
subsequent stage benefits at near-zero cost. This is the mechanism by which controls migrate leftward
across the stage-cost gradient as cost curves shift — not because the analysis got cheaper, but
because its result became a lookup.

## Property Categories

Interface requirements, not implementation specs.

**Interoperability.** Produces structured findings. Consumes attributed enrichment. Integrates with
the deterministic backbone rather than running beside it.

**Attribution.** Emits findings with source, version, confidence, and inputs. Supports coexistence of
multiple attributed sources for the same artifact, because real pipelines have more than one tool with
an opinion about the same code.

**Cadence fit.** Elapsed time and resource cost that match the stage's budget pair from the placement
decision. A tool that cannot meet the budget of the stage it is placed at will be disabled in
practice, and a disabled control is worse than none.

**Determinism boundary.** Deterministic where the role requires it. For AI-augmented controls,
non-determinism is bounded and auditable rather than denied. The requirement is not that the tool
behave deterministically; it is that the tool be honest about where it does not.

**Verifiability.** Attribution chains can be verified, not just consumed. Enrichment is itself a
supply chain, and a supply chain that cannot be verified is a trust assumption wearing a data
structure.

## What Enrichment Looks Like

The range matters more than any one artifact type.

**Library-level.** A dependency is identified as a GraphQL implementation with a known class of
injection patterns. Earlier stages route accordingly without rerunning the analysis.

**Code-level.** A variable is provably bounded by a physical constant. Earlier stages treat the bound
as a given rather than re-deriving it, and range checks downstream can be tightened or elided.

**Architectural.** A control flow path is verified unreachable from external input. Findings against
code on that path can be deprioritized at every earlier stage that has access to the enrichment.

Any finding any stage produces is a candidate to flow inward, at any level of the stack. The
architecture has to allow for kinds of enrichment nobody has named yet — which is an argument for a
general attribution interface rather than an enumerated set of enrichment types.

## Where Vendors Differentiate

Below the interface, the marketplace decides.

- **Freshness** — how quickly enrichments become stale, and how that staleness is signaled.
- **Conflict resolution** — when attributed sources disagree, who wins and how the decision is exposed.
- **Enrichment depth** — how rich the property vocabulary is, and how much of it is curated versus inferred.
- **Attribution trust** — signing, transparency logs, identity verification for the enrichment supply chain.
- **Coverage breadth** — what languages, frameworks, stages, and finding types each tool participates in.

The architecture says vendors must allow attribution. It does not say what attribution should mean.
That is the marketplace doing its job, and specifying it here would be the wrong kind of rigor —
freezing an answer that should stay competitive.

## What Comes Next

Properties name the interface. Selection picks the implementations. With classification, placement,
and property requirements in hand, the selection conversation finally has a specification to answer
to.
