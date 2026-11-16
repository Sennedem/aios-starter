# AIOS starter

A personal AI operating system for Claude Code. You clone it, open it, and Claude interviews you until it knows who you are, what you work on and how you work. From then on every session starts with that context instead of from zero.

It is a folder of plain files. There is no app and no server, and nothing leaves your machine unless you set up a backup.

## What you get

- **A second brain.** `brain/` is an Obsidian vault of markdown that Claude writes and keeps current: who you are, one page per project, your priorities, your decisions with their reasons, and a wiki of what you learn from videos, articles and PDFs.
- **A router.** `CLAUDE.md` tells Claude where everything lives, so it reads the one page a task needs and skips the rest.
- **21 skills.** Setup, a consultant-style interview, a decision jury, a writing route with an AI-tell filter, a weekly audit, an inbox labeller, an offer designer and more. The list is below.
- **Hooks that do the upkeep.** A first-run trigger, an inbox check, a date stamp on every edited note, a link checker, a private-only backup, and a guard that stops paid API calls you did not approve.
- **A dashboard.** One local HTML page with your tasks, deadlines, priorities and what is due.

## Install

You need [Claude Code](https://claude.com/claude-code), git and Node 18 or newer. [Obsidian](https://obsidian.md) is free and optional; setup offers to install it for you.

1. Click **Use this template** at the top of this page and create your own repository. Make it **private**: your brain will hold personal notes.
2. Clone your new repository and check the machine:

   ```bash
   git clone https://github.com/<you>/<your-repo>.git aios
   cd aios
   node scripts/doctor.mjs
   ```

   The check reports what is missing and prints the Obsidian install command for your system (`winget` on Windows, `brew` on macOS, `flatpak` on Linux).

3. Start Claude Code in that folder and say anything:

   ```bash
   claude "start"
   ```

Setup begins with the first message. You do not have to configure anything first.

If you cloned this repository directly instead of using the template button, that works too. Setup notices that `origin` points at the public starter, removes it on your yes, and offers a private backup at the end.

## What the first run does

| Phase | What happens |
|---|---|
| Open | Claude asks your name, checks the machine, and offers to install Obsidian and open the vault |
| Sources | "What can I build context from?" You pick: sent mail, calendar, cloud drive, folders, your LinkedIn or website, a CV or business plan dropped in `inbox/`, another AI's memory. You also say what is off limits. Claude reads only what you picked, read-only |
| Interview | Nine blocks, one question at a time: you, your work map with a mini-interview per project, priorities, how you work, where your time goes, people, tools and money, how Claude should behave with you, your writing voice |
| Write | The brain gets filled: context pages, one page per project, registries, tasks, the working agreements in `CLAUDE.md` |
| Hand over | A summary of what Claude now knows, the three best automation candidates from your week, and an offer to create a private backup |

A full run takes about an hour and is often fifty questions or more. Every answer is saved to `brain/brainstorms/` before the next question, so you can say "pause" and pick up tomorrow. Ask for the short version if you want fifteen minutes now and the rest later.

## Layout

```
CLAUDE.md          the router
connections.md     tools, connectors, accounts, budgets
cadence.md         recurring work: last run, next due
tasks.yaml         tasks and deadlines
inbox/             drop files here, Claude files them
otherworlds/       one note per external place (code repo, cloud folder, site)
dashboard/         the local HUD
scripts/           the link checker, the machine check, the hooks
.claude/           skills, rules, agents, hook wiring
brain/             the second brain (open this folder in Obsidian)
  context/         about you, your work, how you work, priorities, network
  projects/        one folder per business, job or course
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
| `/goal` | Captures a goal and routes it into priorities, tasks and cadence |
| `/deadline` | Puts a hand-in on your calendar with reminders |
| `/dashboard` | Refreshes and opens the HUD |
| `/ingest` | Files a video, article or PDF into the wiki as small linked pages |
| `/audit` | A weekly report on how complete and current your context is |
| `/level-up` | Builds one automation from your list of repeated tasks |
| `/janitor` | The weekly curator: recent sessions into the brain, stale context retired |
| `/memory-curate` | Tidies Claude's memory store, with your approval |
| `/inbox-janitor` | Labels your mail inbox. Labels only, it never sends or deletes |

Mail, calendar and drive skills use the connectors you have in Claude. Without a connector a skill says so and skips that step.

## Recommended connections

Nothing is required, and setup works with none of them. These give the most for the least effort:

| Connection | What it unlocks |
|---|---|
| Mail (Gmail or Microsoft 365) | Setup learns your people, recurring work and writing voice from sent mail. Morning check and inbox labels |
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

- The wiki follows the LLM-wiki pattern popularised by Andrej Karpathy.
- The AI-tell catalogue in the writing skill is [blader/humanizer](https://github.com/blader/humanizer), MIT. See `THIRD-PARTY-NOTICES.md`.
- The offer and sales skills summarise methods from Alex Hormozi's *$100M Offers* and *$100M Leads*.
- For video ingest, the optional `watch` skill is [bradautomates/claude-video](https://github.com/bradautomates/claude-video).

## Licence

MIT. See `LICENSE`.
