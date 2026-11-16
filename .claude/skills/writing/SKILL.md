---
name: writing
description: The universal writing route. Every drafting or editing request (email, message, LinkedIn or social post, video script, proposal, report, essay) goes through this skill: Pyramid Principle, SCQA opening, direct sentences, no AI tells. Reads the user's voice samples, learnings, ban list and playbooks first, then logs every correction so the voice keeps improving. Use for "write", "draft", "edit this", "rewrite", "reply to this email", "write a post about", "make this sound like me".
---

# Writing

Every piece of writing the user asks for goes through this skill, whatever the format or length.

## Where the voice lives

The user's voice lives in two files and nowhere else:

- `references/voice-samples.md` holds 3 to 5 real, unedited pieces the user wrote. The `setup` skill fills it.
- `references/learnings.md` holds every correction the user has made, each turned into a rule.

Until those files hold samples or entries, write neutral and direct: plain sentences, the answer first, no flourish, no invented personality. Say once in the delivery note that drafts will match the user's voice after they add samples to `references/voice-samples.md`.

Precedence when files disagree: the user's own samples and `learnings.md` > `references/ban_list.md` > `references/humanizer.md`.

**Draft-first.** Nothing this skill writes is sent, posted or published until the user approves it.

## The non-negotiables

These four rules apply to every output.

1. **Pyramid Principle (Barbara Minto).** Lead with the answer. Supporting points come after, grouped under the main message. A reader who stops after the first sentence or paragraph still knows the answer.
2. **SCQA framing, opening only.** Situation, Complication, Question, Answer. Use it once, to open the piece. For long pieces the opening paragraph carries it; for short messages compress it into the first one or two sentences. The body follows the Pyramid (claim, then evidence) and does not repeat SCQA.
3. **Direct, no fluff.** No throat-clearing ("I hope this finds you well"), no hedging ("I just wanted to..."), no preamble ("In today's fast-paced world..."). If a sentence can go without losing meaning, cut it.
4. **No AI tells.** `references/ban_list.md` catches words and stock phrases. `references/humanizer.md` catches structure: staged contrasts, one-line closers, colon reveals, forced triads, dashes. If either fires, rewrite the sentence or the paragraph around its point.

## The workflow

### Step 0: Load context
Read `references/voice-samples.md`, `references/learnings.md`, `references/ban_list.md`, `references/humanizer.md` and `references/playbooks.md`. The samples and learnings are the current picture of the user's voice and override the defaults where they conflict.

### Step 1: Interview first
Before writing, get the three facts you need. Ask only what is missing; if the prompt already gives them, skip the question. Use tappable options where the interface offers them.

- **Audience:** who reads this? (a potential client, a hiring manager, a class, a mixed LinkedIn audience)
- **Length:** offer concrete options adapted to the format, for example short (~100 words), medium (~300), long (~600+).
- **Goal:** what should happen after they read it? (book a call, agree to a meeting, understand a concept, click through)

Skip the interview only when the user says "just write it" or similar.

### Step 2: Pick the playbook
Load the matching playbook from `references/playbooks.md`: `email_short`, `social_post`, `long_form` or `script`. If the format is unclear, ask. If several apply, pick the dominant one and note the hybrid.

### Step 3: Draft using Pyramid and SCQA
Build the structure before the prose:

- Top of the pyramid: one sentence with the single answer, message or ask.
- Supporting points: 2 to 4 grouped reasons, mutually exclusive where possible.
- Evidence under each: facts, examples, data, an anecdote.

Then open with SCQA: what the reader already knows, what changed, the question that raises, and your answer. In short messages the first three often collapse into two sentences. The structure is a thinking tool; do not fill it in mechanically.

### Step 4: Self-check
- Does the first sentence or paragraph contain the answer?
- Does only the opening carry SCQA, with the body following claim and evidence?
- Any phrase from `references/ban_list.md`?
- Zero em or en dashes in the prose (unless the user's samples use them)?
- Could any sentence be cut without losing meaning?
- Does it sound like the samples in `references/voice-samples.md`, or neutral and direct if there are none?
- Does the length match the request?
- Does it respect every rule in `references/learnings.md`?

Revise before delivering if any check fails.

### Step 4b: Humanizer pass (every draft)
Run the "How to work" steps of `references/humanizer.md` on the draft in embedded mode: mark the tells strongest first (sections 1 to 5 act on one sighting), at sentence and paragraph scale; rewrite; check that no fact, name, number, price, date or claim was dropped or changed; read it aloud and search again for the survivors (contrasts, closers, triads, dashes, bold labels); write the final version. For writing in another language, use that language's addendum at the end of the file if the user has added one. Only the final text goes to the user.

### Step 5: Deliver and offer one next step
Deliver the draft, then offer one concrete next step ("tighten it", "rework the opening", "try a different angle"), never a vague "let me know what you think". For long work or study deliverables, offer a `.docx` version if the user hands work in as Word files.

### Step 6: Capture the correction (do not skip)
When the user corrects a draft ("too formal", "I'd never say X", "open with a number"), append it to `references/learnings.md` before the turn ends, in the entry format at the top of that file: date, what was corrected, the general rule it became, and a short before and after. A new banned phrase also goes into `references/ban_list.md`. The next draft then follows it.

## Format notes
- **Language.** Write in the language of the prompt. If the audience reads a different language than the prompt, ask. Do not mix languages in one piece.
- **Claims and statistics.** Every number must be real and verifiable. Without a source, flag it and ask. Never write "studies show" without the study.
- **Academic work.** Name the frameworks you apply (SCQA, MECE, Pyramid Principle, issue trees); graders reward visible framework use.
- **Business proposals.** Keep claims concrete: specific markets, platforms, timelines. No generic "this industry is booming" openers.

## When in doubt
- Shorter beats longer. Specific beats general. A real example beats an abstract claim.
- If you are tempted to write "moreover" or "furthermore", the sentence is probably not needed.
- Never compliment the user's prompt or thank them for context. Write.

## References
- `references/voice-samples.md`: the user's real writing. Read every time.
- `references/learnings.md`: the user's corrections as rules. Read every time.
- `references/ban_list.md`: banned words, patterns and crutches.
- `references/humanizer.md`: the catalogue of AI-writing tells and the final pass.
- `references/playbooks.md`: format playbooks (Step 2).
