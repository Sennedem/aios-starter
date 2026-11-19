---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=rL5tw6h78zo
tags: [concept, verification, evidence, research]
related: ["[[wiki/concepts/prove-its-work]]", "[[wiki/techniques/reverse-engineer-from-the-output]]", "[[wiki/tools/rea-reverse-engineer-anything]]", "[[wiki/sources/nateherk-reverse-engineer-anything-skill]]"]
---

# Seen / inferred / unknown

A three-way tag for every finding an agent reports about something it investigated. From [[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk on REA]] [09:36-10:23]:

- **Seen**: the agent actually found it and can cite where. Nate's example: Loom's 11 custom native add-ons.
- **Inferred**: the code or data points that way, but it is a guess.
- **Unknown**: the agent could not see it at all (the native recorder internals).

If you accept inferred items and build on them as if they were seen, you "get into some pretty messy situations" [10:05-10:14]. The tag stops a silent guess from becoming a foundation. The repo's own wording is evidence / confidence / limitations; "seen / inferred / unknown" is Nate's (and a Substack write-up's) plain-English shorthand.

## Where it applies

Any investigation whose output feeds a decision: a competitor scan, a research brief, a source check for an assignment, a diagnosis. It turns the habit of grading claims into three labels you can ask for in a prompt.

## Related

Extends [[wiki/concepts/prove-its-work|Prove its work]], which says "only report work you can point to evidence for" and to say so when something is unverified. Seen / inferred / unknown applies the same rule to findings about the world instead of the agent's own work, and adds an explicit middle bucket.

## In this system

`.claude/rules/common/verification.md`: anything unverified is stated as unverified, never rounded up to done. [[references/research-source-objectivity]] covers grading sources.
