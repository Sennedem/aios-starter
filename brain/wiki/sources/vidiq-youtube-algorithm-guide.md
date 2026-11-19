---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: creator
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=SIp7MeYbz8U
tags: [source, youtube, long-form, algorithm]
related: ["[[wiki/sources/dmscales-shorts-algorithm]]", "[[wiki/concepts/youtube-channel-baseline-and-explore-exploit]]", "[[wiki/techniques/youtube-baseline-outlier-spreadsheet]]"]
---

# Source: "The Complete Guide to the YouTube Algorithm" by vidIQ

A roughly 21-minute explainer (published 2026-05-29) at three levels: beginner (CTR and AVD), intermediate (traffic sources, satisfaction, format saturation), expert (Google's two-stage recommender, explore-exploit, channel baseline).

**Source grading:** vidIQ sells a YouTube SEO and analytics extension, so advice that needs keyword tooling (the search section) deserves a discount; the video itself pitches nothing mid-roll and ends on "watch this next". It mixes **official** facts (the recommender paper, satisfaction surveys), **corroborated** statements (the Todd Beaupre interview) and **creator-inferred** mechanics stated with more confidence than evidence. It mostly covers long-form, which complements the Shorts-only [[wiki/sources/dmscales-shorts-algorithm|dmscales]] set. Quote attributions were web-checked against YouTube's help page and secondary write-ups of the Creator Insider interview; the interview video itself was not watched.

## Claims, graded

| Claim | Time | Grade |
|---|---|---|
| The algorithm asks "will they click" and "will they watch", which map to CTR and AVD | 0:55 | Corroborated ([[wiki/concepts/youtube-ctr-and-avd-two-questions]]) |
| The algorithm finds videos for people rather than pushing them; it needs richer signals than title and description (Beaupre) | 1:20 | Corroborated (secondary coverage of the interview) |
| About 10 consistent videos "starts to tell a story", 50 gives a reliable model | 3:15 | Folklore; the source itself says "no exact numbers, presumably" |
| Retention is judged against similar topic and length; 60% on 6 minutes can beat 50% on 12 | 4:15 | Creator-inferred |
| TV overtook mobile watch time; top-creator video length nearly doubled | 4:29 | Attributed to YouTube; not verified |
| Browse is not subscriber-driven; viewer history decides | 6:44 | Corroborated in direction |
| Suggested moved from topic matching to session and micro-niche matching | 7:46 | Creator-inferred ([[wiki/concepts/youtube-traffic-sources-browse-suggested-search]]) |
| Satisfaction surveys feed recommendations and outrank watch time | 8:55 | **Official** for the surveys; "outranks everything" is rhetoric ([[wiki/concepts/youtube-satisfaction-signal]]) |
| Padding for watch time can get a video suppressed; "good abandonment" | 9:44 | Creator-inferred |
| Format saturation: clones get buried by larger channels using the same format | 11:13 | Creator-inferred ([[wiki/concepts/youtube-format-saturation]]) |
| Two-stage pipeline, co-visitation, a few hundred candidates | 14:20 | **Official** (Google paper) |
| Off-topic posting makes a "null candidate"; the Ryan Trahan pivot story | 14:56 | Inferred from the paper plus anecdote |
| Scoring aims at "will they come back tomorrow" | 16:26 | Plausible; the framing is vidIQ's |
| Explore-exploit; expansion takes 48 hours to a week | 16:57 | Concept official; timing creator-empirical |
| The prediction baseline is your last ~10 videos; subscriber count is irrelevant | 17:49 | **Unverified creator inference** ([[wiki/concepts/youtube-channel-baseline-and-explore-exploit]]) |
| A spreadsheet of the last 20 videos to find outliers that beat baseline on every number | 19:05 | Practical method, not a claim ([[wiki/techniques/youtube-baseline-outlier-spreadsheet]]) |

## Agreements and contradictions with dmscales (Shorts)

- **Agree:** new videos get a small test slice and expand on a pass; oversaturated formats and niches favour the channel with the most data; one clear audience signal beats scattered topics.
- **Tension 1, cadence:** dmscales says upload daily and that posting less re-jails you. vidIQ never asks for volume; it asks for consistency of topic and says an off-topic upload "resets the picture". Different levers; neither official.
- **Tension 2, the hidden score:** dmscales posits a channel [[wiki/concepts/youtube-trust-score|trust score]] and a "30k jail". vidIQ explains the same stalls through baseline-relative performance and null-candidate status, with no 30k number. Two creator models, no official third.
- **Tension 3, watch-through:** dmscales wants near-100% AVD on short Shorts; vidIQ warns against padding long-form for watch time. Surface-specific, not a true contradiction.

## Split pages

- [[wiki/concepts/youtube-ctr-and-avd-two-questions]]
- [[wiki/concepts/youtube-traffic-sources-browse-suggested-search]]
- [[wiki/concepts/youtube-satisfaction-signal]]
- [[wiki/concepts/youtube-channel-baseline-and-explore-exploit]]
- [[wiki/concepts/youtube-format-saturation]]
- [[wiki/techniques/youtube-baseline-outlier-spreadsheet]]

## In this system

Claims are graded with [[references/research-source-objectivity]]; `/ingest` files a new video source the same way.
