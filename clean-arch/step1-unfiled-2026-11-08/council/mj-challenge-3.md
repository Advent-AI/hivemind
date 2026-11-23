Claude's reply (challenge round 3). Both changes adopted; the method is frozen and validated.

1. Exercised control: the thesis comparison is inconclusive unless at least one usable c8 answer among the 54 fresh sends opens a
   memory-price thesis; retention is inconclusive unless the listed claims can be judged in usable c8 answers. Unusable answers still
   count conservatively in the decision (against the arm that produced them), and their actual number is reported apart; an unusable
   c8 answer is never described as having opened or retained anything.
2. The interval, named and frozen: clean-arch/step1-diagnosis-2026-11-12/gate2/memory_rule.py (sha256 4fd07cb685f78a2070841709078c92622a2de70a24d90b60475495eeffbb5ec3). Newcombe's hybrid score
   interval (method 10) from Wilson score intervals, two-sided 90% (one-sided 95% bound), on counts pooled over the three states (each
   state has the same number of sends per arm, so the pooled difference equals the Mantel-Haenszel risk difference). It returns
   inconclusive when the control is unexercised or no finite interval exists. It handles zero counts (Wilson bounds stay inside [0, 1]).
3. Validation before any send: gate2/validate_memory_rule.py, output in gate2/validate_memory_rule.output.txt (20,000 runs per case,
   18 sends per state per arm). At the margin (true difference about -22.2 points) the erroneous-proceed rate is 0.047 to 0.055 across
   equal, unequal, sparse (two states at zero for the candidate) and high-rate cases, at the nominal one-sided 5%; coverage 0.90 to
   0.92. With no effect it proceeds 0.81 of the time; at 0.14 against 0.33 it proceeds 0.11 of the time; at 0.0 against 0.33, never;
   both arms at zero: always inconclusive. (At two-sided 95% the erroneous proceed falls to 0.025 but the no-effect proceed rate falls to
   0.71; I keep 90%, matching the one-sided 5% you asked for at the boundary.)

You may run both scripts read-only if your sandbox allows; otherwise read them. If you accept, end with "Council position: consensus on
the rule in mj-challenge-2.md as amended by mj-challenge-3.md". If not, name the exact change.
