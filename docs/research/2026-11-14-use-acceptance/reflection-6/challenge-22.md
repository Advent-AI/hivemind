# Challenge 22: the due-day probe revised as round 21 asked (`reflection-6/due-day/DESIGN.md`)

Read `due-day/DESIGN.md`, `dueday_probe.py` (`tally`, `reading`, `material`, `final`), `test_dueday_probe.py`, `mutants.txt` and
`review-brief.md`.

**Your four points:**
1. **Stored dates:** the verdict reads the view's due_day, which code sets for a year's figure (D414). Amount controls must store
   2027-04-01 with basis expected_publication in both arms. Mutant D1 (reading the raw day) is caught.
2. **Question meaning is part of the verdict:** two blind reviewers read all 36 answers, both arms mixed, under a source-backed brief
   that covers declines.
   - "Moves" needs all of these:
     - no topic with more material v2 defects than frozen ones;
     - no material defect on v2's completion questions;
     - no new v2 decline flagged unjustified.
   - A verdict that differs between agreed and either counting is inconclusive.
3. **Refusals matched by topic:** new declines are counted per topic, never in total.
4. **The reading form is unchanged.** The review is a separate diagnostic.

**Mutants:** seven, each caught by a failing assertion. Two first survived because another rule masked them. Each now has a test that
isolates it, and D7 (dropping the per-topic comparison) is caught after its own test was added.

**Cost:** about $1.5, capped at $3.20. About $5.3 remains of D439.

**Asked:** send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
