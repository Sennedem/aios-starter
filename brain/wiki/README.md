---
type: index
status: active
updated: 2026-11-19
domain: wiki
parent: "[[README|Brain]]"
---

# Wiki

This is where outside knowledge goes: videos, articles, PDFs and books. It follows the LLM-wiki pattern: Claude splits each source into small pages, one idea per page, and links them to the pages that already exist. Two sources on the same subject end up connected instead of sitting in two separate summaries.

Run `/ingest <url or file>` and Claude does the filing. Notes about your own work do not belong here; they go in `context/` and `projects/`.

## Structure

- `raw/`: the source as it came in (transcript, article text). Never edited after ingest.
- `sources/`: one page per source: what it is, the main takeaways, links to the pages it produced, and how far to trust it.
- `concepts/`: one idea per page.
- `tools/`: one page per tool or product.
- `techniques/`: how-tos you can act on.
- [[wiki/log|log]]: append-only list of what was ingested and when.

## Index

_Maintained by `/ingest`, one line per page. Pages outside the core pack carry their pack in brackets; `node scripts/packs.mjs` removes a pack with its lines._

### Sources

- [[wiki/sources/buildyourtribe-instagram-algorithm-2026|"NEW Instagram Algorithm: How To Go Viral And Get Followers" by Build Your Tribe]]: Build Your Tribe on the 2026 Instagram algorithm: 15 claims graded (creator)
- [[wiki/sources/dmscales-shorts-algorithm|"The Entire Shorts Algorithm Explained in 180 Seconds" by dmscales]]: dmscales' 180-second Shorts algorithm model: takeaways, on-screen lists and every claim graded (creator)
- [[wiki/sources/nateherk-10000-ai-websites|"I Studied 10,000 AI Websites… Here's what I learned" (Nate Herk)]]: Five conversion patterns for AI-built sites: mirror test, one accent, layers, motion, free sample (web-design)
- [[wiki/sources/nateherk-4-claude-systems-that-sell|Nate Herk: "4 Claude Systems That Sell For $3000+ Right Now (With PROOF)"]]: Four productized Claude builds with prices, pitch math and a blunt proof grade for each (business)
- [[wiki/sources/nateherk-6-best-github-repos-for-claude|"I Tried 100+ Github Repos for Claude. These 6 Are the Best" (Nate Herk)]]: Ten Claude Code repos checked by name, with an overlap table and plugin security cautions
- [[wiki/sources/nateherk-ai-businesses-ranked|Nate Herk: "Every AI Business Ranked from Worst to Best"]]: Thirteen AI business models scored on skill, market and durability; sell judgment, not builds (business)
- [[wiki/sources/nateherk-anthropic-engineers-10x-claude-code|Nate Herk: "Anthropic Engineers Just 10x'd Everyone's Claude Code"]]: Context rules for Claude 5 models, the doctor audit, and what a skill should keep
- [[wiki/sources/nateherk-astra-automations-trigger-dev|Nate Herk: "How to Build GPT-6 Astra Automations (that don't eat your usage limit)"]]: Move deterministic steps to free hosts, keep AI for judgment; a triage table for automations
- [[wiki/sources/nateherk-build-skills-not-agents|Nate Herk: "Anthropic Engineer Explains: What to Build Instead of AI Agents"]]: Skills as apps on a general agent: scripts in skills, descriptions, corrections, verify first
- [[wiki/sources/nateherk-claude-code-mods|Nate Herk: "Claude Code Mods Are Game Changers. Set Up These 5 NOW."]]: Five Claude Code mods toured and graded; mods are unsandboxed plugin code, so review first
- [[wiki/sources/nateherk-fable-5-1-kills-website-slop|"Fable 5.1 FINALLY Kills AI Website Slop" (Nate Herk)]]: Seven rules against AI website slop: concrete references, components, mobile checks, scroll screenshots (web-design)
- [[wiki/sources/nateherk-fable-5-1-release|"Fable 5.1 Just Dropped. It Looks Unreal." (Nate Herk)]]: A release-day video used as a worked example of grading vendor-stated vs creator-observed claims
- [[wiki/sources/nateherk-fable5-karpathy-llm-wiki|"Fable 5 + Karpathy's LLM Wiki is Basically Cheating" (Nate Herk)]]: The video behind the LLM wiki method: auto cross-links, emergent structure, router, portability
- [[wiki/sources/nateherk-grokbot-inbox-agentmail|"Grok Bot Manages My Inbox (and has its own)" (Nate Herk)]]: A labels-only inbox bot on cron, plus a webhook-woken bot with its own inbox
- [[wiki/sources/nateherk-how-anthropic-prompts-fable-5-1|"I Analyzed How Anthropic ACTUALLY Prompts Fable 5.1" (Nate Herk)]]: Four prompting tricks from Anthropic docs: finish line, matched effort, proof, parallel delegation
- [[wiki/sources/nateherk-make-it-better-100-times|Nate Herk: "I Told Claude to 'Make it better' 100 Times (It Went Too Far)"]]: Same prompt 100 times: quality peaked early, then forced changes with no judge turned to churn
- [[wiki/sources/nateherk-managed-hermes-setup|"Set Up a Personal Hermes in 14 Mins (no VPS or mac mini)" (Nate Herk)]]: Managed agent setup end to end, Telegram wiring, and giving an agent real context first
- [[wiki/sources/nateherk-one-person-business-claude|Nate Herk: "Anthropic's CEO: How to Build a 1 Person Business with Claude"]]: Three filters, a live solo product build, a golden-dataset eval run and a human-gated boundary (business)
- [[wiki/sources/nateherk-reverse-engineer-anything-skill|Nate Herk: "I Tested the Viral Reverse Engineer Anything Skill. What You Need to Know."]]: Show the agent finished examples, analyse before building, tag findings seen, inferred or unknown
- [[wiki/sources/nateherk-roast-room|Nate Herk: "Roast Room: How I Use Claude to Think Like the Top 1%"]]: A persona council of subagents debating a decision in rounds; useful perspective, circular validation
- [[wiki/sources/robertbenjamin-tiktok-algorithm-2026|"The FASTEST Way to Go Viral on TikTok in 2026 (TikTok Algorithm Explained)" by Robert Benjamin]]: Robert Benjamin's TikTok growth claims graded against TikTok's own statements (creator)
- [[wiki/sources/vidiq-youtube-algorithm-guide|"The Complete Guide to the YouTube Algorithm" by vidIQ]]: vidIQ's long-form YouTube algorithm guide graded, with where it agrees and clashes with dmscales (creator)

### Concepts

- [[wiki/concepts/30k-view-jail|30k view jail]]: A Shorts ceiling near 30k views is a passed seed test while YouTube learns targeting, not suppression (creator)
- [[wiki/concepts/agent-skills-as-yaml-frontmatter|Agent skills as YAML frontmatter]]: A skill is markdown plus name and description frontmatter, so it ports between harnesses and loads on demand
- [[wiki/concepts/agent-to-agent-email|Agent-to-agent email]]: Give an agent its own inbox only when agents outside your account must reach it; webhooks wake it
- [[wiki/concepts/ai-agent-nondeterminism|AI agent non-determinism]]: One passing rerun proves little because agents vary per run; a growing golden dataset raises confidence
- [[wiki/concepts/ai-business-ranking-criteria|AI business ranking criteria: Technical, Market, Durability]]: Score any AI business on Technical, Market and Durability, plus one business-outcome metric per offer (business)
- [[wiki/concepts/ai-systems-pyramid|AI systems pyramid]]: Climb from plain script to script with AI steps to full agent loop only when needed
- [[wiki/concepts/ai-website-slop|AI website slop]]: Generic AI sites come from vague "make it premium" prompts; fix with references, components, skills and copy (web-design)
- [[wiki/concepts/automation-boundary-human-in-the-loop|The automation boundary]]: Agents handle routine requests end to end; anything touching money or customer data goes to a human
- [[wiki/concepts/broad-appeal-vs-niche-shorts|Broad-appeal vs niche-appeal shorts]]: New channels break out with content anyone enjoys; niche content converts once audience data exists (creator)
- [[wiki/concepts/claude-code-mods|Claude Code mods]]: Mods are unsandboxed TypeScript event handlers in plugins that can rewrite events and draw UI, unlike hooks
- [[wiki/concepts/claude-md-as-router|CLAUDE.md as router]]: CLAUDE.md holds a light map of where things live, not the knowledge itself, so agents search less
- [[wiki/concepts/company-brain-system|Company brain system]]: Sellable client system: an AI that answers from the company's docs and tools (business)
- [[wiki/concepts/context-engineering-then-and-now|Context engineering: then and now]]: Six retired prompting practices for newer models: judgement over rules, interfaces over examples, progressive disclosure
- [[wiki/concepts/corrections-into-durable-instructions|Corrections into durable instructions]]: Route each correction to the skill file, a reference file or an explicit rule, then rerun to verify
- [[wiki/concepts/creator-os-system|Creator OS system]]: Sellable client system producing content in a creator's cloned voice and likeness, sold up front plus monthly (business)
- [[wiki/concepts/cross-source-connections|Cross-source connections]]: One shared wiki lets the AI notice where sources reference each other; humans still check the comparison
- [[wiki/concepts/demand-vs-supply-constrained-business|Demand-constrained vs supply-constrained business]]: Ask whether a client lacks customers or capacity before choosing which AI system to sell them (business)
- [[wiki/concepts/deterministic-vs-nondeterministic-automation|Deterministic vs non-deterministic automation]]: Mark which steps truly need AI; host the deterministic majority as plain code, not an agent harness
- [[wiki/concepts/effort-level-vs-model-tier|Effort level vs model tier]]: Low effort on a newer model can beat max effort on the old one; recheck at each release
- [[wiki/concepts/expert-persona-brain-files|Expert persona: thin agent file, fat "brain" folder]]: Build an expert sub-agent as a thin agent file plus a fixed-schema brain folder
- [[wiki/concepts/flat-vs-foldered-wiki-structure|Flat vs foldered wiki structure]]: Let wiki structure follow the data: folders for varied sources, flat when that makes AI search easier
- [[wiki/concepts/forced-iteration-degrades-output|Forced iteration degrades output]]: Forcing a change every round makes quality plateau then decay; add a judge, keep-or-revert and a stop rule
- [[wiki/concepts/free-sample-pattern|Free sample pattern (interactive tool before the contact form)]]: Put a quiz, estimator or small tool before the contact form so visitors taste the result first (web-design)
- [[wiki/concepts/highlighter-rule-60-30-10|Highlighter rule (one accent colour, 60-30-10)]]: Use one accent colour only on click targets, inside a 60 background, 30 structure, 10 accent split (web-design)
- [[wiki/concepts/instagram-ai-content-labeling|Instagram's wider "AI content" labelling]]: Claim that Instagram over-labels generative edits as AI; the label may cost engagement (creator)
- [[wiki/concepts/instagram-carousel-advantage|Instagram carousels outperform reels (claimed)]]: Claim that carousels get 1.9x reel views; weak evidence from a seller, worth one cheap test (creator)
- [[wiki/concepts/instagram-skip-retention-share-gates|Instagram's three reel gates: skip rate, retention, share rate]]: Instagram reels as three gates (skip rate, retention, sends), compared with the Shorts model (creator)
- [[wiki/concepts/instagram-text-flashing|"Text flashing" on Instagram reels]]: Text shown too briefly to read may cut reel reach; the read-aloud test costs nothing (creator)
- [[wiki/concepts/instagram-trial-reels-duplicate-detection|Trial reels and duplicate detection]]: Trial reels that only swap text over the same footage reportedly count as duplicates (creator)
- [[wiki/concepts/intake-and-follow-up-funnel-system|Intake and follow-up funnel system]]: Sellable client system taking leads from social post to paid booked call without manual chasing (business)
- [[wiki/concepts/intent-and-context-over-task-lists|Intent and context over task lists]]: Tell the model why you ask, not only what; standing context and handoff logs supply that intent
- [[wiki/concepts/layering-for-premium-feel|Layering for premium feel]]: Parallax planes and stacking cards read as premium when subtle, copied from a named reference, checked on mobile (web-design)
- [[wiki/concepts/llm-wiki-pattern|LLM wiki pattern]]: raw sources in, small linked pages out, an index and a log, maintained by the model
- [[wiki/concepts/managed-vs-vps-agent-hosting|Managed vs VPS agent hosting]]: Hosting a standing agent: a managed app for one agent, a VPS for a multi-tool server
- [[wiki/concepts/markdown-portability|Markdown portability]]: A wiki of plain markdown plus routing works with any agent; skills port too, output may differ
- [[wiki/concepts/mirror-test-first-screen|Mirror test (first-screen copy)]]: The first screen must say who it is for, what they get and what to do next (web-design)
- [[wiki/concepts/model-matters-less-than-the-brief|Model matters less than the brief]]: With the same prompt, assets and skill, two model versions matched on quality; the cheaper one wins
- [[wiki/concepts/motion-with-a-job|Motion with a job]]: Every animation does one job; one mover per screen, text readable instantly, a reduced-motion switch (web-design)
- [[wiki/concepts/one-person-business-three-part-architecture|The three-part one-person business architecture]]: A solo software business needs three parts: product workflow, sales and support agent, lead sourcing (business)
- [[wiki/concepts/parallelize-and-delegate|Parallelize and delegate]]: Split large tasks into independent legs run by parallel subagents; the main session stays clean
- [[wiki/concepts/persona-review-panel|Persona review panel]]: Review subjective work with several subagent personas and act only on issues that recur
- [[wiki/concepts/post-viral-honeymoon-phase|Post-viral honeymoon phase]]: After a first viral short distribution gets easier, but posting less or weaker videos reportedly loses it (creator)
- [[wiki/concepts/progressive-disclosure|Progressive disclosure]]: Skills load name and description first, the full body only on a match, to avoid context rot
- [[wiki/concepts/prompt-cache-read-economics|Prompt cache-read economics]]: Why cache-read pricing cuts agentic bills more than one-shot prompts, and when the cache expires
- [[wiki/concepts/prove-its-work|Prove its work]]: Make the agent verify its work against evidence before reporting, and flag anything unverified
- [[wiki/concepts/routine-drift|Routine drift]]: Agent routines reinterpret instructions each run and drift; hard-code destinations and side effects in scripts
- [[wiki/concepts/routine-failure-modes|Routine failure modes]]: Six failure modes to pre-mortem before scheduling stateless agent wake-ups
- [[wiki/concepts/save-scripts-inside-skills|Save scripts inside skills]]: Save a proven script in the skill's folder so later runs reuse it instead of regenerating
- [[wiki/concepts/scroll-feedback|Scroll feedback]]: Sites need some scroll response, but its intensity should match the audience, never maxed by default (web-design)
- [[wiki/concepts/seed-audience-testing|Seed audience testing]]: Each short is tested on a fresh audience group so YouTube can find who the content is for (creator)
- [[wiki/concepts/seen-inferred-unknown|Seen / inferred / unknown]]: Tag every investigative finding as seen, inferred or unknown so guesses never become foundations
- [[wiki/concepts/sell-judgment-not-the-build|Sell your judgment, not the thing you build]]: AI commoditizes built artifacts; diagnosis, change management, taste and trust stay sellable (business)
- [[wiki/concepts/shorts-retention-vvsa-avd|VVSA and AVD: the two Shorts retention metrics]]: VVSA and AVD targets for Shorts, retention curve shape, and diagnostic view bands (creator)
- [[wiki/concepts/skill-description-hygiene|Skill description hygiene]]: A skill's description is its routing: one job, real user words, no overlap with other skills
- [[wiki/concepts/skills-as-apps-model-as-processor|Skills as apps, model as processor]]: Build skills on one general agent instead of a separate agent per job
- [[wiki/concepts/smallest-sufficient-context|Smallest sufficient context]]: Give the smallest context that gets the best result; a keep or cut table for trimming skills
- [[wiki/concepts/stateless-wakeup-handoff-log|Stateless wake-up and handoff log]]: Scheduled agents have no memory; continuity comes from a handoff log written as actions happen
- [[wiki/concepts/subagents-over-agent-teams-for-debate|Sub-agents over agent teams for multi-persona debate]]: For chaired multi-persona debates, a hub of subagents is enough; agent teams cost more
- [[wiki/concepts/subscription-oauth-vs-api-key-auth|Subscription OAuth vs API-key model auth]]: Sign tools in with a subscription you already pay for before pasting a metered API key
- [[wiki/concepts/subscription-vs-api-hosting|Subscription vs API hosting]]: Three cost lanes for AI work: subscription task, free deterministic script host, metered SDK
- [[wiki/concepts/telegram-as-agent-channel|Telegram as an agent channel]]: Wire a standing agent to Telegram for one conversation shared across phone and web
- [[wiki/concepts/tell-it-what-done-looks-like|Tell it what done looks like]]: Give the model the outcome and the definition of done, then let it plan the tasks
- [[wiki/concepts/three-filters-one-person-business|Three filters for a one-person business]]: Three filters for picking a solo business: own capital, software, automatable sales and support (business)
- [[wiki/concepts/three-ps-pain-person-promise|Three P's: pain, person, promise]]: Pin down pain, person and promise before designing a site or positioning an offer (business)
- [[wiki/concepts/tiktok-account-niche-signals|TikTok account niche signals]]: Niche keywords in TikTok name, playlists and bio may help search; one case, cause unproven (creator)
- [[wiki/concepts/tiktok-bot-suspicion-and-shadowban-lore|TikTok bot suspicion and the "shadowban" story]]: The TikTok shadowban story for accounts that only post: unfalsifiable folklore, a cheap habit anyway (creator)
- [[wiki/concepts/tiktok-keyword-signal-stack|TikTok keyword signal stack]]: Same topic keywords in hook, description, three hashtags and comments; graded layer by layer (creator)
- [[wiki/concepts/tiktok-length-and-format-matching|TikTok length and format matching]]: Match the format and length of a topic's winners; completion matters, the length proof is confounded (creator)
- [[wiki/concepts/token-saver-repos-vs-measured-savings|Token-saver repos: advertised vs measured]]: Token-saver repos advertise big cuts but measured savings are small; test before trusting them
- [[wiki/concepts/viewer-tier-conversion|Viewer tier conversion (new, casual, regular)]]: Turning new viewers into casual and regular ones is the channel health metric that matters most (creator)
- [[wiki/concepts/voice-note-to-document-system|Voice note to document system]]: Productized build: a field worker's voice note becomes a branded compliance document, with a review step (business)
- [[wiki/concepts/webhook-vs-cron-routines|Webhook vs cron routines]]: Schedule-triggered and event-triggered agent routines compared; treat a webhook URL and key as a password
- [[wiki/concepts/youtube-channel-baseline-and-explore-exploit|Channel baseline, explore-exploit, and candidate generation]]: Two-stage recommender, explore-exploit testing, and judging uploads against your own channel baseline (creator)
- [[wiki/concepts/youtube-ctr-and-avd-two-questions|YouTube's two questions: will they click, will they watch]]: Long-form YouTube asks will they click and will they watch: CTR and AVD, with curve diagnostics (creator)
- [[wiki/concepts/youtube-format-saturation|Format saturation: when a copied packaging stops working]]: When thousands copy a format, feeds show the biggest channel; find angles the big ones skip (creator)
- [[wiki/concepts/youtube-satisfaction-signal|The satisfaction signal (the metric above the metrics)]]: YouTube satisfaction surveys shape recommendations, so padding for watch time can backfire (creator)
- [[wiki/concepts/youtube-traffic-sources-browse-suggested-search|YouTube traffic sources: browse, suggested, search]]: What browse, suggested and search traffic each reveal about a channel (creator)
- [[wiki/concepts/youtube-trust-score|YouTube trust score and "view jail"]]: The creator model of hidden channel trust and view jail, graded claim by claim (creator)
- [[wiki/concepts/zero-view-jail|Zero view jail]]: A new channel gets zero distribution after failing YouTube's identity screen; graded folklore (creator)

### Tools

- [[wiki/tools/21st-dev|21st.dev]]: UI component gallery whose copy-prompt button hands an agent one proven component to reproduce (web-design)
- [[wiki/tools/addy-osmani-agent-skills|Agent Skills (Addy Osmani)]]: About 25 spec, plan and build skills that keep the plan in files to beat context rot (coding)
- [[wiki/tools/agentmail|AgentMail]]: Real email inboxes for agents, wired to routines by webhook; URL plus key equals trigger access
- [[wiki/tools/apify-mcp-server|Apify MCP server]]: MCP connector to paid ready-made scrapers for sites Claude cannot reach; terms and privacy caveats
- [[wiki/tools/claude-fable-5-1|Claude Fable 5.1]]: Fable 5.1 release facts: savings come from cache reads; check effort claims and model strings yourself
- [[wiki/tools/clay|Clay]]: Sponsored B2B lead-sourcing and enrichment tool, used as the lead leg of a solo business (business)
- [[wiki/tools/codex-scheduled-tasks|Codex scheduled tasks]]: Codex local vs cloud scheduled tasks, one shared thread, handoff endings, probe model access first
- [[wiki/tools/codex-sdk|Codex SDK]]: Runs a Codex agentic loop outside the app on metered credits; top rung of the pyramid (coding)
- [[wiki/tools/design-inspiration-galleries|Design inspiration galleries (godly.website, Awwwards, Motion Sites)]]: Page-level reference galleries to name before generating a site (web-design)
- [[wiki/tools/google-workspace-cli|Google Workspace CLI (`gws`)]]: One CLI plus skills for Gmail, Drive, Calendar, Docs and Sheets; scope OAuth access tightly
- [[wiki/tools/grokbot|Grokbot]]: xAI desktop agent app with bots, cron or webhook routines, connectors and bot-to-bot chat
- [[wiki/tools/hermes-agent|Hermes agent]]: Agent harness with a shared web and Telegram thread, tasks, kanban, skills and memory
- [[wiki/tools/hostinger-managed-agents|Hostinger managed agents]]: One-click managed agent hosting, with provisioning steps and env-var gotchas
- [[wiki/tools/humanizer|Humanizer (blader/humanizer)]]: The skill that strips AI writing tells; the writing skill ships its catalogue
- [[wiki/tools/obsidian|Obsidian]]: the app that shows this vault as linked pages and a graph
- [[wiki/tools/playwright-cli|Playwright CLI (Microsoft)]]: Token-light browser driver that clicks through like a customer and writes re-runnable tests (coding)
- [[wiki/tools/rea-reverse-engineer-anything|REA: Reverse Engineer Anything]]: Open-source skill plus MCP for taking apart an app feature; claims graded against tests (coding)
- [[wiki/tools/scroll-craft|ScrollCraft]]: A scroll-site plugin with design rules and a scroll-screenshot checker; read its hooks first (web-design)
- [[wiki/tools/trigger-dev|trigger.dev]]: Free TypeScript host that runs agent-written automations from a repo, independent of subscriptions (coding)

### Techniques

- [[wiki/techniques/apply-60-30-10-palette-with-claude|Apply a 60-30-10 palette with Claude]]: Pick three colours, give Claude the hex codes, keep the accent on buttons and links only (web-design)
- [[wiki/techniques/claude-doctor-setup-audit|Claude doctor setup audit]]: What the doctor command reports (unused skills, duplication, hidden loaders, broken skills) and how often to run it
- [[wiki/techniques/comparing-model-cost-with-cost-and-usage|Comparing model cost with /cost and /usage]]: Run the same prompt on two models and compare cost and output before switching defaults
- [[wiki/techniques/diagnosing-a-flatlined-short|Diagnosing a flatlined short]]: Read the view ceiling a short stalled at to tell retention, concept and data problems apart (creator)
- [[wiki/techniques/env-file-as-portable-key-vault|.env file as a portable key vault]]: Keep every API key in one gitignored .env so keys move between tools and hosts
- [[wiki/techniques/escaping-zero-view-jail|Escaping zero view jail (new-channel setup)]]: New-channel setup before posting: enable advanced feature eligibility first (creator)
- [[wiki/techniques/front-middle-back-layers|Front, middle, back (three-layer page build)]]: Build pages in three layers (backdrop, content, one lifted action) so the eye knows where to look (web-design)
- [[wiki/techniques/give-agent-context-via-aios-and-grill-me|Give your agent a context repo, or interview it into context]]: Give a fresh agent context by pointing it at a context repo or letting a skill interview you
- [[wiki/techniques/golden-dataset-eval-loop|Golden-dataset eval loop]]: Test an agent against fixed known-answer conversations, fix failures, rerun the full suite
- [[wiki/techniques/inbox-triage-routine|Inbox triage routine]]: A twice-daily inbox bot that labels mail into a few categories and digests to chat, never drafts
- [[wiki/techniques/inspiration-driven-site-prompting|Inspiration-driven site prompting]]: Avoid AI site slop by naming a reference site, the element you like, and why (web-design)
- [[wiki/techniques/instagram-reel-posting-checklist|Instagram reel posting checklist]]: Graded pre-post checklist and Insights reading order for Instagram reels (creator)
- [[wiki/techniques/interview-before-building-an-automation|Interview before building an automation]]: Have the agent interview you on destination, timing, scope, research limits and cost cap first
- [[wiki/techniques/llm-as-judge-with-defined-good|LLM-as-judge with defined good]]: For subjective work, write your own definition of good and give it to a model as the judge
- [[wiki/techniques/main-session-as-orchestrator|Main session as orchestrator]]: The main session dispatches and interprets subagents, yet still owns the outcome and the final pass
- [[wiki/techniques/map-your-day-to-agent-wakeups|Map your day to agent wake-ups]]: Schedule one narrow agent wake-up per moment you would naturally check in yourself
- [[wiki/techniques/match-effort-to-the-task|Match effort to the task]]: Start at high effort, test medium then low, and know that low effort calls fewer tools
- [[wiki/techniques/mod-cache-keeper|Mod: Cache keeper]]: A Claude Code mod that shows the prompt-cache countdown, session costs and a handoff button
- [[wiki/techniques/mod-collision-guard|Mod: Collision guard]]: A mod that asks before one chat edits a file another chat changed recently
- [[wiki/techniques/mod-goal-tracker|Mod: Goal tracker]]: A mod pane showing each running goal's tasks, progress and runtime across parallel chats
- [[wiki/techniques/mod-next-steps-toast|Mod: Next steps]]: A mod that offers about three suggested next actions at the end of every turn
- [[wiki/techniques/mod-recording-mode|Mod: Recording mode]]: A mod that blurs sensitive values on screen while recording, though the model still sees them
- [[wiki/techniques/model-routing-for-ingest|Model routing for ingest]]: Ingest sources with a cheaper model and save the frontier model for synthesis
- [[wiki/techniques/narrow-the-niche-before-general|Narrowing the niche before going general]]: Own one narrow, repeatable niche before expanding: sharper promise, fewer rivals, learnable risks (business)
- [[wiki/techniques/pitch-ai-systems-on-business-outcome|Pitch AI systems on business outcome]]: Pitch AI systems with one numeric question, multiplied out, then prove it cheaply before selling (business)
- [[wiki/techniques/read-only-workflow-audit-prompt|Read-only workflow audit prompt]]: A read-only prompt that finds the smallest cited fix in a multi-skill pipeline
- [[wiki/techniques/refactor-skills-for-newer-models|Refactor skills for newer models]]: Skills written for older models are over-prescriptive; audit and trim them when models improve
- [[wiki/techniques/reverse-engineer-from-the-output|Reverse-engineer from the output]]: Have the agent analyse a finished example first, tag findings, then build from that analysis
- [[wiki/techniques/roast-room-council-debate|Roast room: a council of expert sub-agents debates your decision]]: Expert-persona subagents debate a decision in rounds and end in a verdict
- [[wiki/techniques/screenshot-scroll-verification|Screenshot scroll verification]]: Have the agent screenshot scroll animations frame by frame, plus mobile, before calling it done (web-design)
- [[wiki/techniques/skill-description-audit|Skill description audit]]: One prompt to find overlapping skill descriptions, then three test prompts to validate each
- [[wiki/techniques/start-low-climb-to-judgment-businesses|Start low, climb to judgment businesses]]: Begin with a visible beginner offer and climb through workshops and audits to paid judgment (business)
- [[wiki/techniques/stopping-criterion-for-self-improvement-loops|Stopping criterion for self-improvement loops]]: Stop improve loops with a judge, keep-or-revert, best-so-far snapshots and a plateau rule
- [[wiki/techniques/stress-test-with-subagents|Stress-test with subagents]]: Send many subagents to break a form or webhook automation before real users do
- [[wiki/techniques/tiktok-pre-post-checklist|TikTok pre-post checklist]]: Nine-step graded TikTok checklist: comparables, hook, pacing, keywords, hashtags, account setup (creator)
- [[wiki/techniques/verify-before-returning|Verify before returning]]: Build the human's checks into the skill so it inspects and fixes before returning output
- [[wiki/techniques/wiki-ingest-workflow|Wiki ingest workflow]]: Drop a source in, give one ingest instruction, let the agent split pages and update index and log
- [[wiki/techniques/youtube-baseline-outlier-spreadsheet|The baseline and outlier spreadsheet]]: Spreadsheet your last 20 videos, find what beat your own baseline, and repeat it deliberately (creator)
