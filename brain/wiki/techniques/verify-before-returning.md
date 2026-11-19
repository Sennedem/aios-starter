---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, skills, anthropic, verification]
related: ["[[wiki/sources/nateherk-build-skills-not-agents]]", "[[wiki/concepts/persona-review-panel]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/techniques/read-only-workflow-audit-prompt]]"]
---

# Verify before returning

From Nate Herk relaying Anthropic's Barry Zhang and Mahesh Murag in [[wiki/sources/nateherk-build-skills-not-agents|Build skills, not agents]], who call it "probably the most important" of their four practical tricks: a skill should not hand over its first attempt and call the job done. The common failure they describe: the AI does 70 to 80% of the job, reports "done", and the human ends up doing the last 20 to 30% by hand, catching broken formatting, unsupported claims, or a script that falls flat for its audience. **[06:43-07:16]**

The fix is to build the checks a human would already run into the skill itself, matched to the artefact type **[07:16-07:31]**:

- **Slide deck:** render each slide as an image, inspect the screenshots, fix anything cropped, hard to read or out of bounds, and render again.
- **Research report:** open the primary sources, match claims to evidence, and remove anything that could not be verified.
- **Subjective work (script, ad, copy):** run a [[wiki/concepts/persona-review-panel|persona review panel]] and act on the issues that recur.

## The prompt template

> "Before returning the final output, define the acceptance criteria. Create the first version, inspect it using the relevant verification method, fix every issue you find, and then run another pass. Return the output only after it meets the criteria, with a short summary of what you checked. If something can't be verified, tell me exactly what remains." **[08:12-08:30]**

Where possible, set an **objective success metric** and keep working until the output hits it, instead of relying on a subjective final look. **[08:30-08:37]** The point of the loop: the first version becomes an internal draft that Claude reviews and improves before the human sees any of it. "Your first look should not be the agent's first look... it should be the agent's fourth or fifth or maybe even sixth look." **[08:37-09:00]**

## Related

Some checks are structural (a duration, a hash, a passing build), and some need someone to actually look. Only looking answers "is this good". [[wiki/concepts/prove-its-work|Prove its work]] covers the same idea from a different Nate Herk video. [[wiki/techniques/read-only-workflow-audit-prompt|Read-only workflow audit prompt]] applies it across a handoff between two skills.

## In this system

`.claude/rules/common/verification.md`: "done" is a claim and verification is evidence; report what was checked and state anything unverified as unverified.
