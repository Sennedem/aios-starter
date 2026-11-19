---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=rL5tw6h78zo
tags: [wiki, technique, skills, prompting, reverse-engineering]
related: ["[[wiki/sources/nateherk-reverse-engineer-anything-skill]]", "[[wiki/tools/rea-reverse-engineer-anything]]", "[[wiki/concepts/seen-inferred-unknown]]", "[[wiki/techniques/inspiration-driven-site-prompting]]", "[[wiki/concepts/tell-it-what-done-looks-like]]"]
---

# Reverse-engineer from the output

Nate Herk's core point in [[wiki/sources/nateherk-reverse-engineer-anything-skill|his reverse-engineer-anything video]]: AI is not creative, but given a clear vision it executes well. So instead of describing what you want, **point the agent at a finished example, have it analyse the example, and build from the analysis**. The example becomes the PRD. **[00:54-03:05]** This works without the [[wiki/tools/rea-reverse-engineer-anything|REA]] repo.

## Steps (usable by hand)

1. **Pick a feature or a style, not the whole thing.** "How does Loom's camera bubble move and resize" beats "reverse engineer Loom". [07:36-07:55]
2. **Gather the artefacts.** One video to copy (he downloaded Jordan Watkins' reel and gave it to Opus), about 30 of your best-performing Reels, five good Friday reports, a competitor's live page. [00:58-02:32]
3. **Decompile first, build second.** Prompt: analyse frame by frame or file by file what is going on, how and why. Do not ask for the build yet. [01:41-02:09]
4. **Route by what it is built with.** The tech stack decides which inspection tools apply, so give the agent that context. Nate admits he would not know this off the top of his head. [08:17-08:58]
5. **Write a summary first.** Raw analysis can be huge (Loom's was over 1 GB). Keep a short summary the model can read in full, with what works, how, and what is not yet figured out. Do not re-run the full analysis each time; it is already saved. [08:59-09:33]
6. **Tag findings seen, inferred or unknown** ([[wiki/concepts/seen-inferred-unknown|concept]]). Build only on seen; test inferred. [09:36-10:23]
7. **Rebuild, test, iterate.** Run test cases instead of shipping once because it looks done. [10:40-11:08]
8. **Do not copy exact code or assets.** Take the behaviour, not the expression. [11:09-11:25]
9. **Bonus Nate flags:** a later, cheaper model may now build the same thing from the saved analysis (Opus to Sonnet). [12:26-12:47] Creator speculation, untested.

## Evidence it works

Creator-observed only: his Reels-editing skill (matched the style of his 30 best Reels), a partial recreation of a motion reel (the original was still better on motion and sound design), a Loom-style recorder, a Sandcastles-like Instagram analyser, and an eval studio inspired by Langfuse. None was independently reviewed. The speed and quality trade (the REA agent is slower and better) rests on one run. [13:00-13:20]

## Limits

- It cannot invent the original creative leap; Nate says Opus could not have designed the reel itself. [02:13-02:21]
- Quality still depends on the model doing the writing.
- Pick the example well: it copies the flaws too.

## Related

Same family as [[wiki/techniques/inspiration-driven-site-prompting|Inspiration-driven site prompting]] (name the reference, say what to take). That page is the web-design case; this one adds the analyse-before-build step and the evidence tags. It is also the "show it the end result" version of [[wiki/concepts/tell-it-what-done-looks-like|Tell it what done looks like]].
