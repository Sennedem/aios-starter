---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, audit, skills, handoff, prompting]
related: ["[[wiki/sources/nateherk-anthropic-engineers-10x-claude-code]]", "[[wiki/techniques/verify-before-returning]]", "[[wiki/concepts/smallest-sufficient-context]]"]
---

# Read-only workflow audit prompt

Nate Herk's prompt for finding the smallest fix in a multi-skill pipeline (his example: a raw YouTube idea to a filming-ready script). From [[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk, Anthropic engineers on 10x Claude Code]] **[09:43-10:52]**.

> "Audit this repo and show me the smallest change that would make the path from a raw YouTube idea to a filming-ready script faster. Use the systems already here. Cite the exact files you would reuse and do not edit anything yet."

Why it works, in his reading: it demands the *smallest* change, forces reuse of existing files, requires file citations so you can check the claim, and stays read-only until you approve.

## What it found (creator-observed, his repo)

- The outline skill gathered facts but did not have to save its evidence to a file the script skill could check, and the script skill had a hard "verify facts again" rule. The double check was deliberate, but redundant when the primary source had already been checked. Fix direction: hand the evidence forward in a file the next step reads.
- It counted 25 video folders with a script and only 3 with a `sources.md`, so the handoff convention was inconsistent (he notes this does not prove the others lacked research).
- Result: three edits across two existing skills, approved with a one-line reply.

## Pattern to reuse

In a pipeline of skills A to B, make A write a named evidence file, and make B read it and re-verify only what is missing. This applies [[wiki/techniques/verify-before-returning|Verify before returning]] across a handoff instead of inside one skill.

## In this system

`/audit` is the standing read-only audit of the whole setup; this prompt is the targeted version for one pipeline.
