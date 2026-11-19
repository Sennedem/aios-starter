---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: creator
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=N-q-XLQymnU
tags: [source, youtube, shorts, algorithm]
related: ["[[wiki/concepts/shorts-retention-vvsa-avd]]", "[[wiki/concepts/youtube-trust-score]]", "[[wiki/concepts/seed-audience-testing]]", "[[wiki/techniques/diagnosing-a-flatlined-short]]", "[[wiki/sources/vidiq-youtube-algorithm-guide]]"]
---

# Source: "The Entire Shorts Algorithm Explained in 180 Seconds" by dmscales

A 3-minute YouTube Shorts growth explainer. The creator's claim to authority is his own analytics, shown on screen: a 12.4M-view short (+195.4K subscribers, 65.3% stayed to watch, 0:29 AVD), a channel period of 71.0M views, 400K watch hours, +41.4K subscribers and $5,962.84, and a post-breakout week of daily uploads landing 25K, 524K, 633K, 467K, 263K, 3,521K and 12K views.

**Source grading** (per [[references/research-source-objectivity|research source objectivity]]): a creator-empirical source, not a platform-official one. The author sells nothing directly but closes with two funnels (a "viral niches" playlist and a Discord offering free channel reviews), so there is a mild incentive toward confident, simplified rules. It uses community vocabulary ("trust score", "view jail", "30k seed audience") that YouTube has never published. Treat the metric targets as useful empirical benchmarks and the mechanism story as folklore with a real kernel. The single directly verifiable item is feature eligibility, a real YouTube Studio setting. The retention claims were cross-checked against YouTube's own Shorts ranking documentation.

## Key takeaways, timestamped

- **00:01-00:24** A new channel is first screened for bot-ness. Fail it and shorts are pushed to nobody: [[wiki/concepts/zero-view-jail|zero view jail]]. The claimed fix: an aged channel, an old email with history, and above all advanced ("third level") feature eligibility. See [[wiki/techniques/escaping-zero-view-jail|escaping zero view jail]].
- **00:24-00:35** Everything feeds a hidden [[wiki/concepts/youtube-trust-score|trust score]]: how confident YouTube is that spending viewers on you will pay off.
- **00:35-01:18** Each short goes to a fresh, roughly 30,000-person [[wiki/concepts/seed-audience-testing|seed audience]]. The flatline near 30k is a test being passed, not a punishment ([[wiki/concepts/30k-view-jail|30k view jail]]). The slide at about 01:10 reads: "my last 10 shorts all got 30k views :( youtube hates me. DONT FALL FOR THIS TRAP. A short getting to 30k views means it passed every seed audience test. Shorts <35k views did really well in the seed audience tests."
- **01:04-01:07** Two diagnostic lists for where a short flatlines; sub-10k and 10k-low-20k are different problems. See [[wiki/techniques/diagnosing-a-flatlined-short|diagnosing a flatlined short]].
- **01:18-01:28** On a brand-new channel with no audience data, broadly appealing content breaks out; niche-interest content needs data the channel does not have yet. See [[wiki/concepts/broad-appeal-vs-niche-shorts|broad-appeal vs niche-appeal shorts]].
- **01:28-01:43** Retention outweighs every other stat: flat curve, high, small initial dip. Good retention can rescue a video whose other stats are bad. Worked example on screen: a 0:26 short, 79.6% stayed to watch, 0:29 AVD. Targets in [[wiki/concepts/shorts-retention-vvsa-avd|VVSA and AVD]].
- **01:43-01:50** Engagement can also rescue a weak video, but spammy CTAs cost trust, and the on-screen example (a fake share-button overlay) is against YouTube policy.
- **01:50-02:07** The biggest trust lever is [[wiki/concepts/viewer-tier-conversion|converting new viewers into casual and regular viewers]] (example panel: 88.7% new, 11.3% casual, under 0.1% regular), which is the argument for daily uploading.
- **02:07-02:38** After a first viral video comes a [[wiki/concepts/post-viral-honeymoon-phase|honeymoon phase]], but high trust can be lost: posting less or dropping bad videos pushes you back into view jail or subscriber-only distribution.
- **02:38-02:49** Niche saturation is the overriding constraint: in a crowded niche YouTube favours the most trustworthy channels, so a new channel starts at a disadvantage.

## On-screen lists the narration only gestures at

```
Views flatline at 100 - 10,000:
  - Low quality short
  - Low trust score
  - Oversaturated niche
  - TERRIBLE VVSA+AVD

Views flatline at 10k - low 20k:
  - Bad VVSA+AVD
  - Bad retention
  - Oversaturated niche
  - Unoriginal idea/topic
  - Low trust score

VVSA:  <80%
AVD:   100% on shorts >30 seconds
       85-90% on shorts 40 - 1 min+
vvsa = viewed versus swiped away
avd  = average view duration
```

The `<80%` and `>30 seconds` on the targets slide are almost certainly slips for "at least 80%" and "under 30 seconds"; the reasoning is on [[wiki/concepts/shorts-retention-vvsa-avd|the VVSA and AVD page]].

## Claims, graded

| Claim | Grade | Note |
|---|---|---|
| Retention matters more than any other stat; get the curve flat, high, with the smallest initial dip | **Corroborated** | YouTube's own Help doc names "average percentage viewed" and "% who chose to view" as core Shorts ranking inputs. Direction matches. |
| Targets: VVSA about 80%, AVD about 100% of length on sub-30s shorts, 85-90% on 40s to 1min+ | **Creator-empirical** | VVSA and AVD are real YouTube Studio metrics, so they are checkable. The thresholds are the author's, not YouTube's. Still the most useful numbers in the video: they turn a vague "improve retention" into a pass/fail test. |
| Views flatlining at 100-10,000 means low-quality short, low trust, oversaturated niche, terrible VVSA and AVD | **Creator-empirical** | Rough bands. |
| Views flatlining at 10k-low 20k means bad VVSA and AVD, bad retention, oversaturated niche, unoriginal topic, low trust | **Creator-empirical** | Rough bands. |
| Videos that "appeal to anyone without needing data" go viral on new channels | **Plausible** | Mechanically sensible: broad-appeal content survives a poorly targeted seed audience. |
| "Trust score" as a hidden channel-level metric | **Folklore (real kernel)** | Not a published YouTube metric, but channel-level quality signals demonstrably exist. Useful as a metaphor, useless as a number. |
| Seed audience of "around 30,000 people", the "30k view jail" | **Folklore** | No official basis. vidIQ describes the same test-then-expand shape with no such figure. Do not plan against this number. |
| Fix view jail with an aged channel, an aged Gmail and a YouTube Premium subscription | **Reject** | Unverifiable account-farming lore. |
| Enable "third level feature eligibility" | **Real, and actionable** | Maps to YouTube's genuine Advanced Features verification tiers. Whether it affects distribution is unproven; that it gates upload volume is documented fact. |
| Spammy CTAs cost you trust and breach policy | **Corroborated in direction** | Aggressive engagement bait is against YouTube policy. |
| Upload daily; posting less in a high-trust state re-jails you | **Folklore, consequential if true** | No official support. Build Your Tribe says the opposite for Instagram. |
| Oversaturated niches favour the most-trusted channels | **Plausible** | vidIQ makes the same point about copied formats ([[wiki/concepts/youtube-format-saturation|format saturation]]). |

## How it sits next to other sources

- [[wiki/sources/vidiq-youtube-algorithm-guide|vidIQ]] covers long-form and agrees on the test-then-expand shape and on saturation, but explains stalls with a channel baseline instead of a trust score and asks for topic consistency instead of daily volume.
- [[wiki/sources/robertbenjamin-tiktok-algorithm-2026|Robert Benjamin]] (TikTok) agrees that completion is the engine and tells a parallel bot-suspicion story.
- [[wiki/sources/buildyourtribe-instagram-algorithm-2026|Build Your Tribe]] (Instagram) has the same hook, retention, spread shape and disagrees on posting gaps.

## Split pages

- [[wiki/concepts/shorts-retention-vvsa-avd|VVSA and AVD: the two Shorts retention metrics]]
- [[wiki/concepts/broad-appeal-vs-niche-shorts|Broad-appeal vs niche-appeal shorts]]
- [[wiki/concepts/youtube-trust-score|YouTube trust score and "view jail"]]
- [[wiki/concepts/seed-audience-testing|Seed audience testing]]
- [[wiki/concepts/30k-view-jail|30k view jail]]
- [[wiki/concepts/zero-view-jail|Zero view jail]]
- [[wiki/concepts/viewer-tier-conversion|Viewer tier conversion]]
- [[wiki/concepts/post-viral-honeymoon-phase|Post-viral honeymoon phase]]
- [[wiki/techniques/diagnosing-a-flatlined-short|Diagnosing a flatlined short]]
- [[wiki/techniques/escaping-zero-view-jail|Escaping zero view jail]]

## In this system

Claims are graded with [[references/research-source-objectivity]]; `/ingest` files a new video source the same way.
