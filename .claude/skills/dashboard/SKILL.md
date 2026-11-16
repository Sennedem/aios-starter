---
name: dashboard
description: Refresh and open the local HUD dashboard. Optionally syncs the calendar, regenerates the data file from tasks.yaml and the brain, opens dashboard/index.html, and updates task progress in tasks.yaml when asked. Use when the user says "/dashboard", "open my dashboard", "refresh the dashboard", "update the dashboard", or "mark <task> X%".
---

# /dashboard: refresh the HUD

The dashboard lives at `dashboard/index.html`. It is presentation only: it reads a data file that `dashboard/build-data.mjs` generates from `tasks.yaml` and the brain (`brain/context/priorities.md`, `brain/context/work.md`, the newest `brain/audits/audit-*.md`). The browser needs no server; the page works from `file://`.

## Steps

1. **If the user asked to change a task,** edit `tasks.yaml` first.
   - "mark <task> 70%": set that task's `progress: 70`.
   - "<task> is done": set `status: done`.
   - New work: append a task block with scalar fields only, values free of colons: `title / area / status / progress / deadline / priority / note`. `area` is a project slug from `brain/projects/` (or `aios`).

2. **Sync the calendar (optional).** Only when a calendar connector exists and the dashboard reads a calendar cache (check `dashboard/build-data.mjs` for a `calendar.json` read). List events for the next 14 days on the primary calendar in the user's timezone, map each to `{date: "YYYY-MM-DD", time: "HH:MM" or "all-day", title}` (all-day events carry a start date instead of a start time), and write:
   ```json
   { "fetchedAt": "<ISO now>", "events": [ ... ] }
   ```
   Get the real current time from `node -e "console.log(new Date().toISOString())"`. If the calendar call fails, leave the existing cache untouched. No connector: skip this step and say so.

3. **Rebuild the data file:**
   ```
   node dashboard/build-data.mjs
   ```
   It prints a one-line summary. If it errors, report the error and stop; never hand-edit the generated data file.

4. **Open it in the browser** (launch it, don't just print the path):
   - macOS: `open dashboard/index.html`
   - Linux: `xdg-open dashboard/index.html`
   - Windows: `start "" dashboard\index.html` (from cmd) or `Start-Process dashboard\index.html` (PowerShell)

   If a tab is already open, tell the user to hard-refresh so the page reads the new data.

## Notes

- `dashboard/build-data.mjs` is the single source of build truth.
- Countdowns come from tasks that have a `deadline:` in `tasks.yaml`.
- The health ring reads the newest `brain/audits/audit-*.md`. Run `/audit` first if it is stale.
