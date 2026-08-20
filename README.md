# SSDLC in the Mythos Era

Working notes and reference artifacts for rethinking a Secure Software Development
Lifecycle (SSDLC) around current frontier-model capabilities — blending traditional
Application Security Testing (SAST, SCA, penetration testing; Coverity and Black Duck
as the reference deterministic backbone) with defensive use of frontier models.

The through-line: **the rigor floor has risen.** Attacker attention used to be a scarce
resource that quietly subsidized everyone's SSDLC. Frontier capability — autonomous
exploit-chain construction with automated proof generation at scale — has removed that
subsidy. The tools will keep changing; the process discipline is the invariant.

## Contents

**Anchor documents**

- [`ssdlc-thesis.md`](ssdlc-thesis.md) — the thesis and supporting argument: why the floor
  rose, the two-loop model, the eight-phase reference frame, the collapsing cost of the
  heavyweight phases, brownfield adaptation, and the open questions carried into implementation.
- [`mythos-briefing.md`](mythos-briefing.md) — shared factual baseline on Claude Mythos and
  Project Glasswing that anchors the design decisions.

**The deck series (companion documents)**

One document per deck, `NN-*.md` matching `NN-*.pptx`.

- [`00-reading-the-series.md`](00-reading-the-series.md) — the meta-guide: what each deck
  does and when to open it.
- [`01-classification.md`](01-classification.md) — the classification practice: exposure and
  project shape, six illustrative vectors on each axis, and re-classification triggers.
- [`02-placement.md`](02-placement.md) — the stage-cost gradient and placing each control at
  the earliest stage whose elapsed-time and resource budgets it fits.
- [`03-tool-properties.md`](03-tool-properties.md) — the feedback architecture (findings out,
  enrichments in) and the interface properties a tool must satisfy to participate in it.
- [`04-tool-selection.md`](04-tool-selection.md) — matching products to the upstream
  specification; the two selection profiles and multi-vendor reconciliation.
- [`05-ai-roles.md`](05-ai-roles.md) — three simultaneous placements for AI (deep analysis,
  continuous oversight, contextual triage) and the boundary on each.
- [`06-economics.md`](06-economics.md) — the two cost components (generation cost down,
  response cost up) and the strategy that follows.
- [`07-agentic-oversight.md`](07-agentic-oversight.md) — the oversight role for agentic AI
  and the traceable handoff to human decision-making.

**Presentation build**

- [`build-merged-deck.py`](build-merged-deck.py) — assembles `ssdlc-mythos-full.pptx` from the
  individual decks, dropping Tool Selection for runtime and renumbering every footer. Edit the
  `PLAN` list and re-run to cut slides; numbering follows automatically.

## Status

Draft working material. The durable claims (the floor has risen; the two loops; deterministic
backbone with AI augmentation on top) are meant to be stable across tool generations. The
tactical specifics (which tools, which autonomy levels, which integration points) are expected
to drift and should be revisited on the quarterly calibration cadence.
