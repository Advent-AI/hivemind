# Council round 4: decomposition at medium, models, and the next full run (read-only)

Same 27 articles, fixed K5 before-states, 3 draws. Gold matching uses the frozen scorer, kept evidence only. Thesis verdicts come from
blind Codex readers, each comparison read in one mixed packet.

**Decomposition at medium (Luna):**

| | K5 medium | K6a medium | K6b medium |
|---|---|---|---|
| Helpful (of 255) | 235 | 214 (of 246; 1 empty answer failed) | 217 |
| Core (of 75) | **75** | 72 | 72 |
| Not-kept kept | 95 | 78 | 68 |
| New theses | 93 | 61 bet / 12 small / 2 duplicate | 53 bet / 9 small / 0 duplicate |

**Models on K6b** (DeepSeek in JSON mode with the schema stated in the system text and checked by code; 0 of 162 failed the
schema; $5.78):

| | Luna medium | DeepSeek Flash (high) | DeepSeek V4-Pro (high) |
|---|---|---|---|
| Helpful | 217 | **218** | 211 |
| Core | **72** | 70 | 68 |
| Not-kept kept | 68 | **50** | 50 |
| Theses: bet / small / duplicate | 52 / 9 / 1 | **52 / 2 / 2** | 44 / 7 / 1 |
| Unfiled: fine / should_open | 37 / 1 | 18 / 5 | 22 / 5 |
| Cost per article, wall time per call | about $0.003, about 50 s | about $0.017, about 1–2 min | about $0.05, slower |

**Medium's added hits.** I read all 16 helpful entries medium catches in at least 2 of 3 draws where K5 low caught them in at most 1
(`round1-medium-pair/added-hits.json`). 14 are faithful: Huang's $60 of $100, the CPU:GPU 1:8 to 1:1 shift, Micron's revenue and
margin, memory at half of 2027 data-centre spend, and 75 blocked projects. 2 are quote-only matches on #54, your example.

**The 9 small theses of K6b medium.** 6 are on article 2 (the Intel $5bn stake and the Xeon 6 selection), 2 on lidar policy (#85),
1 on the Firmus Batam scale. Article 2 is read with a one-thesis library, so the risk sits in the early, near-empty phase of a
forward run.

**Running:** the K6b medium forward run over 115 gold articles (69 of 115 done, 0 failed).

**Plan, to challenge.**
1. Finish the Luna run and score it against the pass line: a blind library read, plus gold.
2. Add a DeepSeek path to the runner and run Flash forward over 115. The runner today accepts gpt-6-luna only. The path:
   - JSON mode, with the schema appended to the system text, as in the probe;
   - the exact sent request recorded;
   - a nonconforming answer fails the item and is never repaired.
3. Compare the two full runs on the pass line and noise; read the libraries blind together.

Questions:
- (a) Is Flash's small-thesis advantage (2 against 9) a real model difference, or an artefact of the JSON-mode request, given that the
  schema text sits in its system message? Is there a cheap check?
- (b) Flash's per-call latency of 1–2 minutes makes a sequential 115-article run take about 3 hours. Is it worth it now, or should
  Flash at low effort be probed first?
- (c) Anything in the Luna run's partial trace (`poc/data/clean-step1-takeover-2026-11-07/gold-k6b-medium/trace.sqlite`, completed
  rows) that already shows a pass-line failure?

Under 600 words.
