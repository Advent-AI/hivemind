# Council round 40 (Alex active, 2026-11-17): plan the next step for astra on the answer-choice step. Be brief.

Alex: "你测试吧，但是你跑一下council 稍微整一下下面一步该怎么做". He has authorized about $6: an outside-44 test (~$1) and a gate-1 rerun on the 44 (~$5).

## State (read the files; out of scope: the frozen ruler, Steps 1-3, the judging stage)
- D648/D649 (`docs/DECISIONS-log.md`, tail): astra-frozen on the 44 meets lines 1, 3 and 6. It misses line 4 by 7 answers: acc/clean-9 3/3, acc/clean-8 3/3 and
  u3/clean-10 1/3. Each is a topic with a main figure plus a sub-part or a condition, declined as "no main one". Lines 2 and 5 depend on 20 unresolved points;
  14 of them are one rule, the due day of an existing obligation (next annual report ~Feb vs code's 60 days after FY end, Apr 1; D403, Alex's call, unanswered).
  Report: `poc/data/clean-ladder-stage-a-astra-2026-11-17/run-1/report-output.txt`.
- D650: one 26-topic draw cannot rank models; luna's agreed count moved 7 to 1 between draws.
- The candidate fix is D436 (Alex): a second side of the same bet is one question, context, listed as not judged. A2's text
  (`docs/research/2026-11-14-use-acceptance/reflection-6/astra-a2/a2_probe.py`, EDITS) adds:
  "A second side of the same bet, for example a market's tightness beside the volume shipped, a share beside the total it is part of, or capacity beside the demand
  it serves, stays in the one question as context: list it in not_judged. A second side is not by itself a reason to decline; decline only when no part is the main
  one, or when the main part itself meets a case below." It also changes "wording" to "description and outcome" in three places, the closing and the schema.
  The A2 readings were VOID (D640, D641). audit-2.md says "NOT SOUND: 'The question leaves out' can include event alternatives already decided by the answer
  choices".
- **My concern:** two of A2's three examples mirror the two failing 44 topics: HBM growth plus "still short of demand", and total semiconductor revenue plus its
  AI part. AGENTS §6: no example taken from a test article, no case-fitted fix, and the examples must read the same for a bank, a drug maker or a retailer.

## My proposal (challenge it)
1. **Edit (minimal):** only D436's sentence, with no examples, or with cross-domain examples not taken from the 44: "A second side of the same bet stays in the one
   question as context: list it in not_judged. A second side is not by itself a reason to decline; decline only when no part is the main one, or when the main part
   itself meets a case below." No "description and outcome" change, so audit-2's finding is not inherited.
2. **Outside test (~$1), astra, both the frozen and the edited request,** 3 draws each, on topics outside the 44:
   - targets: topics with a main figure plus a second side, from the 26 outside topics and the reference-control set;
   - controls that must stay declined: week-10-06 clean-4 and clean-12 (two years with no main one) and fortnight clean-8 (no theme), all justified by both
     families before;
   - read blind by both families with planted controls.

   Pass rule, fixed before the send: the target declines turn into questions the readers accept; no control flips to a question; no new agreed failure on
   another topic.
3. **If it passes:** gate 1 on the 44 with the edited request, read with the run-4 procedure, both countings reported. The due-day rule stays Alex's.

## Ask
Agree or correct, with the smallest change. In particular:
- (a) the edit text: examples or none;
- (b) whether the outside set has enough target cases (name them from the files);
- (c) the pass rule;
- (d) any reason the gate-1 rerun on the 44 is unsound after this, given the 44 were seen.

End with CONSENSUS: <one line> or DISAGREE: <one line>.
