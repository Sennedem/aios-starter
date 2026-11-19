# AIOS starter

A personal AI operating system for Claude Code. You clone it, open it, and Claude interviews you until it knows who you are, what you work on and how you work. From then on every session starts with that context instead of from zero.

It is a folder of plain files. There is no app and no server, and nothing leaves your machine unless you set up a backup.

## What you get

- **A second brain.** `brain/` is an Obsidian vault of markdown that Claude writes and keeps current: who you are, one page per project with its open tasks, your priorities, your decisions with their reasons, and a wiki of what you learn from videos, articles and PDFs.
- **A wiki that is not empty.** About 150 pages on working with AI and Claude Code, running a one-person business, web design and social platforms: one idea per page, linked, each source credited. Setup keeps the packs that fit your work and removes the rest.
- **A router.** `CLAUDE.md` tells Claude where everything lives, so it reads the one page a task needs and skips the rest.
- **25 skills.** A guided setup, a consultant-style interview, a decision jury, a writing route with an AI-tell filter, a study engine, a cold-email engine, session save and resume, an update path from this repository, and more. The list is below.
- **Hooks that do the upkeep.** A first-run trigger, a check of both your inboxes, a date stamp on every edited note, a link checker, a guard when two Claude windows edit the same file, a root tidy, a private-only backup, and a guard that stops paid API calls you did not approve.
- **Default working rules.** Twenty-six agreements learned the expensive way (fix small problems instead of listing them, never confirm a guess with a leading search, nothing sent without your yes), in `.claude/rules/common/working-agreements.md`.
- **Optional e-mails.** A morning brief and a weekly review from Claude cloud routines, sent from your own mail account, only if you say yes during setup.

## Install

You need [Claude Code](https://claude.com/claude-code) in any form (the Claude desktop app, the VS Code extension or the terminal command), git, and Node 18 or newer. [Obsidian](https://obsidian.md) is free and optional; setup offers to install it for you.

### 1. Get the files

The quickest way needs no GitHub login. Open a terminal (Terminal on macOS, PowerShell on Windows) in the folder where you want it, for example Documents:

```bash
git clone https://github.com/Sennedem/aios-starter.git aios
```

This creates a folder called `aios`. Setup later disconnects it from this public repository and offers you a private backup of your own.

If you would like your own repository from the start: click **Use this template** at the top of this page, create the repository as **private** (your brain will hold personal notes), and clone that one. Cloning a private repository asks you to log in. Your GitHub password does not work there, so log in once with the [GitHub CLI](https://cli.github.com) (`gh auth login`) or use GitHub Desktop.

### 2. Open the folder in Claude Code and say "start"

| You use | Do this |
|---|---|
| The Claude desktop app | Open the Code tab, start a session on the `aios` folder (running locally on your machine) and type `start` |
| VS Code | Open the `aios` folder, open the Claude Code panel and type `start` |
| The terminal | `cd aios`, then `claude "start"`. The `claude` command is its own install and does not come with the desktop app |

Setup begins with the first message. You do not have to configure anything first. If Claude answers like a normal chat, the session is not opened on the `aios` folder.

### 3. Optional: check the machine

```bash
cd aios
node scripts/doctor.mjs
```

It reports what is missing and prints the install commands for your system (Obsidian, git, Node and the GitHub CLI, through `winget` on Windows, `brew` on macOS, `apt` or `flatpak` on Linux). Setup runs the same check for you.

## What the first run does

| Step | What happens |
|---|---|
| 1. Open | Your name, and how technical you are. Everything after adapts: a first-timer gets plain words and Claude runs the installs; a developer gets three lines and the file paths |
| 2. How it works | A short walkthrough in chat and a diagram page in your browser (`docs/how-it-works.html`) you can reopen any time |
| 3. Installs | Obsidian, asked as its own question, installed and opened on a yes. git and Node if missing |
| 4. Work folder | Where you keep your work (OneDrive, Google Drive, Documents, Desktop). Claude maps it, files your drops there, and can add an `_inbox` folder in your cloud drive for files from your phone |
| 5. Connect the basics | A click-by-click walk through connecting mail, calendar and drive (Google or Microsoft). You can skip; setup says what will not work without them |
| 6. Sources | "What can I build context from?" You pick: sent mail, calendar, drive, folders, your LinkedIn or website, a CV dropped in `inbox/`, another AI's memory. You say what is off limits. Claude reads only what you picked, read-only |
| 7. Interview | Thirteen blocks, one question at a time: you, your work and a typical day, priorities, goals and life outside work, learning, how you work, where the time goes, pain points and AI wishes, people, tools and money, how Claude should behave, your writing voice, and which packs to keep |
| 8. Write | The brain gets filled: context pages, one page per project, your first feedback memories, the working agreements in `CLAUDE.md`. Packs you declined are removed |
| 9. Backup | A private GitHub repository of your own, and a fetch-only link to this one for `/update-aios` |
| 10. Cadence | What runs when, permission for the morning and weekly e-mails, and a hand-over: what Claude now knows and the three best automations to build first |

A full run takes about an hour and is often sixty questions or more. Every answer is saved to `brain/brainstorms/` before the next question, so you can say "pause" and pick up tomorrow. Ask for the short version if you want fifteen minutes now and the rest later.

## Layout

```
CLAUDE.md          the router
connections.md     tools, connectors, accounts, budgets
cadence.md         recurring work: last run, next due
inbox/             drop files here, Claude files them
otherworlds/       one note per external place (work folder, code repo, site)
docs/              the how-it-works page, the community skills list
scripts/           the hooks, the machine check, the link checker, packs, updates
  routines/        specs for the cloud e-mails (morning brief, weekly review)
.claude/           skills, rules, agents, hook wiring, packs.json
brain/             the second brain (open this folder in Obsidian)
  context/         about you, your work, how you work, priorities, network
  projects/        one folder per business, job or course, open tasks under Next
  decisions/       the append-only decision log
  references/      frameworks and notes you reuse
  wiki/            outside knowledge, filed by /ingest
  brainstorms/     raw interview captures
  audits/          weekly reports
```

## Skills

| Skill | What it does |
|---|---|
| `/setup` | The first run described above |
| `/onboard` | A ten-question context refresh after a big change |
| `/grill-me` | A long interview on one plan or topic, saved answer by answer |
| `/jury` | Several jurors attack one decision and return green-light, reshape or kill, with the cheapest test |
| `/second-opinion` | Challenges a piece of work with a model from outside the Claude family |
| `/five-gates` | The working discipline for hard, multi-step tasks |
| `/anthropic-prompt` | Turns a rough ask into a well-formed prompt |
| `/review-deliverable` | Reviews a report, deck or sheet before you send it |
| `/writing` | The route for everything written, in your voice, with the AI-tell filter |
| `/offer-design` | A priced, named offer with the risk reversed |
| `/sales-engine` | A funnel, a sales-call script and a retention plan |
| `/cadence` | The morning check: what is due, what is on the calendar |
| `/goal` | Captures a goal and routes it into priorities, the project's open tasks, the calendar and cadence |
| `/deadline` | Puts a hand-in on your calendar with reminders |
| `/ingest` | Files a video, article or PDF into the wiki as small linked pages |
| `/audit` | A weekly report on how complete and current your context is |
| `/level-up` | Builds one automation from your list of repeated tasks |
| `/janitor` | The weekly curator: recent sessions into the brain, stale context retired |
| `/memory-curate` | Tidies Claude's memory store, with your approval |
| `/inbox-janitor` | Labels your mail inbox. Labels only, it never sends or deletes |
| `/save-session`, `/resume-session` | Writes a hand-off before you close a session; the next session reads it and picks up there |
| `/update-aios` | Pulls new and fixed skills, rules and wiki pages from this repository into your copy, merges where you edited, never touches your notes |
| `/study` | Study pack: learn a week's material, attempt-first quizzes, timed practice exams, redo only the misses <!-- pack:study --> |
| `/outreach` | Outreach pack: personalised cold e-mail with a lint gate, sent from your own Gmail through your private repository, drafts first <!-- pack:outreach --> |

Mail, calendar and drive skills use the connectors you have in Claude. Without a connector a skill says so and skips that step.

## Packs

Some of the system only fits some people. Setup asks which packs fit your work and removes the rest cleanly, links and index lines included (`node scripts/packs.mjs list` shows them).

| Pack | What it adds |
|---|---|
| core | Working with AI and Claude Code. Always kept |
| business | Offers, niches, funnels, pricing, selling AI work |
| creator | How YouTube, Shorts, TikTok and Instagram distribute posts, with posting checklists |
| web-design | Design quality, palettes, layout and motion for sites and interfaces |
| coding | Developer tools and techniques |
| study | The `/study` engine and the learning-science reference behind it |
| outreach | The `/outreach` engine and the cold-email playbook |
| community | A list of third-party skills worth installing, with install steps (`docs/community-skills.md`) |

## Getting updates

This repository keeps improving. Setup links your copy to it as a fetch-only `upstream`. Run `/update-aios` now and then: it lists what changed, applies on your yes, merges where you edited a shipped file, and never touches your brain, registries, voice files or learnings.

## Recommended connections

Nothing is strictly required, but setup walks you through the first three because most of the system leans on them:

| Connection | What it unlocks |
|---|---|
| Mail (Gmail or Microsoft 365) | Setup learns your people, recurring work and writing voice from sent mail. The morning and weekly e-mails, the morning check, inbox labels |
| Calendar | Today's agenda, clash warnings, deadlines with reminders |
| Cloud drive | Setup reads the documents you point at. Finished work lands where you keep it |
| GitHub CLI | The private backup |
| Obsidian | Browsing the brain as linked pages and a graph |

The full list, with the optional ones (a browser driver, web search, video tools, a second model for cross-checks), is in `connections.md`. Setup checks what you already have and recommends the next two or three based on your answers.

## Your notes stay private

- The session-end backup hook commits locally and pushes only when it can confirm that `origin` is a private repository. A public or unknown remote gets no push.
- `.env` is gitignored. Keys never enter the repository.
- During setup Claude reads only the sources you picked, never opens trash or spam, and sends nothing.

Never push a filled-in brain to a public fork.

## Make it yours

Everything is a text file, so change it. Tell Claude "new project: <name>" and it adds the page. Correct a result and the skill that produced it gets patched, so the same mistake does not come back. When a task shows up three times a week, Claude flags it and `/level-up` turns it into a skill.

## Credits

- The wiki follows the LLM-wiki pattern popularised by Andrej Karpathy. Its source pages summarise public videos and articles and credit each creator by name, with a link; the transcripts themselves are not included.
- The AI-tell catalogue in the writing skill is [blader/humanizer](https://github.com/blader/humanizer), MIT. See `THIRD-PARTY-NOTICES.md`.
- The offer and sales skills summarise methods from Alex Hormozi's *$100M Offers* and *$100M Leads*.
- For video ingest, the optional `watch` skill is [bradautomates/claude-video](https://github.com/bradautomates/claude-video).

## Licence

MIT. See `LICENSE`.
