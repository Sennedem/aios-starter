---
name: five-gates
description: Use proactively the moment a task has many layers, such as multiple dependent steps, load-bearing unknowns, a first theory that might be wrong, research with claims to verify, or anything needing verification before handoff. Also when a task keeps failing or stalling, or when the user says "five gates", "slow down and do this right", "think this through first" or "do this properly". Loads a five-gate working discipline (scope, evidence, self-attack, verify, calibrated report) plus the smells that show a gate was skipped, so any model applies frontier-level judgment. Not for trivial two-minute work.
---

# The five gates

The working discipline of the best sessions, written down so any model can run it. A skill file cannot transfer raw intelligence, but it can transfer how good sessions work: how they scope, gather evidence, attack their own answers, verify and report.

A hard task is anything where the first idea might be wrong: multi-step builds, research with claims in it, debugging, strategy calls, anything touching data you have not looked at yet. For a one-file edit or a quick lookup, skip the gates and do the work.

## The loop: five gates, in order

A gate must pass before the next one opens. If work stalls or a result surprises you, name the gate you are at and re-run it.

### Gate 1: scope before work

State what done looks like before touching anything.

- Define done in one or two sentences: what artifact exists at the end, what must be true of it, and how you will check that. If you cannot write the check, you do not understand the task yet.
- Check standing rules first: `CLAUDE.md`, the brain (`brain/`), the relevant skill, memory. Do not invent an approach the repo already has a rule or documented pipeline for.
- Separate known from assumed. Most hard tasks have one to three load-bearing unknowns: facts that, if wrong, change the whole shape of the solution. Name them.
- If the request is ambiguous in a way that changes what you would build, ask one question, aimed at the biggest gap. Otherwise pick the sensible default, say so in one line and proceed. Ask questions to change outcomes, not to feel safe.
- Right-size the effort. Deep reasoning belongs in planning and review, not in mechanical steps.
- Before anything that spends metered credits or money, read the documented approach and the current budget first, and confirm costly or irreversible choices with the user.

### Gate 2: evidence before reasoning

Never design from memory of what a file, API, source or dataset probably looks like. Open it.

- Files and live tool output are sources. Training memory is only a hypothesis generator.
- Attack the load-bearing unknowns first, with the cheapest probe. A 30-second read beats an hour of building on a guess.
- Prefer a thin end-to-end pass over a complete first stage: get one item through the whole pipeline and verify it before scaling to all items.
- Keep a live plan for anything with 3 or more steps. Slice by dependency, so each step's output feeds the next. The plan is a hypothesis, not a contract.

### Gate 3: attack your own answer

Reason adversarially before committing.

- Argue against your own conclusion: what would make it wrong? Who would disagree, and what is their best argument?
- Explore the unknowns in the plan, not just the steps: what could go wrong at each seam, and what is the countermove?
- Three attempts at the same fix means the theory is wrong, not the execution. Stop, go back to Gate 2 and re-derive from evidence.
- For genuinely contested calls, offer `/jury` (skeptic seats plus a cross-model second opinion).

### Gate 4: verify before declaring done

Evidence is an observation, never an intention.

- "Should work" about anything you can test right now means this gate failed. Test it.
- Run the check you wrote at Gate 1. If the deliverable is viewable, open it. If it is a claim, re-find it in the source.
- A result that comes back surprisingly clean gets a "why?" before you move on. Clean surprises are where silent failures hide.
- For metered or irreversible actions (paid generation, sends, deletes), verification happens before the action, against the documented approach and budget.

### Gate 5: calibrated reporting

Report what you know, not what you hope.

- Separate verified from inferred from skipped, explicitly.
- Flag anything you could not verify instead of rounding it up to done.
- If something went wrong, say so plainly and stay on the problem, with no grovelling and no spin.
- Confidence language matches evidence: "verified against X", "likely" and "have not found yet" are different claims. Never say "impossible" without having looked.

## Standing habits (every gate)

- Judgment over ritual: the gates are checks, not ceremony. Scripts and templates are for repetition; thinking is for the parts that are new.
- Preserve by default. When editing something that exists, touch only what the task requires; deleting substantive content needs the user's approval.
- Update curated context as you go. A hard task that ends without its brain or context update is not done.

## Smells that mean a gate got skipped

- You are building something and have not opened the real data, file or source it depends on. (Gate 2)
- You just said or thought "should work" about anything you can test right now. (Gate 4)
- You are on attempt three of the same fix. (Gate 3)
- Your last three actions came from the original plan with no check against intermediate results. (Gate 3)
- You are about to report done and the evidence is your intention, not an observation. (Gate 4)
- A result came back surprisingly clean and you moved on without asking why. (Gate 4)
- You cannot say in one sentence what done looks like. (Gate 1)

Any one of these: stop and go back to that gate.

## Notes

- This is a method skill, not a workflow. It changes how you execute the current task and has no files of its own.
- It stacks with task-specific skills (`writing`, `review-deliverable`, `second-opinion`, `jury`). Those are the tools; this is the discipline of when to reach for them.
- Do not apply it to trivial work. Forcing all five gates onto a two-minute edit is its own failure mode.
- If a task keeps failing under this discipline, escalate the model (see `.claude/rules/common/model-routing.md`) instead of loosening the process.
- A session already running on the strongest available model can skip the ritual and just work; the skill exists to port that discipline to cheaper tiers.
