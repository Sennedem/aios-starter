---
name: resume-session
description: Load the latest saved session hand-off for this folder (written by /save-session) and brief the user on where things stand before doing any work. Takes an optional date or file path. Use for "/resume-session", "resume", "pick up where we left off", "continue from last time", "load the last session".
---

# /resume-session: read the hand-off, then wait

The counterpart of `/save-session`. It reads the file, gives a fixed-format briefing, and then waits for the user. It does not start working on its own.

## Steps

1. **Find the file** in `~/.claude/session-data/`:
   - no argument: the most recently modified `*-session.md` (or older `*-session.tmp`) whose `**Project folder:**` line matches this folder. If none match this folder, take the newest one and say it belongs to another folder;
   - a date (`YYYY-MM-DD`): the newest file from that date;
   - a path: that file.
   No file found: say "No saved session for this folder. Run /save-session at the end of a session to create one." and stop.
2. **Read the whole file** before saying anything.
3. **Check it against reality:** every file it names still exists (warn for each one that does not), and how old it is (warn when it is more than 7 days old: things may have changed).
4. **Brief the user** in this shape:

```
Session loaded: <path>

Project: <topic>
Building: <two or three sentences in your own words>

Working: <count> items confirmed
In progress: <files>
Not started: <items>

Do not retry:
- <every failed approach with its reason, or "none">

Open questions:
- <items, or "none">

Next step: <the exact next step, or "not set: pick one from Not tried yet">
```

5. **Wait.** Touch no files until the user says what to do. "Continue" or "yes" means: do the next step from the file.

## Rules

- The session file is a read-only record. Never edit it; the next `/save-session` writes a new one.
- "Do not retry" is always shown, even when it says none.
- Facts in the file are as of its date. Re-check anything load-bearing against the live state before acting on it.
