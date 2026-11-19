---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=rL5tw6h78zo
tags: [wiki, source, youtube, skills, reverse-engineering, claude-code]
related: ["[[wiki/tools/rea-reverse-engineer-anything]]", "[[wiki/techniques/reverse-engineer-from-the-output]]", "[[wiki/concepts/seen-inferred-unknown]]", "[[wiki/concepts/prove-its-work]]", "[[wiki/concepts/save-scripts-inside-skills]]", "[[wiki/concepts/skill-description-hygiene]]", "[[wiki/concepts/skills-as-apps-model-as-processor]]", "[[wiki/concepts/agent-skills-as-yaml-frontmatter]]", "[[wiki/techniques/inspiration-driven-site-prompting]]", "[[wiki/sources/nateherk-build-skills-not-agents]]"]
---

# Nate Herk: "I Tested the Viral Reverse Engineer Anything Skill. What You Need to Know."

YouTube, 15:00, Nate Herk | AI Automation, published 2026-10-13: https://www.youtube.com/watch?v=rL5tw6h78zo. The skill is `morluto/rea` on GitHub (verified; see [[wiki/tools/rea-reverse-engineer-anything|REA]]).

**One line:** the viral repo is a good framework but not a new idea; the real lesson is to show an agent a finished example, make it analyse before it builds, and label what it only guessed.

## What the skill claims, what the tests showed, his verdict

- **Claim:** agents study an existing app and recreate a feature; "software is done" (Matthew Berman, which Nate calls half a joke). **[00:01-00:12]**
- **Test:** he used the repo to build a Loom-style recorder (camera bubble, countdown, resizable while recording, local storage instead of cloud), a Sandcastles-like Instagram analyser, and an eval studio inspired by Langfuse. None is a carbon copy: "we cloned the functionality", not the UI. **[03:12-04:50]**
- **Test, the same prompt with and without the repo:** the agent without it always finished first; the one with it was slower but "much better". One person, no scores, no blind review. **[13:00-13:20]**
- **Failures and limits:** the whole Loom analysis was over a GB, so a summary layer is needed; each app type needs different setup; output quality still depends on the model; there are legal limits on copying code and assets. **[09:02-09:15, 11:09-12:25]**
- **Verdict:** a "really cool tool", especially for non-programmers, but "reverse engineering isn't anything new"; he expects the next models to build this in. **[13:35-14:15]**

## Key takeaways

- **[01:00-02:32]** His examples from before REA: he analysed about 30 of his best Reels frame by frame to build a Reels-editing skill whose output looks close to his hand edits, and gave Opus a viral reel and asked for a skill plus a demo edit. Both were still weaker than the originals on motion and sound design. See [[wiki/techniques/reverse-engineer-from-the-output|reverse-engineer from the output]].
- **[02:29-03:05]** "Reverse engineering the output": five good Friday reports in, a skill out. The example is the spec.
- **[07:00-07:55]** Practical lesson: pick features, not whole apps.
- **[07:56-09:33]** His five steps: pick a feature, route by build type, summarise first, tag seen / inferred / unknown, rebuild and test.
- **[09:36-10:23]** The tags matter most: building on inferred guesses as if they were fact makes a mess. See [[wiki/concepts/seen-inferred-unknown|seen / inferred / unknown]].
- **[12:26-12:47]** Cheaper model reuse: a saved analysis might let Sonnet do what only Opus could. Speculation.
- **[14:15-14:57]** Closing generalisation: reverse-engineer processes and skills, not only software. Find someone who does it well and learn why it worked.

## Skeptic note

- **The video is mostly Nate's own earlier workflow relabelled.** The REA-specific evidence is a handful of builds by him, shown on screen, with no tests, scores or second reviewer. "Much better results" is his eye on n=1.
- **Star count and virality are the hook, not evidence.** 192k stars at recording; a later write-up cites 299k. Another viral claim (an Adobe clone) is disputed in the same write-up.
- **A mid-roll plug** for a free ScrollCraft website skill and a community-gated doc **[05:19-05:20, 07:29-07:34]**; the "how to get the most out of it" doc sits behind that community.
- **"Never copy code or assets" is a one-minute aside** while the whole demo clones the behaviour of commercial products. The legal risk is understated; the write-up notes that many licences forbid disassembly.
- **The step list is partly Nate's own synthesis**, from having Claude reverse-engineer the repo **[08:00-08:15]**, not the repo's published steps. The repo's SKILL.md does contain summary-first and evidence-versus-inferred handling (checked).

## Pages from this source

[[wiki/tools/rea-reverse-engineer-anything|REA]] · [[wiki/techniques/reverse-engineer-from-the-output|reverse-engineer from the output]] · [[wiki/concepts/seen-inferred-unknown|seen / inferred / unknown]]

## Cross-source connections

- [[wiki/concepts/save-scripts-inside-skills|Save scripts inside skills]] (from [[wiki/sources/nateherk-build-skills-not-agents|"Build skills, not agents"]]): **extends.** That source says save the proven script; this one says build the skill by analysing proven outputs first. Both end with a skill that carries the know-how instead of regenerating it.
- [[wiki/concepts/skill-description-hygiene|Skill description hygiene]]: **context.** The same creator's earlier rule is one job per skill with clear triggers. Here the input to building a skill is examples, so the two compose: examples decide the content, the description decides discovery.
- [[wiki/concepts/prove-its-work|Prove its work]]: **extends.** Seen / inferred / unknown is prove-its-work applied to findings.
- [[wiki/techniques/inspiration-driven-site-prompting|Inspiration-driven site prompting]]: **confirms.** Same creator, same move (show the reference), now with an analyse-first step.
- [[wiki/concepts/skills-as-apps-model-as-processor|Skills as apps, model as processor]]: **consistent.** REA itself is a skill layered on the general agent, plus an MCP plug-in.
