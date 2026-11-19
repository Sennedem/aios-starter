---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, persona, subagents, knowledge-base]
related: ["[[wiki/techniques/roast-room-council-debate]]", "[[wiki/sources/nateherk-roast-room]]", "[[wiki/concepts/persona-review-panel]]"]
---

# Expert persona: thin agent file, fat "brain" folder

Nate Herk's pattern in [[wiki/sources/nateherk-roast-room|his Roast Room video]]: to make a sub-agent think like a named expert, split the persona in two [02:00-04:20]. **[shown: folder listings and a few file opens]**

- **Agent file** (`.claude/agents/<name>.md`): short. How the person debates, how they talk, their lens. Nate: it "isn't really that long".
- **Brain folder** (`skills/roaster-room/brains/<name>/`): the substance, with the same schema for every person:
  - `hot`: the one pillar question the person asks, plus provenance (for Leila Hormozi: 48 sources, about 0.5M words from 2021 to 2026, 14 interviews, 34 own videos **[claimed by the file, not audited]**)
  - `books`, `frameworks` (Dan Martell: buyback principle, buyback rate, time-and-energy audit, DRIP matrix), `positions` (pricing, discounting, raising money, debt), `principles` (eight decision rules per person), `sources`, `stories`, `voice`

Why the split matters: a fixed schema makes every persona buildable the same way by a `new-roster` skill (one prompt, "Elon Musk", produced the folder, the agent file and a portrait [06:14-06:47, 13:59-14:29]), and the agent file stays cheap to load while the brain is pulled in only when the persona reasons. How the sub-agent decides which brain files to read is **[not shown]**.

## The idea behind it (creator-claimed)

Borrow proven domain expertise instead of trusting the model's gut: find the best copywriter (or operator) in the world, extract their frameworks, examples and decision habits, and put them on the council. "Following someone that's actually walked the path you want to walk is a pretty good signal" [12:00-12:50]. Nate also says the output is a perspective generator, not an oracle.

## Skeptic note

A brain built from public material gives the model a caricature of the stated frameworks, not the person's judgment on your facts; real experts often depart from their own published rules in a specific case. Fidelity was not tested. It is also a legal and ethical grey area when the persona is a living person presented as speaking for them (not discussed in the video). The reliable part is the forced diversity of questions, one lens per seat, which works even with fictional lenses.

Related: [[wiki/techniques/roast-room-council-debate|Roast Room council debate]], and [[wiki/concepts/persona-review-panel|Persona review panel]], where the personas are roles like "beginner" or "skeptical buyer" with no expert brain.

## In this system

`/jury` keeps the reliable part and drops the personas: each seat is a lens with one question, since several personas on one model share the same errors.
