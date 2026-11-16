# Learnings: how the user wants prompts shaped

The living log for `/anthropic-prompt`. Read it in Step 0, every time. Append an entry whenever the user corrects a produced prompt or the interview (Step 5). Newest at top. Wording and voice corrections go to the `writing` skill's `references/learnings.md` instead.

Entry format:
```
## YYYY-MM-DD [target: main-session/subagent/routine/api] [type: interview/anatomy/effort/length]
Rule: <the generalised preference>
Why: <what the user reacted to>
Before → After: "<weak>" → "<preferred>"
```

---

## Seeds (from the standing rules, not yet from prompt-by-prompt feedback)

## Seed [target: subagent] [type: anatomy]
Rule: a brief bound for a Haiku or Sonnet agent keeps its recipe pointer and the delegation lines; "loosen prescriptive prompts" is advice for frontier-tier sessions only.
Why: `.claude/rules/common/agents.md`: an authored recipe outranks the brief, and loosening it turns a factory into many judgment calls by the models chosen not to make them.
Before → After: "figure out the best way to build the video" → "follow `RECIPE.md`; it outranks this brief; flag conflicts"

## Seed [target: all] [type: interview]
Rule: never ask what the brain or the repo already answers; read first, ask only the genuinely open blocks.
Why: questions the brain can answer waste the user's time.
Before → After: "Which project is this for?" → (read `brain/context/priorities.md`, propose the project as the recommended answer)

<!-- New learnings get appended above this line as the user reacts to produced prompts. -->
