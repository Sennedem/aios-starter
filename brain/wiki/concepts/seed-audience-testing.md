---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: creator
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=N-q-XLQymnU
tags: [concept, youtube, shorts, algorithm]
related: ["[[wiki/concepts/30k-view-jail]]", "[[wiki/concepts/broad-appeal-vs-niche-shorts]]", "[[wiki/concepts/youtube-channel-baseline-and-explore-exploit]]"]
---

# Seed audience testing

How Shorts distribution reportedly works on a young channel: each short is shown to a fresh group of roughly 30,000 people, a different group each time, while YouTube builds profiles of both the viewers and the creator. The goal is targeting: finding which audience your content belongs to.

Source: [[wiki/sources/dmscales-shorts-algorithm|dmscales, "The Entire Shorts Algorithm Explained in 180 Seconds"]] (00:35-01:18). The 30,000 figure is single-source folklore with no official basis; the test-then-expand shape is better supported (see below).

## The shape of the graph

Every new channel's view graph looks the same: slow start, spike, flat line. The flat line is the seed audience running out. If the video performs well enough inside that group, YouTube extends it to a few more people to test whether it deserves wider distribution.

## Why each short gets a different group

Because the point is search, not reward. Rotating groups is how YouTube samples the space of possible audiences. Two consequences:

- **A short's performance is partly a draw.** The same video shown to a better-matched seed group performs better, so conclusions from a single video are noisy.
- **Volume is the search algorithm.** Each upload is one sample. On this model, uploading daily is the mechanism by which the targeting converges.

Once it converges, the next short the identified audience responds to gets pushed to a much wider audience: the break out of [[wiki/concepts/30k-view-jail|30k view jail]].

## A second source

[[wiki/sources/vidiq-youtube-algorithm-guide|vidIQ's long-form guide]] describes the same test-then-expand shape ("explore-exploit": a small slice of traffic, expansion if the video beats prediction, 48 hours to a week) but gives no 30,000 figure and says the bar is the channel's own recent baseline. See [[wiki/concepts/youtube-channel-baseline-and-explore-exploit|baseline and explore-exploit]]. Both are creator sources.

## Corollary for new channels

During the search phase the channel has no audience data, so content that needs a matched audience underperforms by construction. Content that works on anyone does not need the search to have finished; see [[wiki/concepts/broad-appeal-vs-niche-shorts|broad-appeal vs niche-appeal shorts]].
