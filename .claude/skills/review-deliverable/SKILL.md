---
name: review-deliverable
description: Pre-submission review of any deliverable (report or doc, deck or slides, model or spreadsheet) before it is handed in or sent. Runs a file-forensic AI-fingerprint scan (metadata, openpyxl/python-docx authorship, edit time, plotting-library tags in figures, formula coverage) then a quality review of referencing, writing quality, fact-checking and flow across paragraphs, slides and sheets. Produces a severity-ranked, location-anchored issue log; review-only, fixes applied on the user's go. Use before submitting coursework or sending a deck or proposal, or when the user says "/review-deliverable", "review this before I hand it in", "check this for mistakes" or "is this ready to send".
---

# review-deliverable

Catch the avoidable mistakes before anything ships: the file fingerprints that get work flagged as machine-made, plus a full quality pass on referencing, writing, facts and flow. Review-only: produce an issue log and never edit the deliverable until the user approves the fixes.

## The two layers

1. Forensic: `scripts/forensics.py` scans the actual file(s) for machine-generation fingerprints. Always runs. See `references/forensic-checklist.md`.
2. Quality: you read the content for referencing, writing quality, fact-checking and flow. See `references/quality-checklist.md`.

## Workflow, in order

### Step 0: load and scope

Read `references/forensic-checklist.md`, `references/quality-checklist.md` and `references/learnings.md` (learnings override defaults). Then set the context:
- Academic or graded work: forensic fingerprints are CRITICAL; the referencing style and any AI-use declaration apply.
- Business, client or personal work: fingerprints are INFO only (script-built files and library charts are normal there); a citation style may not apply; weight quality, flow, fact-checking and brand voice.

Infer the context from the file's location and the matching `otherworlds/` note or `brain/projects/<slug>/CONTEXT.md`; ask only if it is genuinely unclear.

### Step 1: identify the exact files and the standard

Confirm the precise file(s) to be handed in: the version that will actually be submitted, not a draft. Ask if it is ambiguous, since metadata differs per copy. For graded work, find the rubric or requirements file to hold the work against, and ask the user for it if it is not found. A deck or proposal is held against its brief or brand standard.

### Step 2: forensics

Run the scanner on every file to be submitted:
```
python .claude/skills/review-deliverable/scripts/forensics.py "<file1>" "<file2>" ...
```
It handles `.docx`, `.xlsx` and `.pptx` with the standard library; formula coverage needs `openpyxl` and is skipped without it. Capture every `[FLAG]` and map each to a severity using the Step 0 context. The AI-use declaration (forensic checklist #6) cannot be auto-detected: ask the user directly.

### Step 3: quality review (read the content)

Run the four dimensions as parallel subagents (Sonnet tier, since each executes a fixed checklist), one per dimension. Each gets the file paths, its checklist section and the Step 0 context, and returns location-anchored findings with severities. The main session merges, dedupes and settles severity conflicts; it does not re-read the whole deliverable. A short deliverable (about 5 pages or less) is cheaper to review inline than to brief four agents on.

- Referencing: one style, consistent in-text format, no key collisions, closure both ways, sources resolve.
- Writing quality: AI tells (the `writing` skill's ban list and `references/humanizer.md`), voice consistency across co-authors, rubric alignment, no leftover scaffolding or placeholders.
- Fact-checking: triangulate load-bearing claims, weigh source objectivity, flag the unverifiable, check internal arithmetic.
- Flow and cross-artifact: report numbers match the spreadsheet and the slides, one value per fact, paragraph-to-paragraph and slide-to-slide logic, numbering and captions, page, word and slide limits.

Look at the pages, not only the text. Export the document to PDF the way it will be handed in, then render or open each page and look at it. Layout defects (an equation that collapsed into plain text, a table split across pages, a breached page limit) only show on the rendered page. Check the PDF's page count and its properties too (Author, Creator, for example with `pypdf`), since the PDF is usually what is submitted.

For figures and numbers, open the companion files (the spreadsheet behind a report's tables, the data behind a chart) and reconcile them. Cross-artifact contradiction is the highest-signal failure.

### Step 4: write the issue log (do not touch the deliverable)

Write `REVIEW_<deliverable-stem>_<YYYY-MM-DD>.md` beside the reviewed file:
- A one-line verdict, plus what was reviewed, against what standard, and the date.
- CRITICAL / HIGH / MEDIUM / LOW sections, each issue location-anchored as problem → why → fix.
- Fact-check verdicts (✅ confirmed, ⚠️ verify).
- A suggested fix order (dependent fixes gated).

Take today's date from the environment; do not guess it.

### Step 5: deliver and offer fixes

In chat, lead with the verdict: submit-ready, or these blockers first. List CRITICAL and HIGH inline so the user need not open the log. For graded work, always include the AI-use declaration reminder. Then offer to apply the mechanical fixes on the user's go: strip metadata (a save in the native app plus its document inspector), standardise references, reconcile numbers, rebuild figures natively. Judgment calls stay with the user.

### Step 6: capture feedback (do not skip)

When the user corrects the review (what to catch, what to ignore, severity, phrasing), append a dated, tagged before → after entry to `references/learnings.md`. If it is a durable cross-skill fact, also save it to the Claude Code memory directory for this project.

## When in doubt

- The file convicts before the prose does: forensics first, always.
- Hold every finding to a location; an abstract note is not actionable.
- Never edit the deliverable in this skill. Review, then fix on the user's go.
