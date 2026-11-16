---
name: sales-engine
description: Get, close and keep customers for a project. Funnel mode picks channels in a fixed order (leak audit first, then warm, direct, content, paid) with pre-committed kill/scale gates and the jobs Claude runs; call mode scripts the sales call with CLOSER plus an objection bank (MEDDPICC overlay for B2B); keep mode runs a retention audit (churn by cohort, first-weeks fixes, win-back, upgrades). Use when the user asks "how do I get customers", "where do my customers come from", "why do they leave", "how do I keep them", wants a lead funnel, channel plan, sales-call script, objection handling or a retention plan, or says "/sales-engine".
---

# /sales-engine: get, close and keep customers

Three jobs: get the lead (funnel mode), close the lead (call mode), keep the customer (keep mode). Built on Alex Hormozi's *$100M Leads* and the CLOSER sales framework.

**B2C-first.** Everything stands on its own for consumer sales. For a B2B deal, add the MEDDPICC overlay in `references/closer-and-objections.md`: it is the qualification layer on top of CLOSER, not the spine.

**Draft-first.** Funnels, scripts and sequences are drafts for the user's approval. This skill never sends a message or makes a call; the user does, after review. All copy goes through the `writing` skill.

Pairs with `/offer-design`: an offer should exist, or be sketched, before you build the funnel that sells it. If there is none, say so and offer to run `/offer-design` first.

## Step 0: Load context
1. `references/core-four-and-funnel.md` and `references/closer-and-objections.md`: the mechanics. Funnel mode also reads `references/acquisition-plays.md`; keep mode reads `references/retention.md`.
2. `references/learnings.md`: the user's corrections. Overrides the defaults on conflict.
3. The project's brain files: `brain/projects/<slug>/CONTEXT.md`, plus any channel map, funnel or call-script notes in that folder. Update an existing channel list; never start a parallel one.
4. Note B2B or B2C up front. It decides whether the MEDDPICC overlay loads.

## Step 1: Pick the mode (ask only if unclear)
- **Funnel mode:** "I need leads", "a channel plan", "a launch funnel". Go to Step 2A.
- **Call mode:** "I have a call", "I need a script", "how do I handle this objection". Go to Step 2B.
- **Keep mode:** "why do they leave", "how do I keep them", "upsell", "win them back". Go to Step 2C.
- Often several in a row: design the funnel, script the call it feeds, then the retention it hands over to.

## Step 2A: Funnel mode
0. **Leak audit first** (`references/acquisition-plays.md`, "The order"): measure speed to first answer, test the capture path end to end yourself, check the follow-ups happen. Report the leaks with their fixes before proposing any new channel; most "we need more leads" problems are leads lost on the way in.
1. **Core Four audit.** Of warm outreach, cold outreach, content and paid ads, which does the user run and which is the underused one? Name the highest-leverage next channel for this project and segment. Default bias: warm, local and referral before cold or paid.
2. **Map the funnel:** awareness, capture, nurture, convert. Name the lead magnet, the capture point, the nurture sequence and the conversion step.
3. **Set tripwire gates.** Every experiment gets a metric, a bar, a date and a decision before it starts (`references/core-four-and-funnel.md`).
4. **Pick plays** from `references/acquisition-plays.md` for the business type, in its order. For each, name Claude's job and the user's job, the contact lane (phone, e-mail, DM), and the expected time to a first customer. Check the cold-contact rules for the buyer's country before any cold send. Paid only when CAC is below a third of LTV on real numbers.
5. **Hand off:** the offer it converts to goes to `/offer-design`; the drafts go through `writing`; the user sends. This skill produces the plan and the gates, not the sends.

## Step 2B: Call mode (CLOSER)
1. Build the call as a CLOSER arc: Clarify, Label, Overview, Sell, Explain, Reinforce (`references/closer-and-objections.md`). Produce an actual script with rough timings, not just the acronym.
   For a B2B prospect, the first Clarify question is whether the business is demand-constrained or supply-constrained: "if twice as many customers called tomorrow, could you serve them?" If yes, their limit is demand, so pitch something that brings in or converts leads. If no, their limit is capacity, so pitch something that frees hours. Then put one number on it: hours × people saved, or extra sales × price. (A practitioner heuristic; test it on real calls.)
2. **B2B overlay:** fold MEDDPICC discovery questions into the CLOSER beats. For B2C, run CLOSER alone.
3. **Objection bank:** pull the matching objections from `references/closer-and-objections.md` and tailor the answers. Each answer validates first, then reframes with proof.
4. Close consultatively: show the gap and offer to help, never a hard sell. Keep the call to action low-friction.

## Step 2C: Keep mode (retention)
1. **Count it** per named cohort from live data (the user's customer list, CRM or payment records): started, still paying, left, when, stop reason. At small numbers, name people, not percentages.
2. **Find the moment** people leave and match one tactic from `references/retention.md` to it.
3. Each tactic gets a tripwire line. Claude keeps the ledger and flags the dated moments; the user sends.

## Step 3: Deliver and capture feedback
- Present the funnel with its gates, the call script or the retention plan as a draft. Offer one next step: "draft the first-touch messages", "build the lead magnet", "script the objection answers". When a channel bet would commit real money or weeks of work, also offer in one line to put it to `/jury` first. It runs only on the user's yes.
- On approval, write the plan to `brain/projects/<slug>/` (for example `funnel-<YYYY-MM>.md` or `sales-script-<segment>.md`), put the tripwire dates where they will be checked (the project `CONTEXT.md`, or `cadence.md` for a recurring review), and log a direction-setting decision in `brain/decisions/log.md` with the why.
- **Capture corrections.** When the user reacts ("warm-first for this one", "that answer is too defensive", "the gate should be replies, not views"), append an entry to `references/learnings.md` before the turn ends. Wording corrections also go to the `writing` skill's `references/learnings.md`.

## Guardrails
- Draft-first. This skill never sends or calls.
- B2C stays free of MEDDPICC; load the overlay only for real B2B deals.
- Tripwire gates are mandatory for any "let's test this channel" plan. An experiment without a pre-set metric, bar and date is what this skill exists to prevent.
- Every claim or statistic in a script or lead magnet must be real and sourceable. Never invent proof.

## References
- `references/acquisition-plays.md`: the order (leaks, warm, direct, compounding, paid), plays per business type, Claude's jobs, the never-list. Funnel mode.
- `references/core-four-and-funnel.md`: Core Four, lead magnets, funnel design, tripwire gates. Step 0.
- `references/closer-and-objections.md`: CLOSER, the MEDDPICC overlay, the objection bank. Step 0.
- `references/retention.md`: the retention audit, tactics, expansion. Keep mode.
- `references/learnings.md`: the user's sales corrections. Read every time.
