GATE FAIL

Run 14 reproduced all 63 passes and 29 mutant catches. The three invalid rungs were refused without a crash.

**A — Blocking.** C6 treats a strict bound as an exact value. In an R4 replay, a forecast of **less than $40B** passed both checks and was marked for publication on rung 2 ($40B to under $50B). The same forecast was refused on rung 3 ($30B to under $40B), which it overlaps. Preserve open and closed bounds when checking band overlap, and add both cases to the gate. [C6 band check](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:353) · [R4 bands](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/gate.py:175)

**B — Non-blocking.** No relabelling findings.