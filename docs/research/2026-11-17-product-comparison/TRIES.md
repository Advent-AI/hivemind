# Tries toward the comparison's criteria (D674)

**The criteria:**
- D665's verdict on the frozen instruments: `stage0/verdict-rule.json` and `stage0/census/matters.json`. A **practical lead** means
  a − b ≥ max(3, ⌈0.15·N⌉) and a ≥ 2b under both countings, with every guardrail exercised and passing.
- The hard checks:
  - D400's code-decided parts;
  - Step 2's three lines.

**Rules for every try:**
- The ruler and the instruments never move to make a try pass.
- A try that does not pass goes through the council loop on its traces before the next one.
- Each row records the try, its result, and what it taught.

| # | Date | Try | Result | What it taught |
|---|---|---|---|---|
| 0a | 2026-11-17 | Slice 1 (07-01..07-07) | Old system complete. The new system stopped at the ladder: a $10 guard against about $10.7 of concurrent astra reservations | Size every guard for the concurrent worst-case reservations, not the expected spend |
| 0b | 2026-11-17 | Slice 2 (07-01..07-03, new guard $25) | All six slice checks pass after two of the checks were corrected (copies merged by the old system; day-end judgements carry their day) | Read a failing check to its first differing line: both failures were the check's error, not the system's |
| 1 | 2026-11-17 22:36 | Full comparison, try 1: three draws of each system, 07-01..09-20, frozen instruments | running | — |
