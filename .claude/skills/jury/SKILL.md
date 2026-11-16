---
name: jury
description: Put one decision the user faces in front of a jury of parallel agents. Seats are a skeptic, a fact-checker, a buyer and one or two lens seats (cash and risk, will they pay, time cost, leverage, legal), with an outside model as an optional extra skeptic. It forces a dissenter when the vote is unanimous, adds an optional rebuttal round, and ends in exactly green-light / reshape / kill plus the cheapest ~48h test. Use when the user says "/jury", "jury this", "put this to the jury", "roast this decision", "should I do X or Y", "go or no-go", "stress-test this decision", or says yes when another skill offers a jury. Not for interviewing the user to get facts out of their head (grill-me), not for reviewing one finished artifact (second-opinion, review-deliverable).
---

# /jury: a decision, attacked from several sides, ending in a verdict

A jury runs when the user asks for one. Left as a rule that fires "when Claude judges a call contested", it almost never fires, so it is a command instead. Personas and celebrity voices are left out on purpose: several personas on one model share the same errors, so the seats are lenses with one question each.

## Step 0: frame the decision (main session)

1. Write the decision in one line, plus 2 or 3 options. Always include the do-nothing or wait option, even if the user did not name it.
2. Read the context first: the project's `brain/projects/<slug>/CONTEXT.md`, the relevant entries in `brain/decisions/log.md`, `brain/context/priorities.md`, and live sources for any number. Every price, wage or count in the brief is read live at framing time and cited `[live, <url or source>, <date>]`. Never copy a number from a CONTEXT line; context notes go stale, and a juror reasoning from a wrong number votes on it.
3. Name the load-bearing facts. If one is missing and only the user knows it, ask at most 3 questions in one batch. If more than 3 are missing, stop and recommend `/grill-me` first. A jury on missing facts argues over guesses.
4. Decidability check. If the fact that decides it will not exist until later (real usage numbers, a pending quote, next term's schedule), stop with the verdict "not decidable yet", plus what to measure, by when, and the date to rerun. Do not convene.
5. Write the brief to `brain/brainstorms/<YYYY-MM-DD>-jury-<slug>.md` with frontmatter `type: note`, `domain: meta`, `parent: "[[brainstorms/README|Brainstorms]]"`, `updated:`. It holds the decision, options, the facts with their sources, and the open unknowns. Jurors read this file; the brief is the only context they get.

## Step 1: seat the jury

Always seated:
- Skeptic. Builds the strongest case that the leading option is wrong, and names the alternative the user would regret skipping. Runs on the session model.
- Fact-checker. Re-finds every load-bearing claim in the brief at its source (file, live site, web). It reports each one as seen, inferred or unknown, and never confirms from a search query that contains the hypothesis.
- Buyer, when the decision touches customers. It role-plays the person who pays and answers whether they would actually pay or use this, and what would stop them.

Plus 1 or 2 lens seats picked for this decision. Each gets exactly one question:

| Lens | The one question |
|---|---|
| Cash and risk | What does it do to cash, what is the worst case, and how reversible is it? |
| Will they pay | Who pays, how much, and how does the sale close? |
| Time cost | How many hours a week does it take from the user, and does it still run while they are busy or away? |
| Leverage | Does it build an asset the user owns, or rent out their time? |
| Legal and compliance | Does it fit the user's legal situation: contracts, privacy law, employment rules, licences, residence or work status? |
| Opportunity cost | What in `brain/context/priorities.md` does this push out? |
| Brand and taste | Does it fit the brand, and would the user be proud to show it? |

Outside skeptic (optional). Seat it by default when money or anything hard to reverse is involved, if the user has an outside model available. Run it exactly as `.claude/skills/second-opinion/SKILL.md` prescribes, with the decision/plan lens. If no outside model is set up, or it is capped, run without it and say so.

Cap: at most 5 Claude seats plus the outside skeptic. Show the seating to the user in one line before dispatch. If they asked for the run, do not wait; they can still edit seats mid-run.

## Step 2: round 1, independent positions (parallel)

Dispatch every seat in one message: Claude seats as `general-purpose` agents, the outside model via its own call. Every juror brief contains:
- the brief file path, its one question, and the instruction that it may read files and the web;
- Return exactly (12 lines at most): vote (go / reshape / kill), confidence 1 to 5, the single strongest reason, the biggest risk it sees, what evidence would flip its vote, and each factual claim tagged seen / inferred / unknown;
- What good looks like: a position a smart outsider would find specific to the user's situation (their numbers, their constraints, their time). Generic advice that fits any founder fails this bar.

## Step 3: forced dissent

If every vote is the same, ask the skeptic (or a fresh agent if the skeptic agreed strongly) to argue the opposite vote as hard as it honestly can, in 10 lines at most. Unanimity without a stress test is how a confident wrong call gets through.

## Step 4: round 2, rebuttal (optional)

Run it only when the votes split and the stakes are high (money, months of work, or something hard to undo), or when the user asks. Each juror gets the others' round-1 returns and answers in 6 lines at most: which point changed its mind, which it rejects and why, and its final vote. One round only. This doubles the agent cost, so skip it when round 1 already agrees on the substance.

## Step 5: adjudicate (main session, never delegated)

1. Per juror, one line: agree / reject / investigate, with the why. Never silently drop a point.
2. Disagreements are the headline, especially the outside model against the Claude seats. Do not average them away.
3. Close with exactly:
   - Verdict: green-light / reshape / kill
   - Why: one line
   - Cheapest ~48h test: one action against reality that would confirm or kill this verdict. It is chosen against the final verdict, never a new idea borrowed from the dissent seat, and never manual fulfilment work for the user; their effort is at most one message or one look at a number.
   - What would flip it: one line
4. Append the round-1 returns, the dissent, any rebuttals and the verdict block to the brief file.

## Step 6: after the user decides

- On their decision, append it with the why to `brain/decisions/log.md` and update the project's `CONTEXT.md` if it changes direction.
- Never act on a verdict without the user's go. The jury advises; it does not execute.
- Corrections go to `references/learnings.md` in this folder, dated, as Rule / Why / Before → After.

## Where the jury is offered (one line, never auto-run)

`/grill-me` (end of session, when a decision surfaced), `/offer-design` (before a price or stack is final), `/sales-engine` (before a channel bet is final). The user says yes and it runs; otherwise nothing happens.
