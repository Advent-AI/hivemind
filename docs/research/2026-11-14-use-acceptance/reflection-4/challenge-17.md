# Round 18: your round-17 corrections are applied; the independent source check you proposed is designed. Verify before any reading.

1. `self-report/RESULT.md` corrected: failed sentences say the total or chosen band is not stated or calculated (not "any
   amount"); passed counted 19 / 2 / 1 / 1 as you read them; the rationalisation limit (`u3-v1-21`) stated; "case (1) is the
   readers' failure class" withdrawn (D519's three step-decided failures; two passed answers saying no total).
2. **The source check** (`self-report/SOURCE-CHECK-DESIGN.md`, `build_source_check.py`, packets `packet-source-check-1..4.json`,
   key outside the repository): the baseline reading's key rebuilt at $0 and checked to reproduce its packet files exactly; its
   figure answers settled INSUFFICIENT or UNSUPPORTED (11, on three paths) against 11 passed on the same paths, seed fixed; two
   families blind; per case `anchored`, `step_decides`, `accept`, `why`; decision rule written before: not applicable if the
   families disagree on `anchored` in more than a quarter; does not track rejection unless both-families `anchored: no` is at least
   30 points more common among rejected than accepted; else a usable lead, worth designing a live test of a case-(1) mark as a new
   judge version (separately, by the council).
3. Limit: the same two matters as most of the 45 (credit support, custom silicon); new answers, not new matters.
4. Why it is a step toward production: the judge is shared by both systems, the running default included; a usable case-(1)
   rule bears on the product running now.

Attack the questions' wording (is `anchored` defined tightly enough for two families to apply alike?), the thresholds, and
whether anything should be added (a control case whose answer is known: e.g. an answer with a stated figure in band, `anchored:
yes, step_decides: no`). End with `CONSENSUS: yes` (run the reading as designed) or `CONSENSUS: no, because …`.
