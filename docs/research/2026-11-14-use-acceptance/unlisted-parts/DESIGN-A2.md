# Arm A2: arm A plus D436's rule for a second side of the same bet (design for the council, 2026-11-16, version 4 (council rounds 75 and 76), nothing sent)

**Why.** Alex's standing instruction is to keep going until the current challenges to production are solved; it outranks the hold
(D581). Arm A removed the unlisted parts in its written answers but declined two topics wrongly.

**The blind reading** (`d436-reading/RESULT.md`): two readers, one per family, applied D397, D417, D436 and D437 to twelve topics.
- **One bet, by both:**
  - the two topics arm A declined;
  - four topics whose stored refusals the first readers had split on.
- **Refusals kept, by both:** four (two years, two measures, a rolling twelve months).
- **Split:** two.

The frozen step already declines some one-bet topics.

## The change: arm A plus one clause at system line 5 (`make_arm2.py`, `arm-a2/`)

> *A second side of the same bet, for example a market's tightness beside the volume shipped, a share beside the total it is part of,
> or capacity beside the demand it serves, stays in the one question as context: list it in not_judged. A second side is not by itself
> a reason to decline; decline only when no part is the main one, or when the main part itself meets a case below.*

| Part | Source |
|---|---|
| a second side of the same bet stays in the one question as context, listed as not judged | D436 (Alex: "算一个题，第三处不改"), D397 |
| the three examples | D436's own three ("the shortage beside the shipments, the AI-chip share beside the chip total, the capacity keeping pace beside the demand"), without their companies; given as examples, not a closed list |
| not by itself a reason to decline | D436: one question |
| decline only when no part is the main one, or the main part itself meets a case | D397 ("A thesis with no main part gets no judged question"); line 6's cases, D417 |

**Changed from version 1, as round 74 asked:**
- **Removed:** "two bets … leave the topic with no main part" (D397 permits two bets with a main part).
- **Removed:** the checkpoints example (an interpretation of two readers, not Alex's ruling).
- **Added:** "by itself", so the main part can still require a refusal.

Size: system 9,545 → 9,978 characters.

## The test (`probe.py --arm a2`, `probe_score.py --arm a2`)

**Two arms** on the same day: the frozen request (control) and A2. There is no fresh arm A, so a difference cannot be split between
arm A's definition and the clause. That is a stated limit.

**28 topics, three sends each (168 sends, about $0.22, $0.25 an arm by reservation):**
- D577's 18: 7 motivating, 5 regression watch, 6 harm controls.
- **Refusal controls (4):** week clean-4 and clean-12 (two years), July c2/clean-6 (two measures), July c1/clean-13 (twelve months,
  D417).
- **Recovery leads (4):** July c1/clean-11, c1/clean-2, c2/clean-10, week clean-13 (one bet by both blind readers; stored refusals).
- **Disputed (2):** July c1/clean-15, c3/clean-3. Reported only; no rule reads them.

**The rule, fixed now** (D577's guards, readers, plants and scorer, extended):
- **Stop or inconclusive, checked in this order:**
  1. A missed plant stops the reading.
  2. If the control fails L on fewer than 3 motivating topics, the result is inconclusive.
  3. If the control declines in 2 of 3 sends on fewer than 3 refusal controls, the result is inconclusive.
  4. If the control already writes 10 or more correct recoveries of 12, the result is inconclusive.
- **A lead needs all four, under both countings:**
  1. On the motivating topics, A2 fails L or declines (the model's or code's refusal) on at most 1 topic, in at most 1 send.
  2. Every mark other than L stays within the control's count plus one, in every group. On refusal controls and recovery topics only
     the model's refusals are left out of this count. Unjustified refusals (N) and code refusals still count.
  3. Every refusal control on which the control makes a **justified refusal** (the model declined and N did not fail; a code refusal is
     not one) in 2 of 3 sends, A2 also does in 2 of 3. Each topic is reported.
  4. A2's correct written recoveries are at least the control's plus 3. A **correct** recovery is a written answer with no failed
     gate-accounted mark (the marks gate 1's accounting settles), W and H included. G, whether the ranges are a fair division around
     the article's amount, is not in it: gate 1's accounting reports G apart, and so does this. Each recovery topic is reported
     separately, with the sends whose G both first readers mark as failing. A recovery counted correct is not called wholly sound
     when its G fails.
- **What a recovery does not show:** which main part a reader would judge. Each one's question is printed beside both blind readers'
  named main parts and read by me.

## Checks done ($0)

- **`probe.py --arm a2 check`** (`check-output-a2.txt`):
  - all 28 controls equal their stored first requests;
  - all 28 changed requests equal the control plus exactly the arm;
  - 18 stored written answers accepted (the other 10 stored sends were refusals);
  - a mutant answer refused and a synthetic answer accepted.
- **Tests:** `test_probe_score_a2.py` has 10: each new rule, the three round-75 distinctions, and the whole A2 pipeline on its 28 topics
  through a fake transport. D577's 17 tests still pass.
- **Mutants:** all eight of the new rules' mutants fail their tests (`test-mutants.txt`).
- **The cap is conditional,** as for D577: the sum of single-attempt reserves is $1.755. The $0.50 of caps may stop the probe before
  all 168 sends finish, which would read NOT MEASURED.

## What would stop it

- the council finds the clause wider than D436, D397 or D417;
- a check above fails on the day of the send.
