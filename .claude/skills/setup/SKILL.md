---
name: setup
description: First-run setup of this AI operating system, as a guided ten-step run. Asks how technical the user is and adapts to it, explains how the system works (chat plus a diagram page), installs Obsidian and the basics, maps their work folder and phone inbox, walks them through connecting mail, calendar and drive, harvests the sources they pick, runs a deep interview, writes the brain, sets up a private backup, and offers daily and weekly e-mails from cloud routines. Use on a fresh clone, when the first-run hook says setup is not finished, or when the user says "/setup", "start", "get started", "set me up", "onboard me from scratch" or "continue setup".
---

# /setup: from an empty folder to a system that knows you

A fresh clone knows nothing about its owner. This skill fixes that in one sitting of about an hour, in ten steps, in this order:

| Step | What happens | Time |
|---|---|---|
| 1. Open | Name, and how technical they are. Everything after adapts to the answer | 2 min |
| 2. How it works | A walkthrough in chat plus a diagram page they can reopen | 3 to 8 min |
| 3. Installs | Obsidian (its own question), then git and Node if missing | 3 min |
| 4. Work folder | Where their work lives, mapped, plus a phone inbox in their cloud drive | 5 min |
| 5. Connect the basics | Mail, calendar, drive, click by click. Usually ends this session; a fresh one continues | 5 min |
| 6. Sources | They pick what Claude may read; harvester agents read it | 10 to 20 min, mostly Claude |
| 7. Interview | One question at a time, thirteen blocks | 30 to 60 min |
| 8. Write the brain | Context pages, projects, first memories; declined packs removed | 5 min |
| 9. Backup | A private GitHub repository, plus the fetch-only link for updates | 5 min |
| 10. Cadence | What runs when; permission for the morning and weekly e-mails; the hand-over | 5 min |

The user can say "pause" at any point. Every answer is on disk before the next question, so nothing is lost and a later session resumes exactly there.

## Resume first

Before anything else, look for `brain/brainstorms/*-setup.md`.

- A capture file exists and `.aios-setup-done` does not: this is a resume. Read the file (the Progress list and the `Level:` line), tell the user in one line where you left off ("We stopped at step 5, connecting your mail. Let me check whether it shows up now."), and continue. Do not re-ask what is captured. A resume at step 5 starts by checking which connectors this session can see.
- `.aios-setup-done` exists: setup is finished. Say so and offer `/onboard` (a short refresh) or `/grill-me <topic>` (depth on one subject).
- Neither exists: start at step 1.

## Adapting to the user's level

Step 1 asks one question that decides how every later step runs. Record the answer as `Level:` in the capture file.

| | Never used a terminal | Some experience | Developer |
|---|---|---|---|
| Explaining | Plain words, one idea at a time, an everyday comparison where it helps, no jargon without a one-line meaning | Short, names the parts, skips the basics | Three lines and the file paths; they read the rest |
| Installs and commands | Claude runs them itself after a yes, and says in one line what each did. Anything that needs the user's own hands (a login in a browser) gets numbered click-by-click steps | Claude runs them after a yes and shows the command | Claude shows the command, and runs it if they say so |
| Connector walkthrough | Every click, and what the screen should show after it | The path through the settings | One line |
| Interview | Same depth for everyone. Say why a question is asked when it might seem odd | Same | Same |

When unsure, explain one level simpler. Never make anyone feel slow for asking.

## Step 1: open

1. Open in at most three sentences: what is about to happen (a short explanation, a few setup steps, then an interview of about an hour), that everything stays in files on their own machine, and that they can pause any time. In the same message ask: **what should I call you?**
2. Create the capture file `brain/brainstorms/{YYYY-MM-DD}-setup.md` the moment they answer, using the structure at the bottom of this file. Tell them the path in one line.
3. Ask the level question with the choice tool: **How comfortable are you with computers and terminals?** Options: "I've never used a terminal", "I've used one a bit", "I'm a developer". Write the answer as `Level:` in the capture file.

## Step 2: how it works

The user should understand what they are building before they build it. This is the only tour, and it is short.

1. Open the diagram page: `node scripts/doctor.mjs --open-page` (it opens `docs/how-it-works.html` in their browser). If Node is not installed yet, give them the file path to open by double-clicking, or come back to it after step 3.
2. Walk through it in chat, sized to their level. The parts, in this order:
   - **The folder is the system.** Plain text files on their machine. Claude reads them at the start of a session, so it starts with context instead of from zero.
   - **The router** (`CLAUDE.md`): the page Claude reads first. It holds pointers (where things are, how to behave), never the knowledge itself.
   - **The brain** (`brain/`): everything about them and their work, as linked notes. Obsidian shows it as pages and a graph. Claude reads only the page a task needs.
   - **Skills** (`.claude/skills/`): written recipes for jobs that repeat (`/writing`, `/deadline`, `/jury`). Typing the name runs it.
   - **Rules** (`.claude/rules/`): how Claude works here: check before saying done, ask before sending or spending, hand bulk reading to helper agents.
   - **Hooks** (`scripts/hooks/`): small scripts that run on their own at fixed moments: stamping dates on edited notes, checking the inbox, backing up at the end of a session, blocking paid API calls nobody approved.
   - **Cadence** (`cadence.md`): the list of recurring work, with when it last ran and when it is due. Optional cloud routines can e-mail them a morning brief and a weekly review.
   - **Memory:** when they correct Claude ("don't do that again"), the correction is saved as a feedback memory and applies in every later session. A correction also patches the skill that made the mistake, so it does not come back.
   For "never used a terminal", use one comparison for the whole picture: a new assistant's desk, with a notebook about the boss (the brain), a sheet of house rules (the rules), recipe cards (skills), alarms that ring by themselves (hooks) and a wall calendar of routines (cadence).
3. Ask: "Any questions before we set it up?" Answer them, then go on.

## Step 3: installs

1. Check the machine: `node scripts/doctor.mjs`. If `node` itself is missing the command fails; check `git --version` and `node --version` directly and use the table below.
2. **Obsidian, as its own question** (choice tool): "Obsidian is a free app that shows your brain as linked pages and a graph. Want me to install it?" Never fold this into another question.
   - Yes: run the install command the doctor printed (`winget` on Windows, `brew` on macOS, `flatpak` on Linux) for "never used a terminal" and "some"; show it to a developer. Then, with Obsidian closed, register the vault (`node scripts/doctor.mjs --register-vault`) and open it (`node scripts/doctor.mjs --open-vault`). If either fails, give the manual route: open Obsidian, "Open folder as vault", pick the `brain` folder. Ask them to say when they see the vault.
   - No: say they can install it later from obsidian.md, and move on.
3. **git and Node**, if the doctor marks them missing. Say what each is for in one line (git: history and backups; Node: the hooks), and install on a yes:

   | System | git | Node |
   |---|---|---|
   | Windows | `winget install -e --id Git.Git` | `winget install -e --id OpenJS.NodeJS.LTS` |
   | macOS | `xcode-select --install` | `brew install node` |
   | Linux | `sudo apt install -y git` | `sudo apt install -y nodejs npm` (needs 18 or newer) |

   A fresh install is only on the PATH in a new session: if the next check still says missing, ask them to restart Claude Code in this folder and say "continue setup".
4. **The starter remote.** If the doctor says `origin` is the public starter repository, first record the starter commit (`git rev-parse HEAD > .aios-upstream`, the base for future updates), then remove the remote on a yes (`git remote remove origin`): their notes must never be pushed there. Step 9 sets up their own private backup.

## Step 4: where your work lives

1. Ask with the choice tool: **Where do you keep your work?** Options: OneDrive, Google Drive, Documents, Desktop, and "somewhere else". Several allowed.
2. Find the folder. Usual places:

   | Choice | Windows | macOS |
   |---|---|---|
   | OneDrive | `%USERPROFILE%\OneDrive` (or `OneDrive - <organisation>`) | `~/Library/CloudStorage/OneDrive-*` |
   | Google Drive | a drive letter such as `G:\My Drive` | `~/Library/CloudStorage/GoogleDrive-*/My Drive` |
   | Documents, Desktop | `%USERPROFILE%\Documents`, `%USERPROFILE%\Desktop` | `~/Documents`, `~/Desktop` |

   List the candidates you find and confirm the path with them. If the cloud app is not installed or not syncing, say so and offer to continue with a local folder.
3. Ask what in there is off limits, then **map it**: folder names two levels deep, no file contents. Write `otherworlds/work-folder.md` from `otherworlds/_template.md`: the path, what each top folder holds (ask about any folder whose name does not explain itself), and where finished work of each kind should be filed.
4. **Phone inbox.** When the work folder is a cloud drive, offer an `_inbox` folder at its top: "Anything you save there from your phone lands on this computer, and I file it." On a yes, create it and put its absolute path in the note's frontmatter as `inbox: <path>`. The inbox-check hook reads that line and lists both inboxes at the start of every session.
5. Point the filing at the map: update the routing table in `inbox/README.md` so each kind of file goes to its folder in the mapped tree.
6. Check: run `node scripts/hooks/inbox-check.mjs`. With both inboxes empty it prints nothing, and it must not print "not reachable". Tell them the two-inbox rule in one line: "When you say a file is in the inbox, I check both."

## Step 5: connect the basics

Mail, calendar and drive make most of the system work: the morning e-mail, reading their sent mail for voice and people, putting deadlines on the calendar, filing into their drive. This step is guided and treated as close to required.

1. Check which connectors this session can see (the available tools; `/mcp` lists them). Note which of mail, calendar and drive exist, and whether they are Google or Microsoft.
2. For each missing one, walk them through it at their level. The route, for Google and Microsoft alike:
   1. Open claude.ai in the browser and sign in with the account Claude Code uses.
   2. Open Settings, then Connectors.
   3. Google: connect **Gmail**, **Google Calendar** and **Google Drive**, one by one. Microsoft: connect **Microsoft 365** (it covers Outlook, the calendar and OneDrive).
   4. Each one opens a sign-in window from Google or Microsoft. Sign in with the account their work is on and allow the access it asks for.
   5. The connector now shows as connected in that list.
   In the desktop app, the same Connectors page is in the app's settings.
3. New connectors appear in the **next** session. Mark step 5 as "connect pending" in the capture file, then say: "Close this session, open a new one in this folder, and say: continue setup." End the turn there.
4. On resume, check the tools again. Record each connected one in `connections.md` with status `active`. If one is still missing, help once more (being signed in with a different account is the usual cause), then move on.
5. **Skipping is allowed.** If they skip any of the three, say plainly what will not work without it, then continue:
   - no mail: no morning or weekly e-mail, no harvest of sent mail, no voice samples from mail;
   - no calendar: `/deadline` cannot put anything on a calendar, and the brief has no agenda;
   - no drive: Claude cannot read or file documents in the cloud.
   Record the skip in the capture file so the hand-over offers it again.

## Step 6: what can I build context from?

The goal is to arrive at the interview already knowing a lot, so the questions are sharp and the user confirms instead of dictating.

### 6a. Look before asking

Find out what is reachable, without reading any content yet: the connectors from step 5, `gh auth status` if the GitHub CLI exists, the work folder from step 4, and top-level names in the usual places (home, Documents, Desktop, any notes vault).

### 6b. Ask once, as a menu

Present what you found and ask which sources you may use (choice tool, several allowed):

| Group | Sources | What each gives |
|---|---|---|
| Connected accounts | Sent mail, calendar, cloud drive, notes app, task tracker, code host | People, recurring work, rhythm, projects, voice |
| This machine | The work folder, project folders, an existing notes vault | Projects, plans, past work |
| Public footprint | LinkedIn profile (pasted text or the PDF export), their website, their company's site, a GitHub profile | Identity, offer, positioning, public voice |
| Files to drop in `inbox/` | CV, business plan, pitch deck, price list, course syllabus, brand guide | Facts that are already written down |
| Another AI's memory | An export or paste of ChatGPT memory, custom instructions, an old system prompt | Preferences they already taught a model once |

In the same turn ask what is off limits (folders, labels, people, topics) and whether anything not listed would tell you who they are faster. Record the off-limits list; it goes into `brain/context/how-i-work.md` under "what Claude must always ask first".

A user who picks nothing is fine: go to step 7 and ask everything.

### 6c. Harvest

- Read-only. Never send, label, move, delete or reply. Never open trash or spam.
- Sample, do not crawl: recent sent mail, a few weeks of calendar either side of today, the index or newest documents of a folder.
- Bulk reading goes to `harvester` agents, one per source, launched together. Each returns a short table of facts with where each fact came from. Raw material never enters the conversation or the brain.
- Tag every fact **seen** (the source states it) or **inferred** (you concluded it). Inferred facts become interview questions, never brain facts.
- For a public profile, open the page itself. A search result with a matching name is not evidence that it is the same person.

Write the result into the capture file under "What I found", then show the user about ten lines: "Here is what I think I know. Now I'll check it with you."

## Step 7: the interview

The centre of setup, and meant to be long: often sixty questions or more. The friction is the point: it surfaces what the user has never written down.

### Method

- **One question at a time**, with your recommended answer when the harvest gives one ("I think you run two businesses and study part-time. Right?"), so they can confirm or correct in a few words.
- **Checkpoint after every answer, before the next question.** Append to the capture file: the topic, the facts in their words where wording matters, any flag. Never batch answers into one write.
- **Never ask what a source answered as seen.** State it and move on. Ask about what is inferred, thin, surprising or contradictory.
- **Follow thin answers down** once or twice: "What does that look like in a normal week?" "When did that last happen?"
- **Choice tool for choices**, plain text for stories.
- **Unknowns become flags** under "Open flags", with who could answer.
- **Upstream before downstream.** The project list is settled before any project is discussed.
- **Never argue with their picture of their own life.** A contradiction between a document and what they say is a question, and their answer wins.
- A block that does not apply (no studies, no team) gets one confirming question and is skipped.

**Short version.** If they ask for it: blocks 1, 2 (the list plus three questions per project), 3, 11 and 13, then write the brain and note in the capture file which blocks are owed. `/setup` resumes them later.

### The thirteen blocks

The questions are a bank, not a script: skip what is known, add what the answers call for.

**Block 1. You.** What you would say you do, in one line. Where you live and your **time zone** (the cloud e-mails need it). Languages you work in. Background that still matters. What changed in the last year. Hard constraints: time, money, health, legal, family. Where you want to be in one to three years.

**Block 2. The work map, and the work itself.** First the complete list: every business, job, course, side project, and anything parked, each with one line and a status. Then, for each active project: what it is and who it is for; the stage and the two or three numbers that matter; what is sold, shipped or handed in, at what price or by which deadline; the people involved; where its files and accounts live; the tools; the jobs that repeat; what is stuck; the next milestone; what a win in ninety days looks like.
Then the work itself, for their main work: their role and industry; their clients or customers; **a typical day, task by task**; the deliverables they produce; who they report or answer to; what good work means in their field, and how they know they did it well.
Finish with how the pieces relate: what pays the bills, what is the bet, what comes first when they clash.

**Block 3. Priorities.** The top three for this quarter, ranked. What is deliberately not happening now. Fixed dates in the next ninety days. The tie-break rule. "If only one thing could get done this month, which?"

**Block 4. Goals and life outside work.** Personal goals for this year. Health and energy: anything Claude should plan around. Hobbies, and what they protect time for. Family, and the commitments that come with it. Money goals (saving for something, a target income, a runway). The point: Claude can weigh work against the rest of their life instead of treating every hour as work time.

**Block 5. Learning and school.** Courses or programmes they are in, with exam and hand-in dates. How they study and what works for them. What they want to learn next, for work or for themselves. Where course materials live. This feeds `/study` (if the study pack stays) and the calendar.

**Block 6. How you work.** The shape of a normal week. Fixed days and hours. Best focus time. Where tasks live today, and whether that works. How they plan, and whether they review. What they put off.

**Block 7. Where the time goes.** Walk through last week day by day (from the calendar if it was harvested). What do they do three or more times a week? Which of those do they dislike? What would they hand off first if they had an assistant tomorrow? What falls through the cracks? Write every repeated task as an automation candidate with a rough weekly count.

**Block 8. Pain points and AI wishes.** What frustrates them every week. What they have already tried with AI, what worked and what disappointed. What they wish were automated, in their words, even if it sounds impossible. Which of the block 7 candidates they would pay never to do again. This feeds `/level-up`.

**Block 9. People.** Who they work with and for. Who decides things that affect them. How they talk to each (mail, chat, calls). Anyone to handle with extra care. Whose messages always matter.

**Block 10. Tools, accounts and money.** The tools they live in. Paid subscriptions worth knowing. Any paid or metered API, with a monthly ceiling. Where money comes in and where it is tracked. What needs their approval before a cent is spent.

**Block 11. Working with Claude.** Tone: blunt, gentle, formal. How much pushback they want (the default is plain disagreement when they are wrong). What Claude may do without asking. What always needs a yes first (default: sending, spending, deleting, publishing). Language for replies. Format preferences. What annoys them about AI assistants. Which plan and models they use. Every clear preference here becomes a feedback memory in step 8.

**Block 12. Voice.** Three to five real pieces they wrote and sent: mails, posts, messages. Pasted, or picked from harvested sent mail with their approval; never typed fresh for the occasion. What they hate in machine-written text. This feeds the `writing` skill.

**Block 13. Packs.** Run `node scripts/packs.mjs list` and propose which optional packs to keep, from what the interview showed, with one line of why for each:

| Pack | Keep it when |
|---|---|
| business | they run or are starting a business, freelance, or sell their work |
| creator | they post content on YouTube, TikTok, Instagram or similar |
| web-design | they build or commission websites or interfaces |
| coding | they write code |
| study | they are studying or preparing for exams |
| outreach | they contact people cold to find clients, partners or interviews |
| community | they want more skills and are comfortable installing them |

Ask with the choice tool (several allowed), defaulting to your proposal. Core always stays. Record the declined packs; step 8 removes them.

**Close.** "What have I not asked that I would need to know to work for you for a year?" Then read the whole capture file for contradictions and gaps, and settle them.

## Step 8: write the brain

Turn the capture file into the curated layer. Synthesised facts only; the capture file stays as the raw record.

| Write | From |
|---|---|
| `brain/context/about-me.md` | Block 1 |
| `brain/context/work.md` | Block 2: the overview, the work itself, how the pieces relate |
| `brain/projects/<slug>/CONTEXT.md` (from `brain/templates/project-context.md`), one per project and one per course, plus a line in `brain/projects/README.md` | Blocks 2 and 5. Open tasks and next milestones go under `## Next`, one `- [ ]` line each, with a date where there is one |
| `brain/context/priorities.md` | Blocks 3 and 4 |
| `brain/context/how-i-work.md` | Blocks 6, 7, 8 and 11, the off-limits list, the automation candidates. It must contain a `Timezone:` line (an IANA name such as `Europe/Berlin`) and a `Calendar reminders:` line |
| `brain/context/network.md` | Block 9 |
| `connections.md` | Block 10 and the connectors from step 5, status `active`. Ones you recommend get status `planned` |
| `cadence.md` | Recurring jobs from blocks 2 and 7, one row each |
| `otherworlds/<name>.md` | Each external place a project lives (repo, cloud folder, site), next to `work-folder.md` |
| `.claude/skills/writing/references/voice-samples.md` | Block 12, pasted unedited |
| `.claude/skills/writing/references/ban_list.md` | Append what they said they hate |
| Feedback memories | Block 11 (below) |
| `CLAUDE.md`, only between `<!-- setup:start -->` and `<!-- setup:end -->` | Their name, the working agreements from block 11, the two-inbox rule with both paths, and the project list for "where to find things" |
| `brain/README.md` | One index line for every page created |
| `brain/decisions/log.md` | First entry: the date the system was set up, and any real decision the interview surfaced |

Then:

1. **Dates go on the calendar.** List the fixed dates from blocks 2, 3 and 5 and offer to put them on the calendar with `/deadline`, in one batch. Only on a yes, and only with a calendar connector.
2. **First feedback memories.** For each clear preference from block 11 (and any correction they made during setup), write one memory file in the Claude Code memory directory for this folder, with `type: feedback`, the rule, **Why:** and **How to apply:**, plus its line in `MEMORY.md` (format in `.claude/rules/common/working-agreements.md`, "How corrections stick"). Usually three to eight. Tell them where the memory lives, and that "remember that ..." adds more.
3. **Remove declined packs.** Run `node scripts/packs.mjs remove <pack> [...] --dry`, show the user the count, then run it without `--dry`. It deletes the files and every index line and link to them, and records them as removed so updates never bring them back.
4. **Check.** `node scripts/brain-janitor.mjs --local`: fix everything it reports until it shows zero broken links and zero orphans. Reread `about-me.md` and one project page as a stranger would; if a new session could not act on them, fix them now.

Rules: set `status: active` and today's `updated:` on every page you fill (an empty page keeps `status: template`); an inferred fact the user did not confirm stays out or carries "(unconfirmed)"; files dropped in `inbox/` get filed and the inbox ends empty.

## Step 9: private backup

Required before step 10: the cloud routines read the user's private copy on GitHub.

1. **The starter link for updates.** If `.aios-upstream` does not exist yet and the history still matches the starter, write it now (`git rev-parse HEAD > .aios-upstream`). Add the fetch-only upstream: `git remote add upstream https://github.com/Sennedem/aios-starter.git`, then `git remote set-url --push upstream DISABLED-fetch-only`. Say in one line what it is for: `/update-aios` pulls improvements from the public starter and never sends anything back.
2. **GitHub CLI.** If it is missing, install it (the doctor prints the command). Logging in needs the user's own hands: ask them to run `gh auth login --web --scopes workflow` in a terminal (for "never used a terminal": how to open one, then the command, then "it shows a code and opens your browser; paste the code there and approve"). The `workflow` scope matters: without it GitHub refuses the push, because this folder contains workflow files. If they are already logged in without it: `gh auth refresh -s workflow`.
3. **Git identity.** If `git config user.email` is empty, set `user.name` and `user.email` for this folder. Offer GitHub's no-reply address (GitHub settings, Emails) if they prefer their address stays out of commits.
4. **Create it, private.** Ask for a repository name, commit everything (`git add -A` and `git commit -m "chore: setup"`), then run `gh repo create <name> --private --source . --remote origin --push`. Never create or push to a public repository.
5. **Verify.** `gh repo view --json visibility -q .visibility` must print `PRIVATE`, and `node scripts/doctor.mjs` must show origin as private. From now on the session-end hook backs up automatically.
6. No GitHub at all (they decline): explain that the cloud e-mails in step 10 need it, then continue; step 10 falls back to the in-session morning check.

## Step 10: cadence, the e-mails, and the hand-over

1. **Explain cadence** at their level: `cadence.md` is the list of recurring work, with when each item last ran and when it is next due. At the start of every session Claude reads it and says what is due. Some jobs can run in the cloud without their computer: a morning brief and a weekly review.
2. **Ask permission** for the e-mails (choice tool): the morning brief (what is due, today's calendar, deadlines and open tasks this week), the weekly review (what got done, what is stale, the system's score, and the weekly clean-up), both, or neither. For each yes, ask the time (and for the weekly one, Friday afternoon or Sunday morning) and the address (default: the connected mail account). Nothing is sent before this yes.
3. **Create the routines** with the built-in `/schedule` skill, one per e-mail:
   - repository: their private backup from step 9 (the routine needs access to it; if `/schedule` asks to connect GitHub, walk them through it);
   - connectors: the mail connector, plus the calendar for the brief;
   - schedule: their time, converted from their time zone;
   - prompt, exactly one line: "Read `scripts/routines/morning-brief.md` in this repository and follow it exactly. That file outranks this prompt." (or `weekly-review.md`). The spec lives in the repo so it never drifts.
   Add a row per routine to `cadence.md` (Command: the routine name; Interval: daily or weekly; Notes: recipient, mail connector, send time and zone, routine id). Remove the manual "Weekly janitor" row when the weekly review now runs it. Offer to run each routine once now so they see a real e-mail, and check the sent folder to confirm it went.
   **No routines on their plan, or they declined:** say that the morning check runs at the start of each session instead (`/cadence`), and that they can turn the e-mails on later by asking.
4. **Hand over.** Show a short summary:
   - how many pages were written, with the paths of the main ones;
   - five things Claude now knows that it could not have guessed;
   - the three best automation candidates from blocks 7 and 8, ranked by weekly time saved, with an offer to build the first with `/level-up`;
   - the connections worth adding next (from "Recommended connections" in `connections.md`), one line each, skipping what they have or put off limits, plus any basic they skipped in step 5;
   - the open flags, each with who can answer it.
5. Write `.aios-setup-done` at the repo root with today's date. The first-run hook stops firing once it exists.
6. Close with what to try next, one line each: drop a file in the inbox and say "file this", `/ingest <url>` on something worth keeping, `/grill-me <project>` for depth on one project, `/goal` for something they want to achieve, `/save-session` before closing a long session, and "remember that ..." whenever Claude should keep a preference.

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
Started: {date} · For: {name} · Level: {never used a terminal | some | developer}

## Progress
- [ ] 1 Open
- [ ] 2 How it works
- [ ] 3 Installs (Obsidian: yes/no)
- [ ] 4 Work folder (path: ... / phone inbox: ...)
- [ ] 5 Connect the basics (mail / calendar / drive: connected, pending or skipped)
- [ ] 6 Sources (chosen: ... / off limits: ...)
- [ ] 7 Interview: blocks 1 [ ] 2 [ ] 3 [ ] 4 [ ] 5 [ ] 6 [ ] 7 [ ] 8 [ ] 9 [ ] 10 [ ] 11 [ ] 12 [ ] 13 [ ] (packs kept: ... / declined: ...)
- [ ] 8 Brain written (memories: N, packs removed: ...)
- [ ] 9 Backup (repo: ..., private verified)
- [ ] 10 Cadence (brief: time / weekly: day, time / routines created) and handed over

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
