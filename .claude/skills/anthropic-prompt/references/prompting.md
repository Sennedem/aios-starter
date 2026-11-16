# Prompting Claude the way Anthropic recommends

The house reference for `/anthropic-prompt`. Source: Anthropic's platform documentation on prompting the Claude Fable 5 / 5.1 generation. Quoted lines are from those docs; the rest is the distilled rule.

## The one-line version

Give the model the finish line, the reason it matters, what "done" means, the real constraints and the context behind the ask. Then let it plan the tasks, verify its own work and parallelise the grind. Pick the effort level per task, not per habit.

## The four practices

### 1. Tell it what done looks like, not the task list

- State the outcome, why it matters, what done means (countable) and any real constraints. Do not enumerate steps; the model derives them.
- Docs: *"Claude Fable 5 tends to perform better when it understands the intent behind a request. Context lets it connect the task to relevant information rather than inferring intent on its own."*
- Docs: *"Skills developed for prior models are often too prescriptive for Claude Fable 5 and Fable 5.1."* Old step-by-step recipes can make a frontier model slower and worse.
- Example: a paragraph of individual tasks collapses to "Create an appealing landing page offering voice agent solutions tailored to our target audience."

Conflict to watch: recipes in this repo are deliberately prescriptive so cheaper models execute without judgment (`.claude/rules/common/agents.md`, "an authored recipe outranks your brief"). The loosen-it advice applies to frontier-tier sessions; keep recipes for Haiku and Sonnet dispatch.

### 2. Match the effort to the task

- Docs: *"Start with the default at high, then test on other levels like low, medium, xhigh and max against your own evals."* Reserve xhigh and max for deep, multi-constraint work.
- Docs: at low effort the model is *"more likely to answer from memory"* instead of calling a search tool. Low suits ideation; it is wrong when tool calls are the point.
- This repo's default stays medium (`.claude/rules/common/model-routing.md`); "start high, test down" is the calibration habit for any repeated task.

### 3. Make it prove its work

- Ask how you would check the output if a human handed it to you, and put that check in the prompt.
- Docs: *"Before reporting progress, audit each claim against a tool result from the session. Only report work you can point to evidence for. If something is not yet verified, say so explicitly."*
- Subjective outputs need a judge with "what good looks like" defined by you. Defining the goal is not enough; define the bar.

### 4. Parallelise and delegate

- Break the work into independent legs, run them at the same time, and keep the main session for strategy, interpretation and the final pass.
- The orchestrator still owns the outcome: it dispatches verifiers and checks the result itself at the end.

## Prompt anatomy (what `/anthropic-prompt` produces)

A finished prompt carries these blocks, in this order. Omit a block only when the interview showed it is genuinely empty.

| Block | Holds | Practice |
|---|---|---|
| Outcome | one sentence, the finish line | 1 |
| Why it matters | the intent and who it is for | 1 |
| Context | facts, files, prior work, audience, voice; pointers, not pastes | 1 |
| Done means | countable conditions, what would prove it works | 1, 3 |
| What good looks like | the quality bar in positive terms, a reference example if one exists | 3 |
| Constraints | only real ones: budget, deadline, banned moves, things not to touch | 1 |
| Verify before reporting | the check a human reviewer would run; the audit-each-claim rule | 3 |
| Delegate | which legs are independent, what the main session keeps | 4 |
| Effort | `low / medium / high / xhigh / max` with a one-line reason | 2 |

Output style: no step lists unless a step is a hard constraint; pointers to files over pasted content; one sentence per block where one sentence does it; plain prose, and XML sections only when the target is the API.

Also standard and compatible (from Anthropic's general prompting docs): a stated role, XML-tagged sections for API prompts, worked examples, and room to think before answering.
