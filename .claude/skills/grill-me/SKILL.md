---
name: grill-me
description: Interview the user relentlessly about a plan, design, project or topic, consultant-style, saving every answer to a brainstorm file so nothing is lost, then routing the durable facts into the brain. Use when the user wants to stress-test a plan, get grilled on a design, run a brainstorm or discovery session, sharpen their context, get what is in their head into a document, or says "grill me".
---

# Grill me

Interview the user about every aspect of the topic until you both understand it the same way. Walk down each branch of the decision tree and resolve dependencies one at a time. The goal is to get what is in their head into an organised markdown file, and then to fold the durable facts back into the brain so the system knows more after every session.

This is a thorough intake. Expect to ask many questions. The friction is what surfaces the things they have never written down.

## The capture file comes first

Long interviews fill the context window. Answers held only in the conversation get misremembered, merged or dropped. So every answer goes to disk before the next question. The file is the source of truth. The user should never have to ask you to save.

## Setup, before the first question

1. Create `brain/brainstorms/{YYYY-MM-DD}-{topic-slug}.md` with frontmatter (`type: note`, `status: active`, `domain: meta`, `parent: "[[brainstorms/README|Brainstorms]]"`, `updated:`), a title, the date, the goal of the session and an empty "Open flags" section. Every capture lives in `brainstorms/`, whatever the topic. A polished deliverable that comes out of a session can move to its project folder later; the raw capture stays.
2. Read what the brain already knows about the topic: the relevant `brain/context/*.md` and `brain/projects/<slug>/CONTEXT.md`. Never ask what is already written down.
3. Tell the user where you are saving, in one line. Then ask the first question.

## The checkpoint rule

After every answer, before the next question:

- Append an entry to the capture file: the topic of the question, the facts and decisions from the answer (in their words where the wording matters), and any flags.
- Correct earlier entries when a later answer changes them.
- Then ask the next question.

One answer per write. If the session dies at any moment, the file already holds everything said so far.

## Interview method

- Ask one question at a time. Give your recommended answer with it (your best inference from the brain, the files and the conversation), so the user can confirm, correct or redirect.
- Settle the upstream decision before the ones that depend on it.
- If a question can be answered by reading a file, read the file. If the user hands you a document, read it and raise only what is new.
- When the user cannot answer, record a flag with who could, and move on.
- Continue until the user says you are done or every branch is covered. Near the end ask: "what have we not touched?"

## Capture file structure

```
# {Topic}: discovery notes
Date: {date} · Goal: {one line}

## Summary and key decisions
(running synthesis, updated as you go)

## Q&A log
### Q1: {topic}
- Asked: {question}
- Captured: {facts, decisions, their words where it matters}
- Flags: {open item -> who can answer}

## Open flags
- {item} -> {who can answer}
```

## At the end

- Read the capture file once more for contradictions and gaps, and settle them.
- Give a short recap: what is captured, what is still flagged, the suggested next step.
- If the session surfaced a real decision (a go or no-go, a choice between options, a price), offer the jury in one line: "this surfaced a decision on X. Put it to `/jury`?" It runs only on a yes, with the capture file as its context.

## Route the findings into the brain

The capture file is the raw record. Propose these updates and apply them on the user's OK:

| The session surfaced a durable fact about | Update |
|---|---|
| A project | `brain/projects/<slug>/CONTEXT.md` |
| A shift in what matters now | `brain/context/priorities.md` |
| Who the user is or their situation | `brain/context/about-me.md` |
| How they work or want Claude to work | `brain/context/how-i-work.md` |
| A person | `brain/context/network.md` |
| A new tool, connector or account | `connections.md` |
| A decision and its why | append `brain/decisions/log.md` |
| A standing preference for how Claude behaves | a memory file and its index line |

Rules:

- Only synthesised, durable facts move. The transcript stays in `brainstorms/`.
- Bump `updated:` on every page you touch, and add a line to `brain/brainstorms/README.md` for the new capture.
- A decision is logged with its why.
- If the session changed nothing durable, propagate nothing.
