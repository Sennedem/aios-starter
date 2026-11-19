---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/QDsenEcAJIk
tags: [wiki, technique, evals, verification, agents]
related: ["[[wiki/concepts/ai-agent-nondeterminism]]", "[[wiki/techniques/llm-as-judge-with-defined-good]]", "[[wiki/techniques/stopping-criterion-for-self-improvement-loops]]", "[[wiki/sources/nateherk-one-person-business-claude]]", "[[wiki/sources/nateherk-make-it-better-100-times]]"]
---

# Golden-dataset eval loop

A repeatable loop for proving an AI agent behaves correctly, built around a **golden dataset**: a fixed set of test conversations where the correct answer or correct agent action is already known. From [[wiki/sources/nateherk-one-person-business-claude|Nate Herk's one-person business video]] **[04:44-05:59]**.

## The loop

1. **Run the full suite** against the agent. In the worked example that is 16 "mystery shopper" conversations: some normal questions, some designed to provoke a risky action (a billing dispute, a private-data request) or an answer without enough information.
2. **Score it and open the failures.** See the customer's question, the agent's actual answer, and why that answer failed the check (for example, it should have escalated to a human and did not).
3. **Diagnose with the model.** Hand the failed conversation to Claude and ask it to explain the failure and propose a tighter instruction or policy update, instead of working it out by hand.
4. **Rerun the full suite, not only the fixed case.** Agents are non-deterministic (see [[wiki/concepts/ai-agent-nondeterminism|AI agent non-determinism]]), so a fix can hold while a different test now fails. Only a full rerun catches that.
5. **Produce the client report:** score, tests run, what changed, what is still open. Private conversations and prompts stay inside the agency's workspace. The report is what the client is paying for, "proof that their agent was tested before it reached real users," more than the app's score screen. **[06:00-06:19]**

## Why the report matters as much as the score

"The app isn't forcing a perfect score just to make the result look good. It's helping you diagnose and fix." **[05:53-05:59]** The loop does not hide open issues. A report with a known remaining failure ("the agent still mishandled a request to export private customer data") is more useful to a client than a falsely clean scorecard, because it says exactly what is still unverified. A 94 with one open issue, reported as such, is the honest version; calling it "passing" is not.

## Related

A golden dataset is the "defined good" of [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]] made concrete and numeric for agent behaviour, where that page uses a written rubric for subjective work.

[[wiki/sources/nateherk-make-it-better-100-times|Nate Herk, "Make it better" 100 times]] shows the loop step 4 exists to prevent: 100 improvement rounds with no regression suite, so features were silently removed or broken (one model's nav bar, another's dead section). For where to put a stop rule in such a loop, see [[wiki/techniques/stopping-criterion-for-self-improvement-loops|Stopping criterion for self-improvement loops]].

## In this system

`.claude/rules/common/verification.md`: iterate inside the loop, re-verify against the whole spec before reporting done, and state anything unverified as unverified.
