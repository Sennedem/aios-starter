---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: creator
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=N-q-XLQymnU
tags: [concept, youtube, shorts, retention, metrics]
related: ["[[wiki/techniques/diagnosing-a-flatlined-short]]", "[[wiki/concepts/broad-appeal-vs-niche-shorts]]", "[[wiki/concepts/youtube-ctr-and-avd-two-questions]]", "[[wiki/concepts/instagram-skip-retention-share-gates]]", "[[wiki/concepts/tiktok-length-and-format-matching]]"]
---

# VVSA and AVD: the two Shorts retention metrics

The two numbers that decide whether a YouTube Short gets pushed past its first test audience, and the source treats them as the primary quality signal, above views and subscribers. Both are real metrics in YouTube Studio, so they work as a pass/fail test rather than a vibe.

Source: [[wiki/sources/dmscales-shorts-algorithm|dmscales, "The Entire Shorts Algorithm Explained in 180 Seconds"]] (01:28-01:50), cross-checked against YouTube's own ranking documentation.

| Metric | Full name | What it measures |
|---|---|---|
| **VVSA** | Viewed versus swiped away | Of the people served the short, the share who chose to watch rather than swipe straight past. The hook metric. Shows in Studio as "stayed to watch" or "chose to view". |
| **AVD** | Average view duration | How long the average viewer stayed, in seconds. Meaningful only as a percentage of the video's length. |

## The targets

The slide at about 01:41, verbatim:

```
VVSA:  <80%
AVD:   100% on shorts >30 seconds
       85-90% on shorts 40 - 1 min+
```

Two slips in the slide, read against the narration:

- **VVSA `<80%`** contradicts the narration, which says to get VVSA and AVD "up to here". The worked example on screen shows 79.6% stayed to watch, so the intended target is a floor of roughly 80%, not a ceiling.
- **AVD `>30 seconds`** only makes sense as "under 30 seconds", since the next line covers 40 seconds and up.

Read that way:

- **VVSA:** about 80% floor.
- **AVD:** about 100% of length on shorts under about 30 seconds. Over 100% is normal and good, because rewatches count.
- **AVD:** 85-90% on shorts of 40 seconds to a minute or more.

These thresholds are creator-empirical, not YouTube-published. The metrics themselves are official: YouTube's Help documentation independently names "% of viewers who chose to view", "average view duration" and "average percentage viewed" as core Shorts ranking inputs. The choice of metrics is platform-confirmed; the numbers are not.

The AVD targets are strict. On a sub-30-second short you are being asked for full watch-through, and only past about 40 seconds does 85-90% become acceptable. That is a direct argument for keeping shorts short unless the content really sustains a longer hold.

## Percentage, not seconds

A raw AVD in seconds is meaningless without the video's length. Seven seconds is excellent on a 7-second short and catastrophic on a 45-second one. Always divide.

The counterintuitive consequence: shortening a video raises its score without improving the content. At a fixed absolute AVD, a shorter video scores a far higher percentage viewed, which is the actual ranking input. Length is a lever on the metric as well as on the edit.

## The target curve

The worked example on screen (about 01:34): a 0:26 short with 79.6% stayed to watch and a 0:29 AVD, about 111% of length. The curve starts above 200%, has a small initial dip, then sits near flat at about 100-119% across the body and tails to about 70% at the end.

The stated goal for the retention graph, in priority order:

1. **As flat as possible:** no mid-video cliff.
2. **As high as possible:** the body near or above 100%, rewatches included.
3. **Smallest possible initial dip:** the drop in the first second or two is where most shorts die.

The initial dip is the most diagnostic part of the curve, because it is where setup, framing and throat-clearing live. That is why the opening frame and the first spoken line carry so much weight. [[wiki/concepts/broad-appeal-vs-niche-shorts|Broad-appeal vs niche-appeal shorts]] covers the content-side lever on the same problem.

## Why it dominates

Retention is described as able to rescue a video whose other stats are bad: the algorithm weights it above the rest. Engagement can also rescue a weak video, but chasing it with spammy CTAs costs [[wiki/concepts/youtube-trust-score|trust]] and can breach policy, so retention is the safe lever and engagement the risky one.

In practice: when reviewing a short, open the retention curve before the view count. Views are an outcome of retention plus targeting luck; retention is the part you control.

## Diagnostic bands

Where a short's views plateau tells you which failure you have. Both bands list retention first; the boundaries are creator-empirical and rough. Full method in [[wiki/techniques/diagnosing-a-flatlined-short|diagnosing a flatlined short]].

| Views flatline at | Likely causes (on-screen list) |
|---|---|
| 100-10,000 | Low-quality short, low trust, oversaturated niche, terrible VVSA and AVD |
| 10k-low 20k | Bad VVSA and AVD, bad retention, oversaturated niche, unoriginal topic, low trust |

## Other surfaces

- **Long-form:** the same pair becomes CTR and AVD, and [[wiki/sources/vidiq-youtube-algorithm-guide|vidIQ]] warns that padding to raise watch time can cost satisfaction. The near-100% targets here are Shorts-specific. See [[wiki/concepts/youtube-ctr-and-avd-two-questions|the two questions]] and [[wiki/concepts/youtube-satisfaction-signal|the satisfaction signal]].
- **TikTok:** TikTok's own newsroom post says finishing a longer video is a strong interest signal, weighted above weak ones, so completion is the shared engine across platforms. TikTok publishes no VVSA or AVD style targets. See [[wiki/concepts/tiktok-length-and-format-matching|TikTok length and format matching]].
- **Instagram:** skip rate (a 3-second window), retention above 50% at the end, then send rate form the reels equivalent; see [[wiki/concepts/instagram-skip-retention-share-gates|Instagram's three reel gates]]. That host's retention bar is far looser than the ~100% AVD here, and the two measure different things, so they are not directly comparable.
