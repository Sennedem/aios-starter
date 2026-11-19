---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: business
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/QDsenEcAJIk
tags: [concept, business, one-person-business, automation]
related: ["[[wiki/concepts/three-filters-one-person-business]]", "[[wiki/concepts/automation-boundary-human-in-the-loop]]", "[[wiki/tools/clay]]", "[[wiki/sources/nateherk-one-person-business-claude]]", "[[wiki/techniques/golden-dataset-eval-loop]]"]
---

# The three-part one-person business architecture

The source splits what a one-person software business needs into exactly three parts. Each runs on a different piece of the stack, so one founder can operate all three without a team [04:14-04:30].

1. **The product workflow**: the work the customer pays for. In the worked example (Agent Report Card) this is the [[wiki/techniques/golden-dataset-eval-loop|golden-dataset eval loop]]: run tests against a connected support agent, diagnose the failures, produce a client report.
2. **The sales and support agent**: handles new leads (reads a trial-request submission, explains the fit, recommends a trial) and routine support (answers product-guide questions directly), while [[wiki/concepts/automation-boundary-human-in-the-loop|routing money and data actions to the human]] every time.
3. **The lead-sourcing workflow**: finds companies that fit the ideal customer profile (via [[wiki/tools/clay|Clay]]'s B2B data), has Claude check public sources and draft a personalized outreach message explaining the fit, then holds it **unsent** until the founder reviews and approves it.

## Why three parts

Each part answers a different question a one-person business has to solve at the same time: what am I selling (1), who closes and supports it without me on every call (2), and who hears about it in the first place (3). A founder who only builds part 1 has a product with no distribution. One who only automates part 2 has support without a pipeline.

The source states that all three parts are built but none of the 168 paying customers its pricing model needs exist yet. Having the architecture is a precondition for the business; it proves nothing commercially (see the skeptic note on [[wiki/sources/nateherk-one-person-business-claude|the source page]]).

Part 3 also carries a rule worth copying into any one-person business: outreach is drafted by the machine and released by a person. Nothing goes out unreviewed.

## Related

- Lead sourcing (part 3) ranks #5 in [[wiki/sources/nateherk-ai-businesses-ranked|Nate's later ranking]] (T4 / M3 / D5). It is the most durable of the build-type services, because leads are the clearest KPI and a retainer is sticky, but he warns you must crack lead generation for your own business first. That supports owning part 3 in-house.
- [[wiki/sources/nateherk-4-claude-systems-that-sell|4 Claude Systems That Sell]] shows the same jobs sold to clients instead of run internally. The [[wiki/concepts/intake-and-follow-up-funnel-system|intake funnel]] packages part 2 with the lead flow of part 3, and the [[wiki/concepts/creator-os-system|creator OS]] is the content half of part 3. Same creator, services framing; neither transcript shows customer data.

## In this system

`/sales-engine` plans the funnel (parts 2 and 3). `/outreach` is a draft-first lead workflow with the same unsent gate.
