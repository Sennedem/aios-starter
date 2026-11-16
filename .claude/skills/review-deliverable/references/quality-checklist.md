# Quality checklist: the four review dimensions

The content review, done by reading the deliverable (not by script). Hold every finding to a location (section or paragraph, cell or tab, slide number, table or figure number), never an abstract note. Tier each with the severity scheme below.

## Severity
| Tier | Meaning | Action |
|---|---|---|
| CRITICAL | Integrity or hard-constraint failure (AI fingerprints on graded work, numbers that contradict the source model, a breached page or word limit, a missing mandatory file) | BLOCK: fix before submitting |
| HIGH | Real quality or accuracy issue (wrong figure, broken citation, unsupported claim) | WARN: fix before submitting |
| MEDIUM | Clarity or process concern | INFO: consider |
| LOW | Polish or minor style | NOTE: optional |

Plus a separate fact-check verdicts section: ✅ confirmed correct, ⚠️ fix or verify.

---

## 1. Referencing (graded work; skip for business work unless it cites sources)
- One style throughout. No Harvard in one section and APA in another, and no second informal reference list after the clean one.
- In-text format consistent: `(Author, year)` everywhere, not a mix such as `(Company 2025a)`, `(Company, 2025a)` and `(Company Inc., 2025c)`.
- No key collisions: the same in-text key must resolve to the same source in every section. Multi-author reports often reuse "2025a" for different documents in different sections. Build a source-to-key map and check every section against it.
- Closure both ways: every in-text citation has a reference-list entry, and every entry is cited.
- Sources resolve: open each link and confirm it exists and supports the figure. No fabricated references, no bare-domain URLs.
- Every figure is traceable to a named source in the text, not only in the end list.

## 2. Writing quality
Reuse the `writing` skill's `references/ban_list.md` and `references/humanizer.md` for AI tells.
- AI tells and filler: ban-list phrases, hedging, generic openers, tricolons, dash overuse, "it's important to note", restated-conclusion padding.
- Voice consistency across co-authors: a report stitched together by several people swings in register. Flag the jarring jumps and recommend a unifying edit pass. The unevenness is itself a soft AI signal.
- Rubric alignment: map sections to the marking criteria and flag any criterion thinly served or missing. Name the frameworks the course teaches where graders reward visible use.
- Hygiene: no leftover template scaffolding ("[Target ~4 pages | Name]", "[Auto-populate]"), no placeholder table of contents or summary, no duplicated sections.

## 3. Fact-checking
- Triangulate key claims: verify the load-bearing numbers and dates against a credible external source; do not trust the draft. A "record close" or a percentage quoted from a paywalled article are typical slips.
- Source objectivity: never lean only on the subject's own materials; flag advocacy or political sources and weight them explicitly; state the basis when a figure has competing definitions.
- Flag the unverifiable: anything you cannot confirm gets ⚠️ with what is needed to close it.
- Internal arithmetic: totals sum, ratios are plausible (a 720-day collection period or negative interest coverage is a red flag), percentages reconcile.

## 4. Flow and cross-artifact consistency
The dimension that catches stitched-together work, and the highest-signal one for multi-author documents.
- Cross-artifact agreement: the same fact must match everywhere, so report numbers equal the spreadsheet model equal the slides. A report table that contradicts its own mandatory spreadsheet is what a grader catches first. Reconcile every shared figure to one source of truth.
- One value per fact: the same metric must not appear with different numbers in different sections.
- Paragraph to paragraph: each paragraph follows from the last, and transitions carry an argument instead of just "Moreover". Section intros set up what follows; conclusions discharge what was promised.
- Slide to slide (decks): one idea per slide, a through-line across the deck, titles that state the takeaway instead of the topic, no later slide contradicting an earlier one.
- Sheet to sheet (workbooks): tabs reference each other with live links instead of re-typed values; a change in inputs flows through; labels and units are consistent across tabs.
- Numbering and captions: tables and figures numbered 1 to N in order, the table of contents matches, every table and figure has a caption and a source line.
- Hard constraints: page, word and slide limits, required sections, mandatory attachments. A breached limit is CRITICAL.
