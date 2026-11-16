# Writing: the humanizer pass on everything

> Companion to the `writing` skill, which stays the route for anything in the user's voice.

Every piece of prose Claude writes in this repo gets the humanizer pass before it leaves the turn. The catalogue of tells is [`.claude/skills/writing/references/humanizer.md`](../../skills/writing/references/humanizer.md) (adapted from blader/humanizer, MIT licence).

| Writing | Route |
|---|---|
| Anything the user sends, posts, records or hands in (mails, posts, scripts, captions, messages, coursework) | the `writing` skill, which runs the pass as one of its steps |
| Writing a skill produces on its own (outreach drafts, captions, reports, digests) | the skill's own recipe, then the pass on the final text |
| Claude's own prose: chat replies, brain notes, decision-log entries, skill and rule docs, commit messages, PR bodies | the pass directly |

The pass, short form: mark the tells, strongest first (not-X-but-Y framing, one-line dramatic closers, deep-sounding sayings, staged run-ups and colon reveals, arguing with no one), at sentence and paragraph scale; rewrite; check that no fact, number, price, date or claim moved; then search again for the survivors (not-X-but-Y, closers, triads, dashes, bold run-in labels). Zero em- or en-dashes in prose.

Precedence: the user's own samples and the `writing` skill's `references/learnings.md` come first, then its `references/ban_list.md`, then the catalogue. Leave code, paths, commands, quotes and proper names alone.

When a prose rule fails three times, move it into a lint script that blocks the output (see the escalation table in [agents.md](agents.md)).
