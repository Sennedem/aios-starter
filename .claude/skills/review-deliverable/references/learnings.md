# review-deliverable: learnings

Accumulated feedback on how the user wants deliverables reviewed. Read this first (Step 0); it overrides defaults where it conflicts. Append a dated, tagged entry whenever the user corrects the review: what to catch, what to ignore, how to tier severity, how to phrase findings.

Entry format (newest at top):
```
## YYYY-MM-DD [context: graded/business · format: report/deck/sheet]
Rule: <generalised preference>
Why: <what triggered it>
Before → After: "<what I did>" → "<what they wanted>"
```

---

## Seed [context: graded · format: report+sheet]
Rule: detection of AI in graded work is file-forensic, not prose-based. Lead the review with the metadata and fingerprint findings (Author=openpyxl, plotting-library image tags, near-zero edit time, formula coverage), then quality.
Why: a team report with clean prose was graded down as "full of AI" purely on file provenance. An earlier cleanup pass had added fingerprints (python-docx, matplotlib) while fixing content. This skill exists to stop that.
Before → After: "review prose for AI tells first" → "run forensics.py first; prose is the weakest signal"
