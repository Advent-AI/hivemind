GATE FAIL

**A — Blocking.** Change detection still reads the model’s declared amount. In two accepted R2 replays with the same rung and sources, the published forecast moved from $52.70B to $53.00B. That exceeds the configured change threshold, but `changed()` reported `unchanged` because it compared against the declared $52.75B. Feed change detection the same recomputed outcome used for publication, and add the two accepted runs as a regression case. [Publication result](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:651) · [Change detection](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:671)

**B — Non-blocking.** No relabelling findings.