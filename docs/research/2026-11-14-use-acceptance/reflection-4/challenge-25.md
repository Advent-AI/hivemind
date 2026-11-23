# Round 26: your three round-25 points are fixed and every check was re-run after the final change. Accept or not.

1. **The count** (`ladder_adapter._write_link`): a link to a closed question is counted only when it is new (checked before and after
   the write); an existing link writes and counts nothing. Label: "links to a closed question written (not judged)".
2. **The decisive replay fails on a breach** (`carried-run/closing_replay.py`): exit 1 unless every judge request is answered from
   the archive and their number equals the stored draw's (37 = 37), no judgement after the last article day, every question due by
   the end day closed on its due day at its last answer and open the day before, the others open, and closings counted equal the
   questions due (6 = 6). Run after the final change: exit 0 (`closing-replay-output.txt`). Against a mutant copy that skips the
   2027-01-31 closing: exit 1 (`closing-replay-mutant-output.txt`; the loop's invariant refused the run on 2027-02-01).
3. **The missing loop-level checks, now tests through `replay`:** a question never judged by its due day closes "no data to
   verify" (its opening day's links dropped by the fixture); a revision of a statement linked to a closed question is linked, not
   judged, and counted (clean-3 due 07-05; e92 revised on 07-06); a closed theme is absent from every later asset request's theme
   block, present the day before, and its closing on a day without articles writes no judgement. Dependencies: the new system writes
   none (open defect 4), so a closed dependency cannot appear in its requests; production's presentation is unchanged and not
   re-tested here.

Evidence after the final change: `test_ladder_adapter.py` 34 passed; `carried-run/mutants-closing.txt` control passes and all ten
mutants fail their tests (adding "every attempt counted" and "links to closed questions dropped"); `stage_b/mutants.output.txt`
21, all as expected; extension proof 19 of 19, all 235 sequences equal their trace numbers; full suite 288; frozen tests 21;
`docs/check.py` passes.

Then: the next step toward production, by D548's gates. End with `CONSENSUS: yes` (accept the integration slice; record) or
`CONSENSUS: no, because …`.
