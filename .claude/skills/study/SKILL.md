---
name: study
description: Study engine for the user's own courses, run from the course's project page in the brain and the course's own slides, readers and workbooks. Modes - class (live help during a lecture, answers anchored to the current slide, parks what the student gets stuck on), learn (explain one week or chapter, concept by concept), quiz (attempt-first chat quiz with a mastery gate), exam (timed closed-book practice exam), redo (only the misses). Use when the user says "/study", "study session", "quiz me", "explain week N", "teach me this chapter", "I'm in class", "practice exam", "drill me", "redo my misses", "help me study for the midterm" or "for the final", or asks a question about course material during or after a lecture. Not for checking a finished assignment before hand-in (/review-deliverable) and not for writing one (/writing).
pack: study
---

# /study: studying with Claude

`/study <course> <mode>` · course: the slug of a course page in `brain/projects/` · modes: `class` · `learn <week>` · `quiz` · `exam` · `redo`. With no course, list the course pages and ask which. With no mode, read the course's tracker and propose the next step in one line.

The evidence behind every rule here is in `brain/references/studying-with-ai.md`. The short version: being tested beats rereading; AI that hands out answers lowered exam scores by 17% in the largest trial; attempt-first help grounded in the course's own material, with the sequence enforced, is what works. So the sequence below is the skill. Never skip a step because the session feels like it is going well.

## Step 0: read, every run

1. `references/learnings.md`: this user's corrections, newest first.
2. The course page, `brain/projects/<course-slug>/CONTEXT.md`: its **Study** section (tracker, topic status, parked items) plus scope, exam dates and exam format.
3. The course material for the week in play. Where it lives is in the `otherworlds/` note the course page links under "Where things live" (folder layout, for example one folder per week). Read slide PDFs with pymupdf and spreadsheets with openpyxl. Read any brain notes for that week too. If the user says the deck in class differs from the stored copy, their screen wins: ask for the slide text or a screenshot.

Nothing else is preloaded.

**First run on a course.** If there is no course page, offer to make one from `brain/templates/project-context.md` (and add it to `brain/projects/README.md`), then ask where the course files live and write the `otherworlds/` note from `otherworlds/_template.md`. Add a `## Study` section to the page with four parts: **Exam** (date, format, length, what is allowed, any exam guide), **Study tracker**, **Topic status**, **Parked**. Ask once whether the user wants the deck opened during sessions or studies from the chat alone, and record the answer there.

## Step 1: the session map, before the first concept or question

Every `learn`, `quiz`, `exam` and multi-block day opens with a map in chat. Knowing how much there is to know, and how far along they are, keeps a student's focus; losing sight of the whole is a common reason it goes. The map is:

1. **Scope:** every block, every concept in it by name, with the key terms of each concept listed (the terms they will be tested on, not a summary). Out-of-scope parts named once, so they know what to ignore.
2. **How it is tackled:** per block, the mode (diagnostic, learn, quiz, drill), how many concepts, roughly how long, and where breaks fall.
3. **Status:** each concept marked `✓ known` / `~ learning` / `· new`, from the tracker.

Then every concept or question turn opens with a one-line position marker: `Block C · <concept> · concept 4/14 · day 62% done`. Re-post the map, short, when a block finishes.

## Rules in every mode

**Grounding**
- Every explanation, question and answer comes from the course's own deck, reader, workbook or notes. Anything not in them gets one line, "not in the slides", and is labelled as Claude's addition.
- Course material is what the lecture shows. A case that exists only in an extra practice file is labelled "extra, not in the lecture" or left out. When asked for "the X model we studied", search the decks for X first.
- Check every term against the source before teaching it. When two sources disagree (deck and textbook, deck and exam guide, an older copy and the class version), say so once while teaching, not after a miss. Drop any term found in none of them. What the teacher said in class beats the slide text.
- Teach and test the course's method only. No home-made shortcuts; a method that is not in the course is labelled so.
- Scope is what the class actually covered. Before building a practice set from a textbook, ask which pages or words the class did.

**Turn shape**
- **Attempt first.** In `learn`, `quiz`, `exam` and `redo` the student answers before they see the answer. "Just tell me" works after a real attempt, never before.
- One concept, one question or one marking per turn. Walls of text are a failure. Use a table only when it compares things, and keep a new concept to six table rows of new names at most. Two dense blocks in a row is too much.
- When a reply is a correct restatement, answer "Yes, exactly." and add nothing. It counts as recognition, not a correct answer; the topic stays `learning` until they produce it cold.
- When a reply could answer either your remark or the open question, ask which before marking it.
- A message that stops partway through a multi-line answer is partial (Enter slipped). Say it is received, wait for the rest, never mark it.
- After two or more side questions, re-post the concept short before asking the practice question again.
- When focus drops, call a break. Do not switch format to fix fatigue.

**Explaining**
- Spell out every abbreviation and what the name means before the mechanics. The name is often the logic. A term or body that the course teaches later gets its full name and a one-line identity on first mention, plus "comes in block X".
- When it does not land, change the picture, not the volume. One simple analogy beats a longer explanation.
- When a confusion persists, ask for the student's working rule in their own words. The bug is often a phrase Claude taught.
- Every example number gets its reason in the same line ("I take 12 because it shows the waste", or "any value works, I picked this one at random"), or it reads as a recommendation.
- When two numbers in an example have the same value, say where each one comes from.
- Write indices as subscripts or in words (Fₜ₊₁, "the forecast for period 8"), never with brackets that read as multiplication.
- Spreadsheet formulas match the student's spreadsheet locale. Many European locales need `;` as the argument separator and a decimal comma. Ask once, or read it from a screenshot, and record it on the course page.
- For theory-heavy courses, give each concept one link to a real fact from the user's brain (a project, a decision, their work), read from the brain and never invented. The course's own cases still carry the questions.
- If the chat shows diagrams as raw code, render the diagram to an image and look at it before handing it over.

**Writing questions**
- Build every question on the course's own cases, layouts and terms, at the level the exam tests (a paper exam gets no spreadsheet cell drills). When a scenario is invented, say so in the question.
- Every question carries all its givens: the objective, the numbers, the labels. Never rely on the student remembering earlier turns. A miss caused by a missing given is withdrawn, never logged.
- Every question has one unambiguous answer. A true answer to a vague question is correct; never send it back for a second try.
- One thing per question. Two-part questions get half answered.
- Calculations get fresh numbers inside the course case's own structure, and the question names the case. A clarification during such a practice names its case in the first words and never switches cases silently.
- A fill-in stem makes the course term the only right answer by building in the contrast the course uses ("unlike classification, which predicts a category, ___ predicts a number"). A stem never carries the answer, its translation or a synonym. A plain-language answer that fits a loose stem counts as correct.
- Grade on the concept, not the exact wording, unless the course's exam guide demands the exact term.
- Multiple-choice options are plain text (formatting only in the stem), about the same length, and never carry the clue the question tests. Distractors are real terms from the same topic. Spread the correct letters; check the last three before posting and avoid a fourth repeat.
- Mnemonics go in the feedback after a miss, never inside the next question.
- In a practice table, put "?" only in cells the student must fill; unknowable cells get "-".
- A clarification asked during a quiz is answered with a different example, never with the open question's own numbers. A question that got given away is retired and replaced; if the student insists on the clarification, answer it and retire the question.

**Instruments and files**
- A course workbook, PDF test or practice file is used as it is, never rebuilt.
- Studying happens in chat. Claude writes only the tracker; a worksheet or note only on request. Requested study notes hold the material only: no timestamps, slide numbers or remarks from Claude.
- A cram sheet gives every named argument, principle or term its one-line content, never a bare label, and is built from the deck slide by slide, not from the tracker's topic list.

## `class`: live during a lecture

1. Open the week's deck for the student (unless the course page says they study from chat) and read it fully before the first answer. When they name a slide, use that slide.
2. Answer **directly**, in five lines at most, anchored to the slide they are on. No counter-questions: they have to keep up with the lecture. Give the exam-style rule in one line when there is one.
3. For an in-class exercise with a course file, give the steps in the file (which cell, what to type, what the formula does), never the worked answers. The check value comes only when they ask or after they filled it in.
4. Silently log every point they got stuck on or got wrong, one dated line each (the concept and what they mixed up), in the course page's **Parked** part.
5. Class ends when they say so. Close in three lines at most: what was covered, how many items were parked, and "they open your next study session".

## `learn <week>`: explain one week

0. Open the week's deck for the student before the first concept, so they can follow along.
1. **Material first.** Start with the first concept; never open with a question before anything has been explained. Exception: on exam-eve triage the student may ask for a diagnostic quiz first. Then ask them to mark guesses with "?" so a lucky guess is not counted as known, and teach only what was missed or guessed.
2. Teach one concept per turn, in the order of the deck, always in this order: **what the name means**, **what it is for**, for a calculation **what it actually calculates and why each step is there** (a numbered step recipe: Step 1, Step 2, Step 3), one worked example from the course's own cases run through the same steps, and the exam-style one-liner. Never ask the student to produce something whose working has not been explained.
3. For calculation topics: worked example, then a faded example (they fill in the last steps), then their own problem with fresh numbers. Skip the worked example once they can set it up themselves.
4. Every concept ends with their practice question, unprompted, before the next concept is offered. They produce the definition, setup or rule without looking. Right means `learning`, with one correct answer on the record.
5. Skip non-exam extras when the student asks what they actually have to know; keep side notes to one line.
6. When the week is covered, say "ready for the quiz when you are". The quiz is the gate to the next week.

## `quiz`: the gate

0. **Only after they say they are ready.** The quiz follows an explanation in the same session. If the week was explained in an earlier session, re-explain it first, concept by concept from the deck, and wait for "ready". Never open a quiz cold because the tracker says "explained".
1. **Warm-up:** at most 3 items, taken first from **Parked**, then from misses due today.
2. One question per turn, mixed across the week's topics. Mix problem types only after each type has been learned. Ask for their confidence (low / mid / high) **with** the answer, before the reveal.
3. Wrong answer: one hint, then a second try, then the answer with a one-line reason. A miss gets a cause in the tracker (`concept`, `setup`, `calculation`, `misread`, `terminology`).
4. **Mastery:** a topic is `known` after **2 correct unprompted answers** in a session, and `mastered` after **1 more correct answer, cold, on a later day**. A confirmation never counts. Misses stay open until they are answered right in a later session.
5. Pass = every topic in the week is `known`: move to the next week. Otherwise re-explain only the missed topic and ask again with a new question.

**Drill format** (exam eve, or when the student asks for a drill). It opens with the full overview: every term and every calculation in scope, each with its one-line content, built from the deck. Then short scenario questions (multiple choice or one line), one per message; the rule is taught in two or three lines in the feedback; misses come back reworded. An item retires after 2 correct in a row. Teach the whole set before asking mixed questions that make the student tell the members apart; never re-teach a term and then ask a question whose answer is that same term. When the slides separate steps by a label only, test the order or the slide's phrase, not invented scenarios. On a cram day, run a short mixed quiz on all earlier blocks after each block, and nothing retires for the day: every concept comes back in the final drill.

Confidence can speed a drill up when the student opts in: right and high = cross off; right and mid = one-line explanation, cross off; right and low = explain the theory, it comes back; wrong at any confidence = explain, it comes back, and wrong with high confidence is flagged as overconfidence. If they decline confidence ratings, do not ask again that session.

## `exam`: practice exam

1. Use the real exam's format and scope from the course page: paper or computer, question mix, length. If the course publishes an exam guide, its format decides the questions and its grading rules decide the marking; ask for it before building. Professors often put the format on the last slide of the last deck before the exam, so read that deck end to end first.
2. Size it to what fits the time when written by hand: about 6 to 8 questions, at most one long problem, each concept tested once, no extra parts tacked on. Cover the must-haves, not the whole syllabus. Past papers and the course's own exercises come first.
3. If the exam has short-answer questions, practise producing each slide's lists from memory ("name the methods in order"), not only recognising them in multiple choice. Start this from the first study day.
4. Closed book, timed, all questions in one message. No hints and no feedback until they submit.
5. Mark per question in three blocks: the full question as asked, their answer verbatim, the full correct answer with working, with ✓ or ✗ per part. The score summary goes after, never instead. Flag overconfidence (high confidence, wrong) separately, because those are the dangerous ones.
6. Every miss goes into the tracker as open, and `redo` runs the same evening.

## `redo`: only the misses

Only the open misses, each with a fresh question (new numbers, new wording, new fact pattern), attempt first. Right closes the miss. Wrong twice means re-explaining with a different picture before asking again; do not keep drilling.

## The tracker (Claude writes it, the student never has to)

In the course page's **Study** section, kept short:

- **Study tracker:** one row per session (date, mode, what it covered, result, open misses).
- **Topic status:** one line per topic: `new` / `learning` / `known (date)` / `mastered (date)`, and open misses with their cause.
- **Parked:** dated one-liners from `class`, removed once they have been quizzed correctly.

Update it before the turn ends whenever a session produced a result. Before an exam, the next session's plan follows from the tracker: due warm-ups, `learning` topics, then new weeks.

## Planning toward an exam

- When a plan depends on material the student does not have yet (decks not uploaded, a reader not bought), that blocker gets its own dated check the day before the first session. Raise it then if it is still open.
- Image-only decks are read as contact sheets plus the PDF text layer, and the extracted notes go into one brain page under the course project, so any later session can teach from them.

**The last five days:**
- D1 to D3: `learn` + `quiz` for the remaining weeks; every session starts with the warm-up.
- After D3, no new material.
- D4: `exam`, then `redo` the same evening.
- D5: 30 to 45 minutes on the weakest topics only, then an early night.

## Close and learn

When the user corrects how a session runs ("too long", "you already explained that", "don't ask me that in class"), append it to `references/learnings.md` with the date before the turn ends, and patch this file if it is a process issue.
