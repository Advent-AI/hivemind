# Council A, close-out round. Challenge the plan before the sends (read-only)

**Alex, 2026-11-08:** "确认 K6b + DeepSeek，把剩下的收尾做完 step 1 and 2, run council loop and we stop here first without going
further". His three answers:
- a record matching several groups joins **only the group it is most like**: Jev's highest same_statement probability, ties going to
  the earliest group;
- Step 2 lines: (1) search finds the stored version for at least 90%; (2) clear wrong merges at most 2%; (3) grouped dossiers keep no
  fewer later details than no merging;
- a DeepSeek format failure is retried once, and if it fails again the item is marked failed and the run continues.

**Step 1 (running).**
- Retry policy built in `clean-arch/step1/runner.py`: 3 new tests and 1 updated, all 3 mutants caught.
- Test-set run `poc/data/clean-step1-takeover-2026-11-07/test-k6b-flash/`, inputs byte-identical to the dev Flash run.
- 4 of the 30 test articles are untagged macro items (OPEC, Fed, Asia week ahead). They were refused by the same selection check the
  dev run passed and were excluded before any send. The amendment is in takeover `LOG.md` §16.
- Line: helpful at least 81.2% of 42, so at least 35; at most 3 small theses, no fragments.

**Step 2 (about to run).**
- `clean-arch/step2/compare.py`: search, Jev, the outcome with best match, and forward order. 6 tests, all 4 mutants caught.
- `run_forward.py` reads the Step 1 dev Flash trace directly (282 records) and reuses the cached embeddings (0 to embed).
- This is a fresh Jev archive, so the forward run is a new draw, about 5 cents.

**Scoring plan:**
1. For each record with a true same-statement earlier counterpart (reference v2 plus agreed v3 labels), take the groups where those
   counterparts sit. Found if any of those groups is among the record's candidates.
2. For every repeat, the pair (chosen group's original, incoming record):
   - labelled same_statement: right;
   - labelled otherwise: a candidate wrong merge;
   - unlabelled: two readers label it with the v2 prompt.

   I then read every candidate wrong merge against exactly what Jev saw and classify it clear or arguable. The line counts clear
   wrong merges out of all merges.
3. A structural check by code: every record is either placed in a group with its own text or listed as refused, and every record the
   reader-test key cites is present. The 25-against-25 reader measure was taken on the fixed-decision reconstruction, and I would not
   re-run the 18-reader test.

**Questions:**
- (a) Is anything in the scoring biased, or circular, given that the reference was built from the same items?
- (b) Is the structural check enough for line 3 under best match, or must the reader test be re-run?
- (c) For Step 1, is the exclusion of the 4 untagged articles sound, and is anything missing from the test-set verdict, such as
  production's test draws for noise?

Under 300 words.
