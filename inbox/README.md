# Inbox

Your drop zone. Put any file here (a PDF, a screenshot, an export, a document) and tell Claude what it is, or just say "it's in the inbox". Claude moves it to where it belongs and leaves this folder empty.

**There are two inboxes.** This folder, and the `_inbox` folder `/setup` creates in your cloud drive for drops from your phone (its path is the `inbox:` line in `otherworlds/work-folder.md`). Claude checks both before saying a file is not there, and empties both when it files.

| What you dropped | Where Claude files it |
|---|---|
| An image a note uses | `brain/attachments/` |
| An article, transcript or PDF to learn from | `brain/wiki/raw/`, then `/ingest` splits it into pages |
| A document that belongs to a project | the project's own home, listed in its `otherworlds/` note |
| Finished work, by kind | the matching folder in your work folder, mapped in `otherworlds/work-folder.md` (setup fills in this row per kind of file) |
| Something for setup (CV, business plan, price list) | read, the facts go into the brain, the file goes back to your own folders |

A session-start hook (`scripts/hooks/inbox-check.mjs`) lists what is waiting in both inboxes. Large media and office files are gitignored, so nothing dropped here reaches your backup by accident.
