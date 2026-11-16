# Inbox

Your drop zone. Put any file here (a PDF, a screenshot, an export, a document) and tell Claude what it is, or just say "it's in the inbox". Claude moves it to where it belongs and leaves this folder empty.

| What you dropped | Where Claude files it |
|---|---|
| An image a note uses | `brain/attachments/` |
| An article, transcript or PDF to learn from | `brain/wiki/raw/`, then `/ingest` splits it into pages |
| A document that belongs to a project | the project's own home, listed in its `otherworlds/` note |
| Something for setup (CV, business plan, price list) | read, the facts go into the brain, the file goes back to your own folders |

A session-start hook reminds Claude when something is waiting here. Large media and office files are gitignored, so nothing dropped here reaches your backup by accident.
