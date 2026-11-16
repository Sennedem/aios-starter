---
name: goal
description: Capture a goal, sharpen it with a few questions, and route it into the system: priorities in the brain, tasks.yaml and the dashboard, cadence if it recurs, the decisions log if it changes direction. Use when the user states a goal, says "/goal", "my goal is", "I want to achieve X", or wants a goal broken into trackable work.
---

# /goal: capture a goal and wire it into the system

One run = one goal, sharpened and routed to where the OS will act on it. This is a light interview: a few sharp questions, not a full discovery session. For deep stress-testing of a plan, hand off to `/grill-me`.

## Steps

1. **Capture** the goal in the user's words. Read `brain/context/priorities.md` and the relevant `brain/projects/<slug>/CONTEXT.md` first, so you don't ask what is already known.
2. **Sharpen** with at most 3 questions, only the ones the context cannot answer:
   - What does done look like (measurable)?
   - By when? (hard date or ambition)
   - Which project or area does it belong to, and what does it displace? A new goal that displaces nothing is a wish.
3. **Route it:**
   - **Always:** add concrete tasks to `tasks.yaml` (`title / area / status / progress / deadline / priority / note`) so it shows on the dashboard with a countdown.
   - **Always:** stamp the route in the task `note` (`run on <model>/<effort>`, per `.claude/rules/common/model-routing.md`) so whichever session executes it later starts on the right tier. Keep note values free of colons.
   - **If it changes what matters now:** update `brain/context/priorities.md` and say what moved down.
   - **If it is recurring work:** add a row to `cadence.md` instead of a one-off task.
   - **If it is a real change of direction:** append the why to `brain/decisions/log.md`.
4. **Close** with the first concrete next action the user (or Claude) can take today, and the tier it should run on.

## Rules

- Challenge weak goals: no measure, no deadline, or a clash with `priorities.md` gets said plainly, with a proposed fix.
- Don't pad the brain: a goal that is just a task gets a `tasks.yaml` row and nothing else.
- Bump frontmatter `updated:` on any brain page you touch.
