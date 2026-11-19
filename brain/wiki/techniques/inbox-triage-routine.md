---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/ff7om2bBLKM
tags: [wiki, technique, email, triage, routine]
related: ["[[wiki/tools/grokbot]]", "[[wiki/concepts/webhook-vs-cron-routines]]", "[[wiki/sources/nateherk-grokbot-inbox-agentmail]]"]
---

# Inbox triage routine

The setup Nate Herk demos for an inbox-cleanup bot ("Nat"), built on [[wiki/tools/grokbot|Grokbot]] in well under 10 minutes (creator-observed) [00:56-01:03][03:03-03:04]. Source: [[wiki/sources/nateherk-grokbot-inbox-agentmail|Grokbot inbox and AgentMail video]].

## The pattern

1. **Fix a small label set up front**, stated in plain language to the bot: **primary, notifications, outreach, urgent**. The bot itself proposed **newsletters** as a fifth during setup, and that suggestion was accepted. [01:18-02:05]
2. **Define each label with one example per category.** Notifications are bank and service alerts; outreach is sponsorship or pitch emails; primary and urgent are anything that needs the human's attention, marked read immediately on arrival ("mark those as red right away"). [01:28-01:45]
3. **Connect the real inbox** through a marketplace connector (Gmail in the demo). Several accounts can each get their own bot or routine. [02:07-02:28]
4. **Run on a fixed twice-daily cron** (6:45am and 6:45pm in the demo) instead of continuously or on every message. That batches the noise into two check-ins a day. [02:29-02:36][03:03-03:04]
5. **Send the digest to a chat surface**, not back into the inbox. The routine posts a message (a ClickUp DM in the demo) summarising what it labelled and flagging what needs a response, tagged with which bot sent it. [02:36-02:44][02:56-03:02]

## The hard constraint: labels only, never drafts

Stated directly and more than once as the defining rule of this bot: **"It doesn't draft anything for me. It literally just labels and marks as red and stuff like that."** [02:49-02:51] The bot changes how the inbox is organised (labels, read state) and reports on it. It never composes or sends on the human's behalf, so every actual reply still goes through the human's own judgment.

The cron choice is the scheduled half of [[wiki/concepts/webhook-vs-cron-routines|webhook vs cron routines]]: email triage tolerates a few hours of delay, so a fixed schedule is enough.

## In this system

`/inbox-janitor` follows the same rule: one label per unread thread, nothing drafted or sent, and a five-line digest of what needs you.
