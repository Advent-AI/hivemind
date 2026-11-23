# Council round 61 (Council B on the D745 targeted test's result): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read (file:line).
Your report is a lead, so read the primary files, not only the summaries named here.

## Context
- **The goal.** Alex: "don't hallucinate with the numbers … get this right" (D725 in `docs/DECISIONS-log.md`).
- **The design.** judging-v13s, the small format: related number questions are judged in one call with labelled figures, and code
  checks identity and arithmetic (`docs/research/2026-11-22-number-answers/SMALL-DESIGN.md`, `calc_small.py`).
- **Alex's rulings on reader questions.** D741, D743, D744 and D745 are in `docs/DECISIONS-log.md`. D745 includes "a justified
  unresolved answer counts as usable" ("算合格").
- **The registered test** is `SMALL-DESIGN.md` §5 [D745] (near the end of the file).
- **Result.** Written in `docs/research/2026-11-22-number-answers/BLIND4-RESULT.md`. The run folder is
  `poc/data/judging-v13s-blind4-2026-11-23/`:
  - `reader-key.json`, `TALLY.json`, `CHECKED.json`;
  - the answers: `S/answers`, `E/answers`, `P-v8/answers`, `controls/`;
  - the readings: `reader-packets/U0?.codex.json` and `U0?.claude.json`;
  - the adjudications: `adjudication/U0?.codex.json` and `U0?.claude.json`.
- **The previous re-reads** are `BLIND3-RESULT.md` and the folder `poc/data/judging-v13s-blind3-2026-11-22/` (`REREAD2-TALLY.json`).
- **The paid gate's reading rule** is `docs/research/2026-11-22-number-answers/PAID-GATE.md` §4.
- **The frozen judgement gold** (reasoning only, never to be edited) is
  `docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json`. Its entries q04 and q19 are the ones that bear on S and E.

## Out of scope
- the frozen ruler and gold files, and production configuration;
- any module other than this judge version's test;
- spending, and changing any file.

## Questions
1. **Is the FAIL real?** Read E's Codex reply (`E/answers/codex.json`) beside the E request (`E/user.txt`). Is the settled "not
   supported" right? Read every split (U02, U04, U06, U08), with both readings and both adjudications. For each, which side is right
   against the passages and the format rules the writer was given (`E/system.txt`, `S/system.txt`, `*/schema.json`)? Is any split a
   reader error that the definitions already settle?
2. **What is the mechanism** behind the remaining failures? Is it the writers, the request, the readers' standard, or the case? Count
   it across the third run's twelve replies and this run's six, where the stored votes allow.
3. **Is the readers' standard for a band-deciding judgement a settled rule?** Consider D741, D745, the system text's own sizing
   method, the frozen gold's q04/q19 reasoning, and the paid gate's third reader (Codex). If it is not settled, is it Alex's to settle,
   and what is the smallest balanced question to put to him?
4. **What is the next step:** one recommendation and one test, with what result would move the decision. Options include going to
   Alex for the paid re-send now, putting a ruler question to Alex, a structural change (request or code), or closing S and E as cases
   the format should withhold. Say what each would cost and decide, and reject the ones that re-measure the same split.

Return a numbered report: findings marked serious / minor / wording, with citations, then one recommendation and one test.
