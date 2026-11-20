# Council B on results 2 and 3: the anchor (read-only, $0)

**Read** in `docs/research/2026-11-20-hybrid/DESIGN-J2.md`: "Result 2" (the frozen gold, rule (c) missed by both J2 arms, with the
J2b regression on d3-q18) and "Result 3" (v7 with and without the previous conclusion). The answers are in
`poc/data/hybrid-2026-11-20/probe/{v7,v7-noprev}/` and `hidden-flags.json`; `without_previous()` is in `judge_probe.py`. D198 is in
`docs/DECISIONS-log.md`, "## D198".

**State:**
- J2b without the previous conclusion is landing in `probe/J2b-noprev/`.
- v7 without the previous conclusion is running on the frozen gold.
- The 432-card reading of the final-request deck is in progress.

**Challenge:**
1. **Is the reading of Result 3 sound?** The previous derivation and the hidden pieces are removed together. What does it support, and
   what does it not?
2. **The cheapest test that separates the two:**
   - (a) For targets and controls with at most about 100 hidden pieces: the request rebuilt with every piece in force shown, sent with
     and without the previous conclusion.
   - (b) The previous conclusion kept as its rung only, with no reasons, and the hidden line kept.
   - (c) Something else.
   Which one, with what rule written now?
3. **D198** is Alex's decision: the evidence in view, with "the previous conclusion carries" the rest. Is a change to how the
   previous conclusion is shown within D198, or a change to it that only Alex can make? Name the options for him.
4. **Reading.** Is the right next reading a blind deck of the v7-noprev and J2b-noprev answers that moved, plus the moved controls and
   a matched unmoved sample, mixed with the stored answers?
5. **The J2 line.** Should J2a and J2b stop now? Rule (c) missed, (a) is pending the reading, and the falsifier fired for J2a.

**Out of scope:** as before. Under 350 words, then `CONSENSUS: …` or `DISAGREE: …`.
