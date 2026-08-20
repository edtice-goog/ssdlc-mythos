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
  rose, the two-loop model, the eight-phase reference frame, brownfield adaptation, and the
  open questions carried into implementation.
- [`mythos-briefing.md`](mythos-briefing.md) — shared factual baseline on Claude Mythos and
  Project Glasswing that anchors the design decisions.

**The deck series (companion documents)**

- [`00-reading-the-series.md`](00-reading-the-series.md) — the meta-guide: what each deck
  does and when to open it.
- [`06-economics.md`](06-economics.md) — the two cost components (generation cost down,
  response cost up) and the strategy that follows.
- [`07-agentic-oversight.md`](07-agentic-oversight.md) — the oversight role for agentic AI
  and the traceable handoff to human decision-making.

**Greenfield sections (illustrative, in progress)**

- [`classification-tight.md`](classification-tight.md) / [`classification-loose.md`](classification-loose.md)
  — two drafts of the classification practice (exposure × project shape), a tighter and a
  more expansive set of vectors, kept side by side for comparison.
- [`placement.md`](placement.md) — placing controls along the stage-cost gradient.
- [`thesis-addition.md`](thesis-addition.md) — the stage-cost gradient section intended for
  insertion into `ssdlc-thesis.md`.

## Status

Draft working material. The durable claims (the floor has risen; the two loops; deterministic
backbone with AI augmentation on top) are meant to be stable across tool generations. The
tactical specifics (which tools, which autonomy levels, which integration points) are expected
to drift and should be revisited on the quarterly calibration cadence.
