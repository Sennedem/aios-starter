---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: creator
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=N-q-XLQymnU
tags: [technique, youtube, shorts, diagnostics]
related: ["[[wiki/concepts/30k-view-jail]]", "[[wiki/concepts/shorts-retention-vvsa-avd]]", "[[wiki/concepts/seed-audience-testing]]", "[[wiki/concepts/youtube-trust-score]]"]
---

# Diagnosing a flatlined short

Read the ceiling a short flatlined at as the diagnosis. Different ceilings mean different problems, and treating them all as "the algorithm hates me" throws the signal away. Both lists below are transcribed from the video's on-screen slides (01:04-01:07); the narration only says "it's due to one of these".

Source: [[wiki/sources/dmscales-shorts-algorithm|dmscales, "The Entire Shorts Algorithm Explained in 180 Seconds"]]. The bands are creator-empirical and rough.

## Flatlined at 100-10,000 views

The short failed its [[wiki/concepts/seed-audience-testing|seed audience test]] outright.

- Low quality short
- Low [[wiki/concepts/youtube-trust-score|trust score]]
- Oversaturated niche
- **Terrible VVSA + AVD**

## Flatlined at 10k-low 20k views

The short partly held its seed audience but did not earn extension.

- Bad [[wiki/concepts/shorts-retention-vvsa-avd|VVSA + AVD]]
- Bad retention
- Oversaturated niche
- **Unoriginal idea or topic**
- Low trust score

## Flatlined around 30k

The source does not count this as a failure. Reaching about 30k means the short passed every seed audience test it was given; shorts under about 35k views "did really well in the seed audience tests". The constraint is missing audience data, not video quality; see [[wiki/concepts/30k-view-jail|30k view jail]]. The response is to keep uploading, not to overhaul the content.

## Reading the two lists against each other

Four causes appear on both lists: quality, trust, saturation and retention are always in play. The differences are the useful part:

- **Sub-10k adds no unique cause** but rates the retention failure as terrible rather than bad. It is a severity signal: something is badly wrong with the hook or the first seconds.
- **10k-20k uniquely adds "unoriginal idea/topic".** The video was watchable enough to hold a partial audience but gave no reason to extend it. In this band the concept is the bottleneck, not the execution.

Order of investigation: open the retention curve first (initial dip, then flatness, then height), then ask whether the idea was original, then look at niche saturation. Trust is the slowest to move and the least useful thing to react to on a single video.
