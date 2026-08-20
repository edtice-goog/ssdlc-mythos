# Classifying Before Controlling

**Status:** Draft
**Purpose:** Companion document for Deck 1 in the SSDLC in the Mythos Era series. Names the
classification practice that precedes every other SSDLC decision, and illustrates what the two
axes look like when they are made explicit.

---

## Why This Deck Exists

Control decisions get made whether or not anyone writes down what is being protected. Practitioners
with judgment already classify implicitly every time they choose a control. The value of making the
step explicit is twofold: it becomes a shared artifact the calibration loop can revisit when the
threat landscape shifts, and it surfaces the reasoning so that disagreement between practitioners is
argued about the inputs rather than the conclusions.

This deck does not propose a framework, a scoring system, or a derivation rule from classification to
control set. That is the job of practitioners, and good ones will produce different answers in
different contexts. It names the practice and illustrates the axes.

## The Principle

Before deciding what controls an SSDLC needs, classify what you are protecting and what you are
protecting it with. Two axes:

- **Exposure** — what an attacker can reach, and what they get if they succeed. Drives which
  controls are mandatory and how aggressive they need to be.
- **Project shape** — what the SSDLC has to operate against. Drives how those controls are
  implemented and sequenced.

Collapsing the two produces wrong answers in both directions. Keep them separate so the reasoning
stays visible.

## Exposure: Illustrative Vectors

Illustrative, not exhaustive. The vectors that matter in your context are the ones to make explicit.

**Network reachability.** Is the application reachable from the public internet, from a partner
network, from an internal network, or air-gapped. This drives the baseline assumption about who can
attempt to interact with it at all, and the controls that follow — DDoS protection, edge filtering,
network-level authentication — only make sense once this is established.

**Authentication to reach.** Can anyone interact with the application, or is some identity assertion
required first. Anonymous, registration-only, verified-identity, federated-with-employer-IdP,
hardware-token-required. The thing being measured is who can be on the other side of the request,
which determines whether application-layer controls are defending against the world or against a
known population.

**Authorization granularity.** Once a request is authenticated, does that imply access to everything,
or are there meaningful permission boundaries inside the application. This determines whether a
compromised account is a full compromise or a partial one. Applications with flat authorization need
application-layer controls that segmented applications can defer to permission enforcement.

**Data sensitivity.** What classes of data does the application handle. Public,
business-confidential, personally identifiable, regulated, national-security-equivalent. Multiple
classes typically apply; the highest one governs control selection, and the *combination* of classes
often matters more than the highest single class on its own.

**Blast radius on compromise.** What does a successful exploit let an attacker do next.
Single-tenant, multi-tenant-isolated, multi-tenant-shared-state, infrastructure-control-plane,
supply-chain-upstream. This vector is the one most often missing from existing frameworks, and it
matters because it inverts the intuition that small applications need small controls. A small
internal tool that holds infrastructure credentials has a larger blast radius than a large external
product that holds only its own data.

**Adversarial sophistication expected.** Who is the application likely to be attacked by.
Opportunistic scanners, financially-motivated criminals, organized crime, state actors, insiders.
This affects how much defensive depth is justified — the same controls cost the same to build but pay
off differently against different attacker classes. It is also the vector most likely to shift under
the threat-landscape change that motivates this entire series, because capability that was previously
state-actor-only is becoming broadly accessible.

## Project Shape: Illustrative Vectors

Shape constrains what classification can actually implement. Honesty on these vectors is part of the
discipline.

**Codebase size.** Order of magnitude. <10KLOC, 10-100K, 100K-1M, >1M. The cost and cadence of every
control scales non-linearly across these, and the same control regime that is sustainable at one size
is paralyzing at another.

**Language memory safety.** Memory-safe, memory-unsafe, mixed. Drives whether sanitizer
infrastructure, fuzzing, and exploit-mitigation compiler flags are table stakes or optional. Also
drives the false-positive rate of AI-augmented analysis, which the Mythos briefing noted is
materially higher for C/C++.

**Dependency surface.** Count and depth of third-party dependencies, and whether the dependency tree
includes native code. SCA tooling load scales with this, and the modern attack surface increasingly
lives upstream rather than first-party — a project with a small first-party codebase and a large
dependency tree has a larger effective attack surface than its line count suggests.

**Update cadence achievable.** Can the project ship a patch in hours, days, weeks, or quarters. This
is partly a deployment-model consequence and partly an organizational one, but it has to be
classified honestly because patch latency is the dominant risk variable in the current threat
landscape. An embedded device with a quarterly update window needs fundamentally different controls
than a SaaS that can ship in an hour — not because the bugs are different but because the time
between disclosure and weaponization is shrinking.

**Change velocity.** Commits per day, deploys per week. High-velocity projects need controls in the
inner loop (pre-commit, pre-merge) because anything that runs only at release cadence is bypassed by
definition. Low-velocity projects have more room for batch-cadence controls but less margin for slow
remediation.

**Team security maturity.** Does the team have anyone with security background, do they have security
review as a habit, is there a security function they can escalate to. This drives how much of the
SSDLC has to be tool-enforced versus process-enforced. Process-enforced controls work when the team
has the muscle memory; tool-enforced controls work when it does not.

## Why Two Axes

One axis produces the wrong answer twice.

**Collapsed toward exposure.** High-exposure projects with constrained shape get prescribed controls
they cannot operate. The classifier looks rigorous; the implementation is theater.

**Collapsed toward shape.** Low-exposure projects with permissive shape adopt controls they do not
need. The classifier looks pragmatic; real risks elsewhere go uncovered.

Exposure tells you what controls have to exist. Shape tells you which ones the team can actually run.
Both questions deserve to be argued before either is answered.

## Re-Classification

Classification is re-runnable, not one-time.

**Drift on the exposure axis is fast.** Data classes accumulate quietly. Internal tools get exposed
for partner integrations. Small services accumulate trust relationships and grow their blast radius.
None of these announce themselves as security events.

**Drift on the project-shape axis is slower but still matters.** Codebases cross size thresholds.
Language mixes change. Deploy cadences shift as infrastructure or team practices evolve.

**Cadence and triggers.** Re-classification runs on a defined cadence in the calibration loop, and on
triggering events: major feature additions, dependency-tree changes, organizational restructuring.
Classification that is never revisited describes the application that was, not the one that is.

## What Comes Next

Classification names *what*. Placement decides *where*. Each downstream decision constrains the next,
and each is independently re-runnable:

1. **Classification** — required controls follow from exposure and shape.
2. **Placement** — each required control runs at the stage whose elapsed-time and resource budgets it fits.
3. **Tool Properties** — what attributes tools need to operate as a feedback architecture rather than
   as standalone analyzers.
4. **Tool Selection** — pick specific products against the upstream specification.
