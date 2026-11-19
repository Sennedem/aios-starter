---
type: reference
status: active
updated: 2026-11-19
domain: meta
pack: core
parent: "[[references/README|References]]"
tags: [postmortem, agents, verification, worked-example]
---

# Postmortem: the batch that passed every check and was rejected on first look

A worked example of how a system of AI agents can produce confident, verified, wrong work, and what fixed it. The details are anonymised; the numbers and the lessons are from the real case.

**What happened:** five explainer videos were built by five parallel builder agents, rendered, structurally verified, uploaded and reported done. The owner opened one frame and rejected the whole batch: the scenes that should have shown real places were **drawn with CSS shapes**, a house made of a triangle and a rectangle.

Everything after that is the useful part. Six distinct failures compounded, and none of them was "an agent was careless".

## 1. The causal chain: why five independent builders made the same wrong choice

This was not five mistakes. It was one system producing the same output five times.

| Link | What it said | Effect |
|---|---|---|
| The design file | "Scene art references: `scene-art/*.png`", inside a list of assets | A pointer to a folder, never phrased as a rule. The file said "never" six times, all about fonts and tone, never about drawing places in CSS. |
| The build recipe, step 4 | "composed from registry archetypes" | The registry was about 36 **CSS components**, so the only actionable instruction pointed *at* CSS. |
| The budget ledger | "$0 spent on image generation", logged as an achievement for three batches running | Positively rewarded skipping the art. |
| The five dispatch briefs | Nine named failure modes, all from the previous month's incident log | Told agents what not to break. Never told them what good looks like. |

**The general lesson:** a rule that lives in a document agents do not read, contradicted by the document they do read, and rewarded in the opposite direction by the tracker, is not a rule. It is a preference nobody can act on.

The fix moved it into the build recipe as a decision table at the point of use, and banned "$0 image spend" as a standalone achievement in the ledger.

## 2. Defect-avoidance briefs produce defect-free mediocrity

In a narrow sense the briefs were excellent: nine specific failure modes with countermoves, each traceable to a real earlier incident. The output was technically flawless and visually worthless.

**Optimising a brief against the last batch's defects fixes the last batch's defects and nothing else.** Everything outside the list is invisible to the agent, because the list is its definition of done.

The fix: every delegation brief now carries a line stating **what GOOD looks like**, in positive terms. See [[wiki/concepts/tell-it-what-done-looks-like]].

## 3. When a rule fails three or more times, it is a design problem

Two rules failed repeatedly while written down and restated in bold:

- **The imaginary render watcher.** Agents invented a background watcher or notification that did not exist and ended their turns while a render was still running: **six times across two batches**, four different agents, one of them twice, in briefs that pasted the correct blocking wait loop verbatim. It stopped only when the wait moved inside a blocking render command, so ending early became impossible instead of forbidden.
- **The caption band.** Elements overlapping the subtitle area: **seven videos, six builders**, and it broke twice *after* an exact pixel value was written into the recipe. It stayed unfixed for as long as it stayed prose. It needs to fail the build.

**The tell:** writing the same warning louder (bold, red markers, capitals) instead of differently. If the third restatement is meant to be the fix, it is not.

## 4. An unvalidated estimate that drives decisions is a liability

The budget guard estimated about 27,500 characters of voice generation for five videos. The actual figure was 13,029, or 47%, and it was the third under-run in a row in the same direction (an earlier batch planned about 17,000 and spent 7,421).

That phantom number caused **two separate wrong decisions in two sessions on the same day**: the guard declared the week "over budget by more than half", and a parallel session held four videos unbuilt to avoid the spend.

The fix: log actuals against estimates every batch. When an estimate is wrong three times in the same direction, replace it instead of reasoning from it.

## 5. Structural verification is not quality verification

Duration, file hashes, the project's linter, silence detection and speech-to-text all passed on videos that looked like clip art. Those checks answer "did the machine do what it was told?", never "was it told the right thing?" For anything a human will look at, the check is looking at it.

Sub-lessons, each earned:
- **Check per beat, not per scene.** One scene held two beats; only the first was checked, and the second shipped broken with a CSS triangle mountain.
- **Compare against the previous render** to separate a regression from a weakness that was always there. One extracted frame settled it at once.
- **Never report "verified" without saying what was verified.** "Duration and audio verified; visuals not yet looked at" is honest and would have caught this on day one.

See [[wiki/concepts/prove-its-work]] and [[wiki/techniques/verify-before-returning]].

## 6. Rationalisation is a signal, not a conclusion

A builder kept a CSS triangle for a beat showing a famous mountain landmark, justifying it as "a stylised graphic, not a literal place-depiction". It survived two review passes on that phrasing before a frame check caught it.

**When an agent argues for a category exception to a rule it was just given, the rule was right.** The recipe now says so: "it's stylised, not literal" is not an exemption, since a simplified drawing of a place is still a drawing of a place.

## 7. The pipeline had no version control

The build pipeline's folder was not a git repository. Any session could rewrite any build recipe with no diff, no history and no rollback, which is how the drift in the art rule survived three batches, and why "did the other session change the recipe?" could not be answered when the owner asked.

The fix: put it under git, tracking recipes, the shared library, tools, compositions, manifests and generated art; ignore renders, work folders, audio and a 1.2 GB font file the scaffold had copied into about 90 builds. A repository with no remote is still lost with the machine, so it also needs an off-machine copy.

## 8. Parallel sessions collided, harmlessly, by luck

Two Claude sessions worked the same batch at once. They split cleanly by accident (one built, one measured) and the paid voice generation only ever ran in the build session, so nothing was wasted. But two agents briefly edited the same file, and one session held work back based on the other's stale estimate.

The fix: a session lock at the top of the batch's queue file, naming one owner per lane. Any parallel work starts by reading it.

## What actually caught each defect

| Defect | Caught by |
|---|---|
| CSS-shape visuals | **The owner, opening one frame** |
| Washed-out background plates, unreadable header, caption collision, low-contrast text | **The orchestrating session's frame checks** |
| The CSS triangle mountain | **A frame check**, after a builder had rationalised it |
| An animation call dropping an element's base classes | A builder's snapshot sweep |
| A dead selector (missing `id`, so a fade did nothing) | A builder's frame inspection |

**The builders' own structural self-checks caught none of the visual defects.** The independent quality pass that was in the approved plan, the designed safety net, never ran, and nobody flagged dropping it. That is its own lesson: a step silently left out of an approved plan is a decision made without the person who approved it.

## Cost of the whole episode

$0.42 of image generation and no extra voice generation. The rebuild was cheap because the audio was never touched, so every duration stayed byte-identical. The expensive part was render time and attention, not credits.

## In this system

The lessons live on as rules: the "what GOOD looks like" line and the escalation table in `.claude/rules/common/agents.md`, and "structural verification is not quality verification" in `.claude/rules/common/verification.md`.
