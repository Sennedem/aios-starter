---
name: offer-design
description: Turn a project and a target segment into a priced, stacked, named offer with the risk reversed, using the method from Alex Hormozi's $100M Offers (Value Equation, offer stack, value-based pricing, guarantees, real scarcity and urgency, MAGIC naming). Use when the user is launching, repricing, productizing or repositioning something they sell, or says "design an offer", "what should I charge", "price this", "package my service", "free vs paid tier", "/offer-design".
---

# /offer-design: offer builder

Turn "I have a thing to sell" into a concrete offer: the right segment, a value-scored promise, a stacked list of deliverables, a price justified by value, a guarantee that removes the risk, and a name. The method comes from Alex Hormozi's *$100M Offers*.

**Draft-first.** The offer is a draft for the user's approval. Nothing is logged as a project's live offer, sent or published until they say so. All customer-facing copy (names, guarantee wording, the offer one-pager) goes through the `writing` skill.

This is the design layer. It feeds `sales-engine` (the funnel and the sales call that sell it).

## Step 0: Load context
Read, in this order:
1. `references/value-equation.md` and `references/pricing-and-guarantees.md`: the mechanics. Apply them; do not paraphrase from memory.
2. `references/learnings.md`: the user's corrections on how they want offers built. Overrides the defaults on conflict.
3. The project's brain files: `brain/projects/<slug>/CONTEXT.md`, plus any pricing or offer notes in that folder.
4. If pricing or segment data is thin, say so and offer to research it first (a `researcher` subagent, or numbers the user already has). Never invent willingness-to-pay numbers.

## Step 1: Frame the job
Ask only for what the context does not already answer:
- **Project and segment:** which project, and the "starving crowd" inside it: who has the sharpest pain and the means to pay today.
- **Job:** a new offer, a reprice, productizing (free to paid tiers), or a repositioning.
- **B2B or B2C:** it changes the pricing psychology and how `sales-engine` closes it.
- **Constraints:** a free proof case first? a hard price floor? a platform already chosen?

## Step 2: Score the offer on the Value Equation
Value = (Dream Outcome × Perceived Likelihood of Achievement) ÷ (Time Delay × Effort and Sacrifice).
Score the current offer (or the raw idea) on all four terms (`references/value-equation.md`), name the weakest term and fix that first, since it is the cheapest lever. Most offers are weak on Perceived Likelihood (no proof) or Time Delay (too slow), not on the dream. State the diagnosis in one line before building.

## Step 3: Build the offer stack
List every obstacle between the buyer and the outcome, turn each into a deliverable, give each a defensible standalone value (anchored on real competitor pricing, never made up), prune anything high in delivery effort and low in perceived value, and present the stack so the total value dwarfs the price. For productized plays, split it into a free tier (the wedge) and a paid tier (the core transformation) and say what lives in each and why.

## Step 4: Price, guarantee, scarcity
- **Price by value,** not by cost or by the hour. Anchor high and justify with the stack.
- **Reverse the risk** with a guarantee the user can actually honor (unconditional, conditional or outcome-based; see `references/pricing-and-guarantees.md`). For a seller with little proof it is often the biggest conversion lever.
- **Add scarcity and urgency only when real:** a capped cohort, a founding price that really closes. Never a fake countdown.

## Step 5: Name it (MAGIC)
Generate 3 to 5 names (Magnetic, Aspirational, Graphic, Identity-tied, Catchy) and rank them. Naming copy goes through `writing`.

## Step 6: Sanity-check the economics
Before presenting, a back-of-envelope check: rough gross margin, delivery cost and time, and payback (how many sales clear the effort). If the price cannot survive a basic unit-economics look, raise the value or cut the deliverable; do not quietly discount. Say so if a real financial model is needed.

## Step 7: Deliver and capture feedback
- Present the offer as a one-page draft: segment, value diagnosis, stack, price, guarantee, scarcity, name.
- **Every offer names one customer-side outcome metric:** hours saved per week, extra paying customers, a grade gained. That is the number the customer judges the offer by, distinct from the price. If none can be named, the promise is too vague: go back to Step 2.
- Offer one next step: "tighten the stack", "push the price", or "draft the funnel in `/sales-engine`". Before a price or stack becomes the live offer, also offer in one line to put it to `/jury` first. It runs only on the user's yes.
- On approval, write the offer to `brain/projects/<slug>/offer-<segment>-<YYYY-MM>.md`, append a line with the why to `brain/decisions/log.md` if it sets direction, and update the project's `CONTEXT.md` if the live offer changed.
- **Capture corrections.** When the user reacts ("too cheap", "lead with the guarantee"), append an entry to `references/learnings.md` before the turn ends. Wording corrections also go to the `writing` skill's `references/learnings.md`.

## Guardrails
- Draft-first. Never publish a price, name or guarantee, or log it as the live offer, without the user's OK.
- Every value or price anchor traces to real data or a stated assumption. No invented numbers, no "studies show".
- Check `brain/context/priorities.md` and flag an offer that asks for more time than the project's status warrants.

## References
- `references/value-equation.md`: Value Equation, Grand Slam Offer, building and refining the stack, one worked example.
- `references/pricing-and-guarantees.md`: pricing, guarantees, scarcity and urgency, bonuses, MAGIC naming, free to paid tiers.
- `references/learnings.md`: the user's offer-design corrections. Read every time.
