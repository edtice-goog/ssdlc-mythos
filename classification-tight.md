# Classifying Before Controlling (Tight)

**Status:** Draft for comparison
**Purpose:** Illustrative section for the greenfield SSDLC artifact. Names the classification practice that precedes any control decisions.

---

## The Principle

Before deciding what controls an SSDLC needs, classify what you're protecting and what you're protecting it with. Two axes:

- **Exposure** — what an attacker can reach, and what they get if they succeed.
- **Project shape** — what the SSDLC has to operate against.

This is not new. Practitioners with judgment already do this implicitly every time they make a control decision. The value of making it explicit is twofold: it becomes a shared artifact that the calibration loop can revisit when the threat landscape shifts, and it surfaces the reasoning so that disagreements between practitioners can be argued about the inputs rather than the conclusions.

We are not proposing a framework, a scoring system, or a derivation rule from classification to control set. That is the job of practitioners, and good ones will produce different answers in different contexts. We are naming the practice and illustrating what the axes look like when made explicit.

## Why Two Axes

Exposure drives *which controls are mandatory and how aggressive they need to be*. An anonymous-internet-reachable application handling regulated data needs controls a single-tenant internal tool does not, regardless of how either is built.

Project shape drives *how those controls are implemented and sequenced*. A 50KLOC service in a memory-safe language with daily deploys can adopt controls a 2MLOC C++ codebase with quarterly releases cannot, regardless of what either holds.

Collapsing the two produces wrong answers in both directions. High-exposure projects with constrained shape get controls they can't operate; low-exposure projects with permissive shape get controls they don't need. Keeping the axes separate lets the reasoning stay visible.

## Exposure: Illustrative Vectors

**Network reachability.** Is the application reachable from the public internet, from a partner network, from an internal network, or air-gapped. This drives the baseline assumption about who can attempt to interact with it at all, and the controls that follow — DDoS protection, edge filtering, network-level authentication — only make sense once this is established.

**Authentication to reach.** Can anyone interact with the application, or is some identity assertion required first. Anonymous, registration-only, verified-identity, federated-with-employer-IdP, hardware-token-required. The thing being measured is who can be on the other side of the request, which determines whether application-layer controls are defending against the world or against a known population.

**Data sensitivity.** What classes of data does the application handle. Public, business-confidential, personally identifiable, regulated, national-security-equivalent. Multiple classes typically apply; the highest one governs control selection, and the *combination* of classes sometimes raises the bar above any single class on its own.

**Blast radius on compromise.** What does a successful exploit let an attacker do next. Single-tenant, multi-tenant-isolated, multi-tenant-shared-state, infrastructure-control-plane, supply-chain-upstream. This vector is the one most often missing from existing frameworks, and it matters because it inverts the intuition that small applications need small controls. A small internal tool that holds infrastructure credentials has a larger blast radius than a large external product that holds only its own data.

## Project Shape: Illustrative Vectors

**Codebase size.** Order of magnitude. <10KLOC, 10-100K, 100K-1M, >1M. The cost and cadence of every control scales non-linearly across these, and the same control regime that is sustainable for one size is paralyzing at another.

**Language memory safety.** Memory-safe, memory-unsafe, mixed. Drives whether sanitizer infrastructure, fuzzing, and exploit-mitigation compiler flags are table stakes or optional. Also drives the false-positive rate of AI-augmented analysis, which the Mythos briefing noted is materially higher for C/C++.

**Update cadence achievable.** Can the project ship a patch in hours, days, weeks, or quarters. This is partly a deployment-model consequence and partly an organizational one, but it has to be classified honestly because patch latency is the dominant risk variable in the current threat landscape. An embedded device with a quarterly update window needs fundamentally different controls than a SaaS that can ship in an hour — not because the bugs are different but because the time between disclosure and weaponization is shrinking.

**Team security maturity.** Does the team have anyone with security background, do they have security review as a habit, is there a security function they can escalate to. This drives how much of the SSDLC has to be tool-enforced versus process-enforced. Process-enforced controls work when the team has the muscle memory; tool-enforced controls work when it doesn't.

## Re-Classification

Classification is not a one-time exercise. Applications drift, especially on data sensitivity (data classes accumulate quietly), network reachability (internal tools get exposed for partner integrations), and blast radius (small services accumulate trust relationships). The calibration loop should re-examine the classification on a defined cadence and on triggering events — major feature additions, dependency-tree changes, organizational restructuring.

Drift on the project-shape axis is slower but also matters: codebases grow past size thresholds, language mixes change, deploy cadences shift. The classifier earns its keep by being re-runnable, not by being right once at kickoff.
