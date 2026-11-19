---
type: note
status: active
updated: 2026-11-19
domain: wiki
pack: core
parent: "[[wiki/README|Wiki]]"
tags: [concept, tokens, claude-code, benchmarks, cost]
related: ["[[wiki/sources/nateherk-6-best-github-repos-for-claude]]", "[[wiki/techniques/comparing-model-cost-with-cost-and-usage]]"]
---

# Token-saver repos: advertised vs measured

Popular "save your tokens" repos advertise large cuts; the one independent test Nate Herk cites found far smaller ones. From [[wiki/sources/nateherk-6-best-github-repos-for-claude|his 10-repo video]] [08:57-09:47]. All figures are creator-relayed from a JetBrains test he does not link. **Unverified:** the test itself was not found.

| Repo | Advertised | Measured (per Nate, citing JetBrains) |
|---|---|---|
| Caveman | about 65% output-token cut | about 8.5% |
| RTK | n/a | no real saving; costlier at low effort |
| Ponytail | about 20% (implied: "half of what it advertises") | about 10% per task; an open Windows bug can stall each message for several seconds |

Also from the video: **Codeburn** shows token spend and flags waste (for example an MCP server that loads on every message but is never used). **Claude Mem** sends usage data by default. **Context Mode** has an open bug that can burn usage. Nate walked back his earlier recommendation of both.

## The lesson

A self-reported saving is a marketing claim until someone runs the same tasks with and without the tool. Measure it yourself before you trust the README: run the same task both ways and compare, as in [[wiki/techniques/comparing-model-cost-with-cost-and-usage|Comparing model cost]].
