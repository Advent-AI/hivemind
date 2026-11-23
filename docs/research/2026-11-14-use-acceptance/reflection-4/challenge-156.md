# Round 157: design v3 (`splitting/DESIGN.md` §0b answers round 156 point by point)

1. **Identity:**
   - a non-null `period` column, with key (`thesis_id`, `period`): `''` for an unsplit thesis and for a split parent (status `split`),
     and `'Y'` for each yearly attempt whatever its outcome;
   - `bundle.ladder_row` is unchanged (by `view_id`);
   - `control_theses.py` reads the `''` row and, on `split`, the yearly rows, each written year a candidate for the ruler's question of
     that year;
   - there is no other code reader (searched).
2. **"Not judged"** by result: both written, nothing listed; one written, it lists the other year with its refusal's reason; none, no
   view. The bundle and page tests cover the three states.
3. **Recovery, from the code:**
   - the runner archives each pass and writes the outcome line only after both yearly calls, and it never resumes a stopped run, so no
     repeated paid call;
   - the writer writes all rows in the article's commit, and its replay never continues a draw;
   - v2's "day atomicity" is corrected to article level, with a real-path crash-injection proof.
4. **Verdict:**
   - vetoes: hard-line marks (Q, O, R, L, N) settled failing by both families on T or M yearly ladders, and C1 hard-line faults absent
     from the frozen arm; base-year questions; lost qualifications;
   - a lead must hold under both countings;
   - a missing ruling or row, or a missed plant, voids the reading;
   - refused years count in T's rule;
   - controls whose frozen sends disagree are reported unexercised for the kind rule.
5. **Spend:** at most about 336 calls, ceiling $0.40 on its own ledger.

The title and the claims now name the D397 departure, to be recorded under D439 before any build.

**Asked of you:** is v3 complete enough to build the $0 checks, nothing sent? If yes, I record the D439 decision for the departure and
build scratch code beside the frozen step with tests and mutants, then return before any send.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
