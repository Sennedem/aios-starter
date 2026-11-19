---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
tags: [concept, web-design, parallax, motion]
related: ["[[wiki/concepts/scroll-feedback]]", "[[wiki/techniques/inspiration-driven-site-prompting]]", "[[wiki/techniques/front-middle-back-layers]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]"]
---

# Layering for premium feel

Several visual planes moving at different rates as the user scrolls (parallax), plus elements that physically stack on top of each other, read as "premium" far more reliably than a single flat scrolling page. From [[wiki/sources/nateherk-fable-5-1-kills-website-slop|Nate Herk, Fable 5.1 kills website slop]].

## The pattern

- **Depth via parallax planes.** The AI Automation Society hero used four distinct layers (a back mountain, a middle mountain, a laptop screen and a front tree line), each moving at a different scroll speed. The separation between planes is what reads as depth; one background image scrolling at page speed does not.
- **Stacking cards.** Cards that slide in and stack on top of one another, instead of sitting side by side or in a static grid, felt "super dynamic and engaging". Used for the AIS pricing section and again in the one-shot Ferna site.
- **Subtlety matters as much as the effect.** His personal site's interactive background "adds depth… but it's not distracting". Past a point, layering that calls attention to itself stops feeling premium and starts feeling gimmicky. See [[wiki/concepts/scroll-feedback|Scroll feedback]] for the broader restraint principle.
- **Holds up on mobile, but not identically.** The AIS site kept the layered feel on mobile, but the card interaction changed (no stacking) because the desktop mechanic did not translate directly. He notes one more prompt could make it match, so mobile needs its own explicit check instead of assuming desktop behaviour carries over.

## Where it came from

Nate did not invent this from scratch. He found a reference site (Fora) using the same four-layer hero, named the specific elements he liked, and told Fable 5.1 to replicate that structure. See [[wiki/techniques/inspiration-driven-site-prompting|Inspiration-driven site prompting]]: layering is the clearest example in the video of slop versus not coming down to whether the prompt named a concrete reference.

## The recipe

[[wiki/sources/nateherk-10000-ai-websites|Nate Herk, 10,000 AI Websites]] re-explains the same hero as "front, middle, back" and adds one detail: the front tree line covered the laptop layer, fixed by cutting a V into it so the button stays frontmost. Steps: [[wiki/techniques/front-middle-back-layers|Front, middle, back]]. It also adds the caveat that headline and text must not wait on layered animation ([[wiki/concepts/motion-with-a-job|Motion with a job]]).
