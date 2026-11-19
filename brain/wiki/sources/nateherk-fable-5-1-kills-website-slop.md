---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=FFWtxjvW2ts
tags: [wiki, source, youtube, web-design, fable]
related: ["[[wiki/concepts/layering-for-premium-feel]]", "[[wiki/concepts/scroll-feedback]]", "[[wiki/techniques/inspiration-driven-site-prompting]]", "[[wiki/concepts/ai-website-slop]]", "[[wiki/tools/21st-dev]]", "[[wiki/tools/design-inspiration-galleries]]", "[[wiki/concepts/three-ps-pain-person-promise]]", "[[wiki/techniques/screenshot-scroll-verification]]", "[[wiki/concepts/model-matters-less-than-the-brief]]", "[[wiki/tools/claude-fable-5-1]]", "[[wiki/tools/scroll-craft]]", "[[wiki/sources/nateherk-fable5-karpathy-llm-wiki]]"]
---

# Source: "Fable 5.1 FINALLY Kills AI Website Slop" (Nate Herk)

YouTube video (16:13) by Nate Herk | AI Automation, published 2026-09-02: https://www.youtube.com/watch?v=FFWtxjvW2ts.

Nate walks through three sites built with Fable 5.1 (the AI Automation Society site, his personal site, and Glydo, a dictation-app clone of a competitor's feel) and two one-shot sites (Ferna and low-key). He then states seven rules for getting output that isn't slop from an AI website builder, and closes with a controlled Fable 5 vs 5.1 cost comparison.

## Key takeaways

- **[00:00-01:31]** The AI Automation Society site: a four-layer parallax hero (back mountain, middle mountain, laptop screen, front tree line) that moves as you scroll, plus cards that physically stack on top of each other while text streams in. It keeps the same premium feel on mobile, with a different (non-stacking) card interaction. See [[wiki/concepts/layering-for-premium-feel|layering for premium feel]].
- **[01:31-02:40]** His personal site: stat numbers that tick up, a subtle background that reacts to the mouse without distracting, text that appears on scroll, and a nav bar that stays locked through the whole scroll. The throughline is restraint: "not too overwhelming or distracting." See [[wiki/concepts/scroll-feedback|scroll feedback]].
- **[02:40-03:49]** Glydo: he pointed Fable 5.1 at a competitor's live site (Lemon, another dictation app), gave it Glydo's brand guidelines and asked it to reproduce the competitor's product-in-use animations on Glydo's own page. The result was close in feel and effectively a one-shot. See [[wiki/techniques/inspiration-driven-site-prompting|inspiration-driven site prompting]].
- **[03:53-06:19]** The core claim: telling the model "make this look professional, make this feel premium" does not work; you have to give it something concrete to work from. He names Fora as the layering reference, an unnamed site for the stacking-card pattern, and [[wiki/tools/21st-dev|21st.dev]] for individual UI components (one copyable prompt per element). See [[wiki/concepts/ai-website-slop|AI website slop]].
- **[06:19-08:47]** Two one-shot sites (Ferna, low-key) built from a single prompt he calls "gold", which told the agent to use his [[wiki/tools/scroll-craft|ScrollCraft]] skill plus explicit inspiration sources: the AIS site, [[wiki/tools/21st-dev|21st.dev]] components, and [[wiki/tools/design-inspiration-galleries|godly.website, Awwwards and Motion Sites]]. Ferna's layering held up well; low-key had a visible hard-cut defect that he attributes to skipping a verification loop.
- **[10:53-13:24]** Seven rules for AI websites without slop, all built into his ScrollCraft skill: (1) brand guidelines; (2) the three P's: pain, person, promise; (3) scroll responsiveness, where subtle text-appear is enough and not everyone wants a 3D fly-through; (4) inspiration from real sites, because "you can't just say make it premium"; (5) grab existing components; (6) verify on mobile; (7) screenshot the scroll frame by frame as a verification loop. See [[wiki/concepts/three-ps-pain-person-promise|three P's]] and [[wiki/techniques/screenshot-scroll-verification|screenshot scroll verification]].
- **[13:24-16:12]** Controlled test: the same prompt, assets, brand guidelines and skill run on Fable 5 and Fable 5.1 produced near-identical sites: "none of them clearly blew the other one out of the water." But 5.1 was cheaper in all four paired examples (18.24 vs 20.22, 14.52 vs 14.67, 12.83 vs 21.64, 11.18 vs 17.37), and he had used only about 45% of his weekly Fable limit after 5 to 6 hours of work, where Fable 5 had burned through the same limit in 1 to 2 hours. See [[wiki/concepts/model-matters-less-than-the-brief|model matters less than the brief]]; release and pricing details are on [[wiki/tools/claude-fable-5-1|Claude Fable 5.1]].

## Connections

- Gathering real references before writing any frontend code is the same rule as "you can't just say make it premium": name concrete sites and elements before generating, not after.
- Screenshot scroll verification extends the usual habit of screenshotting fixed breakpoints. A scroll-heavy site's defects (a hard cut, an element out of bounds) only show up mid-animation, so capture the motion frame by frame.
- The low-key defect is the general verification lesson in small: for anything a person will look at, the check is looking at it, not reading the build log.
- ScrollCraft, described here as a free community skill, has since been published as a public GitHub repo; see [[wiki/tools/scroll-craft|ScrollCraft]].
- [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|"Fable 5 + Karpathy's LLM Wiki"]] is the same creator's earlier video on the wiki method.
