# Council round 60 (wording and registration of the D745 targeted test, before anything is sent): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read.

## Context
- Alex authorized a targeted $0 test (D745 in `docs/DECISIONS-log.md`, with his answers).
- Alex ruled that an unresolved answer whose reason shows the passages cannot settle the rung counts as usable.
- Council 59 (`docs/research/2026-11-22-number-answers/codex-r59.md`) proposed the test.
- The qualifier fix is done:
  - `calc_small.py` adds "estimated"; `blind_rules.py` shows readers the allowed list;
  - cases 111 of 111, mutants 43 of 43, rehearsal 19 of 19, v13 plan hash unchanged;
  - over the 36 stored replies, the only new change is blind3 S/Claude F11, now refused by S1.

## The proposed request change (system text, `docs/research/2026-11-22-number-answers/judging-v13s.txt`, last bullet)
Current: "… When the evidence cannot support a member's forecast, answer it unresolved and say why."
Proposed: "… When the evidence cannot support a member's forecast, answer it unresolved and say why. This includes the case where one
estimate decides the rung (a share, a deduction or a discount applied to a reference or a total) and the passages support neither its
size nor a bound that settles the rung."

Interaction to check: the same text says "A target for a product with no shipments yet is discounted by default; it is taken in full
only when the evidence shows the volume in hand." E's writers applied an unsized 15% cut under that sentence.

## The proposed reader change (`blind_rules.py`, DEFINITIONS, "supported")
Add: "For an unresolved member, supported means its reason holds: the passages cannot settle the rung (a ruling)."

## The proposed test (to be registered in `SMALL-DESIGN.md` §5 as [D745])
- **Cases and writers.** S, E and P-v8, built as before. Each case is written once by a fresh Claude subagent and once by a fresh
  read-only Codex session, 6 writers.
- **Readers.** Readers get the shared rule text (as in `blind_reread2.py`) plus the new clause. Adjudication runs where they disagree.
- **Controls:**
  - K-unsupported: E's Claude reply with an unsized 140% growth estimate. It must be "not supported".
  - K-unresolved-unjustified: P-v8's Claude reply turned unresolved with a vague reason, where the passages do support a forecast. It
    must be "not supported".
- **Expectations:**
  - On S and E, each reply is either a supported forecast or a justified unresolved answer. The test fails if a forecast picks a band on
    an unsupported share or cut (settled "not supported").
  - On P-v8, a supported forecast. The test fails if it is withheld (unresolved) or not supported.
  - The registered defect stop lines apply as before. Any failed control or registered stop goes back to council.
  - A clean result goes to Alex for the paid re-send.

## Questions
1. Does the proposed sentence state exactly what council 59 meant and what Alex ruled? Is it general (no company, no bench wording)?
   Is it the smallest change? Does it conflict with the "discounted by default" sentence, and if so, what is the smallest fix?
2. Is P-v8 a fair positive case, one where the passages support the narrower figure? Cite the passages.
3. Are the two controls built right? Is anything else needed so the test can actually fail in both directions?
4. Anything that would make this test unable to change the next decision.

Return a numbered report: findings marked serious / minor / wording, with citations, then a verdict: register and run as is, run with
listed changes, or do not run.
