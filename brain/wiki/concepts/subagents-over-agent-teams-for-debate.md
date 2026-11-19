---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, subagents, agent-teams, cost]
related: ["[[wiki/techniques/roast-room-council-debate]]", "[[wiki/sources/nateherk-roast-room]]", "[[wiki/concepts/parallelize-and-delegate]]"]
---

# Sub-agents over agent teams for multi-persona debate

Nate Herk says [09:16-09:37] he first built his roast room on Claude Code **agent teams**, then switched to plain **sub-agents** "after doing lots of testing", because agent teams were "more expensive for a minimal amount of actual value add". The sub-agents still end up "talking to each other": the facilitator (the main session) feeds each round's positions back to them, so the debate runs through the chair instead of peer to peer.

Grade: **creator-claimed**. No cost numbers, test set or comparison output were shown. Treat it as one practitioner's heuristic. For a debate with a fixed round structure and a central chair, a hub of sub-agents is enough. Pay for peer-to-peer teams only when the interaction cannot be routed through the chair.

## Related

Fits [[wiki/concepts/parallelize-and-delegate|Parallelize and delegate]] (independent legs in parallel, the main session synthesizes). Used by [[wiki/techniques/roast-room-council-debate|Roast room council debate]]; source [[wiki/sources/nateherk-roast-room|Nate Herk's roast room video]].

## In this system

`/jury` uses the same hub shape: parallel seats, with the main session as the chair that adjudicates.
