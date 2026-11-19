---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, web-design, fable]
related: ["[[wiki/concepts/ai-website-slop]]", "[[wiki/tools/21st-dev]]", "[[wiki/tools/design-inspiration-galleries]]", "[[wiki/tools/scroll-craft]]", "[[wiki/techniques/screenshot-scroll-verification]]", "[[wiki/techniques/reverse-engineer-from-the-output]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]"]
---

# Inspiration-driven site prompting

The concrete technique behind avoiding [[wiki/concepts/ai-website-slop|AI website slop]]: never ask for a quality adjective; always hand the agent a specific reference and say what to take from it. From [[wiki/sources/nateherk-fable-5-1-kills-website-slop|Nate Herk, Fable 5.1 kills website slop]].

## Three ways to supply inspiration

1. **Name a reference site, the specific elements you like, and why.** For the AI Automation Society hero, Nate found Fora, told Fable 5.1 he loved its four-layer parallax feel, and asked for a hero built the same way: back mountain, middle mountain, laptop screen, front tree line. He made the same move for a stacking-card pattern sourced from a different site.
2. **Pull individual components from a library.** For his personal site there was no single reference site. He browsed [[wiki/tools/21st-dev|21st.dev]] for a background, a gradient and an interactive element he liked one by one, then had Fable 5.1 build around those pieces.
3. **Point the agent at a live competitor and say "clone the vibe."** For Glydo, he told Fable 5.1 to inspect a competitor's site (Lemon, another dictation app), take Glydo's own brand guidelines, and reproduce the competitor's product-in-use animations on Glydo's page. He calls this "very directly just like cloning it". It is the most literal form of the technique, and it worked close to one-shot.

## Scaling it: one combined one-shot prompt

For two fully one-shot sites (Ferna and low-key) he combined everything into a single prompt he calls "gold": use the [[wiki/tools/scroll-craft|ScrollCraft]] skill, use layering, pull inspiration from the AIS site, from [[wiki/tools/21st-dev|21st.dev]], and from [[wiki/tools/design-inspiration-galleries|godly.website, Awwwards and Motion Sites]], with permission to generate any assets needed. Ferna held up well. Low-key shipped a visible hard-cut defect, which he puts down to skipping a [[wiki/techniques/screenshot-scroll-verification|verification loop]] on a one-shot output, not to the technique.

## Related

[[wiki/techniques/reverse-engineer-from-the-output|Reverse-engineer from the output]] generalises the "clone the vibe" move beyond websites and adds an analyse-first step and evidence tags before any build.

The practical rule that follows: before writing any frontend code, gather a small set of real references, and for each one name the site, the element and why you want it.
