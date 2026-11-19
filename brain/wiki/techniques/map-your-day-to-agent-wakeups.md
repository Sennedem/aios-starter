---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
source: https://youtu.be/eg_1NXDcoPk
tags: [wiki, technique, scheduling, automation]
related: ["[[wiki/concepts/stateless-wakeup-handoff-log]]", "[[wiki/tools/codex-scheduled-tasks]]"]
---

# Map your day to agent wake-ups

A technique for deciding how many scheduled wake-ups a recurring agent needs, and when. Nate Herk offers it as general advice in the middle of his video "I Gave GPT 6 Astra $10,000 to Trade Stocks...And This Happened", even though the example is trading [02:07-02:28]:

> "Think about your day like this. You know, market open, market close, what do you do? Maybe before the market opens, do you look at some stuff? Maybe an hour in, do you look at some stuff? You know, maybe before close, do you look at some stuff? And just sort of put yourself on this like one-day calendar because then you can just basically make agents to do those things at those times to help you out a little bit."

## The method

1. Put yourself on a **one-day calendar** for the process you are automating. Use your own natural checkpoints, not the automation's.
2. Name each moment you would personally check in: before it starts, some time in, before it ends (in the source: before market open, an hour in, before close).
3. Turn each checkpoint into **one scheduled wake-up** instead of a single big periodic job. The demoed schedule ends up with six wake-ups across a trading day, each with a narrow, named job: read news and choose stocks; find a qualifying trade; review positions; manage positions; close out; confirm and record [01:49-02:56].

The payoff: how often the agent wakes comes from how a human would naturally check in, instead of an arbitrary interval (every N minutes). Each run gets a clear, bounded job description instead of "check on things."

Use it for any new recurring routine: before setting an interval, ask "when would I check this myself, and what would I be looking for each time?" One wake-up per answer. Because each wake-up starts with no memory of the last, pair this with a [[wiki/concepts/stateless-wakeup-handoff-log|handoff log]].

## In this system

[[references/automation-and-cadence]] covers how recurring work is scheduled here, and `cadence.md` lists it.
