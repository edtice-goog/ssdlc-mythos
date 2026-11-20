# Software Delivery After Opus 5.5: Working Prediction

**Status:** Working prediction, not final
**As of:** November 16, 2026
**Revised:** November 16, 2026 — points 6 to 8 of step 3, after the first split into separate
projects; the velocity and error-rate relation added as the opening of step 3
**Purpose:** State where software organisations that adapt to Opus 5.5 are likely to land, well
enough to decide where tooling should go. To be revised as more software gets built.

---

## What This Is

A prediction made from limited evidence, checked against the evidence already known that could
disprove it. It is not a finding. Lagging indicators will eventually confirm or refute it, and waiting
for them would mean arriving after the market has moved.

The chain has three steps. The first is observed. The second and third are inferred from it.

## Step 1: The Cost of Producing Software Fell by About Two Orders of Magnitude

**Observed.** One domain expert directing Opus 5.5 built Coverity Connect NG, a replacement for the
Coverity Connect server, in 18 days (October 29 to November 16, 2026). The git history records:

| Measure | Value |
|---|---|
| Java, production | about 39,000 lines in 213 files |
| Java, tests | about 18,300 lines, 574 tests |
| Schema migrations | 61 |
| Commits on main | 429, each with a model co-author (396 Opus 5.5, 31 Fable 5.1) |
| Releases | 14, ending at 1.0.0 |
| Reverts on main | 0 |

Basic COCOMO (effort = 2.4 × KLOC^1.05 person-months, organic mode) puts 30,000 to 39,000 lines at
85 to 112 person-months: six to eight people for a little over a year. Less favourable variants reach
about 180 person-months. Against at most 0.6 person-months actually spent, the ratio is roughly 140
to 300 on effort and about 25 on schedule.

The estimate is rough. Lines of code is a weak input when agents write the code, the model was
calibrated decades ago, and the count leaves out the frontend, the SQL and the scripts. An error of
three or four times still leaves more than an order of magnitude.

The human contribution was direction, and it was substantial: the project's status document is full
of dated design decisions and rules. The claim is that one expert with agents can do this, not that
no expert is needed.

## Step 2: Quality Becomes the Economically Rational Choice

**Inferred.** The price of quality fell further than the price of code.

For a human team, thorough tests cost a large share of the effort, paid in salaries. For agents they
cost tokens and compute. Tests are also what let agents work unattended: the test suite is the
agent's feedback signal, and without it errors return to the human, whose attention is the most
expensive input. So cutting tests to go faster is a poor trade on anything of real size.

Three pressures then select for vendors that choose quality:

- **Attackers make poor quality visible.** This is the Mythos series' argument, and it stands on its
  own.
- **Competitors can rebuild a product quickly.** "Nobody can afford to rewrite this" stops protecting
  a weak product.
- **Customers can build an adequate version themselves.** Every vendor now competes with a prompt, so
  a product has to be clearly better than what its customer could direct an agent to build.

Selection works only on quality that buyers can observe, and contracts and switching costs slow it
down. The direction is clear; the timing is not.

## Step 3: What Delivery Looks Like

A delivery process has to handle errors per unit of time: velocity multiplied by error rate. The claim
is not that errors stop. It is that when the error rate falls faster than velocity rises, the absolute
number of errors falls, and the process built to handle them can be simpler.

Before Opus 5.5 the product went up: velocity rose and the error rate did not fall enough, which is
what the 2026 delivery reports show. The prediction is that the inequality has now reversed.

Two things add to the effect. Larger units mean fewer events for the shared process to handle, even
at the same number of errors. And the cost of each remaining error depends on when it is found (point
7 below).

**Inferred**, from steps 1 and 2 together. Larger units come from step 1, because one owner can carry
more. Heavy verification inside each unit comes from step 2.

1. **Units grow.** One person with agents owns what a five- or six-person team owned.
2. **Branches arrive pre-validated.** The agent session does the work a CI pipeline used to do,
   before anything reaches a shared branch.
3. **Sequential integration works much better.** Fewer, larger, cleaner units mean far fewer
   integration failures, and little need for the machinery built to cope with them.
4. **Architecture follows application concerns.** Boundaries that existed only to make integration
   manageable dissolve. Boundaries that exist for scaling, fault isolation or blast radius remain.
5. **Seams become fewer and better defined.** Units communicate through specifications.
6. **Boundary errors remain, at the specification level, and most can be found before integration.**
   Coding errors are caught inside each unit. A consumer whose agents build against the published
   contract alone will list the places where it is ambiguous, silent or contradictory, and the owners
   settle them before any code depends on a guess.
7. **Evictions become rare, and their cost depends on when the specification problem is found.** Found
   while the consumer is still reading the contract, it costs a question and a decision. Found after
   both sides have built on different readings, the work backs up to the specification and involves
   more than one owner.
8. **Avoiding the late ones may become a market of its own.**

### Observed at the first seam

On November 16, 2026, Coverity Connect NG was split into a server, a client project and a consumer
(Code Sight NG, an IDE plugin), each allowed to work only from the others' published documents.

- The consumer built a stub of the server from the contract, not from the server's code, and recorded
  53 numbered questions: each a place where the contract was unclear, with what the stub assumes until
  answered.
- It sent twelve requirements for things the contract lacked.
- The server's design thread began correcting the contract the same day (required and nullable fields,
  real types, declared error codes), and the client project drafted three versioned schemas.
- Capability decisions were left to the human owner and came back within hours.

All three kinds of seam defect appeared, before any integration:

| Kind | Example found |
|---|---|
| Divergent readings | Triage is an array in the API specification and a single object in the API guide |
| Gaps | Almost no field was marked required or nullable; nothing said what a preview answers for a stream with no snapshot |
| Wrong specification | A field named as a SHA-256 hash held an MD5, and was renamed |

The mechanism is that the agent writes its guesses down. A person who meets an ambiguity usually picks
a reading and moves on; here each assumption was declared and sent to the owner.

## What Follows for Verification

- **Integration-time tests find little.** Each side's tests are written from the same reading of the
  specification as its code, so a test that could catch a seam defect would already have caught it
  inside the unit.
- **Whole-program static analysis keeps its value.** It needs no expectation written by either side,
  so on the integrated state it can find defects across a seam that no test encodes. This holds for
  the defect classes an analyzer models, within one program. Consolidation removes the service
  boundaries where analyzers go blind.
- **The witness should not be the author.** When the same agents write and validate, evidence that a
  change is clean needs to come from something else.

## What Tooling Has to Fit

Changes reach a shared trunk in one of three shapes. A tool that handles all three can be adapted to
most organisations.

| Shape | Notes |
|---|---|
| Queue | Serial, batched and speculative queues are one shape; they differ only in throughput |
| Partitioned lanes | Serial within a lane; cross-lane effects surface later |
| Post-land verification | Checks run after landing, with a way to find the responsible change |

A long-lived feature branch owned by one developer is a fourth case: a private trunk with one of the
three shapes inside it. Stacked pull requests are a way of presenting a large change for review, not
a separate shape.

## Where It Applies

Organisations whose pace was limited by writing and integrating code, which is most of them.

Meta is a boundary case. In 2026 it moved to pods of three to five with agents and reported far more
code change, modest growth in shipped features, and more incidents. It already ran a high-throughput
pipeline and was near the limit of what its verification could absorb, so more volume produced more
incidents whatever the team size.

## Known Evidence Against

Nothing found argues against the direction. What was found bears on extent or timing.

- **Meta's pods** show that shrinking teams without more verification fails, which step 2 expects.
- **GitHub's stacked pull requests** (July 2026) are a bet on small reviewable layers. The delivery is
  still large; only its presentation is layered.
- **Boundaries that exist for other reasons** limit how far consolidation goes.
- **Re-architecture is normally slow.** Cheap rewriting may make it faster this time. New builds and
  rewrites should show the shift first.

## Limits of the Evidence

- Step 1 rests on one project. That project is also where the hypothesis came from, so it is evidence
  for the cost change and not confirmation of step 3.
- All published delivery data found (CircleCI, Mergify, DORA commentary, Gartner) predates September
  22, 2026 or is a forecast. It describes the previous era.
- The first seam had one person behind all three projects, so decisions came back within hours.
  Between owners with competing priorities, the listing of questions should carry over; the speed of
  the answers may not.
- Nothing across that seam has been integrated yet. It shows ambiguities found from documents, not
  that none remain.
- Whether static analysis finds anything worth fixing in agent-written code is a separate question.
  Ad hoc runs on Coverity Connect NG found nothing its author would fix. That bears on where tooling
  spend should go, not on the trend.

## What Would Change It

Two kinds of observation, as more software is built:

- Integration failing more often than expected when units are large.
- Where seam defects are actually caught, and by what.

## Points of Contact With the Mythos Series

Listed for reference. The root documents are unchanged.

- **`02-placement.md`, inner-loop budget.** The sub-second inner-loop budget is a human budget. An
  agent session's elapsed-time budget is as long as its base stays still; only its resource budget
  binds.
- **`02-placement.md`, earliest-stage rule.** "Run at the earliest stage that fits" assumed fixing
  gets costlier at every stage. With an agent doing the fix, that cost is roughly flat until release.
- **`06-economics.md`.** Generation cost down and response cost up are the same two forces as step 2,
  applied to vendors instead of security budgets.
- **`ssdlc-thesis.md`, defect loop.** "Earliest stage that could have caught it" will answer
  "specification" far more often.

## Sources

- [Mergify, State of Merge Queues 2026](https://mergify.com/blog/state-of-merge-queues-2026)
- [CircleCI, five takeaways from the 2026 State of Software Delivery](https://circleci.com/blog/five-takeaways-2026-software-delivery-report)
- [CircleCI, 2026 Q2 report (PDF)](https://circleci.com/landing-pages/assets/2026-q2-state-of-software-delivery-report.pdf)
- [Thoughtworks on the CircleCI 2026 report](https://www.thoughtworks.com/en-gb/insights/blog/generative-ai/a-thoughtworks-perspective-on-circleci-s-2026-state-of-software-)
- [LeadDev, Meta tried to shrink engineering teams around AI](https://leaddev.com/ai/meta-tried-to-shrink-engineering-teams-around-ai)
- [Gartner, The future of software engineering: smaller teams](https://www.gartner.com/en/articles/software-engineering-tiny-teams)
- [GitHub Docs, Stack AI-generated code in pull requests](https://docs.github.com/en/copilot/tutorials/stack-ai-generated-code-in-pull-requests)
- [InfoQ, Rootly drops its small-PR rule](https://infoq.com/news/2026/08/rootly-small-pr-agentic-ai/)
- [Tian Pan, The merge queue is the new bottleneck](https://tianpan.co/blog/2026-07-02-the-merge-queue-is-the-new-bottleneck)
