# Placing Controls by Stage

**Status:** Draft
**Purpose:** Illustrative section for the greenfield SSDLC artifact. Names the placement practice that follows classification.

---

## The Principle

Classification names which controls an application requires. Placement decides where each runs. Both deserve to be argued separately and explicitly.

Controls have two costs:

- **Latency cost** — wall-clock time per invocation.
- **Resource cost** — compute, tokens, or dollars per invocation.

Each SSDLC stage has a corresponding pair of budgets. A control fits a stage when both costs fit both budgets — not on average, but in the worst case the stage can tolerate. Controls that fit multiple stages should run at the earliest one whose budgets they fit, because remediation cost rises monotonically across the pipeline.

We are not proposing a derivation rule from control to stage. Practitioners produce different answers in different contexts and should. We are naming the practice.

## Stages: Illustrative Budgets

The reference frame has eight phases. From a placement perspective, several decompose further, because the budgets shift sharply between, say, a keystroke and a release candidate build. Six stages with distinct budget pairs:

**Compile and inner loop.** Sub-second latency, near-zero resource. Compiler warnings, type checking, fast lint, syntax-level security checks. Anything that breaks this latency budget is disabled in practice, and a disabled control is worse than none.

**IDE-integrated assistance.** Seconds to tens of seconds latency, modest resource per invocation but high invocation frequency. AI-suggested fixes, single-file SAST, single-file reachability hints, vulnerability warnings on dependency import.

**Pull request.** Minutes latency with a soft ceiling beyond which context-switching cost outweighs analysis value, bounded resource per PR but high cadence. Full SAST, SCA on the dependency tree, AI analysis targeted at changed surfaces, security-relevant test runs. This is the last stage where a finding can block bad code from landing without paying revert-or-followup cost, which is why pre-merge defensive depth concentrates here.

**Post-merge / continuous.** Tens of minutes to a few hours latency, higher resource amortized across many merges. Cross-procedural static analysis, broader AI agent runs, integration security tests, bounded-budget fuzzing, full transitive dependency analysis. This is where the controls that need to run on every change but cannot fit the PR budget live.

**Release candidate.** Hours to days latency, high resource at low cadence. Exhaustive fuzzing, multi-agent AI harnesses with reachability tracing (Cloudflare-style architecture sits here), pen testing on high-risk surfaces, exploit-chain reasoning across the assembled artifact, supply chain audit, signing and attestation.

**Production / runtime.** Latency bounded by user-facing requirements, resource continuous and therefore aggregate-cost-sensitive. Runtime monitoring, anomaly detection, RASP where appropriate, dependency vulnerability monitoring against running inventory, response automation. Not strictly part of the build pipeline, but its budgets are distinct enough to place separately.

## Refinements

Two recurring complications that classification alone does not resolve:

**High-variance latency.** A control whose typical latency fits a stage but whose tail does not should either be moved one stage later or split: a fast version at the earlier stage, a thorough version at the later stage acting as backstop.

**Resource-cost / cadence tradeoff.** A high-resource, high-yield control may produce more security per dollar at lower cadence at a later stage than at higher cadence at an earlier one. Classification of the application reshapes this calculation directly: high-exposure or high-blast-radius applications justify running expensive controls at higher cadence than cost alone would warrant.

## Re-Placement

Two drift sources warrant calibration-loop attention:

**Cost-curve drift.** AI inference latency and per-token cost fall continuously. Controls that fit only at release-candidate cadence today migrate to post-merge cadence and eventually pre-merge. Non-AI controls drift the same way as build infrastructure, parallelism, and incremental analysis improve. "This control could move left" is a first-class calibration finding.

**Stage-budget drift.** The budgets themselves are not fixed. Faster CI fleets, trunk-based development, or larger merge cadences shift them. So do codebase and headcount growth in the other direction. Placement, like classification, earns its keep by being re-runnable.
