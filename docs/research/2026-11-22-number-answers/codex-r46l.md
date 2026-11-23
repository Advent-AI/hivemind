GATE FAIL

**A — Blocking**

- **G24 can still publish a high endpoint that never uses q01’s high forecast.** The schema and checker accepted the same $560–640B range after I deleted its high calculation. They also accepted a high calculation based on FY2028 consensus with q01’s high forecast listed only in `rests_on`. Require both scenario paths and verify the earlier forecast through the inputs that actually determine each path’s value. The final range can still reflect analyst judgment. [C9](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:436)
- **Change detection misses a wider published range when the midpoint stays fixed.** With the rung and sources unchanged, widening the gold control from $400–435B to $390–445B returned `unchanged`. Compare both endpoints and add that case alongside CH3. [Change detection](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:493)

**B — Non-blocking:** No further relabelling findings.