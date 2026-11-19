---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, automation, human-in-the-loop, agents]
related: ["[[wiki/techniques/stress-test-with-subagents]]", "[[wiki/concepts/deterministic-vs-nondeterministic-automation]]", "[[wiki/sources/nateherk-one-person-business-claude]]", "[[wiki/concepts/voice-note-to-document-system]]"]
---

# The automation boundary

A standing policy line, not a one-off decision: routine requests flow through an AI agent end to end, but any action that touches **money or customer data** goes to the human, every time, however routine the request looks. From [[wiki/sources/nateherk-one-person-business-claude|Nate Herk's one-person business video]]. **[06:19-07:20]**

## The worked examples

- A routine "how do I rerun only the failed tests" question: Claude finds the answer in the product guide and answers directly, no human involved. **[06:19-06:33]**
- A lead-qualification form: Claude reads the submission, explains why it does or does not fit, and recommends a trial, but "I still make the final decision before anything moves forward... Claude doesn't send an email, charge a card, or promise the customer anything on its own." **[06:33-06:58]**
- A request for a **refund and permanent account deletion**: Claude drafts a response and sends the ticket to the founder, but "it left the actual refund and deletion completely untouched." **[06:58-07:20]**

The founder's framing of "zero employees": nobody stops working; the software absorbs the repetitive volume so the one person is left with "the decisions that require judgment", which in this business are the ones that move money or customer data. **[07:20-07:36]**

## Why the line sits on action type

The boundary is a fixed category (money actions, data actions) checked every time, independent of the agent's own confidence. It is not "anything hard" or "anything the agent is unsure about". That is what makes it a boundary instead of a judgment call the agent makes for itself: an agent about to issue a refund does not get to decide it is confident enough to skip the human, because the category triggers the routing, not the agent's view of the case.

The portable lesson: when scoping a new automation, answer "should this auto-send?" by category, not by how good the draft looks.

[[wiki/techniques/stress-test-with-subagents|Stress-test with subagents]] is how to check the boundary holds under pressure (repeated requests, disguised phrasing) before trusting it in production, instead of assuming the agent will recognise a refund request when it sees one.

## In sold client work

[[wiki/sources/nateherk-4-claude-systems-that-sell|4 Claude Systems That Sell]] shows the pattern in practice: [[wiki/concepts/voice-note-to-document-system|voice note to document]] ships a draft that "a person still reviews and signs off" [00:59]. That is a claim of practice, not a tested boundary, and the [[wiki/concepts/intake-and-follow-up-funnel-system|intake funnel]] auto-sends payment links and waivers with no stated gate.

## In this system

`.claude/rules/common/working-agreements.md` holds the default that nothing is sent without the user's go; `/outreach` drafts and holds every message for approval.
