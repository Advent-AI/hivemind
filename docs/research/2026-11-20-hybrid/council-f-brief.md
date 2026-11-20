# Council B on result 1, and the fork probe (read-only, $0)

**Read** `docs/research/2026-11-20-hybrid/DESIGN-J2.md`: the sections "Result 1" and "The fork probe". Then the answers in
`poc/data/hybrid-2026-11-20/probe/{v7,J2a,J2b}/`, `forkcases.json`, and the `forkcases`, `forkprobe` and `forkscore` functions in
`judge_probe.py`.

**Challenge:**
1. **Is the anchor confound real?** Check 3 final requests for the "[Previous conclusion, for comparison only]" block. Check the held
   lengths in `forkcases.json` (`judgements_after`).
2. **Is deferring the 432-card reading right?** Can the reading change rule (a)? Or is it needed for (b) or for the record?
3. **The fork probe:**
   - Is its rule sound, and are its thresholds of 12 and 8 meaningful?
   - Is the fork the right request? Consider one whose previous conclusion was itself wrong, or a fork whose evidence differs from
     the final.
   - What would let a bad conclusion through?
4. **The slice.** The plan's slice from the 09-06 copy carries every earlier wrong rung. Should the end-to-end test of a judge change be
   a judge-only replay of the whole window from 07-01, with old's links fixed? That costs about $2 per draw and arm, from archived
   tokens: 1,007 window calls price at $2.04 for two draws.

**Out of scope:** as before. Under 300 words, then `CONSENSUS: …` or `DISAGREE: …`.
