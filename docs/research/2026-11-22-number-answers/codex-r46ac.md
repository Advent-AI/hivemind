GATE FAIL

**A — Blocking.** Run 25 reproduced all 85 passes and 45 mutant catches, including both CH6 results. Two supported cases still fail change detection.

- **Distinct numbers in one quote count as the same source figure.** In an accepted R1 replay, the calculation stopped using the `±2%` guidance width while retaining the `$108B` midpoint. `changed()` returned `unchanged` because both components have the same evidence ID and quoted expression. Include the verified numeric component in the source figure’s identity. [Source comparison](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:688)
- **A valid unavailable result crashes the comparison.** The checker approved a standalone R4 answer as `unresolved`. Comparing it with the previous numeric result raised `KeyError` because the new answer has no `outcome`. Route unavailable answers before numeric comparison and test that transition. [Change detection](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:671)

**B — Non-blocking.** No relabelling findings.