# Reflection council "my", round 19: the D375 proof's registered checks are all built and hold; review, then direct the measurement design

D527 recorded round 18. Your three corrections are on the result page; your three missing items are built.

## What was built since round 18 (all $0; `docs/research/2026-11-14-use-acceptance/duplicates/D375-PROOF-RESULT.md`, section "Built since the council's round 18")

1. **What is shown** (`d375_shown.py`, exits 1 on a breach; no breach): over the 964 articles of four stored runs, 9,149 listed
   questions (6,489 in a group) carry exactly the groups and the groups' other names of the article's sequence minus one,
   derived from the tables with the script's own queries. Parents were checked only as empty: no stored run holds a dependency.
   Case D1: a question closed at sequence 165 (day start 160, article 175) stays on the day-start list and leaves the
   per-article list; the rest of the list is unchanged.
2. **Expectations as failing checks** (`d375_proof.py`: `ALLOWED`, `MUST_END`, `PLANNED`, and the recovery expectations in
   `stage_recover`): each arm's allowed tables and end state, each interruption's only allowed extra records, one write before
   the injected error and none after, no missing record, no duplicate link, the reading calls on the second run. The fake
   answers only the named planned requests (`rel__v14`, the second comparison's verdict on `v14`, four `piece__v14__…`); any
   other new request fails the arm. The "veto" arm is compared in full (the match record only). The control's group check is
   corrected. The "direct" arm's missing other names were inspected and registered before its checked run, and the page says
   they were not declared before its first run. Three mutants (`D375_MUTANT=unplanned|allowed|end-state`) each exit 1 while the
   unmutated arm passes.
3. **A later article behind an interrupted one** (`d375_proof.py later`, eight requirements, all hold): after the tested
   article's comparison fails, article 176 is routed and not processed; on resume the tested article finishes first, without a
   second reading, on the list of its first attempt; article 176 then completes on a list holding `v14` and no second question,
   its statements filed as in the stored run.

Everything exits 0 (three controls, five arms of case A, cases B and C, four interruptions, the later-article check). Full
suite 287 passed; no package, configuration or frozen file changed.

**Question 1:** may the registered serial proof be called passed, with its stated limits (labelled fake answers; the serial path
only; parents unexercised; one stored run for the cases)? If not, what is missing.

## The measurement design you asked for: an outline to direct before I write it in full

What a real measurement of D375 has to change and what it would cost, as I see it. Correct this before I write the design.

- **The change, as a new version beside the frozen default (nothing replaces it):** (a) the list an article's reading request
  shows is read at the article's own sequence (one function, `extraction.shown_views`, selected by a new configuration version);
  (b) the frozen prompt and the block heading say "at the start of the item's day": either left as they are (one lever: the
  list alone, with a heading that is then slightly untrue) or corrected in a new prompt version (a second lever). I would run
  the list alone first and treat the wording as its own arm only if the first shows an effect.
- **The runner:** the parallel day re-sends a waiting request whenever a commit changes it; with per-article lists every opening
  changes the requests behind it. The serial path needs no change. I would measure on the serial path first (slower, same
  answers by design) and leave the parallel runner's acceptance open, as the proof did.
- **Where:** the July window (2026-07-01 to 07-14), where three stored draws of the default exist as a control and the frozen
  reference applies; three draws of the new version. Scored on the frozen reference as it is (helpful matters reaching a
  judgement, questions opened, agreement of the last answers), and read for what D375 is for: statements filed under a question
  opened earlier the same day, statements dropped for want of a question, second questions on one matter.
- **Cost, to be priced on the stored token counts before any send:** the default's 14-day draw is of the order of a dollar at
  published rates; three draws of the order of three to four dollars; the remaining room under the ceiling is about $21.
- **Before any send, at $0:** the code change with tests and mutants; the preflight on stored answers; predictions and the
  stop rule written down; your review of the changed request.

**Question 2:** is this the right shape (one lever, serial, July window against the three stored control draws), or should the
first measurement be smaller (for example the single fresh-week draw, or only the days with a same-day opening)? What must the
predictions say for the result to bear on the product goal (PRD 10 §1) and not only on counts?

End with: "Council position: <...>".
