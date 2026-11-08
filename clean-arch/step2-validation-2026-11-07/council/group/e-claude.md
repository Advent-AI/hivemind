# Council B, close-out round, Step 2. Challenge the results before I report (read-only)

The run is `poc/data/clean-step2-forward-2026-11-08/`: the real modules over the stored dev Flash Step 1 trace, 282 records to 178
groups.
- Outcomes: 104 repeats, 3 revisions, 175 new; 0 refused.
- 16 records got several same_statement answers; Alex's best-match rule placed them.
- The embedding texts were verified identical to the cached ones (282 of 282 documents, 313 of 313 queries).

**Line 1** (`score_final.py`). Over the 113 records with a known labelled counterpart, a group holding one was among the candidates for
112 (99.1%). For 107 of those, the group's original, which is what Jev compared, is itself a known counterpart. This is recall over
known labelled counterparts only.

**Line 2.**
- All 104 merges were read by two blind readers, previously labelled positives included. 85 were accepted by both.
- The 19 that either reader rejected went to an independent third reader with three verdicts: acceptable 1, overlap 15 (imperfect but
  not misleading to a reader of the record's own text), **wrong 3**.
- The 3 wrong:
  - NVL576 into NVL144, twice. The group's original also states the NVL576 claim; it is a bundled Step 1 record.
  - Analysts' 82% and 41% into the analysts' revenue path: different figures, a Jev error.
- **3/104 = 2.9%, which misses the 2% line by one merge.**
- My own reading had 5 wrong: it put Sharon AI into Firmus, and the bundle into the Sharon group, where the third reader saw overlap.

**Line 3.** The reader test was re-run on views rebuilt from this run, with the frozen questions and key (`FROZEN.sha256` OK), 18 masked
readers and 3 blind graders.
- Detail: none 27.5, source 3, group **28** of 36.
- Unsupported claims: none 3, source 2, group 2. Double counting 0.
- The wrong-group questions F7, R7 and R8 score the same in every view. No falsifier fired.

**My verdict.**
- Lines 1 and 3 are met; line 2 is missed by one merge.
- Mechanism: 2 of the 3 come from a Step 1 record that bundles two claims; 1 is Jev reading different figures as the same statement.
- Per AGENTS (a failed acceptance goes to Alex with its census), I will not start a fix round. Alex said to stop at the close-out.
- I will put the census and two options to him:
  - accept, with the 3 recorded as known defects, since grouping keeps their text;
  - a later fix round aimed at bundled Step 1 records.

Challenge:
1. Is the line 2 count sound: the third-reader design, the "overlap" category, and my reading set aside?
2. Is anything overclaimed on lines 1 and 3?
3. Is stopping and asking right, given Alex's instruction to close out Steps 1 and 2 and stop?

Under 250 words.
