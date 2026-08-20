# The Two Cost Components

**Status:** Draft
**Purpose:** Companion document for Deck 6 in the SSDLC in the Mythos Era series. Names the economic structure of the new environment so the CISO can have the conversation that follows.

---

## Why This Deck Exists

Frontier models are driving down the cost of producing software. Engineering organizations are already moving to capture that — the savings are real, the tools are available, and the competitive pressure to adopt is not waiting on anyone's permission.

The same capability class is driving up the cost of defending software. Adversaries get the same tools. The economic argument the thesis deck makes — that the rigor floor has risen — translates into a cost line that did not exist at this magnitude a year ago.

This deck names the two components and the strategy that follows from them. It does not motivate the threat picture (the thesis deck does that) and it does not specify the implementation (the rest of the series does that). It names the economic structure so that the security function can be funded and operated against a clear frame, rather than against the implicit frame of "hold the line at previous spend."

## The Cost Components

There are two, and they move in opposite directions.

**Generation cost is going down.** Frontier-model-assisted development produces working code faster, with less human time per unit of output. The capture is uneven across teams and codebases, but the direction is settled. Organizations that adopt these tools competently realize the savings; organizations that do not, do not. The savings are not theoretical and they are not waiting for anyone.

**Response cost is going up.** The same capability class is in offensive use. Discovery yield is higher, exploit-chain construction that used to require expert attention is increasingly automated, disclosure waves are larger and faster, and the gap between disclosure and weaponization is shrinking. Each of those produces cost on the defensive side: more findings to triage, more patches to ship under tighter latency, more reachability and enrichment work to keep prioritization honest, more capacity required to absorb disclosure surges. None of these costs are negotiable at the source. The threat landscape sets the floor.

The two components are not coupled. Capturing more generation savings does not lower response cost. Spending more on response does not capture more generation savings. They are independent forces acting on the same P&L.

## The Strategy

Two mandates, owned by two different functions.

**Engineering's mandate is to capture.** This is what engineering already does. They adopt the tools, integrate them into the development loop, measure the productivity gains, and reinvest where the leverage is highest. The deck does not ask engineering to do anything they are not already motivated to do. Naming the capture as one half of the strategy makes it visible as part of the economic frame rather than as an unrelated productivity story.

**Security's mandate is to operate efficiently under elevated response cost.** Not to suppress the cost — the threat landscape rules that out. Not to slow engineering's adoption of generation tools — that forfeits the savings without changing the threat picture, and it is not a credible posture for the function to hold. The mandate is efficient operation: which controls run where, which findings get which level of attention, where the deterministic backbone owns the work and where it does not, how the calibration loops keep defensive spend pointed at the right targets. The rest of the series specifies what that efficiency looks like in practice.

The strategy fails in two predictable ways. The first is treating engineering's capture and security's response as opposed — funding one at the expense of the other, or letting the security function become the brake on AI adoption rather than the discipline that makes adoption survivable. The second is treating response cost as suppressible through additional spending alone, without the discipline the rest of the series describes; this accelerates noise rather than reducing risk and raises response cost faster than the threat landscape would on its own.

## The Division of Labor

Each function has its lever, and neither can pull the other's.

Engineering cannot suppress response cost from inside the development loop. The disciplines that bound response cost — classification, placement, calibration, traceable agents, deterministic backbone — operate on findings, controls, and architectural decisions that engineering does not own end-to-end. Engineering can support these disciplines but cannot substitute for them.

Security cannot capture generation savings by adding more controls. Controls do not produce code. The savings come from engineering's adoption of generation tools and from the productivity those tools unlock; security's role with respect to that adoption is to make it survivable, not to mediate it.

Both levers have to be pulled. An organization that captures generation savings without bounding response cost growth ends up with a security function that cannot keep pace and a cost structure that looks favorable until the first disclosure wave it cannot absorb. An organization that bounds response cost growth without capturing generation savings ends up cost-disadvantaged relative to peers and unable to justify the investment in the discipline that made it safe. Neither posture is durable.

The deck closes here because the rest follows. How engineering captures is engineering's question. How security operates efficiently is what the rest of the series specifies. The economic structure is the frame that lets both functions be funded against the same strategy.
