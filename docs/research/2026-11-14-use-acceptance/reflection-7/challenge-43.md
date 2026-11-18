# Council round 43: the diagnostic's result. Decide the next step in a few lines.

**Run:** `poc/data/clean-second-side-probe-2026-11-17/run-1`, 44 of 44 sends, $1.49. Statuses (Q = a question written, D = declined):

| Topic | Frozen d1, d2 | Edited d1, d2 |
|---|---|---|
| target pool-7: DRAM prices plus whether the shortage persists | D, D | Q, Q |
| target pool-17: China accelerator units plus the GPU/non-GPU split | D, D | D, D |
| targets pool-20, -32, -35, -38 | Q in all four | Q in all four |
| the 5 controls | D in all four | D in all four |

- **pool-7 (edited):** asks the DDR4 contract-price change over 2026 and lists "whether the shortage persists" and graphics memory in not_judged.
- **pool-17 (edited):** "names both … total … and the GPU versus non-GPU composition … without identifying either as the main one". It is the same reason as
  frozen, and the same shape as the 44's acc/clean-9 (a total plus its part), which A2's dropped example "a share beside the total it is part of" covered.
- **The pre-registered verdict:** INCONCLUSIVE. 2 targets are exercised, below 3. On the raw outcome, recovery is 1 of 2, which would fail 80%. No
  reader pass has run; it cannot move the verdict.
- **Per D651:** no gate rerun on this evidence.

**My read:**
- The two sentences move astra on "a main figure plus a condition" (the acc/clean-8 shape).
- They do not move it on "a total plus its part" (the acc/clean-9 shape), which is 3 of the 7 line-4 misses on the 44.
- AGENTS §6 says a classification the model must make is a closed set with two or three examples per class, from varied domains, none from a test article.

**Options:**
- **(a)** Add one cross-domain example sentence for the part-of-total class, e.g. "a bank's total loans and the share that is commercial loans; a drug maker's
  total sales and one product's share". Then test on outside topics of that shape: pool-17, plus boundary cases [13] and [14] if the classifiers agree.
- **(b)** Stop editing and report to Alex:
  - astra-frozen is the best measured configuration;
  - the remaining class is this main-part judgement, his six main-part cases are on his page, and his ruling is the ruler for it.
- **(c)** Read this run anyway, at $0, to check pool-7's question and any harm, before (a) or (b).

**Ask:** which, with the smallest test. CONSENSUS or DISAGREE.
