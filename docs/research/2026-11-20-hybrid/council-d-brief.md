# Council A, round 4 (read-only, $0)

Your round 3 is `council-c-codex.md` (DISAGREE). Fixed, in `judge_probe.py`:

**1. Refusals.**
- `refusals_before()` runs `judging.check_answer` on the store as it stood immediately before the stored judgement. Later judgements are
  shadowed by a temporary `judgements` table on a read-only connection; `store.current_state` reads it unqualified.
- Validation: the 48 stored answers are refused 0/48, as production accepted them. A mutant adding one unshown cite is refused 48/48.
- v7's 144 re-sends: 0 refused (the four false flags are gone).
- The gold probe (`goldscore`): v7's re-sends are refused 3 of 153. Agreement is reported both raw and with a refused answer counted as
  not agreeing: 45/46/44 raw and 45/46/42 strict, of 51.

**2. Coverage.** `expected_files()` refuses scoring or a deck unless every arm × case × repeat answer exists, for the probe and the
gold probe.

**3. The production-path check.**
- The `prodpath replay` copy of old-2 is cut at 09-16 and fed old's own links for 09-17 and 09-18 (every question). The judge's own
  round runs on old's schedule; theme v5's change on 09-18 queues the assets.
- Result: 72 of 72 requests are byte-identical to the archived ones.
- A thread race in the merge test's replay transport is fixed by serialising its database reads.

**4. v7 re-sends.**
- Targets: 21 of 24 reproduce the stored rung in all 3 repeats. Q31 goes 1→2 (3/3), old-2 Q16 goes 1→3 (1/3), old-2 Q9 goes 2→3 (3/3).
- Controls: 0 of 24 change.

Verify the code paths you flagged. If nothing serious remains, answer `CONSENSUS: send J2a and J2b (probe and gold, 3 repeats), score
coverage and refusals, read the complete deck; then the production-path check under v7 and the passing arm`. Otherwise name what
blocks. Under 200 words.
