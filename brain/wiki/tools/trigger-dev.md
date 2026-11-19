---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: coding
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/FqnNL8fnUWo
tags: [wiki, tool, trigger-dev, hosting, automation]
related: ["[[wiki/tools/codex-sdk]]", "[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/concepts/subscription-vs-api-hosting]]", "[[wiki/concepts/routine-drift]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]"]
---

# trigger.dev

A TypeScript task host with a free tier that runs code independently of any chat subscription. In [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk's Astra automations video]], Codex writes the automation as code and pushes it to a **GitHub repo**; trigger.dev syncs to that repo and hosts the schedule or webhook that runs it: "just think of it as giving your skills to something else to run" [01:19-01:22]. Environment variables (API keys, IDs) are pushed in over the CLI instead of typed by hand, once Codex is authenticated to both GitHub and trigger.dev [17:21-17:34].

## What the web console gives you

- A Tasks view per run with status, payload and output, so a failed run's data can be copied straight back to Codex for a fix [16:57-17:07].
- Longer flows split into a scheduler task that calls a separate "runner" task, so sub-tasks give you visibility into multi-step flows [16:24-16:41].
- A per-project GitHub connection that has to be verified explicitly. Nate hit a "GitHub isn't connected" snag and had Codex fix it through browser use [14:57-15:43].

## Known limit (creator-observed)

The free plan's scheduling window "can delay a 6 a.m. start by up to an hour", a real constraint for time-sensitive triggers [08:04-08:14].

The language is TypeScript; the Python equivalent Nate names is Modal [03:09-03:16]. See [[wiki/concepts/subscription-vs-api-hosting|subscription vs API hosting]] for why this category exists, and [[wiki/concepts/routine-drift|routine drift]] for the failure mode it helps avoid.
