GATE FAIL

Run 13 reproduced all 60 passes and 28 mutant catches. C9 alone refused G4x, and G4 and G24 still passed.

**A — Blocking.** The checker can publish a forecast on a nonexistent rung. In R1c, changing v9’s rung from `3` to `-2` passed both checks and returned `publish` because Python indexed back into rung 3’s band. Rung `6` and a missing rung crashed the checker. Require a forecast’s rung to be an integer from `1` through the number of bands before looking up its band. [Rung check](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:354)

**B — Non-blocking.** No relabelling findings.