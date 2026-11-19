---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, web-design, verification]
related: ["[[wiki/concepts/ai-website-slop]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/tools/scroll-craft]]", "[[wiki/tools/playwright-cli]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]", "[[wiki/sources/nateherk-6-best-github-repos-for-claude]]"]
---

# Screenshot scroll verification

Verify a scroll-heavy site by having the agent screenshot the scroll itself, frame by frame or pixel by pixel, instead of trusting that the code behind the scroll animation is correct. From [[wiki/sources/nateherk-fable-5-1-kills-website-slop|Nate Herk, Fable 5.1 kills website slop]], the last of his seven rules for non-slop websites.

## The technique

"Have it screenshot everything. Especially when you're doing scroll animations, have it screenshot frame by frame or pixel by pixel as it's... scrolling down. That way it's essentially watching a video of how you will experience it." The agent then reviews the sequence itself, flags anything that "looks bad... out of bounds... this color's off," and fixes it before calling the build done.

It pairs with his sixth rule, a **mobile check that is not optional**: "so many people are looking you up on mobile... make sure it's verified on mobile." A layout verified only on desktop is not verified.

Static screenshots at fixed breakpoints miss what this catches. A scroll animation's defects (a hard cut, a mistimed layer) only appear mid-motion, so the check has to be a sequence over time.

## Why it is not optional

Nate's own low-key site, built fully one-shot, shipped a visible hard cut mid-scroll. He names the cause: "on more of a verification loop... we'd be able to fix that, but this is a one-shot prompt." The defect came from the missing check, not from a gap in what the model can do.

[[wiki/sources/nateherk-6-best-github-repos-for-claude|Nate's GitHub repos video]] says this check ships as a built-in checker in his [[wiki/tools/scroll-craft|ScrollCraft]] repo (it screenshots the scroll and inspects element positions), and pairs it with [[wiki/tools/playwright-cli|Playwright CLI]] for clicking through app flows. Creator-claimed; nothing was demonstrated in the transcript.

## General principle

This is the scroll-specific case of a broader rule: for anything a human will look at, hear or read, the check is looking at it, not reading a log, a hash or a structural pass. An automated check can pass on a page that is visibly wrong. See [[wiki/concepts/prove-its-work|Prove its work]] for the general form.

## In this system

`.claude/rules/common/verification.md`: structural verification is not quality verification, and a page deliverable gets screenshotted at mobile and desktop and looked at.
