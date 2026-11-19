---
name: save-session
description: Save where this session stands to a dated file, so a fresh session can pick up exactly here with /resume-session. Records what was built, what works (with evidence), what failed and why, what is untried, the state of each touched file, decisions, blockers and the exact next step. Use for "/save-session", "save the session", "save where we are", "I'm closing for today", "we're running out of context", or before clearing a long session.
---

# /save-session: write the hand-off

A session's working memory dies when the window closes or the context fills. This skill writes it to a file that the next session reads with `/resume-session`. Run it at the end of a work block, before `/clear` on a heavy session, or any time the user wants a checkpoint.

Session files are raw hand-offs, not knowledge. Durable facts and decisions still go into the brain as usual (the context-update table in `CLAUDE.md`); this file only carries the in-flight state.

## Steps

1. **Gather.** Look at what changed (`git status` and `git diff --stat` in this folder, plus anything outside it the conversation touched), what was tried, what failed with which error, and what was decided.
2. **Write** `~/.claude/session-data/<YYYY-MM-DD>-<short-id>-session.md`. The short id is eight or more lowercase letters, digits or hyphens that name the topic (`invoice-flow`, `site-redesign-2`). Create the folder if it is missing. Never append to an older file: one session, one file.
3. **Fill every section** of the format below. A section with nothing in it says so ("No failed approaches."). An honest empty section beats a missing one.
4. **Show it.** Print the path and the contents, and ask: "Anything to correct before we close?" Apply corrections.

## Format

```markdown
# Session: <YYYY-MM-DD>

**Project folder:** <absolute path of this folder>
**Topic:** <one line>
**Last updated:** <date and time, user's timezone>

## What we are building
<one to three paragraphs a session with no memory could act on: the goal, why, how it fits>

## What works (with evidence)
- <thing>: confirmed by <the check that proved it: a test run, a screenshot looked at, a fetched-back record>

## What did not work, and why
- <approach>: failed because <exact reason or error>. Do not retry unless <condition>.

## Not tried yet
- <idea, specific enough to start on>

## Files
| File | State | Notes |
|---|---|---|
| `path` | done / in progress / broken / not started | <what is left> |

## Decisions
- <decision>: because <reason>. Settled, do not reopen without new evidence.

## Blockers and open questions
- <item> -> <who or what can answer it>

## Exact next step
<the single next action, precise enough that resuming takes no thinking>
```

## Rules

- "What works" holds only things with evidence. A claim without a check goes under "Not tried yet" or "Files: in progress".
- "What did not work" is the most valuable section: without it the next session retries the same dead ends.
- Never put secrets, keys or passwords in the file.
- If the user asks mid-session, save what is known and mark unfinished items as in progress.
