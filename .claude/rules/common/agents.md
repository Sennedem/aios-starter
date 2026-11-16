# Agent orchestration

## Delegate by default, route by model

Any bulk read, browser grind or independent research leg goes to a subagent, in parallel when the legs are independent. The main session keeps synthesis, routing and decisions. Two reasons: usage (grunt work on Haiku or Sonnet burns the subscription window far slower than the main model) and speed (parallel legs beat serial reading).

| Work smells like | Dispatch | Model |
|---|---|---|
| Harvest, scrape, extract, transcribe, bulk file reads | `harvester` | Haiku |
| A bounded research question (news, market, person, claim to verify), especially several at once | `researcher`, one per leg, in parallel | Sonnet |
| Find something across many files or folders when only the conclusion matters | `Explore` | inherited |
| Multi-step task with judgment, off the main context | `general-purpose` | stated per dispatch (below) |

Every `general-purpose` dispatch states `model` explicitly; left unset, it inherits the main model and quietly eats the usage window:
- `haiku` for mechanical legs;
- `sonnet` for fixed-spec execution, research legs and jury lens seats;
- omit it (inherit the session model) only for judgment-heavy legs and build work.

## Contracts every dispatch follows

- Agents return distilled conclusions (a table, a brief of 15 lines at most), never raw dumps. Raw material goes to files.
- Every dispatch states countable done-conditions. Not "research competitors" but "at least 7 competitors, each with pricing and a one-line wedge". Objective conditions let the main session verify an agent's "done" instead of trusting it. An agent asserting completion is a claim, not evidence; trust the live state, not the report.
- Independent legs launch in one message (parallel), never one after another.
- A browser profile is shared, so browser work is serial. An agent that finds the browser locked reports and stops.
- Agents serve the task in flight. Never fan out to expand scope.
- Writing in the user's voice is not delegated around the `writing` skill: agents may gather material; the voiced draft is written in the main session.

## 🔴 An authored recipe outranks your brief

When a task has a recipe, playbook or build spec written for it, the brief points at it and adds nothing. Such documents are written deliberately by a strong session so cheaper models can execute well without judgment. Overriding one turns a deterministic factory into many independent judgment calls, made by exactly the models chosen because they should not be making them.

- Read the recipe yourself before writing any brief against it. Passing a path to an agent is not reading it.
- Never restate a recipe rule in a brief, and never invent a numeric gate the recipe does not contain. A metric a bad build can satisfy is worse than no metric: it manufactures false confidence and becomes what the agent optimises for.
- If the recipe looks wrong, fix the recipe and say so. Never patch around it per dispatch.
- Only name a verified build as a reference. Pointing agents at an unproven one copies its defects by design.
- Tell agents the recipe outranks their brief, and to flag any conflict in their report.

Origin: a scripting rule was reissued in a brief as a build gate, and the builders mangled approved work to satisfy it.

## The delegation brief (write the plan for the model that runs it)

A happy-path plan strands a cheap model on the hard 20%. Any multi-step Haiku or Sonnet dispatch gets these lines in its prompt. Mechanical one-shot legs (grep this, fetch that) skip them, because on small jobs the overhead costs more than it saves.

- Each step: what the agent should see if it worked (the expected signal).
- Likeliest failure: its signals and the countermove.
- Stop when: the conditions to report back instead of improvising.
- Flag: anything it could not verify, stated as unverified and never rounded up to done.
- 🔴 What GOOD looks like: the positive quality bar, not only the failure list.

Why the last line exists: a brief made only of past defects produces defect-free mediocrity. The agent optimises for the list it was given, and anything not on the list is invisible to it. Origin: a batch of builds came back technically flawless and visually rejected, because no brief ever said what the visuals should be. State the bar ("uses real product screenshots", "should look like a finished page") or you get work that passes every check and is still wrong.

Corollary: an agent arguing for an exception to a rule it was just given is a red flag. When its reasoning is category-shopping ("this is a stylised graphic, not a literal depiction"), the rule was right and the work is not.

## Retracting a rule in prose does not retract it from the scaffold

When you retract or change a rule, grep for it everywhere it is encoded, not just where it is explained: templates, scaffolds, placeholder text, JSON comment fields, checkers, prompts, worked examples. The prose document states the rule; the scaffold executes it, and agents follow what they copy far more reliably than what they read. Origin: a retracted rule kept shipping because the template every new build copies still contained it.

The tell: an agent reports "I ignored the template comment because it contradicts the recipe". That is an incomplete retraction, and the next agent may not catch it.

## When a rule keeps failing, move it into tooling

| Evidence | Response |
|---|---|
| Failed once | Restate it in the dispatch |
| Failed 2 or 3 times | Put a number on it instead of an adjective ("bottom margin at least 260px", not "enough clearance") |
| Failed 3 or more times across agents | Make it structurally impossible: a blocking command, a build check, a schema, a wrapper |

Do not ship a gate you have not calibrated against known-good work. Run any candidate gate against your best-known output and your worst-known defect before it gates anything. If it cannot separate them, ship it as a diagnostic that always exits 0, say plainly that the structural fix is still owed, and record what you tried. Origin: agents repeatedly ended their turn on an imaginary "background watcher" while a render ran; the fix that held moved the wait inside a blocking command, so ending early became impossible instead of forbidden.

The tell that you are in this loop: writing the same warning louder (bold, red dots, capitals) instead of differently.

## Multi-perspective analysis

The jury is the `/jury` skill; that skill is the recipe, and this section only says when it runs: (a) the user asks for it or for a decision to be stress-tested, (b) `/grill-me`, `/offer-design` or `/sales-engine` offers it and the user says yes, (c) Claude meets a genuine go/no-go or contested strategic call mid-task, in which case it offers the jury in one line. A rule that only fires on Claude's own judgment almost never fires, so it is offered, and runs on a yes.

The jury ends in a verdict: green-light / reshape / kill, one line of why, and the single cheapest test the user can run in about 48 hours (for example "message 20 people in the niche before building anything"). For customer-facing calls, one juror role-plays the buyer. On contested calls the jury also seats a cross-model skeptic via the `second-opinion` skill: a different model family has uncorrelated blind spots, and where the two disagree, that disagreement is the headline. The outside model is one juror, never the judge; the main session adjudicates.
