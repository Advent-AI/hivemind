Council B on the Stage 2 result of D392. Read-only, fresh reader, under 450 words. Repository /Users/lchingen/hivemind.

**Read:**
- `clean-arch/e2e-2026-11-09/stage2-frozen.md` (the rule and the dated addenda);
- `stage2-result.txt` (the frozen decision script's output: every question and draw; the control columns are draws 1, 3 and 4);
- `stage2-reasons.txt` (each run's last judgement before 2026-07-14 for q10, q16, q17 and q22: rung, reference, implied outcome,
  reasons, cited evidence);
- `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§60–62 (the plan, Stage 1's predictions and the Stage 2 log).

**Facts:**
- Frozen scorer, gold v1 `636c056d…`.
- Clean totals 18, 18, 17 (53); control 17, 15, 16 (48). The difference is +5 with all questions and +5 without q09, q12 and q23. No
  collapse. q12 is 0 of 3 in the clean arm, so the frozen rule reads INCONCLUSIVE.
- Stops (all disclosed): one control draw and one clean judging stopped on the frozen judge's refusal (v17 naming v8 as a dependency);
  all three clean Step 1 runs stopped once on a cut network reply and were continued.
- Cost from tokens: clean Step 1 $1.79 per draw, clean judging about $0.50 per draw, control $0.64–0.73 per draw.

**My reading, to be attacked:**
- The +5 decomposes into q10 +3 (clean 3/3, control 0/3), q16 +2 (3/3 against 1/3), q17 +1 (2/3 against 1/3), q22 −1 (2/3 against 3/3)
  and q23 0 (1/3 each).
- **q10 and q16 are delivery gains predicted by Stage 1.**
  - For q10, every clean judgement cites NVIDIA's roughly 66% reported operating margin. No control judgement had it; they carried
    62–65.
  - For q16, every clean judgement cites Broadcom's $10.8bn Q2 and $16bn Q3 AI figures. Control d1 and d3 lack them; control d4 has them
    and agrees.
- **q17 and q22 are judge sampling at boundaries.** q17 sits near the 1% line, and in q22 one clean draw weighted a 32%-growth view.
  Both arms held the same items.

**Answer:**
1. Is the q10 and q16 attribution right, or could it be judge luck? Check the cited evidence against the control runs.
2. Is anything in the result a measurement artefact? Consider the adapter, the 400-character quote cut, the dropped links to
   clean-opened theses, the q23 mapping, the continuations and the replaced draws.
3. What does this result support for Alex, and what not? Remember it is seeded, on tuned articles, with an exploratory threshold.
4. **The one next step you would recommend, with its test.** The PRD and the D392 decision tree are in
   `docs/prd/10-filing-phase.md` and D392.

**Out of scope:** changing the frozen ruler, judge or c8.
