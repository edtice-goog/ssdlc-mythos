# Classifying Before Controlling (Loose)

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

**Authorization granularity.** Once a request is authenticated, does that imply access to everything, or are there meaningful permission boundaries inside the application. This determines whether a compromised account is a full compromise or a partial one. Applications with flat authorization need application-layer controls that segmented applications can defer to permission enforcement.

**Data sensitivity.** What classes of data does the application handle. Public, business-confidential, personally identifiable, regulated, national-security-equivalent. Multiple classes typically apply; the highest one governs control selection, and the combination of classes sometimes raises the bar above any single class on its own.

**Blast radius on compromise.** What does a successful exploit let an attacker do next. Single-tenant, multi-tenant-isolated, multi-tenant-shared-state, infrastructure-control-plane, supply-chain-upstream. This vector is the one most often missing from existing frameworks, and it matters because it inverts the intuition that small applications need small controls. A small internal tool that holds infrastructure credentials has a larger blast radius than a large external product that holds only its own data.

**Integrity sensitivity.** Does incorrect output cause harm independent of any confidentiality breach. Medical dosing, financial trades, safety-critical control loops, automated decision-making at scale. Most applications score low here; the ones that score high need controls (input validation, output verification, anomaly detection on outputs) that confidentiality-focused frameworks underweight.

**Availability sensitivity.** What is the cost of the application being unavailable. Inconvenience, business disruption, safety impact, life-threatening. Controls for availability (rate limiting, DoS protection, capacity planning, graceful degradation) are different from controls for confidentiality and integrity, and they justify independent classification.

**Adversarial sophistication expected.** Who is the application likely to be attacked by. Opportunistic scanners, financially-motivated criminals, organized crime, state actors, insiders. This vector affects how much defensive depth is justified — the same controls cost the same to build but pay off differently against different attacker classes. It is also the vector most likely to shift under the threat-landscape changes that motivate this entire artifact, because capability that was previously state-actor-only is becoming broadly accessible.

## Project Shape: Illustrative Vectors

**Codebase size.** Order of magnitude. <10KLOC, 10-100K, 100K-1M, >1M, >10M. The cost and cadence of every control scales non-linearly across these, and the same control regime that is sustainable for one size is paralyzing at another.

**Language memory safety.** Memory-safe, memory-unsafe, mixed. Drives whether sanitizer infrastructure, fuzzing, and exploit-mitigation compiler flags are table stakes or optional. Also drives the false-positive rate of AI-augmented analysis, which the Mythos briefing noted is materially higher for C/C++.

**Dependency surface.** Count and depth of third-party dependencies, and whether the dependency tree includes native code. SCA tooling load scales with this, and the modern attack surface increasingly lives upstream rather than first-party — a project with a small first-party codebase and a large dependency tree has a larger effective attack surface than its line count suggests.

**Deployment model.** Single binary, containerized service, serverless functions, mobile application, embedded firmware, on-premise appliance. Drives what release-phase controls are even possible (signing, attestation, update mechanism) and how much of the security posture can be enforced at deploy time versus how much has to be embedded in the artifact itself.

**Update cadence achievable.** Can the project ship a patch in hours, days, weeks, or quarters. This is partly a deployment-model consequence and partly an organizational one, but it has to be classified honestly because patch latency is the dominant risk variable in the current threat landscape. An embedded device with a quarterly update window needs fundamentally different controls than a SaaS that can ship in an hour — not because the bugs are different but because the time between disclosure and weaponization is shrinking.

**Change velocity.** Commits per day, deploys per week. High-velocity projects need controls in the inner loop (pre-commit, pre-merge) because anything that runs only at release cadence is bypassed by definition. Low-velocity projects have more room for batch-cadence controls but less margin for slow remediation.

**Team security maturity.** Does the team have anyone with security background, do they have security review as a habit, is there a security function they can escalate to. This drives how much of the SSDLC has to be tool-enforced versus process-enforced. Process-enforced controls work when the team has the muscle memory; tool-enforced controls work when it doesn't.

**Operational ownership.** Does the team that builds the application also run it, or is there a handoff to a separate operations function. Handoff models change which controls have to be embedded in the artifact versus which can live in the operating environment, and they change who owns the runtime-phase responsibilities. Applications that hand off to operators need controls and documentation that self-operated applications can leave implicit.

## Re-Classification

Classification is not a one-time exercise. Applications drift, especially on data sensitivity (data classes accumulate quietly), network reachability (internal tools get exposed for partner integrations), and blast radius (small services accumulate trust relationships). The calibration loop should re-examine the classification on a defined cadence and on triggering events — major feature additions, dependency-tree changes, organizational restructuring.

Drift on the project-shape axis is slower but also matters: codebases grow past size thresholds, language mixes change, deploy cadences shift. The classifier earns its keep by being re-runnable, not by being right once at kickoff.
