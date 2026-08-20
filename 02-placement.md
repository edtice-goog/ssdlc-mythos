# Placing Controls by Stage

**Status:** Draft
**Purpose:** Companion document for Deck 2 in the SSDLC in the Mythos Era series. Names the placement
practice that follows classification, and the stage-cost gradient the practice runs on.

---

## The Principle

Classification names which controls an application requires. Placement decides where each runs. Both deserve to be argued separately and explicitly.

Controls have two costs:

- **Elapsed time** — wall-clock time per invocation.
- **Resource cost** — compute, tokens, or dollars per invocation.

Each SSDLC stage has a corresponding pair of budgets. A control fits a stage when both costs fit both budgets — not on average, but in the worst case the stage can tolerate. Controls that fit multiple stages should run at the earliest one whose budgets they fit, because remediation cost rises monotonically across the pipeline.

We are not proposing a derivation rule from control to stage. Practitioners produce different answers in different contexts and should. We are naming the practice.

## The Stage-Cost Gradient

The two costs correlate often enough to be conflated, and the conflation is where placement decisions
go wrong. A heavyweight fuzzer is cheap on tokens and expensive on wall-clock. An AI agent doing
reachability analysis is expensive on both. A parallelized SAST run can be CPU-expensive yet
quick in elapsed time. The pair has to be carried separately.

Both budgets expand monotonically as a change moves through the SSDLC. The inner loop has near-zero
budget on both axes because the developer pays the cost dozens of times a day. The release candidate
has hours of elapsed-time budget and substantial resource budget because both are paid once per candidate.
Every stage between has its own pair, and only controls whose costs fit both can live there.

This is a placement principle, not a learning principle. The two-loop model answers *what should the
SSDLC learn from*. The stage-cost gradient answers *where should each control run*. Neither subsumes
the other.

The gradient also dissolves the question "where does AI fit in the pipeline?" into something
tractable: how much elapsed time does this AI-driven control take, what is its resource cost, which stage's
budgets match. Single-file IDE suggestion and Cloudflare-style multi-agent harnesses are both "AI,"
and they belong at opposite ends of the gradient.

One consequence for the calibration loop: as inference latency and per-token cost fall, AI-driven
controls migrate leftward across the gradient over time. Placement is therefore a calibration target,
not a one-time architectural commitment. The durable claim is the gradient itself; the specific
assignments are tactical and expected to drift.

## Stages: Illustrative Budgets

The reference frame has eight phases. From a placement perspective, several decompose further, because the budgets shift sharply between, say, a keystroke and a release candidate build. Six stages with distinct budget pairs:

**Compile and inner loop.** Sub-second elapsed time, near-zero resource. Compiler warnings, type checking, fast lint, syntax-level security checks. Anything that breaks this elapsed-time budget is disabled in practice, and a disabled control is worse than none.

**IDE-integrated assistance.** Seconds to tens of seconds elapsed, modest resource per invocation but high invocation frequency. AI-suggested fixes, single-file SAST, single-file reachability hints, vulnerability warnings on dependency import.

**Pull request.** Minutes of elapsed time, with a soft ceiling beyond which context-switching cost outweighs analysis value, bounded resource per PR but high cadence. Full SAST, SCA on the dependency tree, AI analysis targeted at changed surfaces, security-relevant test runs. This is the last stage where a finding can block bad code from landing without paying revert-or-followup cost, which is why pre-merge defensive depth concentrates here.

**Post-merge / continuous.** Tens of minutes to a few hours elapsed, higher resource amortized across many merges. Cross-procedural static analysis, broader AI agent runs, integration security tests, bounded-budget fuzzing, full transitive dependency analysis. This is where the controls that need to run on every change but cannot fit the PR budget live.

**Release candidate.** Hours to days elapsed, high resource at low cadence. Exhaustive fuzzing, multi-agent AI harnesses with reachability tracing (Cloudflare-style architecture sits here), pen testing on high-risk surfaces, exploit-chain reasoning across the assembled artifact, supply chain audit, signing and attestation.

**Production / runtime.** Elapsed time bounded by user-facing requirements, resource continuous and therefore aggregate-cost-sensitive. Runtime monitoring, anomaly detection, RASP where appropriate, dependency vulnerability monitoring against running inventory, response automation. Not strictly part of the build pipeline, but its budgets are distinct enough to place separately.

## Refinements

Two recurring complications that classification alone does not resolve:

**High-variance elapsed time.** A control whose typical elapsed time fits a stage but whose tail does not should either be moved one stage later or split: a fast version at the earlier stage, a thorough version at the later stage acting as backstop.

**Resource-cost / cadence tradeoff.** A high-resource, high-yield control may produce more security per dollar at lower cadence at a later stage than at higher cadence at an earlier one. Classification of the application reshapes this calculation directly: high-exposure or high-blast-radius applications justify running expensive controls at higher cadence than cost alone would warrant.

## Re-Placement

Two drift sources warrant calibration-loop attention:

**Cost-curve drift.** AI inference latency and per-token cost fall continuously. Controls that fit only at release-candidate cadence today migrate to post-merge cadence and eventually pre-merge. Non-AI controls drift the same way as build infrastructure, parallelism, and incremental analysis improve. "This control could move left" is a first-class calibration finding.

**Stage-budget drift.** The budgets themselves are not fixed. Faster CI fleets, trunk-based development, or larger merge cadences shift them. So do codebase and headcount growth in the other direction. Placement, like classification, earns its keep by being re-runnable.
