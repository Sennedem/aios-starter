---
name: audit
description: Score the AIOS against the Four Cs (Context, Connections, Capabilities, Cadence), lint the brain's content layer, check skill descriptions for collisions, and surface the top 3 leverage-weighted gaps with the next command for each. Read-only; writes only its dated report to brain/audits/. Use weekly, or when the user asks "is my AIOS working?", "audit my setup", "what's missing", "/audit".
---

# /audit: Four-Cs health check

Read-only. Scan the OS and the brain, score it, and name the 3 highest-leverage gaps with concrete next commands. Optionally save the report to `brain/audits/audit-<YYYY-MM-DD>.md`.

## What to scan

- OS: `CLAUDE.md`, `connections.md`, `cadence.md`, `tasks.yaml`, `otherworlds/*`.
- Brain: `brain/context/*`, each `brain/projects/*/CONTEXT.md`, `brain/decisions/log.md`, `brain/references/`.
- `.claude/` (skills, agents, rules) and which global skills are available.
- The memory index (`MEMORY.md` in the Claude Code memory directory for this project) and whether session context is being updated.

## Scoring (0 to 100, 25 per C)

- **Context (25):** does the OS know the user, their projects, priorities and voice? Penalise `_TBD_` gaps and empty context pages.
- **Connections (25):** are the domains in `connections.md` reachable (revenue, customers, calendar, comms, tasks, meetings, knowledge)? `todo` and `partial` lose points.
- **Capabilities (25):** are there skills and agents that execute real recurring work? Includes a delegation check (standard: `.claude/rules/common/agents.md`): (a) does `.claude/agents/` match the current workload in `brain/context/priorities.md`, where an active project or recurring block with no matching worker is a gap; (b) do the read-heavy skills carry explicit fan-out and model-routing steps, or do they grind bulk work in the main model; (c) roster sprawl: agents nothing has dispatched in about a month are candidates to prune.
- **Cadence (25):** is anything running on a rhythm (weekly `/janitor`, `/level-up`, session auto-persist, scheduled jobs)? Rows in `cadence.md` with no evidence of a recent run lose points.

## Output

1. A short scoreboard: each C, the total, and a stage label (Foundation, Wired, Capable, Autonomous).
2. **Top 3 gaps**, ranked by leverage (a missing tier-1 connection or an unstaffed money-making project outweighs cosmetics).
3. For each gap, the concrete next step ("connect the calendar and record it in connections.md", "fill the open questions in brain/projects/<slug>/CONTEXT.md", "add a weekly /level-up row to cadence.md").
4. **Hand-off:** name which gap is the `/level-up` candidate of the week (the most automatable one, not necessarily number 1). If the user is present, offer to run `/level-up` on it now. Audit diagnoses, level-up ships; they stay separate skills because audit can run unattended and level-up cannot.

## Wiki lint (content-layer integrity)

The mechanical checks are scripted. Read `brain/audits/janitor-latest.md` (written by `node scripts/brain-janitor.mjs`) first and quote its summary counts for checks 1 to 5. Do not re-derive them by reading the vault. If the report is older than 3 days or missing, say so and run the script. Checks 6 and 7 need judgment and stay with this skill.

Scope: the brain's content pages (`brain/README.md`, `brain/conventions.md`, `brain/context/*`, `brain/decisions/log.md`, `brain/projects/*/CONTEXT.md`, `brain/references/*`, `brain/wiki/`). Exclude `brain/templates/`, the OS layer (it uses plain markdown links; wikilink rules apply to the brain only) and the memory directory.

1. **Orphans:** pages with no inbound `[[link]]` and not listed in `brain/README.md`; pages missing a `parent:` frontmatter link.
2. **Broken wikilinks:** any `[[target]]` whose file does not exist.
3. **Missing from index:** pages on disk that `brain/README.md` does not list.
4. **Stale:** `updated:` older than 21 days, oldest first; pages with no `updated:`; pages edited in git after their `updated:` date.
5. **Open markers:** `_TBD_`, `TODO`, "TBD", "open question", "(date TBD)", with file and line.
6. **Missing pages:** entities named 3 or more times across the brain with no page of their own. Suggest, never create.
7. **Possible contradictions:** claims that conflict across pages (a page linked as active that another calls retired; a status that disagrees with `connections.md`). Read the newest `brain/audits/janitor-*.md` first: its *Questions for the user* already lists contradictions found in sessions. Quote it and add only what it missed. Never auto-resolve.

## Skill-description collisions

Read every `.claude/skills/*/SKILL.md` frontmatter `description`. Claude routes on these lines alone, so two skills that could both answer one request are a defect. Flag each pair with the request that would trigger both and name the owner: `- [collision] skill-a / skill-b: "<request>" → owner: skill-a`. Apply the three-prompt test from `.claude/rules/common/skills.md` only to descriptions changed since the last audit. Suggestions only, no rewrites.

## Report format

Append a `### Wiki lint` block under the scoreboard, one finding per line: `- [check] file:line: issue → suggested fix`. Roll broken links and orphans into the Context score as a small penalty. Do not modify any file except the optional dated report (frontmatter: `type: log`, `status: active`, `domain: meta`, `parent: "[[README]]"`, `updated:`).
