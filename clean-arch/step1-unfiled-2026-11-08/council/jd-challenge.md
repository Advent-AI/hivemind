# Council jd: the round after the second result — the event class diagnosed, one fix proved at no cost, the figure's due day counted (same thread; read-only)

By the next step you signed (jc), nothing was sent. This round did items 1 and 2 at no cost. Check it and settle what goes
to the owner.

## What was done

1. **The event class, counted on the second run's 43 event ladders** (`clean-arch/step4-2026-11-10/DESIGN.md` §5.2.1, the
   paragraph "After the second Stage A"): a ruled-out sentence with "after" (31): R held by both readers on 27, failed by both
   on 1, disputed on 3; with no "after" (11): failed by both on 3, held on 2, disputed on 6; no ruled-out rung (1, disputed).
   So the sentence without "after" is behind 3 of the 4 ladders both readers fail and 9 of the 14 failed under the strictest
   counting. Not fixed by it, counted: a question and an answer with different periods (3 ladders, 2 theses); a missing
   ruled-out rung (1); the object of a regulator's decision (4 event ladders failed by both readers).
2. **One change, in code only:** in the ruled-out rung, "was made after <the article's day> and stands on <due day>" is now
   said of the model's own sentence and of every other decision alike (`ladder/ladder_step.py`, `event_rungs`; tests and
   mutants updated: 111 tests, 43 of 43 mutants caught). The request is not touched.
3. **Its proof at no cost** (`clean-arch/step4-2026-11-10/dryrun14/`: `build_scope_reading.py` states the criterion before any
   reader answered; `packet.json`; `reader-codex.jsonl`; `reader-claude.jsonl` when it has arrived): six answers of the second
   run with no "after", each shown with the sentence as it was and as it is, with an earlier decision still standing, a new
   decision, and the event. The Codex reader: the earlier decision is placed in the ruled-out rung for all six under the
   sentence as it was and in the last rung for all six under the sentence as it is; the new decision in the ruled-out rung and
   the event in the first rung under both, six of six each.
4. **The object, a finding from Step 1's own field.** Every thesis carries `opens_as` from Step 1 (product_node,
   binding_obligation, shared_quantity, policy_stage; `clean-arch/PRD.md` §12, section 3). Over both runs: product nodes and
   binding obligations are filed under the company in 101 ladders of 101, none failed on the object by both readers; shared
   quantities under a theme in 78 of 81; and of the 33 policy-stage ladders filed under the company, 10 are failed on the
   object by both readers (China's permission for H200), while the French investigation into the company, also a policy stage
   under the company, is failed by one family and held by the other.
5. **The figure's due day, counted on both runs** at no cost: 64 of 67 and 68 of 71 figures carry a day the model estimated;
   for the company it falls 24 or 28 days after the fiscal year-end in 24 of 27, for a theme 46, 59 to 60 or 91 days after
   the calendar year-end; among the theses whose three sends are figures the day differs in 11 of 19 and 15 of 21, by 1 to 45
   days (the median 4). A replay of a rule on the stored answers (the day set by code as the end of the year the figure covers
   plus 60 days for the company's fiscal year and 90 for a calendar year, when neither the thesis nor the article states a
   day): the three sends agree in 31 of 32 theses in the first run and 32 of 34 in the second, against 21 and 18 now. Its
   cost: two theses whose figure covers twelve months ending in July get a day eight months late, and a quarterly figure that
   should not be a ladder at all gets one.

## What to settle

1. Is the event diagnosis sound and the claim about the fix no wider than its proof? Read `dryrun14/packet.json` and the
   answers; say what the reading does not show.
2. The object: is "a product node or a binding obligation is the company's; a shared quantity is a theme's" something code may
   take from Step 1's field (identity), leaving only a policy stage to the model? Give a stored thesis it would get wrong.
3. The due-day rule changes what the system does and is the owner's to decide. Is the count sound, and is the question to
   him well put: (a) code sets a figure's unstated due day from the year it covers plus a fixed lag (recommended, with the two
   lags and their cost); (b) the model keeps estimating and the line compares months; (c) leave it?
4. **What goes to the owner now, to sign.** The author proposes one message: the event fix proved at no cost; three decisions
   for him (the due-day rule; whether a regulator's process about the company itself is the company's question or a theme's;
   his word for a third Stage A on the same theses once the event fix, the due-day rule if he takes it, and D411's reference
   are each built and proved at no cost and reviewed); and the plain statement that the six lines may be hard to reach. Amend
   or sign. Say whether D411 and the due-day rule may be measured in the same third run as the event fix, given that one run
   would then carry three changes.

## Deliver

Your check, your answers to 2 and 3, and the message's content as you would sign it, with what remains disputed. No praise.
