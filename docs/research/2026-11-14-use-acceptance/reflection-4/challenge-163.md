# Round 163: your round-162 findings, fixed (`splitting/PROBE-PREP.md`)

1. **The 44.** Your finding held, and was wider than the two C2 topics: a census shows 7 of the 13 topics were among the 44 (M, four
   C1, both C2).
   - The probe now draws only from outside the 44, and `stage-b` is gone from its sources.
   - The check refuses any topic whose description is one of the 44's (tested; its mutant is caught).
   - **C1** is re-derived by the same rule over topics outside the 44, allowing event ladders too: fortnight c1/clean-11, c1/clean-9 and
     c1/clean-13, and July c3/clean-5, c2/clean-5 and c1/clean-7. Three of them have both years open.
   - **C2** comes from the two topics outside the 44 that both blind readers of the D436 reading called one bet with a second side:
     July c3/clean-7 (commodity DRAM) and c2/clean-10 (custom-ASIC against GPU purchases).
   - **M** is dropped. Its only stored instance is one of the 44, and the limit is stated.
   - **Both plants** now come from stored ladders outside the 44: fortnight c1/clean-9 rewritten to 2026, and July c3/clean-7 with
     "commodity" dropped.
   - The population is 12 topics.
2. **Retries.**
   - At most 72 and 216 calls, so 216 and 648 attempts with the transport's three tries.
   - The worst-case sum is $2.94 and $8.94 if every attempt were at its worst, with resends estimated as the request plus an answer at
     the output cap.
   - Each attempt is reserved at its own worst cost before it is sent, so the caps ($0.15 and $0.25) stop an arm first, and a stopped
     arm is NOT MEASURED.
   - Expected about $0.10.
3. **Exact population.**
   - `counts` refuses an arm whose sends are not every topic and pass exactly once, including a duplicate row.
   - The reading must hold exactly the items its sends give (derived again by `reading_rows`), each once, and the key exactly those, or
     it is void.
   - Tested: a send filed twice; an extra item; a missing item.
4. **Stated:**
   - yearly items reveal their arm. Arm names are hidden, and C1 items of both arms are read alike.
   - A failed count is negative whatever the reading, because the counts do not depend on readers. The plant check still runs when the
     reading is scored.

**Checks:**
- the probe check passes on the 12 topics;
- 18 probe tests and 52 build tests;
- the suite (346), the new system's folders (261) and the frozen checks pass;
- mutants 36 of 36. Three were caught only after a test was added: a T topic passing with one success, unshuffled third-reader marks,
  and a topic of the 44 not refused.

**Asked:** send the probe now (both arms, three sends each, same day, under the $0.40 caps, about $10 left of D439's ceiling), or name
what must change first.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
