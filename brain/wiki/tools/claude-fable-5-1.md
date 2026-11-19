---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=8IyORt-7rOQ
tags: [wiki, tool, claude, fable-5-1, anthropic, model-release]
related: ["[[wiki/concepts/prompt-cache-read-economics]]", "[[wiki/concepts/effort-level-vs-model-tier]]", "[[wiki/techniques/comparing-model-cost-with-cost-and-usage]]", "[[wiki/sources/nateherk-fable-5-1-release]]"]
---

# Claude Fable 5.1

Anthropic's model release, announced 2026-09-01 alongside a sibling model, Mythos 5.1. Source: [[wiki/sources/nateherk-fable-5-1-release|Nate Herk's release-day reaction video]] [00:00-05:31]. The page is kept for the model facts and for what it shows about reading a release: where the savings come from, and which claims to check yourself.

## What's new (Anthropic-stated, per the release blog as read in the video)

- **Price held flat, cost went down.** Same $10/M input and $50/M output as Fable 5 [00:14-00:19]. The stated figures of about 25% cheaper per workflow and about 50% cheaper on agentic work come from a cut in the cache-read price, not the token price. See [[wiki/concepts/prompt-cache-read-economics|prompt cache-read economics]].
- **Effort-tier claim:** Fable 5.1 on low effort is shown beating Fable 5 on its highest effort settings in Anthropic's published benchmarks, at a fraction of the cost [02:04-02:35]. See [[wiki/concepts/effort-level-vs-model-tier|effort level vs model tier]]. Nate: take the benchmark with a grain of salt [02:09-02:11].
- **Enterprise zero-data option** ("EFS" in the captions, probably a mis-hearing of a zero-data-retention feature name): enterprise customers can opt into no data being retained [01:21-01:34]. The name is unverified from this source; check the Anthropic blog before citing it.
- **Safeguards improved, fewer false positives** [01:35-02:04]. The release came about 12 hours after a separate Anthropic blog on red-teaming an older Claude model into hacking behaviour. Nate notes the timing; it is not a claim about 5.1's own safety work.
- **The release blog was designed by Fable 5.1** (a new colour and theme picker, a "made by Fable 5.1" credit) [00:44-01:00], continuing Anthropic's habit of having the new model design its own announcement.

## Relationship to Mythos 5.1

Mythos 5.1 is stated to be the identical underlying model, differing only in more permissive safeguards for two vetted "trusted access" programs.

## Availability

Same day: the desktop app, the terminal and the API through Amazon Web Services, Google Cloud and Microsoft Azure [03:41-03:56]. The model string was read aloud as "cloud-fable-5-1", almost certainly `claude-fable-5-1`. That is unverified: confirm the exact API string before using it in scripts.

## Creator's hands-on read (one anecdote, not a benchmark)

Nate ran an identical prompt on both models and pulled cost with `/cost` and `/usage` (method: [[wiki/techniques/comparing-model-cost-with-cost-and-usage|comparing model cost with /cost and /usage]]). Fable 5.1 came in at $4.53 and 6m34s, Fable 5 at $5.41 and slightly faster, and he judged the 5.1 output more realistic. In his words it is "not any sort of definitive test or benchmark" [04:38-04:40].

## What to do with a release like this

If the cache-read and effort claims hold, the biggest saving shows up on agentic, multi-turn work that re-reads a lot of cached context. Check that on one of your own real tasks with `/cost` instead of trusting a single demo, and verify the model string before you hard-code it anywhere.
