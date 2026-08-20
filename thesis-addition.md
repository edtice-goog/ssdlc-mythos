# Thesis Addition: The Stage-Cost Gradient

**Intended placement:** New section in `ssdlc-thesis.md`, after "The SSDLC Reference Frame" and before "Brownfield Adaptation."

---

## The Stage-Cost Gradient

Controls have two costs that constrain placement separately:

- **Latency cost** — wall-clock time per invocation.
- **Resource cost** — compute, tokens, or dollars per invocation.

The two correlate often enough to be conflated, and the conflation is where placement decisions go wrong. A heavyweight fuzzer is cheap on tokens and expensive on wall-clock. An AI agent doing reachability analysis is expensive on both. A parallelized SAST run can be CPU-expensive and latency-bounded. The pair has to be carried separately.

Both budgets expand monotonically as a change moves through the SSDLC. The inner loop has near-zero budget on both axes because the developer pays the cost dozens of times a day. The release candidate has hours of latency budget and substantial resource budget because both are paid once per candidate. Every stage between has its own pair, and the controls that fit a stage are the ones whose costs fit both of its budgets.

This is a placement principle, not a learning principle. The two-loop model answers *what should the SSDLC learn from*. The stage-cost gradient answers *where should each control run*. Neither subsumes the other.

The gradient also dissolves the question "where does AI fit in the pipeline?" into something tractable: what is this AI-driven control's latency cost, what is its resource cost, which stage's budgets match. Single-file IDE suggestion and Cloudflare-style multi-agent harnesses are both "AI," and they belong at opposite ends of the gradient.

One consequence for the calibration loop: as inference latency and per-token cost fall, AI-driven controls migrate leftward across the gradient over time. Placement is therefore a calibration target, not a one-time architectural commitment. The durable claim is the gradient itself; the specific assignments are tactical and expected to drift.
