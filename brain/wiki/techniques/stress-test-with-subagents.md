---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [wiki, technique, testing, subagents, verification]
related: ["[[wiki/concepts/prove-its-work]]", "[[wiki/concepts/parallelize-and-delegate]]", "[[wiki/concepts/automation-boundary-human-in-the-loop]]", "[[wiki/techniques/roast-room-council-debate]]", "[[wiki/sources/nateherk-astra-automations-trigger-dev]]", "[[wiki/sources/nateherk-one-person-business-claude]]"]
---

# Stress-test with subagents

After a webhook or form automation is built and verified once, deliberately try to break it before a real user does. From [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk's automations video]]: "spin up 50 different sub agents and have all of them test this thing, try to break it, and then let me know what you find... you can really stress test and QA your own automations before you actually have any sort of human or customer find these bugs" [22:40-22:55].

## The worked example

The edge-case checklist to hand those sub-agents: can the form be spammed several times in a second, and does an email field actually reject input that is not an email?

Separately, a **duplicate-send guard** the build already had was caught working live. A second test run at 12:33 found the same day's earlier message (sent at 12:01) and skipped re-sending "because it would have been essentially the exact same message... duplicate prevention remains intact" [18:39-19:04]. Nobody asked the stress test to check that guard; it surfaced from ordinary re-running, which is itself evidence for running an automation more than once before trusting it.

## The tool-agnostic version

Treat "spin up N agents to attack the thing" as a standard step between build and ship for anything with a form, a webhook or user input. It is the adversarial sibling of [[wiki/concepts/prove-its-work|Prove its work]] (self-verification against a spec) and applies [[wiki/concepts/parallelize-and-delegate|Parallelize and delegate]] to QA.

## Related

- The roast-room skill ([[wiki/techniques/roast-room-council-debate|council debate]]) applies the same many-agents-attack idea to a *decision*, with a forced devil's advocate when the council is unanimous.
- [[wiki/sources/nateherk-one-person-business-claude|Nate Herk's one-person business video]] gives the standing-policy counterpart: [[wiki/concepts/automation-boundary-human-in-the-loop|the automation boundary]], which routes every real refund, deletion or data-export request to a human, permanently. Read together: stress-testing finds where the boundary might leak (spam, malformed input, disguised requests) before launch, and the boundary is the rule that has to hold on every live request afterwards. A boundary that was never attacked is unverified, and an attack with no boundary to test has nothing to check.

## In this system

`.claude/rules/common/verification.md` ("Stress pass for anything interactive") asks for this adversarial pass after the build check.
