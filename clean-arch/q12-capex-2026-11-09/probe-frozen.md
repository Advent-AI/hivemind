# c12 probe: cases, arms and lines, frozen before any send (2026-11-09)

**Setup:**
- Cases: `cases-probe.json`, 14 cases. A is the Zacks article at clean d1's seeded state. B is the same article at dev d1's state 57,
  the library of Alex's ruling. C is the 13 other Stage 1 articles at clean d1's seeded states.
- Arms: c8, the stored sent request unchanged, byte-checked; and c12 (`arms/c12-*`). Three draws each, 84 calls, about $0.88 estimated.
- Tool: `q12_probe.py`.

**Lines. Any failing one stops the line and goes to Alex:**
1. **A:** c12 writes i131 (the Q1 operating and free cash-flow sentence) and links it to v12 in at least 2 of 3 draws.
2. **B (Alex's ruling, "丢掉"):**
   - c12 links neither the cash-flow sentence nor the cash-balance sentence ($80.6bn) to any thesis, in 3 of 3.
   - c12 keeps either of them, unlinked, in no more draws than c8 does. c8's stored dev answer already kept the cash-flow sentence
     unlinked, a defect of its own that is reported.
3. **C:** c12 loses no gold item that c8 writes. A loss is an item c8 writes in at least 2 of 3 that c12 writes in at most 1 of 3.
4. **Added links:**
   - Every link c12 makes that c8 never makes on that case is put, as a (statement, thesis) pair, with every c8 link of the same cases
     as controls, under shuffled labels, before a blind reader.
   - The reader answers "informs" or "does not inform" against the source and c8's linking rule.
   - The share of c12-only pairs judged "does not inform" must not exceed the share of c8 pairs judged so.

**Also reported, not lines:** the number of kept items per arm; prompt tokens per arm from the answers' usage; cost from tokens.

**Labels:** the cases are the motivating article and the Stage 1 articles, on which c8 was tuned. A probe locates; it does not accept a
version.
