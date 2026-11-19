---
type: reference
status: active
updated: 2026-11-19
domain: meta
pack: study
parent: "[[references/README|References]]"
tags: [studying, learning-science, ai-tutors, school]
---

# Studying with AI: what the evidence says

Synthesis of three research legs (learning science, trials of AI study help, existing AI study tools), compiled October 2026. It is the evidence base for `/study`. Evidence labels: **high** = meta-analyses or several randomised trials, **moderate** = a few trials or one lab, **low** = a single small study, a vendor report, or inference. Vendor = the company selling the tool.

## The answer in four lines

1. Being tested beats rereading, by a lot. Retrieval practice and spacing do most of the work (high).
2. AI that hands out answers makes exam scores worse. AI that makes you attempt first, gives hints and works from the course's own solutions is safe and sometimes better than class (high for the harm, moderate for the gain).
3. Feeling you know it is not knowing it. Only producing it yourself, unprompted, after a gap counts (high).
4. Nobody has studied AI help during a live lecture. Everything about that mode is inference.

## Learning science (what to do)

| Technique | What it is | Evidence | Note for the AI helper |
|---|---|---|---|
| Retrieval practice | answer from memory, no notes | high: g = 0.61, 0.51 vs restudy (Adesope 2017, 118 studies) | practise in the exam's format: matched format g = 0.63 vs 0.53 |
| Spacing | spread study over days | high (Cepeda 2008) | for a test in a week, the best gap is about 1 to 2 days |
| Successive relearning | recall to 3 correct, then relearn on later days | moderate to high, one lab (Rawson & Dunlosky 2011) | 3 correct in session 1, then 1 correct on each later day |
| Interleaving | mix problem types | moderate: g = 0.42, maths 0.34, words -0.39 (Brunmair & Richter 2019) | only after each type is learned; never for vocabulary |
| Worked examples, then faded, then problems | see a solved one, fill gaps, then solo | high for novices: g = 0.48 (Barbieri 2023); reverses for experts | skip examples once the student can set it up alone |
| Pretesting and failed attempts | guess before being taught | moderate (Kornell, Hays & Bjork 2009) | a wrong guess plus feedback beats reading |
| Self-explanation | explain why, in your own words | moderate (Dunlosky 2013) | prompts must be specific; vague ones lower the effect |
| Sleep | sleep between learning and relearning | moderate to high (Diekelmann & Born 2010; Mazza 2016) | no new material the night before; no all-nighter |
| Feedback timing | immediate vs delayed | low to moderate, mixed | feedback only after the student commits an answer |

Low utility (Dunlosky 2013): rereading, highlighting, summarising.

### Illusions of knowing

- Judging "I know this" right after seeing it follows fluency and is wrong; judging after a delay with only the cue is accurate (Bjork, Dunlosky & Kornell 2013).
- Students drop flashcards too early, which lowers scores (Kornell & Bjork 2007).
- So a restatement that the AI confirms is recognition, not recall. A topic counts as known only after the student produces it unprompted, after a topic switch or a day. Log their confidence next to the result and flag the gaps.

### Five days before an exam (inference from the sources, not a tested protocol)

- D1: pretest question, then a short explanation or worked example, then free recall to 2 correct. Sleep.
- D2: cold recall of D1 with a confidence rating before the reveal. Re-quiz misses, add new topics.
- D3: mixed recall of D1 and D2; first interleaved set of problem types. No new material after D3.
- D4: closed-book, timed practice exam in the exam's format. Misses to 2 correct. Compare confidence with the result.
- D5: 30 to 45 minutes on the weakest 20% only. Early night.

### By material type

- **Calculations** (statistics, operations research, finance): worked example, faded steps, own problems, then mixed types. A problem only counts on fresh numbers.
- **Rules and theory** (law, management theory): short-answer recall, then apply the rule to a new fact pattern; "why" questions.
- **Arguments** (philosophy): reconstruct the argument from memory, premises then conclusion, then an objection.
- **Language:** block new words first, then spaced production (from your language into the target language); never drop a card early.

## AI tutors: when they help, when they hurt

| Study | Design, N | Result | What drove it | Status |
|---|---|---|---|---|
| Bastani et al., PNAS 2025 | randomised trial, ~1,000 high-school maths students | answer-giving GPT cut the unassisted exam score 17%; a hint-only tutor with teacher solutions did no harm (-0.004) | answers vs hints | peer-reviewed |
| Kestin et al., Scientific Reports 2025 | crossover trial, 194 Harvard physics students | AI tutor beat in-class active learning, 0.73 to 1.3 SD, in less time | instructor solutions in the prompt; steps enforced by the platform | peer-reviewed |
| De Simone et al., World Bank 2025 | randomised trial, ~650 students, Nigeria, 6 weeks | +0.31 SD; +0.21 SD on the year-end exam | teacher-guided sessions | working paper |
| Google, Sierra Leone 2025 | randomised trial, 1,763 | +0.26 SD | 2% of replies gave direct solutions | vendor |
| Oreopoulos & Low, NBER 2026 | 18 schools, 2 years, Khanmigo | no gain beyond Khan Academy without AI | students quit when it refused answers | working paper |
| University of Maryland 2025-26 | randomised trial, 2,379 undergraduates | grades down 0.27 to 0.37 SD | the AI replaced coursework; 0.7% of requests asked for feedback on an attempt | unreviewed |
| Wang & Shane, SSRN 2026 | 4 arms, intro accounting and microeconomics | no AI mode raised the unassisted quiz; "clarify mistakes after own work" was safest | attempt first | preprint |
| Socratic vs direct (Stanford n=122, SIGCSE 2026 n=178, Eastwood 2026 n=132) | small trials | strict Socratic: more engagement, no more learning; rated worst, pushed students to other AIs | rigidity | mixed, small |
| Kosmyna / MIT 2025; Gerlich 2025; Lee (CMU and Microsoft) 2025 | EEG n=54; surveys | heavy AI use goes with less critical thinking | offloading | preprint or correlational |
| Anthropic Education Report 2025 | observational | ~47% of student chats were straight answer-seeking | n/a | vendor, no outcomes |
| OpenAI study mode 2025 | trial, 300+ | +15% in economics, nothing in neuroscience | n/a | vendor, no confidence intervals |

### Design rules that follow

1. The student attempts first; the AI responds to the attempt (Bastani, Wang & Shane, Maryland).
2. Hints, not answers, on the first ask; the answer after a real attempt or on "just tell me" (Bastani; Stanford and Eastwood show rigid refusal backfires).
3. Ground everything in the course's own slides, solutions and workbooks (Kestin, Bastani; students cannot spot AI errors).
4. Put the sequence in the tool's structure, not in hopeful prose (Kestin: the prompt alone could not hold the step order).
5. Short turns, one question at a time (Kestin, LearnLM).
6. Only closed-book, delayed performance counts as learned (Bastani, Wang & Shane).
7. The AI starts the quizzes; on-demand use goes unused (Khanmigo, Sierra Leone).
8. Do not trust the feeling of mastery; check it (Bastani, reviews of OpenAI's study mode).
9. Never replace the lecture or the reading; point back to them (Maryland).
10. Flag anything that is not in the course material.

### Live lecture (no evidence, inference only)

No rigorous study of real-time AI questions during lectures exists; there are only vendor apps and hobby tools. Best guess: answer directly and briefly, anchored to the current slide (being Socratic mid-lecture costs the next slide), park everything else in a list, and turn that list into the after-class quiz.

## Existing systems worth borrowing from

- ChatGPT study mode (leaked prompt): one question per turn, two tries before the reveal, end an activity when it has done its job.
- Claude learning mode: route by request. "Explain or solve" gets taught; "make me X" gets delivered.
- NotebookLM: retake only the missed questions; per card, got it or missed it.
- universal-examprep-skill (GitHub, ~300 stars): slides and past papers in, cites the page, keeps a mistake book. The closest existing match.
- claude-tutor (GitHub, small): new / learning / learned / mastered states; mistakes logged with the diagnosed cause.
- study-skill and ai-tutor (GitHub, small): review warm-up capped at 3 items; intervals computed by a script, not the model.
- socratic-study-mentor (GitHub, small): a `park` command for tangents.

## Gaps

- Almost all trials are in maths, physics, computer science or English; nothing on university law or philosophy.
- The five-day schedule extrapolates lab data; no exam-prep trial of it exists.
- One search engine per research leg; vendor numbers are unverified.

## Sources

- Adesope et al. 2017, retrieval practice meta-analysis: https://doi.org/10.3102/0034654316689306
- Cepeda et al. 2008, spacing: https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf
- Rawson & Dunlosky 2011, successive relearning: https://doi.org/10.1037/a0023956
- Brunmair & Richter 2019, interleaving: https://doi.org/10.1037/bul0000209
- Expertise reversal meta-analysis 2025: https://www.sciencedirect.com/science/article/pii/S0959475225000660
- Bjork, Dunlosky & Kornell 2013, self-regulated learning: https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/RBjork_Dunlosky_Kornell_2013.pdf
- Kornell, Hays & Bjork 2009, failed attempts: http://hayslab.com/publications/kornell.hays.bjork.2009.pdf
- Mazza et al. 2016, sleep and relearning: https://pubmed.ncbi.nlm.nih.gov/27530500/
- Bastani et al. 2025, PNAS: https://www.pnas.org/doi/10.1073/pnas.2422633122
- Kestin et al. 2025, Scientific Reports: https://www.nature.com/articles/s41598-025-97652-6
- De Simone et al. 2025, World Bank: https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099548105192529324
- Google, Sierra Leone 2025 (vendor): https://deepmind.google/blog/measuring-the-impact-of-learning-with-ai-in-sierra-leone-and-beyond/
- Oreopoulos & Low 2026, NBER: https://www.nber.org/papers/w35620
- University of Maryland 2025-26: https://edsi.umd.edu/sites/default/files/ai26-1598.pdf
- Wang & Shane 2026, SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7282556
- Kosmyna et al. 2025: https://arxiv.org/abs/2506.08872
- Gerlich 2025: https://www.mdpi.com/2075-4698/15/1/6
- Lee et al. 2025, CHI: https://dl.acm.org/doi/full/10.1145/3706598.3713778
- Anthropic Education Report 2025 (vendor): https://www.anthropic.com/research/anthropic-education-report-how-university-students-use-claude
- OpenAI learning outcomes (vendor): https://openai.com/index/understanding-ai-and-learning-outcomes/
- LearnLM 2024 (vendor): https://arxiv.org/abs/2407.12687

## In this system

`/study` turns the design rules above into a fixed sequence: attempt first, grounded in the course page and its materials, a mastery gate of 2 correct in a session plus 1 cold on a later day, and parked items from class that open the next session.
