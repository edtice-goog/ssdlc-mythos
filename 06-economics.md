# The Two Cost Components

**Status:** Draft
<!-- deck: number=06 | label=Economics | subtitle=Generation cost down. Response cost up. Two mandates, not one. | blurb=Names the economic structure so the security function can be funded against a clear frame. -->

**Purpose:** Companion document for Deck 6 in the SSDLC in the Mythos Era series. Names the economic structure of the new environment so the CISO can have the conversation that follows.

---

## Why This Deck Exists

Frontier models are driving down the cost of producing software. Engineering organizations are already moving to capture that — the savings are real, the tools are available, and the competitive pressure to adopt is not waiting on anyone's permission.

The same capability class is driving up the cost of defending software. Adversaries get the same tools. The economic argument the thesis deck makes — that the rigor floor has risen — translates into a cost line that did not exist at this magnitude a year ago.

This deck names the two components and the strategy that follows from them. It does not motivate the threat picture (the thesis deck does that) and it does not specify the implementation (the rest of the series does that). It names the economic structure so that the security function can be funded and operated against a clear frame, rather than against the implicit frame of "hold the line at previous spend."

## The Cost Components
<!-- slide: eyebrow=THE COMPONENTS | headline=Two cost components. They move in opposite directions. -->

There are two, and they move in opposite directions.

### Generation Cost
<!-- col: arrow=down | icon=x-circle | style=plain -->

- **More code per developer-hour.** AI-assisted development produces working code faster, with less
  human time per unit of output.
- **Adoption is competitive.** Organizations that integrate these tools competently realize the
  savings. Those that do not, do not.
- **Direction is settled.** Capture is uneven across teams and codebases, but the trajectory is not
  in doubt and is not waiting on anyone.

### Response Cost
<!-- col: arrow=up | icon=user-shield | style=accent -->

- **Higher finding volume.** Discovery yield scales with offensive capability. Triage queues grow.
  Reachability and enrichment work expands.
- **Tighter patch latency.** The gap between disclosure and weaponization is shrinking. Response
  windows that were quarters become days.
- **Disclosure-wave capacity.** Published findings arrive in surges, not steadily. Defensive capacity
  must absorb them or fall behind.

## The Strategy
<!-- slide: eyebrow=THE STRATEGY | headline=Two mandates, owned by two different functions. -->

The two components are not coupled. Capturing more generation savings does not lower response cost.
Spending more on response does not capture more generation savings. They are independent forces
acting on the same P&L.


### The Two Mandates
<!-- col: icon=people | style=plain -->

- **Engineering captures.** What engineering already does — adopt the tools, integrate them into the
  development loop, reinvest the gains. No new mandate, just recognition of one half of the strategy.
- **Security operates efficiently.** Not suppressing response cost; the threat landscape sets the
  floor. Not slowing adoption; that forfeits savings without changing the threat.

### Two Ways It Fails
<!-- col: icon=x-circle | style=accent -->

- **Treating the two as opposed.** Funding one at the expense of the other, or letting security become
  the brake on adoption rather than the discipline that makes adoption survivable.
- **Treating response cost as suppressible by spending.** Without the discipline, additional spend
  accelerates noise rather than reducing risk.

Efficient operation means which controls run where, which findings get which level of attention, where
the deterministic backbone owns the work, and how the calibration loops keep defensive spend pointed at
the right targets. The rest of the series specifies what that looks like in practice.

## The Division of Labor

Each function has its lever, and neither can pull the other's.

Engineering cannot suppress response cost from inside the development loop. The disciplines that bound response cost — classification, placement, calibration, traceable agents, deterministic backbone — operate on findings, controls, and architectural decisions that engineering does not own end-to-end. Engineering can support these disciplines but cannot substitute for them.

Security cannot capture generation savings by adding more controls. Controls do not produce code. The savings come from engineering's adoption of generation tools and from the productivity those tools unlock; security's role with respect to that adoption is to make it survivable, not to mediate it.

Both levers have to be pulled. An organization that captures generation savings without bounding response cost growth ends up with a security function that cannot keep pace and a cost structure that looks favorable until the first disclosure wave it cannot absorb. An organization that bounds response cost growth without capturing generation savings ends up cost-disadvantaged relative to peers and unable to justify the investment in the discipline that made it safe. Neither posture is durable.

The deck closes here because the rest follows. How engineering captures is engineering's question. How security operates efficiently is what the rest of the series specifies. The economic structure is the frame that lets both functions be funded against the same strategy.
