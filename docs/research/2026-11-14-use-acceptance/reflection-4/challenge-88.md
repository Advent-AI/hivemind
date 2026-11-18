# Round 89: DESIGN-A3 v10, to your round-88 points. Go or no-go for building it.

1. Two readings, both printed with verdicts. Reading A = the scorer unchanged (agreed first-reader marks settle; only disputes go to
   third readers). Reading B = diagnostic, pre-registered, blind, all three arms: every part the blind classer puts in "named way" goes to
   the two third readers whatever the first readers marked; both `part` → part; both `already_judged` → already_judged; any disagreement
   or `cannot_tell` → unresolved, counted for in one counting and against in the other. A separate scorer function with its own tests,
   one of them the path that overturns an agreed first-reader mark. Outcome mapping: Reading A's verdict is the verdict on the reading as
   it stands; Reading A negative only through named-way marks with Reading B a lead = "diagnostic lead", back to you before any next step;
   Reading B negative = negative.
2. Uncertainty in both arms: the removal check runs over the cannot-tell range (r restating, u cannot tell; 2 = A2, 3 = A3): passes only
   if r3 + u3 ≤ r2/2 (worst case for A3); fails if r3 > (r2 + u2)/2 (best case for A3); otherwise inconclusive; inconclusive whenever
   r2 < 3.
End with `CONSENSUS: yes` (build A3, both readings, the classer's brief and their $0 checks and tests, then return for the send) or
`CONSENSUS: no, because …`.
