---
name: second-opinion
description: Get a cross-model second opinion from outside the Claude family. OpenAI Codex runs headless (`codex exec`, Claude runs it itself), and any other outside model the user has access to (a chat app, a research mode) runs by hand, with the user pasting a prompt Claude writes and bringing the answer back. It challenges Claude's work on decisions, writing, research or code, and every outside answer is adjudicated point by point. Use when the user says "get a second opinion", "/second-opinion", "challenge this with Codex", "what does GPT think", "write me a prompt for another model", "I'll run a deep research on this", or drops an outside model's answer in the inbox; also offered on genuinely contested go/no-go calls through /jury. Review-only: outside models never edit files and never ghostwrite.
---

# second-opinion: an outside model as challenger

A Claude skeptic subagent fixes anchoring and self-agreement but shares Claude-family blind spots. A model from another family has different training and different errors, so disagreement between the two is real signal. The outside answer is a challenge, never a verdict.

## Preconditions

- Codex lane: the Codex CLI is installed (`codex --version`) and logged in (`codex login status`). If it is not logged in, stop and give the user the one-liner `codex login`. Do not switch to a paid API key without the user's explicit go; record which auth and plan they use in `connections.md`.
- Every outside model is metered somewhere. If a run fails with a rate or usage error: stop, report, do not retry in a loop.
- No Codex and no other outside model: say so and offer a Claude skeptic subagent instead, labelled as same-family.

## Codex invocation

Always through a clean, non-interactive shell, always read-only:

```
codex exec --sandbox read-only --skip-git-repo-check -C "<dir-of-artifact>" "<PROMPT>" < /dev/null
```

- `< /dev/null`: without it, exec waits on stdin when the shell leaves it open.
- `--sandbox read-only`: Codex can read but cannot write. Never lift this.
- `--skip-git-repo-check`: artifacts often live outside a git repo.
- `-C <dir>`: the artifact's folder, so relative reads work.
- exec prints a session header (workdir, model, sandbox) before the answer. Read the model name from it once per run and report it; strip the rest. The answer is at the end of the output, after any tool noise.
- There is no `--ask-for-approval` flag in exec mode; passing it errors.
- Model: omit `-m` and take the account default, unless `connections.md` records a pinned model. If the header shows a small or unfamiliar model, pin a stronger one in Codex's own config file and note it in `connections.md`.
- If the sandbox blocks Codex from reading files on this platform (it answers that every shell read was "blocked by policy"), embed the file contents in the prompt and pipe it in: `codex exec --sandbox read-only --skip-git-repo-check < prompt.txt`. Large prompts (tens of KB) work fine this way.
- Parallel runs: at most 2 at once. This is a scarce resource, not a fan-out tool.

### Context Codex gets

Codex reads `AGENTS.md` files from the repo root down to `-C`'s folder. Keep them thin: the review contract and load-bearing facts only (who the user is, the currency, what stage the project is at), plus pointers to `brain/projects/<slug>/CONTEXT.md` and `brain/decisions/log.md` for self-serve checks. Never put strategy or conclusions in them; briefing the skeptic with the author's worldview destroys the independence that makes its disagreement worth having.

## Prompt templates (refute by default)

Every prompt starts with the shared contract, then one lens. Fill `{file}` with the artifact path relative to `-C`, or paste the artifact below the contract.

Shared contract (always first):
> You are an adversarial reviewer. Read {file}. Your job is to find the strongest case that this is WRONG, weak, or incomplete. Do not be agreeable. Anchor every finding to a specific location (section, paragraph, line). If something is genuinely solid, say so in one line and do not pad. Return at most 15 lines: verdict first (1 sentence), then findings ranked by severity, each as location → problem → why it matters.

Lenses (append one):
- Decision or plan: "Attack the load-bearing assumption. What has to be true for this to work, and what evidence in the doc actually supports it? Name the strongest alternative the author did not take and why they might regret it. Flag any option dismissed without argument."
- Writing: "Critique argument structure, factual claims and persuasiveness for the stated audience. Do NOT rewrite or propose replacement prose; findings only." Rewrites go through the `writing` skill in the main session; outside models never ghostwrite.
- Research: "Attack the sourcing: which claims rest on one source, on the subject's own materials, or on inference presented as fact? What counter-evidence or missing angle would a hostile reviewer raise?"
- Code: "Hunt for correctness bugs, unhandled failure modes and security issues. Give a concrete failure scenario per finding: inputs or state → wrong outcome."
- Compliance: "Check this against the rules that apply to it. Quote the rule for every finding; flag any claim of compliance that rests on an assumption."

## Adjudication (main session, never skipped)

1. Before reading the outside answer, write down your own ranking of the weak points, so agreement means something.
2. Weigh each finding: agree, reject or investigate, one line of why per point. Never silently adopt, never silently drop.
3. Check the outside model's factual claims against the source before adopting them. Outside reviewers sometimes build a finding on a wrong reading of the artifact.
4. Never reject a finding on the strength of a green status you have not opened. A job that "succeeded" may have swallowed the very error the finding names. A finding stays "investigate" until a log or output, not a badge, disproves it.
5. When the finding is about a cause ("this is the root cause"), list which links of the chain were observed and which were inferred before calling it proven.
6. Where the outside model and Claude disagree, that is the headline. Surface it to the user explicitly; do not average it away.
7. Report which model actually ran.

## The manual lane (the user as courier)

For outside models with no programmatic access (a chat app, a model picker, a deep-research mode), Claude writes the prompt and the user carries it. The transport costs the user a minute or two; the payoff is one or more extra model families on a call that matters.

When to offer it: a genuinely contested go/no-go where one outside model is thin diversity, or a load-bearing factual claim worth an independent check. Not for routine drafts or mechanical work.

How it runs:
1. Claude writes the prompt (the same shared contract and lens) in one copy-paste block and names which model to pick from what the user has. Prefer the strongest non-Claude model; pick a different vendor than Codex when the point is a third view. Never pick a Claude model in the outside tool; it shares Claude's blind spots.
2. The user pastes it, then brings the answer back.
3. Claude adjudicates it exactly like a Codex answer and reports which model produced it.

Two modes:

| Mode | When | Prompt | Setting |
|---|---|---|---|
| Review | Challenge a draft verdict, plan or piece of writing | Shared contract plus lens, with the artifact pasted in | A named model, normal search |
| Deep research | A research-heavy question where an independent research leg beats one more critic | The situation in hard numbers, 4 to 6 numbered questions, "cite recent sources", "flag anything anecdotal", end with a ranked action list | The tool's deep-research mode |

A deep-research result is a juror, not a source of truth. Its typical failure is confident synthesis from SEO blogs; it usually states its own evidence limits, so read those sections first. Check its load-bearing claims against the live data and any Claude research legs, and say where it disagrees with them.

Return path: the user pastes the answer, shares a public link, or drops an exported file in `inbox/` (or a second cloud inbox, if `connections.md` lists one). If a shared link only half-loads through a scraper, try a headless browser that scrolls the whole page before asking the user for an export: a link they gave is a result they delivered, and reading it is Claude's problem. File the result into the brain next to the work it served and empty the inbox.

Data rule: anonymise identifiers of third parties (names, companies, addresses) before pasting client or customer material into an outside tool, keeping the problem structure. Turn off the tool's training-on-your-data setting once. The user's own strategy, writing and public research need no anonymisation.

## When it runs

- On demand: the user asks. Any artifact type. If they say only "/second-opinion" with no target, take the artifact shown or discussed last; ask if two are equally recent.
- Contested calls: genuine go/no-go or strategic decisions run through `/jury`, which seats Codex as the outside skeptic using this skill's invocation. When `/jury` runs, offer the manual lane in one line with a ready prompt.
- When the user calls outside output they brought in (another model's report or answer) "the second opinion", that output is the second opinion: adjudicate it point by point and do not dispatch Codex unless they ask for it too.
- Never auto-run on routine drafts or mechanical work; never expand scope.

## Feedback

When the user corrects how a second opinion was used (wrong trigger, too deferential, too dismissive, wrong lens), append a dated before → after line to `references/learnings.md` in this folder (create it at the first correction). When a run reveals a change in model, plan or caps, update `connections.md`.
