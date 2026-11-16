---
name: setup
description: First-run setup of this AI operating system. Finds out what Claude can build context from (connected accounts, folders, files, public profiles, old notes, another AI's memory), harvests the sources the user picks, then runs a long structured interview about who they are, what they work on and how they work, and writes all of it into the brain. Use on a fresh clone, when the first-run hook says setup is not finished, or when the user says "/setup", "start", "get started", "set me up", "onboard me from scratch" or "continue setup".
---

# /setup: build the brain from nothing

A fresh clone knows nothing about its owner. This skill fixes that in one sitting. It has five phases and it starts talking immediately: no preamble about the system, no tour of the folders.

| Phase | What happens | Rough time |
|---|---|---|
| 1. Open | Name, the capture file, a quiet machine check | 3 min |
| 2. Sources | "What can I build context from?" The user picks, Claude harvests | 10 to 20 min, mostly Claude reading |
| 3. Interview | The long grill: nine blocks, one question at a time | 30 to 60 min |
| 4. Write | Everything lands in the brain and the OS files | 5 min |
| 5. Hand over | Checks, a summary, the first automations, a private backup | 5 min |

The user can say "pause" at any point. Every answer is on disk before the next question, so nothing is lost.

## Resume first

Before anything else, look for `brain/brainstorms/*-setup.md`.

- A capture file exists and `.aios-setup-done` does not: this is a resume. Read the file, tell the user in one line where you left off ("We stopped in block 4, how you work. Picking up there."), and continue. Do not re-ask what is captured.
- `.aios-setup-done` exists: setup is finished. Say so and offer `/onboard` (a short refresh) or `/grill-me <topic>` (depth on one subject) instead.
- Neither exists: start at phase 1.

## Phase 1: open

1. Open with three sentences at most. What is about to happen (a few questions about sources, then an interview), that everything stays in local files on their machine, and that they can pause any time. Then ask the first question in the same message: **what should I call you?**
2. Create the capture file `brain/brainstorms/{YYYY-MM-DD}-setup.md` the moment they answer, using the structure at the bottom of this file. Tell them the path in one line.
3. Run the machine check without narrating it: `node scripts/doctor.mjs`. It reports git, Node, the GitHub CLI, whether Obsidian is installed, and where the `origin` remote points. Act on the result:
   - **Obsidian missing:** offer to install it, and name the command the doctor printed for their system. Install only on a yes. If they decline, say they can do it later from obsidian.md and move on.
   - **Obsidian present:** offer to register `brain/` as a vault (`node scripts/doctor.mjs --register-vault`, Obsidian must be closed while it runs). If that fails or they prefer, the manual route is: open Obsidian, "Open folder as vault", pick the `brain` folder.
   - **`origin` points at the public starter repo, or at any public repo:** explain in one line that their private notes must never be pushed there, and remove the remote on their yes (`git remote remove origin`). A private backup is offered in phase 5.
   - **Node or git missing:** say which hooks will not run until it is installed, and continue. Setup itself only needs Claude.

Keep this phase short. The user came for the questions.

## Phase 2: what can I build context from?

The goal is to arrive at the interview already knowing a lot, so the questions can be sharp and the user confirms instead of dictating.

### 2a. Look before asking

Find out what is reachable, without reading any content yet:

- The connectors and MCP tools available in this session (mail, calendar, cloud drive, notes apps, chat, task trackers, code hosts). List the ones you can see.
- `gh auth status`, if the GitHub CLI exists.
- Top-level names only in the usual places: the home folder, Documents, Desktop, any folder that looks like a notes vault or a projects folder.

Then compare what you can reach against the "Recommended connections" tables in `connections.md`. If mail, calendar or a cloud drive is missing, say so before the menu, in two lines: which ones are missing, what each would give the interview (people and voice from sent mail, the weekly rhythm from the calendar), and how to connect them (their Claude connector settings; a new connector shows up in the next session). Offer both routes and let them choose: connect now and say "continue setup" in a fresh session, or carry on without and connect later. Never stall setup on a connector.

### 2b. Ask once, as a menu

Present what you found and ask which sources you may use. Use the multiple-choice question tool when it is available (several choices allowed), grouped like this:

| Group | Sources | What each one gives |
|---|---|---|
| Connected accounts | Sent mail, calendar, cloud drive, notes app, task tracker, code host | People, recurring work, rhythm, projects, voice |
| This machine | Folders they point at: documents, project folders, an existing notes vault | Projects, plans, past work |
| Public footprint | LinkedIn profile (pasted text or the PDF export), their website, their company's site, social handles, a GitHub profile | Identity, offer, positioning, public voice |
| Files to drop in `inbox/` | CV, business plan, pitch deck, price list, course syllabus, brand guide, org chart | Facts that are already written down |
| Another AI's memory | An export or paste of ChatGPT memory, custom instructions, Claude profile preferences, an old system prompt | Preferences they already taught a model once |

Then ask two things in the same turn:

- **What is off limits?** Folders, labels, people, topics. Record the answer in the capture file and later in `brain/context/how-i-work.md` under "what Claude must always ask first".
- **Anything not on this list** that would tell you who they are faster than talking would.

A user who picks nothing is fine. Skip to phase 3 and ask everything.

### 2c. Harvest

Rules for every source:

- Read-only. Never send, label, move, delete or reply. Never open trash or spam.
- Sample, do not crawl. Recent sent mail tells you more than the whole archive. A few weeks of calendar either side of today shows the rhythm. In a folder, read the index or the newest documents first.
- Bulk reading goes to `harvester` subagents, one per source, launched together. Each returns a short table of facts with where each fact came from. Raw material never enters the main conversation or the brain.
- Tag every fact as **seen** (the source states it) or **inferred** (you concluded it). Inferred facts are questions for the interview. They are never written into the brain as facts.
- For a public profile, open the page itself. A search result that matches the name is not evidence that it is the same person.
- If a source needs a login you do not have, say so and move on.

Write the result into the capture file under "What I found": a draft identity line, the candidate project list, people who recur, recurring commitments, tools seen, possible voice samples, and the open questions the sources raised.

Close the phase by showing the user that summary in about ten lines: "Here is what I think I know. Now I will check it with you."

## Phase 3: the interview

This is the centre of setup and it is meant to be long. A full run is often fifty questions or more. The friction is the point: it surfaces what the user has never written down.

### Method

- **One question at a time.** Each question comes with your recommended answer when the harvest gives you one ("I think you run two businesses and study part-time. Right?"), so the user can confirm, correct or redirect in a few words.
- **Checkpoint after every answer, before the next question.** Append to the capture file: the topic, the facts and decisions in their words where wording matters, and any flag. Never batch several answers into one write.
- **Never ask what a source already answered as seen.** State it and move on. Ask about what is inferred, thin, surprising or contradictory.
- **Follow thin answers down.** "What does that look like in a normal week?" "When did that last happen?" "Why that and not the other?" One or two follow-ups, then on.
- **Use the choice tool for choices**, plain text for stories.
- **Unknowns become flags.** When the user cannot answer, write it under "Open flags" with who could, and continue.
- **Upstream before downstream.** The project list is settled before any single project is discussed. Priorities come after the projects.
- **Never argue with their picture of their own life.** A contradiction between a document and what they say is a question for them, and their answer wins.

If the user asks for the short version: run blocks 1, 2 (the list and three questions per project), 3 and 8, write the brain, and note in the capture file which blocks are owed. `/setup` resumes them later.

### The nine blocks

Work through them in order. The questions are a bank, not a script: skip what is known, add what the answers call for.

**Block 1. You.**
What you would say you do, in one line. Where you live and your time zone. Languages you work in. Background that still matters (study, past jobs, skills). What changed in the last year. Hard constraints: time, money, health, legal, family. Where you want to be in one to three years.

**Block 2. The work map.**
First the complete list: every business, job, course, side project, and anything parked. For each, confirm one line and its status. Then one mini-interview per active project:
what it is and who it is for; the stage and the two or three numbers that matter; what is sold, shipped or handed in, and at what price or by which deadline; the people involved; where its files, code and accounts live; the tools it runs on; the jobs that repeat every week or month; what is stuck right now; the next milestone; what a win in ninety days would look like.
Finish the block with how the pieces relate: what pays the bills, what is the bet, what comes first when they clash.

**Block 3. Priorities.**
Rank the top three for this quarter. What is deliberately not happening now. Fixed dates in the next ninety days. The tie-break rule. "If only one thing could get done this month, which?"

**Block 4. How you work.**
The shape of a normal week. Fixed days and hours. Best focus time. Where tasks live today and whether that works. How you plan and whether you review. What you put off.

**Block 5. Where the time goes.**
Walk through last week day by day if a calendar was harvested, or from memory if not. What do you do three or more times a week? Which of those do you dislike? What would you hand off first if you had an assistant tomorrow? What falls through the cracks? Every repeated task is written down as an automation candidate with a rough weekly count.

**Block 6. People.**
Who you work with and for. Who decides things that affect you. How you talk to each (mail, chat, calls). Anyone Claude should handle with extra care. Whose messages always matter.

**Block 7. Tools, accounts and money.**
The tools you live in. Paid subscriptions worth knowing. Any paid or metered API, with a monthly ceiling. Where money comes in and where it is tracked. What needs your approval before a cent is spent.

**Block 8. Working with Claude.**
Tone: blunt, gentle, formal. How much pushback you want (the default is plain disagreement when you are wrong). What Claude may do without asking. What always needs a yes first (the default list: sending, spending, deleting, publishing). Language for replies. Format preferences. What annoys you about AI assistants. Which plan and models you are on, so work can be routed sensibly.

**Block 9. Voice.**
Ask for three to five real pieces they wrote and sent: mails, posts, messages. Pasted or picked from harvested sent mail with their approval, never typed fresh for the occasion. Ask what they hate in machine-written text. This feeds the `writing` skill.

**Close.** "What have I not asked that I would need to know to work for you for a year?" Then read the whole capture file for contradictions and gaps, and settle them.

## Phase 4: write the brain

Turn the capture file into the curated layer. Synthesised facts only; the capture file stays as the raw record.

| Write | From |
|---|---|
| `brain/context/about-me.md` | Block 1 |
| `brain/context/work.md` | Block 2, the overview table and how the pieces relate |
| `brain/projects/<slug>/CONTEXT.md` (copy `brain/templates/project-context.md`), one per project, plus a line in `brain/projects/README.md` | Block 2 |
| `brain/context/priorities.md` | Block 3 |
| `brain/context/how-i-work.md` | Blocks 4, 5 and 8, and the off-limits list from phase 2 |
| `brain/context/network.md` | Block 6 |
| `connections.md` | Block 7 and the connectors seen in phase 2, with status `active`. Connections you are recommending (step 3 of phase 5) get a row with status `planned` |
| `cadence.md` | The recurring jobs from blocks 2 and 5, one row each |
| `tasks.yaml` | Delete the example tasks. Add the fixed dates and next milestones from blocks 2 and 3 |
| `otherworlds/<name>.md` (copy `otherworlds/_template.md`) | Each external place a project lives: repo, cloud folder, site |
| `.claude/skills/writing/references/voice-samples.md` | Block 9, pasted unedited |
| `.claude/skills/writing/references/ban_list.md` | Append what they said they hate |
| `CLAUDE.md`, only between the `<!-- setup:start -->` and `<!-- setup:end -->` markers | Their name, the working agreements from block 8, and the project list in the "where to find things" table |
| `brain/README.md` | One index line for every page created |
| `brain/decisions/log.md` | First entry: the date AIOS was set up, and any real decision the interview surfaced |

Rules:

- Set `status: active` and today's `updated:` on every page you fill. A page with nothing to put in it keeps `status: template`.
- An inferred fact the user did not confirm stays out, or is written with "(unconfirmed)".
- Files dropped in `inbox/` during phase 2 get filed where they belong or returned to the user's own folders. The inbox ends empty.
- Write each page so that a new session with no memory of this conversation could work from it.

## Phase 5: check and hand over

1. Run `node scripts/brain-janitor.mjs --local` and fix what it reports. Run `node dashboard/build-data.mjs`.
2. Reread `about-me.md` and one project page as a stranger would. If a new session could not act on them, fix them now.
3. Show the user a short summary:
   - how many pages were written, with the paths of the main ones;
   - five things Claude now knows about them that it could not have guessed;
   - the three best automation candidates from block 5, ranked by weekly time saved, with an offer to build the first with `/level-up`;
   - the two or three connections worth adding next, picked from the "Recommended connections" tables in `connections.md` by what the interview showed: where their work lives (block 2), the tools they named (block 7) and the automation candidates that need a connector to run. One line each: the connection, what it would unlock for them specifically, how to connect it. Skip any they already have and any they put off limits;
   - the open flags, each with who can answer it.
4. Offer the private backup. On a yes, ask for a repo name and run `gh repo create <name> --private --source . --remote origin --push`. Never create or push to a public repository. Without the GitHub CLI, give them the steps for creating a private repo by hand and adding it as `origin`.
5. Write `.aios-setup-done` at the repo root with today's date. The first-run hook stops firing once it exists.
6. Close with what to try next, one line each: `/cadence` in the morning, `/ingest <url>` on something worth keeping, `/grill-me <project>` for more depth on one project, `/dashboard` to see it all, `/audit` at the end of the week.

## Capture file structure

```
---
type: note
status: active
updated: {date}
domain: meta
parent: "[[brainstorms/README|Brainstorms]]"
---

# Setup: discovery notes
Started: {date} · For: {name}

## Progress
- [ ] Phase 1 open
- [ ] Phase 2 sources (chosen: ... / off limits: ...)
- [ ] Block 1 you
- [ ] Block 2 work map (projects: ...)
- [ ] Block 3 priorities
- [ ] Block 4 how you work
- [ ] Block 5 where the time goes
- [ ] Block 6 people
- [ ] Block 7 tools, accounts, money
- [ ] Block 8 working with Claude
- [ ] Block 9 voice
- [ ] Phase 4 brain written
- [ ] Phase 5 handed over

## What I found (from sources)
(seen facts with their source; inferred facts marked as questions)

## Q&A log
### Q1: {topic}
- Asked: {question}
- Captured: {facts and decisions, their words where it matters}
- Flags: {open item -> who can answer}

## Automation candidates
| Task | Times per week | Disliked? | Idea |

## Open flags
- {item} -> {who can answer}
```

Tick the progress boxes as you go. They are what makes a resume possible.
