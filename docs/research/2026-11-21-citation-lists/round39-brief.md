# Council round 39: review of the built citation-only judge and its $0 results (read-only)

The design you passed (round 38d, `DESIGN.md` v3) is built and its registered $0 checks ran. Review the build against the design and
the results against what they claim. Scope: `git diff` of `src/hivemind/views/judging.py`, `src/hivemind/model.py`,
`scripts/preflight.py`, `tests/test_live_lock.py`, `tests/test_frozen_questions_and_judgement.py`; the new files
`src/hivemind/prompts/judging-v12.txt`, `poc/config/poc-v121.json`, `tests/test_citation_lists.py`, and in
`docs/research/2026-11-21-citation-lists/`: `mutants.py` (+ `mutants.log`), `t1_replay.py` (+ `t1-replay.log`), `t2_offline.py` (+
`t2-result.json`), `preflight-old2.log`, `RESULT.md` (with its disclosed deviations). T1's outputs are in
`poc/data/citation-t1-2026-11-21-run2/` (`t1-result.json`, `transport-log.json`); read its stores read-only. The frozen ruler, the
prompt text and the link direction are out of scope. No paid call.

Questions:
1. Does the code do what DESIGN v3 says, with no change to the v7/v8 path (requests, format, check, the build_prompt hook)? Find a
   concrete defect or a case the tests miss.
2. Do the results support RESULT.md's claims exactly? Is anything overstated? Are the disclosed deviations (the comparison crash, three
   differences named after they were seen) handled honestly and acceptably, or does any of them undermine T1?
3. Is anything missing before this goes to Alex as "built and passed at $0; the paid acceptance step is yours"? Answer ACCEPT or the
   blocking items.
