---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=8IyORt-7rOQ
tags: [wiki, source, youtube, fable-5-1, claude, model-release]
related: ["[[wiki/tools/claude-fable-5-1]]", "[[wiki/concepts/prompt-cache-read-economics]]", "[[wiki/concepts/effort-level-vs-model-tier]]", "[[wiki/techniques/comparing-model-cost-with-cost-and-usage]]", "[[wiki/techniques/model-routing-for-ingest]]"]
---

# Source: "Fable 5.1 Just Dropped. It Looks Unreal." (Nate Herk)

YouTube video (05:31) by Nate Herk | AI Automation, published 2026-09-01: https://www.youtube.com/watch?v=8IyORt-7rOQ. A same-day reaction to Anthropic's Fable 5.1 and Mythos 5.1 release blog: Nate reads the blog live, runs Fable 5.1 next to Fable 5 in the desktop app, and does one quick cost comparison before promising a deeper follow-up.

**Source grading (method: [[references/research-source-objectivity|research source objectivity]]):** the video mixes two kinds of claims. Some are what Anthropic states in its own release blog (pricing, cache-read mechanics, the enterprise data-retention option, safeguard changes, availability); others are what Nate observes in a few minutes of hands-on use (one benchmark screenshot read aloud, one single-prompt 3D-bear comparison). He flags both limits himself: "take these metrics and these benchmarks with a grain of salt" [02:09-02:11] and "this is not any sort of definitive test or benchmark" [04:38-04:40]. Each claim below is graded **Anthropic-stated** or **creator-observed**; treat the second kind as a single anecdote, not a trend.

## Key takeaways

- **[00:14-00:23]** Pricing is unchanged ($10/M input, $50/M output), but Fable 5.1 is billed as more token-efficient, so the same workflow costs less at identical rates. **Anthropic-stated.** See [[wiki/tools/claude-fable-5-1|Claude Fable 5.1]].
- **[01:00-01:20]** Anthropic states Fable 5.1 costs about 25% less than Fable 5 for typical token-billed workflows, and up to about 50% less on highly agentic work, because cache-read pricing dropped. **Anthropic-stated.** See [[wiki/concepts/prompt-cache-read-economics|prompt cache-read economics]].
- **[01:21-01:34]** A new enterprise option (Nate calls it "EFS"; probably Anthropic's zero-data-retention offering, the caption is ambiguous) lets enterprise customers opt into no data retention. **Anthropic-stated**, exact name unverified from this source.
- **[01:35-02:04]** Anthropic says it improved safeguards to reduce false positives. The release came within about 12 hours of a separate Anthropic blog on red-teaming an older Claude model toward hacking behaviour. **Anthropic-stated**; Nate notes the timing as context, not as a claim about 5.1.
- **[02:04-02:35]** Anthropic's benchmark charts show Fable 5.1 on low effort beating Fable 5 on max, high and xhigh effort at a fraction of the cost (Nate reads roughly $11.10 against roughly $44 and $34 off the screen). **Anthropic-stated benchmark, creator-read numbers**, with his grain-of-salt caveat. See [[wiki/concepts/effort-level-vs-model-tier|effort level vs model tier]].
- **[03:17-03:41]** Mythos 5.1 is the identical model with more permissive safeguards, gated to two vetted "trusted access" programs (cybersecurity verification and life-sciences verification). **Anthropic-stated.**
- **[03:41-03:56]** Available the same day in the desktop app, the terminal and the API (AWS Bedrock, Google Cloud, Microsoft Azure). The model string was read as "cloud-fable-5-1", almost certainly a caption error for `claude-fable-5-1`. **Anthropic-stated**, exact model string unverified from this source.
- **[03:59-05:09]** Nate's own one-shot test: the identical prompt ("build me a rotating 3D cartoon bear riding a bike") on both models, checked with `/cost` and `/usage`. Fable 5.1: 6m34s, $4.53. Fable 5: $5.41, slightly faster. The 5.1 output looked more realistic to him (shadows, physics). **Creator-observed, single sample**, which Nate calls non-definitive. See [[wiki/techniques/comparing-model-cost-with-cost-and-usage|comparing model cost with /cost and /usage]].

## What to take from a release video

The method outlives the model: separate what the vendor states from what the creator saw, treat a single paired run as an anecdote, and re-check cost on one of your own real tasks before changing how you route work. The cache-read and effort-tier claims bear directly on model routing; see [[wiki/techniques/model-routing-for-ingest|model routing for ingest]] for the tier split on ingestion work.

## In this system

`.claude/rules/common/model-routing.md` decides which model and effort a task runs on; a release like this is the moment to re-check it.
