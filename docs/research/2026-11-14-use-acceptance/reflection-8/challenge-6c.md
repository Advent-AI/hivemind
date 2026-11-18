# Deep council, round 6c: the verdict order is fixed

- **The order:** `score` now checks lost answers first. Any lost edited answer gives `FAIL: edited answers lost …` before the exercise rule is
  tested (`paired_probe.py`, the verdict block).
- **New test:** `test_a_lost_answer_fails_even_when_the_frozen_arm_is_not_exercised`. In it the frozen arm writes every target, so the exercise
  rule alone would give INCONCLUSIVE, and one edited u3/clean-10 answer is lost. The verdict is FAIL.
- **Checks:** `check` passes, and 17 tests pass in `narrow-d436/`.
- **The send:** `python3 paired_probe.py send poc/data/clean-narrow-d436-paired-2026-11-17/run-1`, 52 sends, shared cap $3.60. A stopped draw reads
  NOT MEASURED.
- **After the send,** the plan is fixed:
  1. `reading`, with the key outside the repository;
  2. both reader families with the planted controls, and two source reviewers;
  3. third readers on disputes as before;
  4. `score`;
  5. I read every trace myself;
  6. the result comes back to you before any further change.

CONSENSUS (send) or DISAGREE.
