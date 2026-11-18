# Review round 8 (read-only, $0; D672's condition): the three §1.6 tools just built, and one question about Step 2's line 3

**Part A.** The tools below were built to `DESIGN-1.6.md` v6, each with fake readers and no model call. Each builder reported where the
design did not fit the code.
- `stage0/d400_reader_lines.py`, with `test_d400_reader_lines.py`. Its builder reported:
  - Stage A's `collect_readings.py` works inside the folder it is given, so readings run on fingerprint-verified copies;
  - there is no item-level ask-again round, so a reader session still void after one retry leaves its draw's reader lines "not measured".
- `stage0/step2_lines.py`, with `test_step2_lines.py`. Its builder reported:
  - the party route is exact text after case folding;
  - the history scan runs in both families;
  - line 3's key, tie-break and rendering prompts are new text, with no frozen source;
  - the line 1 prompt is question 1 of `v2-prompt-1.md`, with one sentence reworded.
- `stage0/d431_reading.py`, with `test_d431_reading.py`. Its builder reported:
  - two third readers, one per family, and a split stays unresolved;
  - the new system's units are its views;
  - units are not compared, because neither frozen rule converts them;
  - on stored draws, the tool reproduced the recorded census of 2026-11-13 except one decisive-reading difference, which is printed beside.

Check, citing file and line:
1. Is each tool faithful to v6?
2. Will each run on the stores the run writes?
3. Is any prompt text wrong against its source?
4. Does anything change a pass or fail beyond what v6 says?

End Part A with `READY` or `NOT READY: <the smallest changes>`.

**Part B, a decision for the council.** Line 3 as v6 defines it is predetermined.
- The frozen `step3/library.group_text` prints a later report's date, publisher, party, summary and quotes. It drops the report's tier,
  stated day, period and reporting speaker (`clean-arch/step3/library.py:135-160`).
- v6's key counts those four fields as details. On stored run c1, 78 of 79 eligible groups have a later report whose fields differ from
  its original's. The line would fail whatever the merging does.
- Meanwhile the product's judge does not read `group_text`. `clean-arch/PRD.md` §6 says: "In the judge's ledger each member of a group is
  its own evidence record, related to the original as the same claim (D204), and the judge reads each copy with that note." Stored judge
  requests carry 741 such notes in c1 and 1,127 in p1.
- The recorded line-3 test (Step 2 log §10 and §12) graded analysts' frozen questions on the dossier content.

Claude's lean: line 3's key counts details of content only, that is "a figure, condition, party, date or qualification" that the later
report's statement adds (v2-prompt question 2). It does not count the record's own attribution fields (tier, stated day, period,
reporting speaker), which the product's judge reads in full on each member record. The fields `group_text` drops are counted and printed
beside.

Is that faithful to D427's line and the recorded test, or should line 3 be read some other way? Give a position and a reason; the
council records the consensus before any output is read.

Under about 500 words in all. Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`, except its six `<draw>/run.json` files.
