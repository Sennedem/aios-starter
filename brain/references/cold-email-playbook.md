---
type: reference
status: active
updated: 2026-11-19
domain: meta
pack: outreach
parent: "[[references/README|References]]"
tags: [outreach, cold-email, playbook, research]
---

# Cold-email playbook: what the evidence says

A research synthesis (five parallel legs, about 40 sources, July 2026) behind the `/outreach` engine. Every claim is graded: **[E]** evidenced (several independent sources, or a primary source), **[V]** vendor data (large samples, but published by a company that sells sending tools), **[C]** practitioner consensus (no measured data), **[U]** unverified or untraceable: never quote these numbers as fact.

Standing caveat: almost every large cold-email dataset comes from a sending-tool vendor (Gong, Woodpecker, Belkins, Lavender, Instantly). The directions agree across vendors; the exact percentages are marketing-grade.

Before any cold send, check the cold-contact rules for the recipient's country. Rules for consumers and businesses often differ, and in some countries unsolicited commercial e-mail is not allowed even to businesses.

## The blueprint for a first-touch cold e-mail

| Element | Recommendation | Evidence |
|---|---|---|
| Length | 50 to 125 words, 3 or 4 sentences; replies drop hard past about 200 words | [V] Gong, 28M+ e-mails (2025); Backlinko, 12M (2019) |
| Subject | 1 to 4 words, lowercase, no sales language ("quick question about [company]") | [V] Gong with 30MPC, 85M+ e-mails (2025) |
| Opener | A personal observation tied to why you are writing. Flattery ("love what you're building") is discounted in 2025-26; the "I hope this finds you well" penalty is consensus, not a study | [V] and [C] |
| Personalisation | **Trigger- or relevance-based is the sweet spot**: about 3x the baseline reply rate across Belkins, Sopro and Woodpecker, while deep one-to-one research hits the same ceiling (about 17 to 18%) for far more effort. Lavender's 231k-e-mail counterweight: well-graded e-mails lift replies only about 27%, so expect modest gains, not vendor headlines | [V] |
| Pitch | Don't. Pitching inside the e-mail cuts replies (Gong: by up to 57%). The offer is one line, no feature list | [V] Gong (2025) |
| Call to action | **Ask for interest or permission, not time.** "Can I send you a short video or example?" beats "do you have 30 minutes?" at the cold stage; asking for a specific time only wins later in the deal. Asking for time triggers a loss-averse refusal, while asking for interest is a low-friction yes (a micro-commitment). Taught by Josh Braun, 30MPC and Alex Berman | [V] direction (Gong, 304k, write-up verified); [U] the exact "2x" and "12% vs 7%" figures are vendor repackaging: don't quote them |
| Format | Plain text or close to it. Claims about the size of the effect are scattered; the direction is consensus | [C] |
| Links and images in e-mail 1 | No images, attachments or tracking pixels; at most one link, ideally none. Move the link or deliverable to the reply in the same thread after a "yes" | [V] placement studies from Smartlead, Instantly and warmforge, triangulated |
| Send window | Tuesday to Thursday, 8:00 to 12:00 in the recipient's time zone | [V] Belkins, 7.5M e-mails (2025-26) |

## The permission-based ask

- **What it is:** end e-mail 1 with "Shall I send you a short video that shows this for [company]?" instead of a meeting request or an embedded sample. On "yes", send the video or deliverable as a reply in the same thread.
- **Why it works (three effects stacked):** (1) a low-friction yes: interest, not time [V]; (2) e-mail 1 stays free of links and attachments, which helps inbox placement [V]; (3) their reply is the strongest engagement signal the mail provider sees for your sender reputation [C], and it is a micro-commitment that makes the follow-up warm.
- **Video prospecting itself:** Vidyard and Loom claim 3 to 5x reply lifts, which is vendor self-report with no independent replication found [U]. Treat the video as unproven and the ask-first structure as the evidenced part.
- **Verdict:** make the permission ask the default first-touch call to action. The deliverable behind it can be a personal video, a link to a relevant example plus a three-line concrete case, or anything else that fits the segment. The ask-first structure is what matters.

## Follow-ups

- **How many:** 2 or 3 follow-ups. Follow-up 1 is the single highest-yield touch; returns fall and spam-complaint risk climbs past touch 3 or 4. [V] Woodpecker (20M) and Belkins (16.5M), which share a data lineage, so they count as one confirmation, not two.
- **Spacing:** 2 to 4 business days after touch 1, wider after that. Vary it; do not be robotic. [C]
- **Same thread** for follow-ups (Woodpecker: sequence reply rate went from about 9% to 13% with threading). Caveat: if e-mail 1 landed in spam, threaded follow-ups land there too. A fake "Re:" on a new thread does harm. [V]
- **Add value; don't bump.** "Just checking in" measurably underperforms, so every follow-up brings a new angle or asset (a case number, a concrete example, a different pain). The widely shared "0.8% vs 5.1%" figures are untraceable [U]; the direction is solid [V] (Gong's "checking in" penalty).
- **A break-up e-mail** as the final touch reliably beats the late-sequence average; the size of the effect is unverified. [C]
- **Multichannel:** adding a LinkedIn touch lifts replies meaningfully (Belkins: about 28% more appointments; "2 to 3x" claims are vendor-inflated). An optional layer, not the core. [V]

## Deliverability at low volume (under about 25 a day from one domain)

- Google's February 2024 bulk-sender rules (DMARC, one-click unsubscribe, a 0.3% spam-rate ceiling) apply in full only from 5,000 messages a day. Below that: SPF or DKIM, and stay under the spam-complaint threshold. [E] Google's own sender guidelines (primary).
- 5 to 25 a day is inside the safe ramp for an established inbox without warm-up tooling. [V]
- Spam-trigger word lists are largely myth in 2025-26: reputation, authentication and engagement dominate. Do not add word rituals. [C]
- Replies are the engagement signal that builds sender reputation, so a call to action that generates replies is itself a deliverability strategy. [C]

## Rejected along the way

- "80% of sales need 5 follow-ups" and "92% of reps quit after 4": recycled pre-2020 folklore, untraceable. Rejected.
- "12% vs 7% reply rate for interest asks": untraceable to any Gong publication. Direction kept, number rejected.
- "Plain text is now blocked more by AI filters": single source, untraceable. Ignored.
- Flattery as personalisation ("love your work"): discounted by 2025-26 consensus. Use relevance observations only.

## Checklist for e-mail 1

1. A permission or interest ask as the call to action; the meeting request waits for the first "yes".
2. No link in e-mail 1; the deliverable goes in the reply after a positive answer.
3. Subject of 1 to 4 words, lowercase, no sales language.
4. About 70 to 110 words; the offer stays one line.
5. Sent Tuesday to Thursday, 8:00 to 12:00 recipient time.
6. Touch 2 brings a new concrete angle; touch 3 is the break-up.

## In this system

`/outreach` builds, lints and sends cold e-mail along these lines, drafts first and nothing sent without your go.
