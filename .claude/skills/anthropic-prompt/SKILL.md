---
name: anthropic-prompt
description: Turn a rough ask into an Anthropic-grade prompt for Claude by interviewing the user, grill-me style, for the parts the raw prompt leaves open, then rewriting it to the house prompt anatomy (outcome, why, context, done-conditions, what good looks like, constraints, verify, delegate, effort). Use when the user says "/anthropic-prompt", "make this a proper prompt", "upgrade my prompt", "turn this into a real prompt", "write a brief for an agent", or pastes a prompt and asks how to make it better. Not for executing the task itself.
---

# /anthropic-prompt: from rough ask to Anthropic-grade prompt

One run makes one prompt. The user hands over a rough ask (a line, a paragraph, a task list); the skill interviews them for what the ask leaves open, then returns a prompt in the shape Anthropic's docs recommend, ready to paste into a fresh session, a scheduled routine, a subagent brief or a cloud agent.

Success looks like this: the rewritten prompt runs first time without a clarification round-trip, and the user's edits on it are taste, not missing information.

Draft-first. The prompt is returned for review; nothing is executed. If the user says "just do it", stop and execute the task on the current prompt instead.

## Step 0: read first

1. `references/learnings.md` in this folder: the user's corrections on how they want prompts built. It overrides defaults on conflict.
2. `references/prompting.md` in this folder: the four practices and the prompt anatomy table. Apply that table; do not paraphrase from memory.
3. Whatever context the raw ask points at (a project's `brain/projects/<slug>/CONTEXT.md`, a skill, a file). If a question can be answered by reading, read; never ask what the brain already knows.

## Step 1: diagnose the raw ask (silently)

Map the raw ask onto the anatomy table and mark each block present, inferable or missing. Typical misses: no done-condition, no quality bar, a step list where an outcome should be, context pasted instead of pointed at, no verification instruction, effort unstated.

Also classify the prompt's target: main-session task, subagent brief, scheduled routine, or API/system prompt. The target changes the output: a subagent brief keeps the delegation lines from `.claude/rules/common/agents.md`, and an API prompt may use XML sections.

## Step 2: short interview

Ask only for the missing blocks, in this order, one question at a time, each with a recommended answer inferred from context so the user can confirm with one word:

1. Outcome: the finish line in one sentence.
2. Why it matters, and who it is for.
3. Done means: countable conditions. What would prove it works?
4. What good looks like: the bar, plus a reference example if one exists.
5. Real constraints: budget, deadline, banned moves, things not to touch. Push back on fake constraints (a step list is usually one).
6. Verification: how would a human reviewer check this?
7. Delegation: which legs are independent?
8. Effort: propose a level per `.claude/rules/common/model-routing.md` and say why.

At most 5 questions for a small prompt; skip any block the ask already answers. If the answers keep changing the goal, the ask is really a design or planning question: stop and hand off to `/grill-me`, which owns deep discovery and checkpoints to `brain/brainstorms/`.

## Step 3: write the prompt

Produce the prompt in one fenced block in anatomy-table order. Style: outcome over steps, pointers to files over pasted content, one sentence per block where one does it, plain prose. Include the effort line and, for subagent briefs, the expected-signal, likeliest-failure, stop-when, flag-unverified and what-good-looks-like lines.

Then add what changed and why, three bullets at most, so the user learns the shape instead of just receiving the output.

## Step 4: save for reuse

Write the finished prompt to `brain/references/prompts/<yyyy-mm-dd>-<slug>.md` with frontmatter `type: reference`, `status: draft`, `domain: meta`, `parent: "[[references/README|references]]"`, `updated`, `tags: [prompt]`, and a one-line header naming the target and the raw ask it came from. Create the folder on first use. The `prompts/` folder gets one line in `brain/README.md`; individual prompts are not indexed one by one.

## Step 5: self-update

When the user corrects the prompt ("too long", "you asked something the brain knew", "wrong effort", "keep the step list here"), append a dated, generalised rule to `references/learnings.md` in the Rule / Why / Before → After format. Wording or voice corrections go to the `writing` skill's `references/learnings.md` instead.

## Boundaries

- This skill never executes the task. Executing is the next session's job, on the prompt it produced.
- The advice to loosen prescriptive prompts applies to frontier-tier sessions. A brief bound for Haiku or Sonnet keeps its recipe pointer; "an authored recipe outranks your brief" in `.claude/rules/common/agents.md` wins.
