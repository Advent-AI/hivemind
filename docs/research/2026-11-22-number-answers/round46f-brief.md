# Council round 46f: gate run 1 failed, the fix, run 2, mutants and the request audit (read-only, same thread)

Read gate-run1.txt, gate-run2.txt, mutants.log, calc_check.py, gate.py, judging-v13-draft.txt and REQUEST-AUDIT.md.

1. Gate run 1 failed on G3: q19's revenue / price-per-unit to units was refused by C8. The fix adds a per-unit identity to C8
   (`_per_unit`) and plant P4 (a price of another product). Run 2: 29 of 29. The fix came after seeing the failure. Is it a
   general identity or fitted to the case? Is a re-run at the same step valid? Did any fixture change other than G3's measure label
   ('units')?
2. Mutants: 6 of 7 single mutants caught. 'C1 accepts any substring' survives because the value, unit and qualifier equality refuses
   the same items; a combined mutant is caught. Is that an acceptable record, or is a gate item missing?
3. Do the reconstructions follow the stored answers' own logic (R1–R4) and the gold's reasoning (G1–G4), without fitting the checks?
   Read the stored answers by call id.
4. Does the request audit find any sentence that keeps wider or narrower than judging-v7 on the standard, or a conflict left?

Output: a verdict line, GATE PASS STANDS or GATE FAIL; findings with the fix you would accept.
