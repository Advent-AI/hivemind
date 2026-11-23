GATE FAIL

**A — Blocking.** The registered cases pass, but two R2 replays show that recomputation still loses bounds.

- **Removing the disputed addition turns a lower bound into a point.** With a retained input of `>$6.5B`, removing the disputed $18B changes the total from `>$53B` to `>$35B`. The checker records exactly $35B and calls the $50B crossing definite. The alternate could still exceed $50B. [Overlap recomputation](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:773)
- **Subtracting a bounded outflow keeps the wrong bound direction.** Subtracting `>$6.5B` from $46.5B gives `<$40B`. The checker refused that result and accepted `>$40B` on the $50–75B rung because bound propagation ignores the minus sign. [Bound propagation](/Users/lchingen/hivemind/docs/research/2026-11-22-number-answers/calc_check.py:150)

Use the same bound-aware arithmetic for the original calculation and its alternate, including each retained operand’s sign. Add both R2 cases to the gate.

**B — Non-blocking.** No relabelling findings.