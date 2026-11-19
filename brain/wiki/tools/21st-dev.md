---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FFWtxjvW2ts
tags: [wiki, tool, web-design, ui-components]
related: ["[[wiki/techniques/inspiration-driven-site-prompting]]", "[[wiki/tools/design-inspiration-galleries]]", "[[wiki/concepts/ai-website-slop]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]"]
---

# 21st.dev

A UI component gallery where each component ships with a "copy prompt" button. You hand that prompt text to an AI coding agent, and it reproduces the component in your own project. Named repeatedly in [[wiki/sources/nateherk-fable-5-1-kills-website-slop|Nate Herk's "Fable 5.1 kills website slop" video]].

## How it's used

Nate browses it for individual pieces rather than whole-page templates: backgrounds, gradients, interactive elements, borders, buttons, an FAQ section layout, a "container scroll" component. For each one: "you can literally give your AI agents the prompts for these animations… copy prompt and then your agent can basically copy that element." He used it for his personal site (a background and an interactive element) and listed it as a standing inspiration source in the one-shot prompt behind two other demo sites.

## Why it beats asking the model to invent components

It avoids [[wiki/concepts/ai-website-slop|AI website slop]] at the component level, the same way named reference sites do at the page level. The model copies a proven, specific pattern instead of generating "a button" or "an FAQ section" from a brief made only of adjectives.

Use it for the "gather real references before writing frontend code" step at component granularity. For the page and site level, see [[wiki/tools/design-inspiration-galleries|design inspiration galleries]].
