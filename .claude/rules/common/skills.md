# Skills: learn from corrections, keep proven scripts

> Companion to [verification.md](verification.md) (check before claiming done) and [agents.md](agents.md) (an authored recipe outranks a brief). This rule is about what happens after a run: the skill must come out of it better.

## A correction is a bug report against the skill, not against the run

When the user corrects a result ("wrong tone", "you skipped X", "not this format again"), fixing the output is half the job. Before the turn ends, decide which of four things was wrong and patch it in the smallest durable place:

| The cause was | Patch goes in |
|---|---|
| The process (a step missing, wrong order, wrong gate) | the skill's `SKILL.md` |
| Missing context (voice, examples, a fact about the project) | a reference file under the skill (`references/...`) or the brain page it should have read |
| A repeat mistake (second time the same thing) | an explicit rule line in the skill, or `references/learnings.md` with the date and the correction |
| Unreliable code (a script that guesses differently each run) | the script itself, under the skill's `scripts/` |

Then rerun the same task and confirm the fix holds. When the output comes from an agent or model (drafts, lint verdicts, builds), one clean rerun proves little: runs vary, and a fix can hold once while a different case breaks. Rerun at least 3 times, or against a saved set of known cases, before calling it fixed. A correction that lives only in the chat is lost when the session closes. Every skill keeps a `references/learnings.md`; a skill without one gets one at its first correction.

Escalation follows [agents.md](agents.md): a rule that has failed three or more times stops being prose and becomes a check, a script or a schema.

## A script that worked is a tool for the skill's future self

When a run produces a script whose result the user liked (a renderer, a converter, a checker, a parser), do not leave it in the conversation to be reinvented:

1. Save it under that skill's `scripts/` folder with a one-line header saying what it does and when it was proven.
2. Point `SKILL.md` at it: "run `scripts/<name>` for step N" instead of "write a script that...".
3. Rerun the skill once and confirm it calls the saved file.

Regenerating code spends tokens on a solved problem, and a fresh guess can differ from run to run, so the output stops being consistent. On the next run the model's job is the new content, not the plumbing.

A script that serves several skills lives at `scripts/<area>/` in the repo root, and every skill that uses it names the path.

## Descriptions decide whether a skill exists

Claude sees only each skill's `name` and `description` until one matches; a skill it cannot find is a skill the user does not have. A description states what the skill does and the words a person would use to ask for it, one job per skill, and never competes with another skill for the same request. The three-prompt test for any new or edited description: an obvious request triggers it, a differently worded request still triggers it, and an unrelated request does not. Collisions across the skill set are checked by `/audit`.
