# metered.json: what the metered-credit guard blocks

`scripts/hooks/metered-guard.mjs` runs before every Bash command Claude issues. When a command
matches one of the patterns in `.claude/metered.json`, the hook blocks it (exit code 2) and tells
Claude to get the user's explicit yes first. After that yes, Claude re-runs the command with the
approval flag appended as a comment, and the hook lets it through.

The file ships with an empty pattern list, so the guard allows everything until you add a pattern.
Add one for every tool that spends money or credits per call: paid text-to-speech, image or video
generation, a paid scraping API, a cloud render.

## Fields

| Field | Meaning |
|---|---|
| `approvalFlag` | The text Claude appends after the user's go, for example `# --user-approved`. |
| `patterns` | Case-insensitive substrings that mark a paid command. A string written as `/regex/` is a regular expression. |
| `safeForms` | Read-only forms of a paid tool (an estimate, a listing) that should never be blocked. They are removed from the command before matching. Same substring or `/regex/` syntax. |

## Example

JSON has no comments, so the example lives here. Copy what fits into `.claude/metered.json`:

```json
{
  "approvalFlag": "--user-approved",
  "patterns": [
    "api.example-voice.com",
    "/\\bnode\\s+\\S*generate-images\\.mjs\\b/",
    "/\\bpython\\s+\\S*tts\\.py\\b/"
  ],
  "safeForms": [
    "/generate-images\\.mjs\\s+(estimate|list)\\b/"
  ]
}
```

Match the invocation (`node ... generate-images.mjs`), not the bare file name, so that reading,
searching or editing the script is not blocked. When a script calls a paid API internally, the
vendor name never shows in the command, so the pattern has to name the script.

## The rule behind it

Before any paid call: read the documented approach and the current budget, tell the user exactly
what will be generated and roughly what it costs, and wait for their yes in this conversation.
Adding the flag without that yes defeats the guard.
