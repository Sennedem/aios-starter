# Forensic checklist: machine-generation fingerprints

What `scripts/forensics.py` looks for, what each tell means, and how to fix it. Severity depends on the context set in Step 0:

- Academic or graded work: every fingerprint below is CRITICAL (blocks submission). Graders run provenance checks, and these are how "this is AI" gets proven, however good the prose is.
- Business, client or personal work: the same fingerprints are INFO only. Library charts, script-built files and metadata are normal in business work. Note them; do not block.

The scanner only reports. You assign severity, write the issue and, after the user's go, fix it.

---

## The fingerprints

### 1. Author or Application field names a library
`dc:creator` or `Application` contains `openpyxl`, `python-docx`, `python-pptx`, `LibreOffice`, `reportlab`, `xlsxwriter`, `pandas` and similar.
- Means: a script wrote the file; it was never created or saved in the native app. This is the most damning tell, since anyone who opens File → Properties sees the library name.
- Fix: open the file in the real app (Word, Excel, PowerPoint or equivalent), save a fresh copy (this rewrites Author and Application), then run the app's document inspector and remove document properties and personal information. Set a real Author name.

### 2. Implausibly low total editing time
`TotalTime` is 0 to 5 minutes for a document of thousands of words or many slides.
- Means: the file was assembled by a script and only briefly opened in the app. Word processors accumulate real edit time; a genuine multi-author report shows hours.
- Fix: do the real formatting and review pass in the native app (which accrues edit time), or build the final file in the team's own document instead of exporting a script-generated one. Spreadsheets do not track edit time the same way: `TotalTime=0` on an `.xlsx` is normal and is not the tell; the Author field is.

### 3. Revision and edit-time mismatch
A high `cp:revision` (for example 300) with near-zero `TotalTime`.
- Means: programmatic saves bumped the revision counter without human editing.
- Fix: same as #2, genuine editing in the native app, then the document inspector.

### 4. Embedded images carry a plotting-library tag
PNG or SVG bytes contain `matplotlib`, `plotly`, `seaborn`, `Pillow`, `cairo` and similar.
- Means: charts or figures were rendered by a code library, not built in the office suite. The library name is embedded in the image file.
- Fix (graded work): rebuild charts as native spreadsheet charts and diagrams as native shapes or SmartArt. If a generated image must stay, re-encoding it (paste-special as picture, or a save through an image editor) drops the tag; a screenshot also works but loses resolution. Native visuals look more authentic and carry no fingerprint.

### 5. Low formula coverage in a model `.xlsx`
Under about 25% of numeric cells are live formulas (most are typed or pasted numbers).
- Means: the "model" is mostly dead values, not a built model with auditable cell chains. A grader who clicks an output cell and sees a number instead of a formula knows it was generated.
- Fix: rebuild derived figures as formulas referencing the input cells. Raw inputs (figures typed from a filing, pasted price history) are legitimately hardcoded; only the computed outputs (ratios, valuations, scores) must be live formulas.

---

## Not auto-detectable: always confirm by hand

### 6. AI-use declaration
Many courses and some clients require a declaration of AI use. The scanner cannot detect a missing one.
- For graded work, always ask the user whether the assignment requires an AI-use declaration and whether it was filed. A missing declaration is both a direct mark loss and the thing that makes a grader hunt for the fingerprints above. It is the cheapest fix and the easiest to forget.

---

## The one rule that prevents all of this

Never hand in a file a script wrote. Generate text and numbers with AI if you like, place them into the human-owned native document by hand, edit there, run the document inspector, then submit.
