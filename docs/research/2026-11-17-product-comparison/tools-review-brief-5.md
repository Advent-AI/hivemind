# Review round 5 (read-only, $0; D672's condition)

**Part A, Codex only.** Your round-4 Part A named three points. D675's "Round 4" entry says how each was fixed, in:
- `stage0/score_comparison.py` (`verify_inputs`);
- `stage0/eligibility.py` (`last_attempt`);
- `stage0/build_cards.py` (the theme context).

Confirm or refute each one, citing file and line. End Part A with `READY TO READ` or `NOT READY: <the smallest changes>`.

**Part B.** `DESIGN-1.6.md` is now v2, answering round 4's Part B (Codex's `tools-review-codex-4.md` and the Claude reader's points
summarised in D675).

Check it against:
- `RUN-PLAN-v12.md` §1.6;
- `stage0/verdict-rule.json`;
- the code it names: `clean-arch/step2-validation-2026-11-07/`, `clean-arch/step3/library.py`, `clean-arch/step4-2026-11-10/stage_a/`,
  `clean-arch/unseeded-2026-11-10/MATCHING-v2.md`, `docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py`,
  `src/hivemind/service.py`.

Questions:
1. Is each item faithful?
2. Is each item buildable on the stores the run writes?
3. Is the reading "a hard check not measured cannot clear release", extended to D400's code parts, right?

End Part B with `BUILD AS WRITTEN` or `CHANGE: <the smallest changes>`. Keep it under about 500 words.

Do not open:
- anything under `/private/tmp`, `~/.codex/memories`, `~/.hivemind-keys` or `stage0/downloaded_files`;
- anything under `poc/data/comparison-2026-11-17/run`, except the six `<draw>/run.json` files.
