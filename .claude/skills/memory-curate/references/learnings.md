# Learnings: how the user wants memory curated

Read this in step 0, every time. Append an entry whenever the user corrects a curation call (step 4). Newest at top.

Entry format:

```
## YYYY-MM-DD: [action: merge/delete/update/index/rank]
Rule: <the generalized preference>
Why: <what the user reacted to>
Before → After: "<proposed>" → "<preferred>"
```

---

## Seed rule: [action: delete]
Rule: Default to UPDATE or FLAG over DELETE. Never delete a memory without an explicit yes; when two memories might be the same, FLAG rather than merge.
Why: the skill's core guardrail. Memory loss is silent and permanent, and a wrong cut cannot be noticed later.

<!-- New learnings go above the seed rule as the user reacts to curation diffs. -->
