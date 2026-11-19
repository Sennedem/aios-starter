---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: creator
parent: "[[wiki/README|Wiki]]"
source: https://www.youtube.com/watch?v=N-q-XLQymnU
tags: [concept, youtube, shorts, algorithm, folklore-graded]
related: ["[[wiki/concepts/youtube-trust-score]]", "[[wiki/techniques/escaping-zero-view-jail]]", "[[wiki/concepts/30k-view-jail]]", "[[wiki/concepts/tiktok-bot-suspicion-and-shadowban-lore]]"]
---

# Zero view jail

The state where a new channel's shorts are pushed to nobody at all: zero viewers, not a small audience. It happens when YouTube's initial account review fails to establish that a real person posting genuine content is behind the channel, so no [[wiki/concepts/seed-audience-testing|seed audience]] is ever allocated.

It is the opposite of [[wiki/concepts/30k-view-jail|30k view jail]], where distribution works normally while YouTube gathers data. Zero view jail is an identity problem; 30k view jail is a data problem.

Source: [[wiki/sources/dmscales-shorts-algorithm|dmscales, "The Entire Shorts Algorithm Explained in 180 Seconds"]]. Creator vocabulary, not an official YouTube term. Graded as folklore with a real kernel in [[wiki/concepts/youtube-trust-score|YouTube trust score]].

## Cause

The bot screen at channel creation. A brand-new account on a brand-new email, with no history and no identity verification, looks like a spam farm, so YouTube declines to spend viewers finding out.

TikTok creator lore tells the same story: a silent "bot suspicion" shadowban for accounts that only post. It is folklore there too, with no official basis. See [[wiki/concepts/tiktok-bot-suspicion-and-shadowban-lore|TikTok bot suspicion]] ([[wiki/sources/robertbenjamin-tiktok-algorithm-2026|Robert Benjamin]]).

## Fix

Prove personhood before posting. The claimed make-or-break is advanced ("third level") feature eligibility in YouTube Studio, which is a real, documented setting. The full checklist and its grades are in [[wiki/techniques/escaping-zero-view-jail|escaping zero view jail]].
