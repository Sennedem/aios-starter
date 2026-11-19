---
name: update-aios
description: Pull improvements from the public AIOS starter (new and fixed skills, rules, hooks, scripts, wiki pages) into this copy, without touching anything the user wrote. Shows what changed, applies on the user's yes, merges where they edited a shipped file and shows conflicts instead of overwriting. Use for "/update-aios", "update the AIOS", "get the latest starter", "are there updates", "pull the new skills".
---

# /update-aios: take the starter's improvements, keep everything that is yours

This copy was cloned from the public starter repository. The starter keeps improving. This skill brings those improvements in through a fetch-only `upstream` remote, and never sends anything back.

The work is done by `scripts/update-aios.mjs`. Do not re-derive its logic by hand: run it, read its output, explain it.

## What it never touches

- Brain content the user wrote: `brain/context/`, `brain/projects/`, `brain/decisions/`, `brain/brainstorms/`, `brain/audits/`, `brain/attachments/`, their own references.
- `connections.md`, `cadence.md`, `otherworlds/` notes (except the template), `.env`.
- Voice files (`writing/references/voice-samples.md`, `ban_list.md`), every `references/learnings.md`, skill state files.
- Packs the user removed during setup (`.claude/packs.json`, `removed`).

## Steps

1. **Clean tree first.** Run `git status --short`. If there are uncommitted changes, commit them (`chore: before update-aios`) or ask the user, so the update is one clean, revertable commit.
2. **Plan.** Run `node scripts/update-aios.mjs --plan`. It adds the `upstream` remote if missing (push disabled), fetches, and groups every file:
   - **New**: added in the starter since the last sync.
   - **Updated, unchanged by you**: replaced with the starter's version.
   - **Changed on both sides**: a three-way merge. Clean merges keep both sides' edits.
   - **Retired**: removed by the starter, and the user never edited it.
   - **Left alone**: a removed pack, a file the user deleted, a retired file they edited.
3. **Explain it in plain words.** Group by what the user will notice: "two new skills (`/x`: what it does), the morning brief got a fix for timezones, 14 new wiki pages in the core pack, one rule you edited and the starter also changed". For anything in the merge group, say what the starter changed. Read the starter's version (`git show <upstream ref>:<path>`) for anything you describe; never guess from the file name.
4. **Ask.** "Apply all, pick some, or skip?" Use the choice tool. Nothing is applied without a yes.
5. **Apply.** `node scripts/update-aios.mjs --apply`, or `--apply --only <path> ...` for a subset.
6. **Conflicts.** For each file the script lists as needing the user: open the merged text in `tmp/update-aios/<path>`, show the conflicting part next to what each side wanted, and propose a resolution. Write it into the real file only on the user's yes, then rerun `--apply` so the sync point advances.
7. **Check.**
   - `node scripts/brain-janitor.mjs --local`: zero broken links.
   - `node scripts/doctor.mjs`.
   - If `.claude/settings.json` changed: show the hook diff and say the change applies from the next session.
   - If a skill was added: add its line to the Commands list in `CLAUDE.md` when the update did not already do so.
8. **Commit** the applied files as one commit: `chore: update from aios-starter <short sha>`. Push only through the usual private backup.
9. **Report:** what was applied, what was left alone and why, any conflict still open.

## Notes

- If the user's copy was made with GitHub's "Use this template" button, it shares no history with the starter. The first run then has no sync point: files that differ are treated as edited and offered as merges with no base, so they show as conflicts for the user to decide. After the first full apply, `.aios-upstream` holds the sync point and later runs are precise.
- If `upstream` cannot be fetched (offline, or the starter moved), say so and stop.
- A wiki page the starter added that belongs to a pack the user removed is skipped by design. If they want a removed pack back, they say so; take it out of `removed` in `.claude/packs.json` and rerun.
