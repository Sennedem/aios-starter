# Model and effort routing

> Companion to [agents.md](agents.md), which routes subagents; this rule routes the main session.

## Why

Model and effort are the two levers on the usage window: heavier models burn it faster, higher effort spends more thinking tokens. Claude cannot pull either lever itself (`/model` and `/effort` are user commands), so Claude's job is to decide the route and say it at the moment the user can act on it in one keystroke.

## When it fires

- Plan mode (primary): every plan ends with a Model & effort line (recommended execution model, effort, one-line why) so the user can switch at approval. That is the cheap moment: a mid-session switch re-reads the whole history uncached. When the task is hard (unknowns, dependent steps, claims to verify), the same line adds `+ five-gates`, so the executing session loads that discipline at start.
- `/goal`: the open task it writes into the project's `## Next` section gets a route stamp (for example `run on sonnet/medium`, plus `+ five-gates` for hard tasks) so whichever session runs it later starts on the right tier.
- Ad hoc: a task lands mid-session that clearly belongs on another tier; use the friction protocol below.

## Routing matrix (main session)

| Task smells like | Model | Effort |
|---|---|---|
| Mechanical grind: bulk reads, scraping, transcription, file moves, reformatting | not the main session: dispatch `harvester` (Haiku); if it must run in the main session, Haiku | low |
| Execute a fixed spec: approved plan, template drafting, a report refresh | Sonnet | low to medium |
| Standard judgment: writing, research synthesis, everyday planning | Sonnet, or a top-tier model | high on Sonnet, medium on top tier |
| Hard synthesis: strategy, contested decisions, multi-constraint design | top-tier model | high |
| Genuinely novel, highest stakes | the strongest model available | high or above |

- Checklist test (tie-breaker): route down when the task has a checklist and verifiable output; otherwise keep it up.
- Taste is a third axis: creative and aesthetic work (visuals, UI, naming, voice) justifies a higher tier even when the checklist test says route down.
- Effort levels: `low / medium / high / xhigh / max`. Default medium; drop to low for anything mechanical, raise only for real ambiguity. Do not pay for xhigh thinking on a task with one right answer.
- Never put the top tier on grind.
- On a planning-heavy day, `opusplan` (plans on Opus, executes on Sonnet) is an option.
- Never suggest a fast or priority mode without saying what it costs; check the current plan terms before recommending one.

## Friction protocol (recommended tier differs from the current one)

- Small task: state the route in one line and keep going on the current tier.
- Costly mismatch: long or bulk execution (many files, many subagent rounds, more than about 15 minutes of grind) about to run on the top tier: pause and wait for the user to switch or say "keep going". Do not quietly burn the window.

## Context companion

Where relevant, the route line also flags:
- Fresh session: a big plan approved in an already-loaded session executes cheaper in a new window; the route stamp lets that window start right.
- Handoff moment: models degrade as the context window fills, well before it is full. When a session is visibly heavy and a distinct new chunk of work is starting, suggest saving the session state, clearing, and resuming in a fresh window. That beats `/compact`, which is slow and lossy. `/context` shows what is filling the window. These are user commands: Claude flags the moment, the user presses the keys.

## Boundary

Subagent model routing lives in [agents.md](agents.md) and in each agent's frontmatter (`model:`). This rule only decides what the main session should run on.
