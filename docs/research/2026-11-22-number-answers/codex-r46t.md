GATE FAIL

**A — Blocking**

- **The boundary record still loses information.** R4b3 lists $20B, $30B, $40B and $50B under one `definite` label, although only $40B is definitely crossed. Passing the same outcome through a one-input sum makes the record report no crossing at all. Preserve open and closed bounds through recomputation and record certainty separately for each boundary. [Boundary records](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:747)
- **The C3 guard can fire on its own and refuse compatible forecasts.** Data Center `>$127.1B` and company revenue `≥$127.1B` were refused. Removing only the open-low-end clause made the case pass. Two lower bounds can both be true while the part stays below the whole. Check whether the bounds make that relationship impossible, and keep the exact-whole case as the refusal control. [C3 guard](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:189)

**B — Non-blocking.** No relabelling findings.