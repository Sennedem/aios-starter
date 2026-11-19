# Community skills worth installing

Part of the **community** pack. These are third-party skills that work well next to this system. Nothing here is copied into the repository: each one keeps its own licence and its own updates, so you install it from its source. Install commands were checked against each project's README in November 2026; if one fails, the project's README has the current command.

**Before installing anything:** a skill or plugin is code and instructions that run with your permissions. Install only from the official repository named here, read what it adds, and add one at a time so you can tell what changed. Note each install in `connections.md`.

## How Claude Code installs them

Most come as plugins from a marketplace. Inside Claude Code:

1. Add the marketplace once: the plugin command with `marketplace add <owner>/<repo>`.
2. Install a plugin from it: the plugin command with `install <plugin>@<marketplace>`.
3. Restart the session. The plugin's skills show up next to the ones in `.claude/skills/`.

Some are single skills you copy into `.claude/skills/<name>/` (this folder, for this system only) or `~/.claude/skills/<name>/` (every folder you open).

## The list

| What | Why it is worth it here | Source and install |
|---|---|---|
| **Anthropic's own skills** (documents, design, testing web apps, MCP servers) | Reference implementations from the people who built skills: Word, PowerPoint, Excel and PDF handling, a web-app tester, a skill creator | github.com/anthropics/skills. Marketplace `anthropics/skills`, then install `document-skills@anthropic-agent-skills` or `example-skills@anthropic-agent-skills` |
| **frontend-design** | Pushes generated sites and interfaces away from the template look. Pairs with the web-design wiki pages | Same marketplace as above, or the Frontend Design plugin on claude.com/marketplace |
| **ECC (Everything Claude Code)** | A large collection of agents, skills and rules. The useful ones for this system: `search-first` (look before building), `deep-research` and `market-research` (cited research), `security-scan` (checks `.claude/` config for injection and misconfiguration), `strategic-compact` (when to compact a long session), `token-budget-advisor`, `verification-loop`, `eval-harness`, `prompt-optimizer`, `claude-api`, and the agent-workflow skills (`agentic-engineering`, `autonomous-loops`, `blueprint`) | github.com/affaan-m/ECC. Whole plugin: marketplace `https://github.com/affaan-m/ECC`, then install `ecc@ecc`. It adds hundreds of skills, so most people are better served picking a few: clone the repository and copy only the skill folders you want into `.claude/skills/`. Do not combine both ways. Install only from the official repository; the project warns about unofficial mirrors |
| **humanizer** | The AI-writing-tell catalogue the `/writing` skill already ships (`.claude/skills/writing/references/humanizer.md`). Install it only if you want it as a separate skill elsewhere | github.com/blader/humanizer (MIT) |
| **watch** (claude-video) | Lets Claude watch a video from a link: downloads it, takes frames, pulls the transcript. Makes `/ingest` work on videos without captions | github.com/bradautomates/claude-video. Needs `yt-dlp` and `ffmpeg` (see `connections.md`) |
| **Addy Osmani's agent skills** | About 25 spec, plan and build skills that keep the plan in files. For people who build software with agents | See `brain/wiki/tools/addy-osmani-agent-skills.md` (coding pack) for what it is and where it lives |

## Overlap with what you already have

Some of these do what a built-in skill here already does. Where they collide, keep one, so Claude is not choosing between two descriptions for the same request (`.claude/rules/common/skills.md`):

- `verification-loop` overlaps the verification rule and `/five-gates`.
- `deep-research` overlaps the `researcher` agent.
- `prompt-optimizer` overlaps `/anthropic-prompt`: that one asks you for what is missing, the optimizer infers it.

When you add one, run `/audit`: its skill-description check flags overlaps.
