---
name: level-up
description: Weekly automation discovery via the Three Ms (Mindset, Method, Machine). Finds one repetitive task, scopes it, and ships one automation per run, tied to one KPI. Use weekly, when something feels manual or copy-paste, or when the user says "/level-up", "automate this", "what should I automate next", "ship one automation".
---

# /level-up: ship one automation

One run = one shipped artifact, tied to a measurable outcome. Default to the simplest thing that works.

## Phase 1: Mindset (find candidates)

1. **A fresh brief wins.** If `brain/audits/level-up-*.md` has a brief 7 days old or newer (a scheduled janitor run can write one), play its Candidate and Scope back to the user in three lines, take their yes or their swap, and go straight to Phase 3.
2. **Otherwise read the latest audit** (`brain/audits/audit-*.md`, newest). If it is 7 days old or newer, its gaps and its hand-off candidate are the starting list; do not re-discover from scratch.
3. Then ask what the audit missed: what repeats 3 or more times a week, feels copy-paste, or could be done by a smart intern, across every area in `brain/context/work.md`. Whatever the user most recently asked to have built also counts: a fresh request beats a stale gap list.
4. Surface 1 to 3 candidates ranked by leverage on `brain/context/priorities.md`.

## Phase 2: Method (scope the winner)

1. Name the constraint (what actually slows it down).
2. Apply **EAD** in order: can we **Eliminate** it? **Automate** it? **Delegate** it, first to a subagent at the right model tier (see `.claude/rules/common/agents.md`), then to a person? Test elimination first: if stopping it does no harm, that is a win, exit happily.
   - Ask explicitly: is the constraint a missing **workflow** (becomes a skill) or a missing **worker** (becomes an agent)? A task that stalls because nobody does the grind wants a worker; a task that stalls because the steps are undefined wants a workflow.
3. Map the steps.
4. Pick an autonomy level, defaulting to the lowest that works (assist, then suggest, then act-with-approval). Nothing fully autonomous without the user's explicit OK.
5. Tie it to one KPI (more customers, more value per customer, or less time or cost).

## Phase 3: Machine (build the smallest thing)

**Triage gate first.** Write the flow as numbered steps and mark each one *deterministic* or *judgment*.

- Zero judgment steps: a script (on a scheduled job such as a CI workflow, if it must run unattended). Never an agent or a routine.
- One or two judgment steps (draft, classify): a scheduled Claude routine that does only that step and hands the rest to the script.
- A loop of judgment: in-session, or a routine if it must run unattended.
- A judgment step that has to sit inside the script: a Claude API call with its own spend limit.

An agent wrapped around a flow with no judgment in it is the thing that drifts; a script cannot. For anything that wakes up repeatedly, decide before the first run what it does when its input is missing, when it fails, and how the user will know it ran.

Build in ascending complexity, stopping at the first that works:

1. A prompt or note template in `brain/templates/`.
2. A deterministic skill in `.claude/skills/`.
3. An AI-assisted skill.
4. A subagent in `.claude/agents/`, only when the same worker shape recurs across two or more skills or needs a pinned model or tool contract. One-off needs use the existing workers (`harvester`, `researcher`, general-purpose). Unused agents are clutter the audit will flag.

A dispatch retrofit also counts as a shipped artifact: adding an explicit fan-out or model-routing step to an existing skill that still grinds bulk work inline.

## Ship

- Save the artifact and verify it once on real input (`.claude/rules/common/verification.md`).
- Note the KPI it serves and append the decision to `brain/decisions/log.md` (why this, alternatives, owner).
- Realistic expectation: about 60% fully automate, 30% become AI-assisted, 10% stay manual. That is fine.
