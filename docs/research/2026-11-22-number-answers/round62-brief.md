# Council round 62 (before any packet of the D747 re-read is built or read): independent review, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite file:line.

## Context
- Alex ruled D747 (`docs/DECISIONS-log.md`, last entry; the question and options are quoted there): "可以发布，要讲清楚".
- Council rounds 61–61b (`docs/research/2026-11-22-number-answers/codex-r61.md`, `codex-r61b.md`) set the next test: a $0 blinded
  re-read of nine stored answers under his words, with expected readings recorded first.
- **What is ready.** Nothing has been built or read yet.
  - The registration: `docs/research/2026-11-22-number-answers/SMALL-DESIGN.md`, the last block, [D747].
  - The changed definition: `docs/research/2026-11-22-number-answers/blind_rules.py`, "supported".
  - The re-read builder and tally: `blind4.py` (`REREAD_BRIEF`, `reread`, `reread_tally`).
  - The adjudication path: `blind_adjudicate.py` (`--reread-d747` and the `case_dir` override).
- **The answers re-read:**
  - `poc/data/judging-v13s-blind4-2026-11-23/` (`reader-key.json` maps U01–U09);
  - the third run's T10 and T15 (`poc/data/judging-v13s-blind3-2026-11-22/reread2-key.json`; answers in `S/answers/claude.json` and
    `E/answers/claude.json` there).

## Questions
1. **Does the definition text carry Alex's ruling exactly**, no wider and no narrower? Compare it with his question and the option
   he chose. Does it conflict with D741 ruling 3 or with D745's unresolved ruling? Is the unresolved clause still right after D747,
   given that Alex allowed a forecast but did not require one?
2. **Are the expected readings right** under the ruling? The four fixed ones are U01 no, U03 no, U05 no and T15 yes. Read each answer
   beside its own request. Should any of the five "must settle" answers instead have a fixed expectation, or be dropped, for example
   U04 as a contested control?
3. **Does the code do what the registration says?** Look at the brief's step 2, the packets carrying each writer's own request
   (`case_dir`, system text and format material), the shuffle and key, the tally's pass, fail and inconclusive rules, the T10 defect
   exclusion, the control exclusion from stops, and the adjudication packets for blind3 items.
4. **Can the result change the next decision?** Name anything that makes it unable to.

Return a numbered report: findings marked serious / minor / wording, with citations, then a verdict: build and run as is, run with
listed changes, or do not run.
