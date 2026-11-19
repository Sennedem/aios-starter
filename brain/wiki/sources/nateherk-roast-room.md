---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=DSS1Yqb6-qE
tags: [wiki, source, youtube, subagents, council, decision-making]
related: ["[[wiki/techniques/roast-room-council-debate]]", "[[wiki/concepts/expert-persona-brain-files]]", "[[wiki/concepts/subagents-over-agent-teams-for-debate]]", "[[wiki/concepts/persona-review-panel]]", "[[wiki/techniques/stress-test-with-subagents]]", "[[wiki/techniques/give-agent-context-via-aios-and-grill-me]]", "[[wiki/techniques/interview-before-building-an-automation]]"]
---

# Nate Herk: "Roast Room: How I Use Claude to Think Like the Top 1%"

YouTube, 15.0 min, Nate Herk | AI Automation, published 2026-10-22: https://www.youtube.com/watch?v=DSS1Yqb6-qE. (The video title writes the skill name as a slash command.)

A demo and walkthrough of Nate's roast-room skill for Claude Code, in which sub-agents modelled on famous founders debate a business decision and return a vote and a verdict.

## Key takeaways

1. **A council of seats, one question each:** Buffett (cash, risk, long-term value), Hormozi (will they pay, how do we close), Wickman (can it run without the founder), Naval (leverage vs renting out your time) [00:37-00:53, 08:41]. Full reconstruction: [[wiki/techniques/roast-room-council-debate|roast room council debate]].
2. **Persona = a thin agent file plus a brain folder** of nine files (hot, books, frameworks, positions, principles, sources, stories, voice) [02:00-04:20]. See [[wiki/concepts/expert-persona-brain-files|expert persona brain files]].
3. **The visual layer is optional:** the web UI (Glydo) is "just a visual layer"; the sub-agents run without it [01:06-01:20, 09:08].
4. **Input discipline:** a decision, 2 or 3 options and context. The skill asks clarifying questions and recommends who sits at the table [07:18-09:06].
5. **Rounds:** independent openings with a vote and a 1-10 score, then cross-attack, then final votes, with a forced devil's advocate if everyone agrees [10:49-11:42, 13:15].
6. **Sub-agents beat agent teams** on cost for value, creator-claimed [09:16-09:37]. See [[wiki/concepts/subagents-over-agent-teams-for-debate|subagents over agent teams for debate]].
7. **Storage:** every session is saved locally with the brief, round 1, round 2, the verdict and per-member logs, plus a PDF export for sharing [00:58-01:05, 09:57-10:40].
8. **Scale by skill:** a `new-roster` skill builds a new expert end to end, portrait included (Musk demoed) [06:14-06:47, 13:59-14:35].
9. **Mindset close:** use councils as perspective generators, not oracles; "follow someone who has walked the path" over trusting the model's gut or your own [12:00-13:10].

## Claim grades

- Demonstrated on screen: the UI run, the folder layout, the vote and score display, the saved session files, the Musk build.
- Creator-claimed: agent teams cost more for little extra value; persona brains are built from 48 sources and 0.5M words (read off a file, not audited); the devil's-advocate rule (stated, not triggered); the council output is useful.
- Not shown: the SKILL.md text, the prompts, how the verdict and aggregate score are computed, what round 3 is, how the brains are researched, how a sub-agent chooses which brain files to load.

## Skeptic note

- The single validation is the event demo, and it is circular: Nate had already booked Salt Lake City, picked the four options himself, and the council agreed (7.9/10). One agreeing, low-stakes data point proves nothing about decision quality.
- Seven LLM personas share one underlying model, so their agreement is weaker evidence than seven humans agreeing. The seat-specific question creates the real diversity, not the famous names.
- Personas of living people are caricatures built from public text; their fidelity was never tested.
- Sponsored segments: Fish Audio (04:45-06:13, an unrelated ad read) and Glydo (a free-month link, product promotion at 01:52). The skill is distributed through Nate's free community, so it cannot be inspected from the video alone.
- Nate's own caveat (do not blindly accept the verdict) is the right one.

## Pages from this source

[[wiki/techniques/roast-room-council-debate|Roast room council debate]] · [[wiki/concepts/expert-persona-brain-files|expert persona brain files]] · [[wiki/concepts/subagents-over-agent-teams-for-debate|subagents over agent teams for debate]]. It also extends [[wiki/concepts/persona-review-panel|persona review panel]], [[wiki/techniques/stress-test-with-subagents|stress-test with subagents]], [[wiki/techniques/give-agent-context-via-aios-and-grill-me|give your agent context]] and [[wiki/techniques/interview-before-building-an-automation|interview before building an automation]].

## In this system

`/jury` is the same idea with fixed seats (skeptic, fact-checker, buyer, lens seats) and a forced dissenter, ending in a verdict and the cheapest test to check it.
