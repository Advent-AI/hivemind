GATE FAIL

**A — Blocking**

- **C9 counts an operand that the arithmetic ignores.** A G24c variant calculated the high path from FY2028 consensus and put q01’s forecast in the third input slot. `apply_growth` uses only the first two inputs, yet both the schema and checker accepted it. Enforce each operation’s operand count and check dependencies through the operands the operation actually uses. [Arithmetic](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:136) · [Dependency check](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:545)
- **C9 still allows a citation to stand in for a calculation when there is only one base scenario.** I removed G4’s FY2028 calculation and left q01’s forecast as a citation on the standalone range estimate. Both checks still passed. Require a verified calculation path for the single-scenario case too, while letting the final range reflect analyst judgment. [C9](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:436)

**B — Non-blocking:** No further relabelling findings.