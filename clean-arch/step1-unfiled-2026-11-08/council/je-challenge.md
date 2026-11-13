# Council je: the reference as D411 decides it, before any send (same thread; read-only)

The next item of the plan you signed: D411's change of the reference, built and checked at no cost on its own. Nothing has
been sent. Review it as a change to a request (AGENTS §6 and §7.3: council before every change is sent).

## The change

Decision D411 (`docs/DECISIONS-log.md`): an amount already reported may be a figure's baseline when the article states no
expectation, named as the last reported amount and never as the market's expectation; a reference stated as a range is carried
as a range.

- The design: `clean-arch/step4-2026-11-10/DESIGN.md` §5.2.2.
- The request: `ladder/candidate-system.txt`, the paragraph beginning "reference is what this figure or event is measured
  against"; `ladder/candidate-closing.txt`, the sentence on the reference; `ladder/candidate-schema.json`, `reference` with
  `words`, `kind` (expected, last_reported), `value`, `value_to`. The request as the second run sent it is in
  `poc/data/clean-ladder-stage-a-2026-11-10/run-2/request-as-sent/`.
- The code: `ladder/ladder_step.py`, check 6 (the value, or the middle of a range, in the middle range; `value_to` null or
  greater than `value`; `last_reported` refused on an event) and the middle rung's text ("the amount last reported when the
  question opened"); tests `test_d411_*` in `ladder/test_ladder_step.py`.
- The readers' form: `ladder/stage-a-reader-brief.md`, the rule on the reference and marks X and XR.
- Shown at no cost: `stage_a/reference_by_hand.py` and `stage_a/result-2/reference-by-hand.txt`.

## Your questions

1. **The request as the model reads it, whole.** After this change: any contradiction between the system text, the closing
   check and the schema's descriptions; any sentence about the reference with no source in D411 or the paragraph it replaces;
   anything said three times; anything that asks for what a check refuses. The paragraph grew by about 400 characters: name
   what could be cut without changing what it asks.
2. **What it lets through, and what it will do to answers.** Give a reference that passes the schema and every check and is
   wrong in a way marks X and XR would not catch. Say what the change is likely to move that it was not aimed at: will "the
   amount most recently reported" pull in any figure the article mentions (a cap such as "guarantees of up to $105 billion" in
   acc/clean-3; last year's figure for another period; a figure for one project standing for a total)? Read the articles of
   u1/clean-7, acc/clean-3 and acc/clean-8 in `stage_a/cases.json`.
3. **Placing a range by its middle.** Right, or should both ends lie in the middle range? Give the stored case where the two
   rules differ, if there is one.
4. **The small send, before any measurement.** Proposed: the changed request once on about sixteen stored theses: the three
   whose reference is the reported $119 billion (u1/clean-7, u2/clean-6, u3/clean-8), the range (acc/clean-8), the cap
   (acc/clean-3), two with a stated expectation as controls (u1/clean-4, u2/clean-4), the two declined for no main thing
   (u1/clean-5, u2/clean-10), three declined in some sends for no theme (u3/clean-4, u3/clean-2, u1/clean-9), and four events
   (u2/clean-3, u1/clean-11, u1/clean-12, u1/clean-3); read by hand against the second run's three sends of the same theses,
   which were sent with the request as it was hours earlier. About three cents. Is the sample right for what the change can
   move, and is the second run an acceptable control for a probe that decides only whether to go on?
5. One line: ready for that small send, or not, and what must be fixed first.

## Deliver

Findings by severity with the file and the words, then your answers to 3 and 4, then the line. No praise.
