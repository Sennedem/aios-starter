---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, subagents, decision-making, council, persona]
related: ["[[wiki/sources/nateherk-roast-room]]", "[[wiki/concepts/expert-persona-brain-files]]", "[[wiki/concepts/subagents-over-agent-teams-for-debate]]", "[[wiki/concepts/persona-review-panel]]", "[[wiki/techniques/stress-test-with-subagents]]", "[[wiki/techniques/give-agent-context-via-aios-and-grill-me]]", "[[wiki/techniques/interview-before-building-an-automation]]"]
---

# Roast room: a council of expert sub-agents debates your decision

A reconstruction of Nate Herk's roast-room skill ([[wiki/sources/nateherk-roast-room]], 2026-10-22), as far as the video supports it. Grades: **[shown]** = on screen in the video, **[claimed]** = Nate said it but did not demonstrate it, **[not shown]** = a gap you would have to fill yourself. The repo was not opened to the viewer beyond folder listings, so the SKILL.md text and the exact prompts are **[not shown]**.

## What it is

A Claude Code skill that takes one business decision and runs it past a council of named expert personas, each a sub-agent with its own written "brain". The personas debate over several rounds, and the run ends in a vote, a score and a verdict. A local web page (the Glydo app, a sponsor-linked tool) draws the debate as cartoon characters; Nate says this is "just a visual layer" and the sub-agents run the same without it [00:58-01:20, 08:58-09:16]. **[shown]**

## The ingredients (file layout) **[shown]** [01:51-04:20]

- `.claude/agents/<name>.md`: one short markdown file per council member (Bezos, Buffett, Graham, Gary V, and others). Per Nate, it holds how that person debates, how they talk, and their lens.
- `skills/roaster-room/brains/<name>/`: one folder per member with nine files: `hot` (the "pillar" question plus what the brain was built from), `books`, `frameworks`, `positions`, `principles`, `sources`, `stories`, `voice` (Leila Hormozi's folder, listed on screen; Musk's later folder lists the same set). Detail in [[wiki/concepts/expert-persona-brain-files]].
- A default roster of **seven** advisors plus **four extras**, 11 seats in all (extras named: Naval, Cody Sanchez, Sara Blakely, Leila Hormozi) [01:42-01:50]. The other default names on screen: Bezos, Paul Graham, Alex Hormozi, Gary V, Dan Martell, Gino Wickman, Warren Buffett.
- A `new-roster` skill that builds a new member on request ("Elon Musk"): it creates the brain folder, the agent file, the sources, and a cartoon portrait for the UI [06:14-06:47, 13:59-14:29]. **[shown]** The research method behind a brain is **[not shown]**. The Leila page claims 48 sources, about 0.5M words from 2021 to 2026, 14 interviews and 34 of her own videos **[claimed by the page, unaudited]**.

## The seats: one question each

Each seat owns exactly one question, which stops seven personas from giving the same generic answer. Questions stated in the video [00:37-00:53, 08:41-08:46, 03:44-03:49]:

| Seat | Question |
|---|---|
| Warren Buffett | What does it do to cash, risk and long-term value? |
| Alex Hormozi | Will people pay, how much, and how do we close? |
| Gino Wickman | Can the business run this without the founder holding it together? |
| Naval | Does this build leverage and equity you own, or rent out your time? |
| Dan Martell | Protecting the founder's time (swapped out for the event example) |
| Leila Hormozi | Can your team and leadership carry this, and who has to change? |

The questions for Bezos, Graham and Gary V were not stated. **[not shown]**

## The run, step by step **[shown]** [06:56-13:30]

1. **Input.** Natural language ("do this on the roast room council") or the skill's slash command. Nate's advice: give a **decision**, **two or three options**, and **context** so the council can reason [07:18-07:26]. His demo: where to host a summer-2027 in-person event; options San Francisco, Salt Lake City, Austin, Chicago; criteria sponsors, incentives, airports, transit, food, activities.
2. **Context gathering.** The skill loads, then asks clarifying questions if it thinks it lacks context (four in the demo, including event size and budget) [07:56-08:50].
3. **Seat selection.** The skill recommends who sits at the table for this decision and lets the user edit. In the demo it dropped Dan Martell (time protection was irrelevant) and added Naval [08:56-09:50]. The default is the standard seven, adjusted per topic.
4. **Round 1: opening positions.** Each member writes a position independently. The UI shows their vote (A or B), a score out of 10, the risk, and what they would do [10:12-11:20].
5. **Round 2: cross-examination.** Members read each other's positions and attack them ("poke holes"). On the opening screen, Bezos, Graham and Hormozi all went after Gary V, and Buffett went after Hormozi [00:20-00:36, 11:20-11:30].
6. **Anti-consensus rule.** If everyone agrees, the chair (Claude Code as facilitator) forces one member to argue another side as devil's advocate [11:30-11:42]. **[claimed]**: it did not trigger in the demo because the vote was not unanimous (only Naval picked San Francisco).
7. **Round 3 and final votes.** The opening teaser says "after all three of those rounds" [00:53]; the demo ends with "final votes" and an aggregate score (Salt Lake City, 7.9/10 at that point) [13:15-13:25]. What round 3 contains is **[not shown]**.
8. **Verdict and artefacts.** A final verdict (option C in the teaser, Salt Lake City in the demo), key points per member, who conceded to whom, who disagreed most, and a downloadable PDF [13:25-13:48]. Everything is stored locally under a project folder ("Founder Council") as sessions containing `brief`, `round-1`, `round-2`, `verdict` and each member's session log, so debates can be reopened and questioned later [09:57-10:40].

How the aggregate score and verdict are computed (a mean, a weighting, or the chair's judgment) is **[not shown]**.

## Rebuild checklist

1. N agent files, each with a voice, a debate style, a lens and one focus question.
2. N brain folders with the nine-file schema above, filled from real material (books, interviews, talks), all built the same way.
3. A skill with: intake (decision, options, context), a clarify step, seat recommendation, round 1 independent positions with a vote and a 1-10 score, round 2 mutual attack, a devil's-advocate trigger on unanimity, a final vote, and a verdict.
4. A session folder per run with one file per phase.
5. Optional: a PDF export and a visual layer.

## Calibration notes

- Nate's own position: he does **not** accept the council output blindly; its value is the perspectives he would not have raised himself [12:22-13:10]. **[claimed]**
- His demo checks the verdict against a decision already made (the event was already booked in Salt Lake City) [13:45-13:52]. That is a single agreeing data point, not a validation, and the question was a low-stakes logistics choice with options he had already narrowed.
- "Each persona reasons like the real person" rests on written summaries of public material; fidelity was not tested in the video. **[not shown]**

## Related

[[wiki/concepts/persona-review-panel|Persona review panel]] reviews a finished artefact; this skill debates a choice before it is made. [[wiki/techniques/stress-test-with-subagents|Stress-test with subagents]] is the same many-agents-attack idea applied to a build. The intake step is the decision-scale version of [[wiki/techniques/give-agent-context-via-aios-and-grill-me|giving the agent context first]] and of [[wiki/techniques/interview-before-building-an-automation|interviewing before building]].

## In this system

`/jury` runs a smaller council on one decision and ends in green-light, reshape or kill plus the cheapest test.
