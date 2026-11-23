# Council round 48 (independent read): the judging-v13 paid gate came back with zero accepted answers

You are an independent read-only reviewer. Read the primary material cold; form your own view before reading Claude's notes at the end.

## What happened

The paid gate of judging-v13 (registered in `docs/research/2026-11-22-number-answers/PAID-GATE.md`, decisions D725 and D731 in
`docs/DECISIONS-log.md`) sent 36 scored first attempts and 36 diagnostic retries to gpt-6-luna ($0.37 of a $0.50 ceiling). Every one of the
72 answers was refused by the code checks (`calc_check.py`), so no answer was published. By the registered lines (PASS needs the joint arm
usable in at least 8 of 9 pairs) the result is STOP.

## Primary material (read these, not summaries)

- The run: `poc/data/judging-v13-paid-gate-2026-11-22/answers.jsonl` (scored first attempts; each finished line has `data` = the model's
  parsed answer, `errors` = the check's refusals) and `retries.jsonl` (diagnostic retries, sent with the first attempt's refusal reasons).
  Lines with `status: started` are markers written before each call. Do not open `ledger*` or `archives/`.
- The request exactly as sent: `docs/research/2026-11-22-number-answers/paid-plan.json`, a list of 12 items; each has `system`, `user`,
  `schema` (the strict JSON schema, with field descriptions), `family`, `passages`.
- The checks: `docs/research/2026-11-22-number-answers/calc_check.py` (`check()` returns early after any C7 structural error, so C1–C10
  are hidden behind C7 on most answers).
- The design the checks implement: `docs/research/2026-11-22-number-answers/DESIGN.md`.
- A diagnostic script Claude wrote (copies only, nothing written to the run):
  `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/normalise_diag.py`. It applies
  mechanical corrections for format classes (unit spelling, prose where an id is expected, value-and-range both set, signs on a
  non-sum) and re-runs the check. Read it critically: its guesses may be wrong.
- Working rules: `AGENTS.md` §1 (diagnose before acting), §6 ("Check before the send, at no cost … a request never asks for what a check
  refuses"; "a field's definition sits in the schema beside the field"), §7.3 ("Before a version is rejected, the rejection is checked …
  a rule or check that refuses right answers is fixed").

## Questions

1. **Census.** Verify, by your own count on the two journals, which fields hold prose where the check expects an id, and the refusal
   classes per arm and attempt. Say where Claude's counts below are wrong.
2. **Model error or check error.** Take at least 12 refusals across classes (both journals, both arms and the singletons). For each,
   read the figure, its inputs, the passage it cites and the rule in `calc_check.py`, and put it down as: (a) the model's error (a wrong
   number, a wrong reading, a real undeclared assumption), (b) a rule the request never states (the model's answer is a reasonable
   reading of the request as sent), or (c) the check refusing a right answer (the rule itself is wrong or too narrow). Quote the
   figure and the rule for each.
3. **Process error.** The $0 gate before the paid run passed with a hand-written conforming answer. Why did it not catch this? Name
   the step that would have caught it at no cost.
4. **The way forward.** Given the result, what is the one recommendation and the one test you would put to Alex? Consider at least:
   (i) fix the request (every field's rule in the schema beside the field; enums where a schema can hold the rule) and the wrong
   check rules, then a $0 blind conformance test and a re-run of the same gate; (ii) move work from the model to code (for example,
   code extracts each numeric expression from the shown passages and the model only references them by id); (iii) close judging-v13
   and keep poc-v118 (already the product, D690). For your choice, say what result of the test would stop it.

Out of scope: the frozen ruler (AGENTS §7.1), the production configuration `poc/config/poc-v118.json`, every module other than
judging-v13's request, checks and gate harness. Do not propose edits to frozen files. Write your report as findings with the file and
the evidence you read.

## Claude's notes (read after forming your own view)

- Prose in id fields, first attempts (36 answers): `evidence` 175 figures, `bridge` 49, `answers[].outcome` 45,
  `answers[].reference.figure` 39, `converts` 2, `adjusts.figure` 1. The `bridge` and `reference` descriptions in the schema read as
  inviting prose ("an estimate stating the conversion …"; "An external figure, or a calculation …, or unavailable with why").
  `evidence`, `outcome`, `unit`, `value`/`low`/`high`, `inputs`, `signs` have no description. The check wants `unit` exactly `USD bn`,
  `%`, `x` or `USD`; the model wrote `USD billions`, `$ billion`, `percent`, `fraction`.
- After the mechanical corrections on copies: 9 of 36 first attempts get past the structural layer, 0 would publish. Remaining
  classes include an expression copied with surrounding words ("65% growth in Q4" where the check's extractor yields "65%"),
  `time_aggregation` refused for Q1 + Q2 = "FY2027 first half" and for "first six months" + Q3 + Q4 = FY2027, `apply_growth` of last
  year's Q4 by a stated year-over-year growth refused for want of a bridge, and a product of $411 billion by 92.5% computed by the
  check as 38,017.5.
- Claude's lean: the gate measured the request contract and the check, not the judging; most refusals are (b) or (c). The lean on the
  way forward is (i) with part of (ii) (code extracts the source expressions), tested first at $0 by a blind conformance answer and
  by re-checking all 72 stored answers under the corrected check, then the same 36-request gate. Challenge this.
