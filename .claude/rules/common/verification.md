# Verification loops

> This rule covers everything Claude claims to have done: sends, renders, pages, documents, automations, not only code. For hard tasks the full working loop (scope, evidence, self-attack, verify, calibrated report) lives in the `five-gates` skill; load it at task start without waiting to be asked.

## The principle

"Done" is a claim; verification is evidence. Looking finished and working are different things. Never report a task complete because the tool ran: check the live state the task was supposed to change. Origin: an agent once reported a mail wave fully sent when only the live sent folder could say so.

## Definition of done, before starting

Any non-trivial task starts with countable done-conditions (to the user in one line, or in the delegation brief): what exists, how many, and what would prove it works. "Landing page done" becomes "all sections render at mobile and desktop with no overflow; the form accepts valid input and rejects malformed input." If done cannot be counted or observed, sharpen the task before running it.

## Verify before asserting, after finishing

| Claimed done | Verification (not optional) |
|---|---|
| Email or message sent | Read the live sent folder or thread, not the tracker |
| File created, moved or filed | List the destination; open non-trivial files and confirm they are non-empty and on spec |
| Page or HTML deliverable | Screenshot it at mobile and desktop width and look at the screenshots |
| Video or render | Play or frame-check the output file, not the render log |
| Calendar event or reminder | Fetch the event back and confirm its fields |
| Subagent reports done | Check its outputs against its countable done-conditions yourself |

Report what was verified and how. Anything unverified is stated as unverified, never rounded up to done.

## 🔴 Structural verification is not quality verification

| Check type | Answers | Cannot answer |
|---|---|---|
| Structural (duration, hashes, linters, silence detection, transcription, file counts) | Did the machine do what it was told? | Was it told the right thing? |
| Quality (look at the pixels, read the prose, play the audio) | Is this actually good? | |

For any deliverable a human will look at, hear or read, the verification is looking, hearing or reading it. Not the log, not the hash, not the checker. Origin: a batch of videos passed every structural check and was rejected on the first frame anyone opened; looking then found several more defects the checks had also passed.

- Enumerate beats, not scenes. A scene can hold two beats; checking the first does not check the second.
- Sample where it can go wrong, not where it is convenient. The start of a scene often comes before the element that breaks.
- When unsure whether something is a regression, compare against the previous version at the same point.
- Never say "verified" unqualified. Say what was verified: "duration and file count verified; visuals not yet looked at."

## Stress pass for anything interactive

Anything shipped with a form or interaction gets a second, adversarial pass after the build check: drive it with junk (malformed emails, leading spaces, odd option combinations, double submits) until edge cases surface or a genuine pass is earned. Report non-blocking findings honestly ("no duplicate guard") instead of declaring it clean.

## Iterate inside the loop, not across turns

When a check fails, fix and re-verify in the same run until the done-conditions hold. Do not hand the user something 65% right and make them find the gaps; their review should be taste and judgment, not QA.

## Know when an improve loop must stop

"Fix until it passes" has an end: the done-conditions. "Make it better" does not, and left open it peaks and then decays into churn (features added, removed and broken, measured only by lines changed). Any repeated improve pass (a polish loop, an agent rerun, a scheduled loop) gets four guards:

1. A judge before round 1: a defined-good checklist or a score that is not "it changed". No judge, no loop: do one pass and hand it over.
2. Keep the best so far. Snapshot each round that beats the judge; revert a round that scores worse instead of building on it.
3. "Nothing left to improve" is a valid round. Never force a change per round; a forced change is how the decay starts.
4. Stop on plateau. Two rounds in a row without a gain on the judge means stop, and hand the user the best snapshot plus what the judge could not settle (taste).
