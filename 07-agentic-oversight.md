# Agentic AI as Oversight

**Status:** Draft
**Purpose:** Companion document for Deck 7 in the SSDLC in the Mythos Era series. Names the oversight role for agentic AI in the architecture and the handoff to human decision-making that role requires.

---

## Why This Deck Exists

The rest of the series already addresses AI in the SSDLC. The two-loop model puts AI inside Loop 1 (per-finding analysis, triage, reach reasoning) and inside Loop 2 (aggregate pattern detection). Placement covers where deep-analysis AI runs and at what cadence. None of that needs to be re-argued.

What the series does not yet specify is the role of agentic AI as an oversight layer above the rest of the architecture. Continuous observation across the entire SSDLC, identification of miscalibration faster than human review cadence allows, and traceable handoff to humans who own the decision. This is a distinct role from the AI uses already named. It deserves its own treatment because the failure modes are different and the accountability boundary is different.

The deck does not extend AI's role into decision-making. It names the one role where agentic AI's particular shape — continuous, broad, capable of holding the whole architecture in working context — produces value the rest of the architecture cannot produce for itself.

## The Role

Agentic AI's place in this architecture is oversight. It watches the entire SSDLC — every phase, every loop, every reconciliation between deterministic systems, every enrichment source, every control output — for conditions that should trigger human review. It identifies miscalibration. It does not fix it.

The span is the point. A human reviewer can attend to one part of the architecture at a time and operates on a cadence the calibration loop sets. The agent attends to all of it, continuously, and the cadence is whatever the agent's compute budget allows. This is not a claim that the agent reasons better than a human. It is a claim that the agent can hold more of the architecture in working context at once and watch it for longer than a human can, and that span and continuity are exactly what the oversight role requires.

The speed is the other half of the point. Miscalibration that becomes visible between scheduled human reviews is invisible to a human-only oversight model by definition. The window between when a condition starts to drift and when it becomes harmful is shorter than the cadence at which humans can review the whole architecture. An agent operating continuously closes that window — not by acting, but by escalating earlier.

## Why Agentic Fits Oversight

Fixed monitoring catches what was anticipated. Thresholds, dashboards, scheduled audits — these find conditions that someone wrote a rule for. They are necessary and they are not in scope here; they live in the deterministic backbone.

The conditions that oversight has to catch are the ones nobody wrote a rule for. Controls that drift below their calibrated threshold for reasons specific to the current codebase. Enrichment data that becomes stale in a way that makes a previously-correct prioritization newly wrong. Reconciliation outcomes between deterministic systems that look fine in isolation but stop adding up across a quarter. Calibration loops producing recommendations that look reasonable individually but that, in aggregate, point at a problem the existing controls were not designed to surface.

These conditions cannot be pre-specified, because if they could, they would already be in the fixed monitoring layer. They are irreducibly ad hoc. Fixed processes do not catch them. Agents — capable of observing without a pre-specified rule and recognizing patterns that do not match the calibrated baseline — do.

The worked example is stale enrichment data. SCA tools tell an organization which packages have known vulnerabilities. They do not tell the organization when an upstream advisory was amended, when the maintainer disputed the classification, when exploit code became public, or when runtime configuration changed in a way that makes a previously-unreachable path now reachable. Each of those is enrichment, and each goes stale on its own timescale. No fixed rule reliably catches the staleness condition because the staleness condition is not pre-specifiable. An agent watching enrichment provenance, freshness, and consistency across the prioritization can catch it. The agent does not decide what to do about it. The agent escalates with enough context for a human to decide.

## The Handoff

What the agent produces is not a decision. It is an artifact that lets a human make a decision the human can defend.

The artifact contains the inputs the agent observed: which findings, from which systems, at which timestamps, with what enrichment freshness, from which sources, with what reconciliation history. The artifact contains the basis for the flag: what made this condition look out-of-calibration, what the agent compared it against, what the agent's confidence is. The artifact contains a recommendation: what kind of human review this condition warrants, with what urgency, and what the agent thinks the relevant options are. The artifact does not contain instructions to act, because that is not the agent's role.

The handoff is what makes the role auditable. A human reviewing the artifact can verify the inputs, evaluate the basis, accept or reject the recommendation, and document the decision. The decision is the human's, accountable in the way human decisions are accountable. The agent's contribution is making the decision possible — finding the condition, assembling the context, presenting it in a form that supports rather than substitutes for human judgment.

The bar on the artifact is traceability, not reproducibility. Reproducibility — would the agent produce the same artifact on rerun — is the wrong target. Agents are non-deterministic in security-sensitive ways; the documented behavior includes semantically equivalent inputs producing different outputs across runs. Pursuing reproducibility fights this rather than accommodating it. Traceability accommodates it: show what was seen, show what was flagged, show the basis. A human can audit that even when rerun would produce something different. An auditor can verify that the decision was not arbitrary. The calibration loop can learn from the traces in aggregate even when no individual trace is reproducible.

## What the Agent Is Not Doing

The boundary is what makes the role safe. The agent does not make calibration decisions. It surfaces conditions that may warrant recalibration; the recalibration call is human, especially the call to *not* recalibrate when signal is present but disruptive. The agent does not adjust controls. The agent does not close findings or modify their priority on its own authority. The agent does not act on production-affecting findings; those stay with the human triager who can be held accountable for the outcome.

The agent also does not replace the deterministic backbone. Coverity, Black Duck, signing infrastructure, pen testing, compiler hardening — these remain the system of record. The agent's observations are inputs to human decisions about them, not substitutes for what they produce. An organization that lets the agent override the backbone has misunderstood the role.

Sandbox-escape governance, breach response, and reporting obligations remain human accountability. The agent operates inside a containment architecture that the organization has decided is appropriate; the decision about what that containment looks like is not the agent's to make. The thesis deck flagged sandbox-escape governance as an open question, and it remains an open question that the human security function owns.

## What This Enables

With the oversight role in place and the handoff bounded as described, Loop 2 can operate at a cadence the threat landscape requires rather than the cadence human attention allows. Calibration decisions still happen at human cadence — quarterly, owned by security leadership, accountable as the thesis deck specifies. What changes is the set of conditions surfaced to that quarterly review. Instead of relying on humans to notice drift between reviews, the review starts with a queue of agent-surfaced conditions that have already been triaged for human attention, each accompanied by the trace that makes auditable decision possible.

This is the form of AI integration the rest of the series has implicitly required without specifying. Loop 2 calibration cannot operate at the cadence the current threat landscape demands using human observation alone. Agentic oversight is what closes that gap, and the boundary on its role — observation and handoff, never decision — is what keeps the closure trustworthy.

The deck closes here because the rest of the discipline is what the other decks already specify. How calibration decisions get made is in the thesis deck. Where AI fits in the placement gradient is in the placement deck. What the deterministic backbone owns is in tool properties. This deck adds one specific role to that architecture, with one specific accountability boundary, and lets everything else stay as the rest of the series argued for it.
