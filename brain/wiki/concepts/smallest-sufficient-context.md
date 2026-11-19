---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, context-engineering, tokens, skills]
related: ["[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code]]", "[[wiki/concepts/context-engineering-then-and-now]]", "[[wiki/concepts/progressive-disclosure]]", "[[wiki/concepts/intent-and-context-over-task-lists]]", "[[wiki/techniques/refactor-skills-for-newer-models]]"]
---

# Smallest sufficient context

Rule of thumb from Nate Herk, his gloss on Anthropic's applied-AI guidance: "the best context is the smallest amount of context that gets you the highest quality result at the cheapest cost." [02:11-02:22] The qualifier Anthropic adds, per Nate: minimal does not mean short, and a detail the model needs stays [02:24-02:30]. The rule's wording is creator-relayed; the Anthropic post itself says "avoid stating the obvious things Claude should know by looking at your file system or your repo". From [[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk, 10x Claude Code]].

## Keep vs cut

Nate's test when trimming a skill [05:58-06:57]:

| Keep | Cut or move |
|---|---|
| Intent and why ("a resource guide for students" drives analogies and simple explanations) | Things it can look up (a long folder listing) |
| Facts Claude cannot infer: voice, goals, audience, how the business works | The same instruction repeated in several files |
| Gotchas and landmines | A procedure for one job (video editing) sitting in always-loaded context; load it when that job runs |
| Pointers to deeper files | Step-by-step placement and format prescriptions on a task where the model now does better alone |

## Evidence quality

- Longer input hurts even with perfect retrieval: a 2025 paper, five models, drops of 13.9% to 85%. **Creator-cited, unchecked.** Nate warns it tested older models in controlled conditions and does not predict what trimming your CLAUDE.md does [02:32-02:56].
- On-demand tool definitions: 85% token reduction and MCP eval gains (49% to 74%, 79.5% to 88.1%). **Creator-cited.** These numbers are about deferred tool loading, which is a different thing from trimming prose [02:57-03:19].
- Nate's single self-experiment: his full AI operating system setup against a fresh session, on the same task (turning a Boris Cherny interview into a student guide). The fresh session was messier but better structured, with timestamps; the loaded one was prettier because of branding. n=1, judged by eye. His fix: keep branding and format in a skill, and give only the intent for structure [04:23-05:15].

## Related

A cousin of [[wiki/concepts/progressive-disclosure|Progressive disclosure]] (how things load) and [[wiki/concepts/intent-and-context-over-task-lists|Intent and context over task lists]] (what to say). [[wiki/techniques/refactor-skills-for-newer-models|Refactor skills for newer models]] is the action that follows. See also [[wiki/concepts/context-engineering-then-and-now|Context engineering then and now]].

## In this system

`CLAUDE.md` is kept as a router of pointers, with knowledge loaded from the brain only when a task needs it.
