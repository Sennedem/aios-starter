---
name: onboard
description: Short refresh of the user's context after the first setup. Finds the gaps and stale parts in the brain's context pages and asks only about those. Use when context feels out of date, after a big change (new job, new project, a move), or when the user says "/onboard", "refresh my context" or "update what you know about me". For a first run on a fresh clone use the setup skill.
---

# /onboard: refresh the context

Keep it fast. Under ten questions, answers written straight into the files.

If `.aios-setup-done` does not exist, stop and run the `setup` skill instead.

## Steps

1. Read `brain/context/*.md`, every `brain/projects/*/CONTEXT.md`, `connections.md` and `cadence.md`. List what is missing (`status: template`, empty sections), what looks stale (an old `updated:` date on a page about something that moves), and what contradicts something else.
2. Ask only about that list. Group the questions. Give your best guess with each so the user can confirm in a word.
3. Write the answers into the right files in one batch. Rewrite a section cleanly; do not leave the old version next to the new one.
4. New project: copy `brain/templates/project-context.md` to `brain/projects/<slug>/CONTEXT.md`, add it to `brain/projects/README.md` and `brain/README.md`. Finished or dropped project: set `status: archived`, keep the page.
5. Append to `brain/decisions/log.md` only when a real decision was made.
6. Close with what changed, in three lines at most.

## The question bank (ask only the gaps)

1. What changed since the last refresh: role, projects, where you live, who you work with?
2. Are the three priorities in `priorities.md` still the right three, in that order?
3. Any project to add, pause or close?
4. New recurring work, or recurring work that stopped?
5. New tools, accounts or subscriptions? Any that were cancelled?
6. Anything about how Claude works with you that should change?
7. New writing samples for the `writing` skill, if your voice or audience shifted?
