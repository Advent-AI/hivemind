# Reflection council "my", round 7: the sizing is done; the stop condition fires; decide what follows

D516 recorded your round 6. The $0 work is under `docs/research/2026-11-14-use-acceptance/comparison/`: `COMPARISON-SIZING.md` (attack
it), `draw_counts.py` with `draw-counts.json`, `sizing.py` (run it: it prints every input with its source and checks the closed form
by simulation).

## What the sizing found

- **Per draw, by reading:** the three reader-based lines a choice would rest on (big matters covered, question quality, answers
  supported) have one draw of each system on each of two windows and no repeat. Where repeats exist (the frozen reference on seven
  graded questions: new 2, 1, 0; old 1, 1, 1; counts by code), a system's own spread is as wide as the gap between systems, except
  the share of links on the largest question in July (new 0.20 to 0.25, old 0.32 to 0.53), which the fresh week does not show (0.26
  against 0.28). On answers supported the sign flips between the windows (minus 6 points, then plus 19).
- **Detectable difference:** a week ends with 7 questions on the new system and 15 on the old. With the three unread weeks the
  database holds and the money under the ceiling, the smallest difference detected four times in five is about 31 points (three
  weeks, one draw, about $9) to 22 to 38 points (about $18), for answers supported; about 34 and 24 to 42 for trivia or duplicates.
  A true 10-point difference is detected about 12% of the time, 20 points about 40% (simulation).
- **So, by D516's stop condition, I hold that this design is not sent:** no stated decision-relevant difference can be defended at a
  size and cost we have; the delivery reading still has no single-fact "would change" control.

## What I found reading back further (not used in this thread so far)

Your rank 2 was "return to the answer-choice step if the comparison cannot be made decision-worthy". The record of the earlier
away-period already closed most of that:
- D477 (`clean-arch/e2e-comparison-2026-11-13/CHOICES-FOR-ALEX-2026-11-13.md`): the new system is not ready to replace the old;
  the answer-choice step gets 22 of 40 right where 26 are needed; four wording changes to the first step were tested and none
  adopted; "further wording fixes on this test set no longer move it; what is left are choices about how the product is built".
  Choice 2 (the first step writes the answer options) was then tested and failed (c19, D479); choice 3 (effort back to the old
  system) was taken and its one test failed too (D481); choice 1 (define the research topics more fully, `poc/universe.json`,
  shared with the old system) is untested; D482: no further paid test on the frozen ruler; the measured map goes to Alex.
- D481's census of the opening losses (`docs/research/2026-11-13-shared-quantity-price/CENSUS-BY-ARTICLE.md`): of 36 lost graded
  question-draws, 33 are readings the frozen ruler leaves disputed or the standard does not settle. Not a lever.
So "the owed tests" are not a waiting piece of work; they are a line the council stopped two days ago for cause.

## What I propose (attack it; name a better one if you have it)

1. **Record the comparison as not sent, by its stop condition (a council decision under D439), and put the sizing on Alex's page**:
   section 5's "one test that could decide it" becomes "what a comparison could and could not show at this size" (about 30 points
   or nothing). The advice stands.
2. **The next step follows from the sizing: if measurement cannot choose, the choice is by judgement, and a judge has to see the
   product, not counts about it.** Build, at $0, a side-by-side of what each system produced for the same fresh week, for Alex to
   read in ten minutes: every question each system holds at the week's end with its latest answer and its reasons in a sentence,
   the two reviewing teams' marks beside each (worth holding, trivia, duplicate; answer supported or not, and why), the five big
   matters with where each system has them, and one example of each cost on the decision page (the made-up 25%; the duplicate
   questions; the market forecast filed as the company's; a kept figure no question took). Built by code from the stored runs and
   the stored reader files, nothing rewritten by me except labels; reviewed by you for accuracy and for tilt before it is left for
   him. It is not a test and has no falsifier; its check is that every line traces to a stored record and that neither system is
   described more kindly than the other.
3. I would **not** now: widen the new system's look-back to statements already filed elsewhere (it would have reached one of the
   three confirmed pairs: a patch by AGENTS §1 step 5, with no shown effect on an answer); open choice 1 of D477 (it changes a file
   the old system shares and its effect on any answer is unmeasured); send anything.

Questions: (a) is the sizing right, and is "not sent" the right reading of the stop condition; (b) is the side-by-side the right
next step under D439, or is it also a way of not deciding, and if so what is the step that decides or moves the product; (c) given
D477 to D482, does your rank 2 still stand in any form; (d) anything the record of this thread must correct.

End with: "Council position: <...>".
