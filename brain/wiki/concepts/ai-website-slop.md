---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: web-design
parent: "[[wiki/README|Wiki]]"
tags: [concept, web-design, prompting]
related: ["[[wiki/techniques/inspiration-driven-site-prompting]]", "[[wiki/concepts/model-matters-less-than-the-brief]]", "[[wiki/sources/nateherk-fable-5-1-kills-website-slop]]", "[[wiki/concepts/forced-iteration-degrades-output]]"]
---

# AI website slop

The generic, template-feeling output an AI website builder produces by default, and why it happens even on a strong model. From [[wiki/sources/nateherk-fable-5-1-kills-website-slop|Nate Herk, Fable 5.1 kills website slop]].

## Why it happens

Nate's central claim: **"you can't just say to Fable 5.1 or any AI model, 'make this look professional, make this feel premium.'"** A vague quality instruction gives the model nothing concrete to anchor on, so it falls back to safe, generic defaults: "unless you're using some sort of skill or unless you're building off of some sort of template, it's probably going to feel that way because AI is AI."

He does not present this as a model-capability gap. In [[wiki/concepts/model-matters-less-than-the-brief|Model matters less than the brief]], Fable 5 and 5.1 produced near-identical output given the same prompt, assets and skill. Slop is mainly a prompting failure.

## The fix

Give the model something concrete to work from in place of an adjective:

- **Named reference sites**, with the specific elements you like and why (Fora for layering, an unnamed site for stacking cards). See [[wiki/techniques/inspiration-driven-site-prompting|Inspiration-driven site prompting]].
- **Existing components** instead of inventing from scratch, such as [[wiki/tools/21st-dev|21st.dev]]'s copy-prompt library.
- **A skill or template** that encodes the design principles once, so they are not re-explained per project. Nate's own is ScrollCraft, now a public repo: [[wiki/tools/scroll-craft|ScrollCraft]], listed in [[wiki/sources/nateherk-6-best-github-repos-for-claude|his repo roundup]].
- **Brand guidelines** and the [[wiki/concepts/three-ps-pain-person-promise|three P's]], so the output is calibrated to a specific audience and not to a generic "professional" default.

## More slop defaults

[[wiki/sources/nateherk-10000-ai-websites|Nate Herk, 10,000 AI Websites]] names three more defaults beyond "no concrete reference":

- generic AI copy (fix: the [[wiki/concepts/mirror-test-first-screen|mirror test]]);
- an accent colour spread everywhere (fix: the [[wiki/concepts/highlighter-rule-60-30-10|highlighter rule]]);
- animation on everything (fix: [[wiki/concepts/motion-with-a-job|motion with a job]]).

So slop is also a copy and colour problem, beyond the missing reference.

[[wiki/sources/nateherk-make-it-better-100-times|Nate Herk, "Make it better" 100 times]] shows a second route to slop: an unbounded loop forced to "ship one bold change every round". Opus's round-100 site was called "AI slop" by Nate himself (dead sections, too much text, a hard-sell upsell), and neither model searched the web for references. See [[wiki/concepts/forced-iteration-degrades-output|Forced iteration degrades output]].
