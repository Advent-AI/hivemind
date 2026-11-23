# Council round 63: Claude's reflection on the D747 re-read, written before Codex's read

## Result
`BLIND4-RESULT.md` §6. FAIL on the stop line: both adjudicators upheld a part-above-whole defect on U02, the S Claude reply. Its prose
calls a figure above its own total spending a floor for the data-center part. Three boundary answers split: T10, T15 and U02's
support vote. Six of nine settle with compatible reasons, and every fixed reading that settled matches what was registered.

## What I take from it
1. **The ruling did its job on the reading.**
   - Three of the four targeted-test splits on the same answers now settle in both families: U04 yes, U06 no, U08 yes.
   - The family alignment is gone. In the remaining splits Codex is strict on S and Claude is strict on E.
   - What remains is single-reader variation on boundary answers. T15 went from accepted by both to split, and the third-run S Codex
     reply went no, yes, no across three readings. I do not think another reader round, or more wording, will close it.
2. **My process error, shared with council 62.**
   - We required five boundary answers to settle without estimating the reader-split rate. AGENTS §7.1: "the criterion's null
     estimated (a conjunction over many items fails by chance)".
   - Using the split rates seen so far, a pass needed luck.
   - The rule I should have applied: a boundary answer's reading is disclosed. A registered line is set only on controls and on
     answers whose reading the record already shows to be stable.
3. **The stop is real, and it is a product finding, not a reading problem.**
   - The format lets a writer state, in prose, a bound that contradicts its own figures.
   - The code checks part within whole only on figures linked in the calculation (D738).
   - Production has no reader, so this answer would publish with a self-contradiction.
   - The request already says "a part cannot exceed its whole", so the writer broke a stated rule.
   - Whether to make the code see such a bound is a design question:
     - if a figure is used to set the rung, it must be in the calculation as a figure linked to the outcome, so S3 checks it;
     - otherwise it may be named only as context.
     That is a new rule, and D738 bounds code to what the structure decides. It goes to the council, not straight in.
4. **The writer-side problems are what bind now.**
   - E: none of the four E replies is cleanly supported. U03, U05 and U06 are settled no; T15 splits.
   - S: one of four S answers carries a self-contradiction (U02).
   - The paid re-send would face both.

## My position (to be challenged)
- **Do not run another reader round.** The reading under D747 is settled enough to judge writers:
  - controls 3 of 3;
  - clear cases agree;
  - the residual boundary splits are disclosed, not chased.
- **The next step is the writer repair that D746 named, with one design question added for the council.** The E repair asks the
  writer to choose between a forecast and "can't tell" before assigning a discount, and to name what makes one side more likely under
  its own assumptions.
  - The design question: should a figure that sets the rung (a floor or a bound) have to be in the calculation, so the code checks it
    against its whole? Or does the request's existing rule suffice, with the U02 case disclosed?
- **One test.** A $0 writer test on S and E with fresh writers, and P-v8 as the supported control. It is scored:
  - by the code;
  - by readers on support, under D747;
  - with registered lines only on things the record shows readers judge stably: settled controls, and defects both families uphold.
- **This is a choice about the next step of work, after a failed registered test.** It goes to Alex as one recommendation and one
  test, with the failure and the process error disclosed.
- **What would change my mind.**
  - If the council shows the remaining splits are a standard gap rather than reader variation (for example a clause of D747 read two
    ways), the next step is a question to Alex instead.
  - If the U02 defect class is common in stored replies (a $0 census over the 18 blind replies' reasons), the code question comes
    first.
