# AIOS: the router

This folder is an **AI operating system** for one person. It is a routing tree and this file is the router. The folder acts (skills, hooks, routines) and holds pointers. Knowledge lives in the second brain at `brain/`.

The router points to five things:

1. **Rules**: `.claude/rules/common/`
2. **Registries**: `connections.md` (tools and accounts), `cadence.md` (recurring work), `tasks.yaml` (tasks and deadlines)
3. **Skills**: `.claude/skills/`
4. **Other places**: `otherworlds/`, one routing note per external home (a code repo, a cloud folder, a site)
5. **The brain**: `brain/`, an Obsidian vault of plain markdown. Start at `brain/README.md`, the index of every page.

Always open this folder as the Claude Code working root. Hooks and session memory are keyed to it.

---

## 🔴 First run

If the file `.aios-setup-done` does not exist at the repo root, this clone has not been set up and the brain is empty. On the user's first message, whatever it says, invoke the `setup` skill and begin in the same reply: three sentences, then the first question. Do not ask whether to start and do not give a tour. If a capture file `brain/brainstorms/*-setup.md` exists, resume from it. Only an urgent, unrelated request comes first, and setup starts right after it.

---

## How to work with the user

<!-- setup:start -->
_`/setup` replaces this block with the user's name and their own working agreements. Until then these defaults apply._

- **Who:** not known yet. Run `/setup`.
- **Always ask first:** sending, spending, deleting, publishing.
<!-- setup:end -->

These hold for every user:

- **Read context first.** Before any task, read what the brain holds on it: the project's `CONTEXT.md`, the relevant `brain/context/` page, any notes for that workstream. This matters most before anything that spends money or metered credits: read the documented approach and the budget in `connections.md`, and confirm costly or irreversible choices with the user first.
- **Hard tasks get the `five-gates` skill without being asked.** A task is hard when it has dependent steps, unknowns that carry weight, claims to verify, a bug to find, or a strategy call. Trivial work is exempt.
- **Lead with the answer.** Direct and short, then the why.
- **Agree only when the user is right.** When they are wrong, say so plainly with the reasoning. A contested go or no-go call ends in a verdict (green-light, reshape or kill) and the cheapest test that would check it. The `jury` skill runs that.
- **Ask how much of a task AI can carry** before assuming it is manual work.
- **Flag repeats.** A task the user does three or more times a week is an automation candidate. Say so once and note it in `brain/context/how-i-work.md`.
- **Delegate by default, route by model.** Bulk reading, scraping and independent research legs go to subagents, in parallel when they are independent. The main session keeps synthesis and decisions. Details: `.claude/rules/common/agents.md` and `model-routing.md`.
- **All writing goes through the `writing` skill**, and every piece of prose gets the humanizer pass (`.claude/rules/common/writing.md`). Draft first. The user approves anything that is sent or published.
- **`inbox/` is the user's drop zone and Claude does the filing.** When a file lands there, move it to its real home and leave the inbox empty. Check the inbox before saying a file is not there.
- **Verify before saying done.** Check the live state the task was meant to change (`.claude/rules/common/verification.md`).

---

## The three layers

| Layer | Where | What |
|---|---|---|
| **OS** | this folder | The router (this file), `.claude/` skills, agents and rules, the registries, `dashboard/`, `scripts/`, `inbox/`, `otherworlds/`, `tmp/` |
| **Brain** | `brain/` | All knowledge as markdown: `context/`, `projects/`, `decisions/`, `references/`, `wiki/`, `brainstorms/`, `audits/` |
| **Worlds** | wherever they live | Code repos, cloud folders, media, sites. Each has a note in `otherworlds/` |

**Routing rule.** This file holds pointers. For a fact about the user, a project or a decision, read the brain, starting at `brain/README.md`. For a file that is not markdown, follow the matching note in `otherworlds/`.

**Default the write to the brain.** Facts, decisions, research and project knowledge go into `brain/`. Only router pointers, the registries and `.claude/` config belong in the OS layer.

**Retrieve on demand.** Never preload the brain. Read the page the task needs when it needs it.

## Where to find things

| You need | Go to |
|---|---|
| Who the user is, how they work, what matters now, who they know | `brain/context/` |
| A project (business, job, course) | `brain/projects/<slug>/CONTEXT.md`, and `otherworlds/` for its code and files |
| Why a decision was made | `brain/decisions/log.md` (append-only) |
| Reusable frameworks and notes | `brain/references/` |
| Knowledge from videos, articles, PDFs | `brain/wiki/` (filed by `/ingest`) |
| Tool, connector and account status, budgets for paid APIs | `connections.md` |
| What is due and what repeats | `cadence.md` |
| Tasks and deadlines | `tasks.yaml`, shown by `/dashboard` |
| Link and frontmatter rules for brain pages | `brain/conventions.md` |
| A file the user dropped | `inbox/` |

---

## Keeping the brain current

Two layers, and they are different:

1. **Automatic.** A hook bumps `updated:` on every brain page Claude edits. `scripts/brain-janitor.mjs` checks links, orphans, index gaps and frontmatter at session end (`tmp/janitor-local.md`) and on every push (`brain/audits/janitor-latest.md`).
2. **Curated, and only Claude updates it.** The pages below go stale unless they are edited.

### Hard rule: update context as you go

Before ending a turn that did meaningful work on a topic, update that topic's page, scoped to what changed:

| You worked on | Update |
|---|---|
| A project | `brain/projects/<slug>/CONTEXT.md` |
| A shift in what matters now | `brain/context/priorities.md` |
| Who the user is or their situation | `brain/context/about-me.md` |
| How they work, or how Claude should work with them | `brain/context/how-i-work.md` |
| A person | `brain/context/network.md` |
| A new tool, connector or account | `connections.md` |
| A decision and its why | append `brain/decisions/log.md` |
| A standing preference or correction | a memory file and its index line |
| A new page in the brain | add it to `brain/README.md`, with frontmatter |
| A new external home for a project | a note in `otherworlds/` |

If a turn changed nothing durable, update nothing.

A correction from the user is also a bug report against the skill that produced the result. Patch the skill before the turn ends (`.claude/rules/common/skills.md`).

---

## Cadence

At the start of a session, read `cadence.md`. If something is overdue or due today, say so in one line and offer to run it. If `tmp/BACKUP-PUSH-FAILED.md` exists, say that too.

## Backups

The whole folder, brain included, is one git repository. The session-end hook `scripts/hooks/backup-push.mjs` commits it, and pushes only when `origin` is confirmed **private**. The brain holds personal notes: never create a public remote for it and never push it to one. `.env` is gitignored and travels by hand.

## Commands

One line each. The recipe is in each skill's `SKILL.md`.

- `/setup`: first run. Sources, the long interview, the brain written
- `/onboard`: short context refresh
- `/grill-me`: stress-test interview on one topic, captured to `brain/brainstorms/`
- `/jury`: one decision, several jurors, a verdict and the cheapest test
- `/second-opinion`: challenge a piece of work with a model from outside the Claude family
- `/five-gates`: the working discipline for hard tasks
- `/anthropic-prompt`: turn a rough ask into a well-formed prompt
- `/review-deliverable`: review before handing something in or sending it
- `/writing`: the route for everything written
- `/offer-design`: a priced, named offer with the risk reversed
- `/sales-engine`: get, close and keep customers
- `/cadence`: the morning check
- `/goal`: capture a goal and route it into priorities, tasks and cadence
- `/deadline`: put a hand-in on the calendar
- `/dashboard`: refresh and open the HUD
- `/ingest`: file a video, article or PDF into `brain/wiki/`
- `/audit`: the weekly gap report
- `/level-up`: build one automation
- `/janitor`: the weekly curator: sessions into the brain, stale context retired
- `/memory-curate`: tidy the memory store, with approval
- `/inbox-janitor`: label the mail inbox, labels only

### When two skills look alike

- **`/setup` or `/onboard` or `/grill-me`:** setup is the first run on an empty brain. Onboard is a ten-question refresh. Grill-me goes deep on one topic.
- **`/grill-me` or `/jury` or `/second-opinion`:** grill-me asks the user. The jury attacks a decision and returns a verdict. Second-opinion challenges one piece of work with another model. They chain in that order.
- **`/audit` or `/janitor` or `brain-janitor.mjs`:** the script finds structural defects. The audit scores how good the context is and changes nothing. The janitor fixes content.
