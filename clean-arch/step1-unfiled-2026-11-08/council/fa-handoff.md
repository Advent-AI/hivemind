Council read of new code before Stage 2 of D392 sends, read-only, fresh reader. Repository /Users/lchingen/hivemind.

**Read:**
- `clean-arch/e2e-2026-11-09/adapter.py` and `test_adapter.py`;
- `stage2-frozen.md`, `calibrate.py` and `calibration.json`;
- `stage2-manifest.json`, `stage2-initial.json`, `stage2-settings.json` and `stage2-limits.json`;
- the plan `clean-arch/step1-unfiled-2026-11-08/council/en-claude.md` (v4 plus qualifications);
- D392 in `docs/DECISIONS-log.md`;
- for the production contract: `src/hivemind/views/judging.py` (evidence_in_view, round_of_judgements, _lines_english),
  `src/hivemind/views/store.py`, `src/hivemind/views/round.py`, `src/hivemind/views/writing.py:240-270` and
  `clean-arch/step3/library.py`.

**Facts:** the adapter tests pass, and a scratch mutant that writes links at a later sequence fails them.

**Check, under 400 words:**
1. Does the adapter feed the frozen judge the way production does: sequence per article, judging once per day with that day's last
   seq, only views with a new link that day, evidence in link-insert order, same_claims and revisions, revision link inheritance,
   later links timed by `later_log`? Name any mapping that biases the score.
2. Are the leakage checks sound? The database holds nothing beyond the day's seq, and each request shows exactly production's selection
   recorded when its prompt was built.
3. Is the frozen decision rule decidable, calibrated as described, and free of the earlier precedence problem?
4. Anything that could spend unboundedly, write outside its folders, or silently differ from the c8 Step 1 configuration?

End with SEND (once the control harness is cleared separately) or the blocker.
