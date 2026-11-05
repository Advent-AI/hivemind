# Acceptance of the coverage-start reading: what runs and how it is judged (written and pinned before launch)

2026-11-05. Alex: "跑验收". PRD 10 §6: the candidate runs the 14-day window three times end to end, scored on the frozen judgement ruler, against a control re-run the same
day. What is accepted is `poc/config/poc-v116.json` (= `poc-v108` plus the coverage-start reading, D364, D365), built and verified at $0 (`production-design.md`,
`baseline-design.md` round 27). Per AGENTS §7.3 ("Before a version is rejected, the rejection is checked"), only the product's goal decides; every failed case is read to
its raw judgement before anything is called a failure.

## What runs (six draws, launched together today)

| Arm | Config | Draws | Folder |
|---|---|---|---|
| candidate | `poc/config/poc-v116.json` | 3 | `docs/research/2026-11-01-e2e-loop/arms/r10-baseline-v116/d1..d3` |
| control (same day) | `poc/config/poc-v108.json` | 3 | `docs/research/2026-11-01-e2e-loop/arms/r10-control-v108/d1..d3` |

All six: `harness/run_arm.sh`, window 2026-07-01..07-14, NVDA, items `poc/data/items-nvda-2026-07-01-10-27.sqlite` (it holds the page text the reading needs), seed
`poc/seeds/nvda-2026-07-01-v2.json`, cap $3 a draw, 8 extraction workers a draw (six draws at once; the default 16 doubled the peak of the three-draw runs that saw no
rate limit). Each draw writes its manifest (code commit, the changed files listed as dirty, config and prompt hashes, seed and items hashes). No edit to `src/hivemind`
while any draw runs (`parallel_day.runtime_key`). Expected cost about $0.8 a draw (the frozen draws: $0.78-0.79 at published rates) plus about $0.03 for each
candidate's reading: about $5; about ninety minutes.

## How it is judged (the product's goal; `score_judgement.py` on each draw, window end 2026-07-14)

1. **The gap closes:** v10 (operating margin) and v12 (capex) each agree with the gold in at least 2 of the 3 candidate draws (in the control they are never judged).
2. **Nothing that was right turns wrong:** for each scored question, the candidate's agreements over its three draws are at least the control's minus one. A question
   that drops by two or more is read: its last judgement in each draw beside the control's, and whether the wrong answer rests on a starting figure (cites one and derives
   its rung from it). It counts against the candidate only when the reasons show the starting figures caused it (read by Claude and by a reader who did not build it);
   otherwise it is reported as the question's own swing with the reasons.
3. **Total:** the candidate's agreements over all scored questions and draws, against the control's, reported; a lower total is explained question by question.
Both 1 and 2 hold: recommend to Alex that `poc-v116` becomes the default. Either fails: stop and report the mechanism; nothing changes in the product.

## Read as well (not conditions)

- The coverage-start step's record in each candidate draw: questions linked, figures kept and refused (the census rules: a wrong figure is a defect, reported).
- The first-day judgements of the questions that received starting figures (v1, v2, v3, v10, v11, v12, v22): do they use the figures sensibly.
- Differences between the arms in evidence written and links per question (the reading changes what Jev shows as each question's first pieces, `thesis_text`).
- Cost per draw from tokens at the published rates; failures and resumptions.

## Files changed since the last commit (the manifests list them as dirty; their hashes pinned in `acceptance.sha256`)

`src/hivemind/baseline.py`, `src/hivemind/config.py`, `src/hivemind/service.py`, `src/hivemind/views/round.py`, `src/hivemind/prompts/baseline-v3.json`,
`scripts/replay.py`, `poc/config/poc-v116.json`.

## Result (2026-11-05; six draws, about $4.79 at the published rates: candidate $0.86, $0.83, $0.80; control $0.77, $0.74, $0.79)

Files: `acceptance-measure.txt`, `acceptance-traces.txt`, `acceptance-adjudication.json`; the run folders `docs/research/2026-11-01-e2e-loop/arms/r10-baseline-v116/d1..d3`
and `r10-control-v108/d1..d3` (manifests inside). All six finished the 14 days without a failure. They were launched at 10:49; the laptop slept on battery from about
10:52 to 15:41 (power log: "Entering Sleep state … Using Batt (Charge:27%)", woken by the USB-C plug), suspending all six; they resumed on their own and finished at 16:34
(`caffeinate` kept the machine awake from 15:43). The control and the candidate ran in the same hours, as PRD 10 §4 asks.

1. **The gap closes: pass.** v10 3 of 3, v12 3 of 3 (control: never judged). Their last judgements use the figures: 53,783 ÷ 81,615 = 65.9% (rung 2); Q1 $1.757 billion,
   the year $5-8 billion (rung 4).
2. **Nothing that was right turns wrong: pass.** One question dropped by two: v17 (China share) 0 of 3 against 2 of 3. Read by Claude and by a reader who did not build it,
   both "not the records" (`acceptance-adjudication.json`): no starting record reached v17; the candidate draws started from Huang's "share has fallen to zero" sentence,
   which the extraction kept in candidate d1 and d3 and dropped in control d1 and d2 from the byte-identical request 3a028dae; control d2 reached rung 5 on its own; the
   question also swung in the frozen draws (1 of 3). Every other question held or rose (v2, v5, v20 +1 each; v16 +1).
3. **Total:** candidate 53, control 45 agreements over 19 questions × 3 draws (+8: v10 +3, v12 +3, v2 +1, v5 +1, v16 +1, v20 +1, v17 −2).

Read as well: each candidate's coverage-start step linked v1, v2, v3, v10, v11, v12, v22 (11-12 records; d3 refused two text items of the yes/no question v7, as the check
should). On the first day, with only the starting figures, total revenue, data-center revenue and next year's revenue were judged low (rungs 3-4, a quarter carried to the
year); all three agree in 3 of 3 draws at the window end, after the window's estimates arrived. Evidence written and links per question vary between the arms as between
draws.

**Both conditions hold: recommend to Alex that `poc-v116` becomes the default.**
