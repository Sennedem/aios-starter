# Dashboard

A single-page HUD for the whole system: deadline countdowns, task progress grouped by project,
cadence rows that are due, projects with their status, the priority order, and the score of the
latest `/audit` with a link to the janitor report.

## Open it

Build the data, then open the page in any browser:

```
node dashboard/build-data.mjs
```

Then open `dashboard/index.html` (double-click it, or drag it into a browser window). No server is
needed: the page reads `data.js` as a plain `<script>`, so a `file://` URL works. Bookmark it.

## How it works

```
tasks.yaml ──────────────────────────────┐
cadence.md ──────────────────────────────┤
brain/context/priorities.md ─────────────┼──► build-data.mjs ──► data.js ──► index.html
brain/projects/*/CONTEXT.md ─────────────┤     (zero-dep Node)    window.AIOS_DATA
brain/audits/audit-*.md (latest) ────────┤
brain/audits/janitor-latest.md ──────────┘
```

- `build-data.mjs` is the only thing that writes `data.js`. Zero dependencies, Node 18 or newer.
  Never edit `data.js` by hand; it is generated and gitignored.
- `tasks.yaml` (repo root) is the task store. Edit status and progress there, or ask Claude
  ("mark the website task 70%"). The `area` of a task is a project folder name under
  `brain/projects/`, or `aios` for work on the system itself.
- Projects come from the folders in `brain/projects/`. The name is the first `#` heading of each
  `CONTEXT.md`, the status is its `status:` frontmatter.
- Priorities are the numbered list in `brain/context/priorities.md`.
- Cadence shows every row of `cadence.md` whose next due date is today or earlier, plus rows that
  have never run.

Before `/setup` has run, the page shows a banner and an empty state in every panel. That is the
expected first look.

## Refresh

| What | How |
|---|---|
| From Claude Code | `/dashboard` |
| By hand | `node dashboard/build-data.mjs`, then reload the page |

## Optional: scheduled refresh

To keep the countdowns current without opening Claude Code, run the build every few hours.

- macOS or Linux, with cron (`crontab -e`):
  `0 */3 * * * cd /path/to/your/aios && node dashboard/build-data.mjs`
- Windows, with Task Scheduler:
  `schtasks /Create /SC HOURLY /MO 3 /TN "AIOS Dashboard Refresh" /TR "node C:\path\to\your\aios\dashboard\build-data.mjs" /F`
  (remove it again with `schtasks /Delete /TN "AIOS Dashboard Refresh" /F`)

## Files

| File | Role |
|---|---|
| `index.html` | HUD shell |
| `styles.css` | Styling (system fonts, no network requests) |
| `app.js` | Renders the panels from `window.AIOS_DATA` |
| `build-data.mjs` | Generates `data.js` from the repo and the brain |
| `data.js` | Generated data (gitignored, do not edit) |
