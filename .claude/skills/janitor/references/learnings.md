# /janitor: learnings

Every correction from the user, dated, plus calibration notes. A correction becomes a rule in `SKILL.md`; two of the same kind demote that change type to "propose only".

Entry format:

```
## YYYY-MM-DD: <change type>
Correction: <what the user reverted or said>
Rule: <the rule now in SKILL.md>
```

## Calibration notes (carried over from the method's first build)

- Dated-claim detection: matching "by" or "until" anywhere near a date floods the scan with history ("proven by", "was a job until"). Require the word directly before the date, or an open-state word ("unresolved", "pending", "days out") nearby, and skip closed-state lines (struck through, superseded, past tense).
- Not catchable by any scan: undated staleness, such as `priorities.md` still describing a finished period. That is what the judgment pass in step 6 is for.
- A scheduled job looked silent because the local clone had not fetched. Fetch first, and mark the check unverified when the fetch fails.

<!-- New entries go above this line, newest first. -->
