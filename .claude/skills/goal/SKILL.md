---
name: goal
description: Capture a goal, sharpen it with a few questions, and route it into the system: priorities in the brain, open tasks on the project page, dated steps on the calendar, cadence if it recurs, the decisions log if it changes direction. Use when the user states a goal, says "/goal", "my goal is", "I want to achieve X", or wants a goal broken into trackable work.
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
   - **Always:** add the concrete steps as open tasks in the project's `brain/projects/<slug>/CONTEXT.md`, under `## Next`, one line each: `- [ ] <step> (due YYYY-MM-DD) · run on <model>/<effort>`. The route stamp follows `.claude/rules/common/model-routing.md`, so whichever session executes it later starts on the right tier. The morning brief lists these lines and the janitor flags dated ones that pass.
   - **Dated steps also go on the calendar** through `/deadline` (conflict-checked, with the user's reminders). The calendar is where a date gets noticed; the project page is where the task is tracked.
   - **No project fits?** Ask which project it belongs to, or create the project page from `brain/templates/project-context.md` with its index line.
   - **If it changes what matters now:** update `brain/context/priorities.md` and say what moved down.
   - **If it is recurring work:** add a row to `cadence.md` instead of a one-off task.
   - **If it is a real change of direction:** append the why to `brain/decisions/log.md`.
4. **Close** with the first concrete next action the user (or Claude) can take today, and the tier it should run on.

## Rules

- Challenge weak goals: no measure, no deadline, or a clash with `priorities.md` gets said plainly, with a proposed fix.
- Don't pad the brain: a goal that is just a task gets one `## Next` line (and a calendar entry if it has a date) and nothing else.
- Bump frontmatter `updated:` on any brain page you touch.
