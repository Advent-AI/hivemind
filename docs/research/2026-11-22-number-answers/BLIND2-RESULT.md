# judging-v13s blind test, re-run after D741: result (SMALL-DESIGN.md §5; D740, D741)

**STOP**, on one confirmed registered stop condition, with unresolved reader marks beside it: a Part B refusal that refuses a right answer.
- P-v4's Claude writer was refused by S4: "v4: uses F4 for NVIDIA | revenue | company | FY2027 Q3 beside its forecast figure F8".
- F4 (the $108.0B Q3 guidance) never enters the total as a Q3 value. It builds F9 = growth(Q2 $96.2B, F4) = 12.27%, the guided Q2 to
  Q3 growth, and Q4 = apply_growth(F8 $112.5B, F9) = $126.3B. The only Q3 value in the revenue sum is F8.
- Both refusal reviewers: the request states the rule (the header's "Shared quantities … through which every figure an outcome uses
  for that quantity goes"), and the answer is right.
- Both readers and both adjudicators call the forecast supported.

Every other registered line passes:
- Part A (104 cases, 40 mutants, 19 rehearsal checks) was green before the run.
- The run is complete: 12 first replies, 24 readings, 6 adjudication packets, each read by two adjudicators.
- Every case has at least one usable reply. The joint case has both forecasts supported in one reply (R05 and R09).
- No accepted reply carries a settled defect: no defect was upheld by both adjudicators, and no reader pair marked the same defect.
  R07 comes closest: both readers marked F3, but under different types, and each adjudicator pair split. Across the six packets, five
  marks were jointly rejected, nine split and none was jointly upheld (Council round 56).

**Run:** `poc/data/judging-v13s-blind2-2026-11-22/`. It cost $0 at the provider: writers, readers, reviewers and adjudicators were fresh
Claude subagents and fresh read-only Codex sessions. Adjudication packets are built by `blind_adjudicate.py`; the tally is
`TALLY.json`.

## 1. Writers' first answers (`CHECKED.json`)

| Case | Claude writer | Codex writer |
|---|---|---|
| P (joint) | publish: v4 413.1, v8 382.4, both rung 2 | publish: v4 419.2, v8 388.3, both rung 2 |
| P-v4 | **refused (S4)**: 416.6, rung 2 | publish: 416.4, rung 2 |
| P-v8 | publish: 383.6, rung 2 | publish: 388.6, rung 2 |
| S (CY2026) | publish: 717.8, rung 4 | publish: 680.8, rung 3 |
| O | publish: 14, rung 1 | publish: 16, rung 1 |
| E | publish: 36, rung 3 | publish: 36, rung 3 |

- 12 of 12 were schema-valid.
- 11 of 12 passed every code check.
- D741's three rulings were applied:
  - S applies a stated deduction from the total in both replies (Claude 3% non-data-center share; Codex 92% data-center share).
  - No v8 reference carries a past quarter's share (the S5 [D741] check refused none).
  - D740's "from … to …" fix is exercised by E's Claude writer, who copied the CPU market figures without a range refusal (E's Codex
    writer did not use them).

## 2. The refusal: mechanism and census

- **The mechanism.** S4's bypass walk starts at each outcome and follows `inputs`. It records every figure whose key is a listed shared
  quantity, and it descends through every non-forecast figure, rates included. F9's unit is %, yet the walk descended into F9's inputs
  and reached F4. A rate computed from a quarter's guidance is another quantity. The quarter's value in the calculation is still F8
  alone.
- **The ruling at issue.** D741 ruling 1 (Alex: "不算错"): a growth rate computed from guidance and used as a benchmark is not a
  second value when one figure supplies the quarter in the revenue calculation. The question Alex answered named the deciding point:
  "进入收入计算的三季度数只有 1136 亿这一个". The system text also asks the writer to give "a run-rate that carries the guided growth
  forward". The schema's benchmark sentence names "an estimate", and that is the narrower wording the code follows.
- **The census, $0** (`s4_census.py`). Every stored v13s first reply from both blind tests (24) goes through the current checker and
  through a candidate copy.
  - **A blanket candidate, rejected by Council round 56.** It stopped the walk beneath any % or x figure
    (`s4-ratestop-calc_small.py.txt`). It changed 1 of 24 and passed the 104 cases. However, it also publishes a reply that builds Q4
    on the guided $108B through a multiple applied twice to Q2 (96.2 × (108/96.2)²) while Q3 = $112.5B stands in the sum. That is a
    second Q3 value, and the current checker refuses it.
  - **A narrowed candidate, rejected by round 56b.** It skipped the rate at an `apply_growth` whose base is the forecast. It still
    published a base pulled back to guidance inside the calculation (F8 × (1 + growth(F8, guidance)) = $108B, then grown 12%), and it
    refused equivalent sound forms.
  - **What was decided (round 56c, D742).** S4 stays. The request now states one rule in three places: guidance informs the pace; the
    forecast pace is an estimate that names its benchmark; the quarter's dollar value is the one forecast figure.
    - `s4_replay.py`: the saved reply and both council resets are refused; the stated-estimate form passes at $416.62B.
    - Part A: cases 109 of 109, mutants 42 of 42, rehearsal 19 of 19.

## 3. Readers and adjudicators (`TALLY.json`)

Each reply had a Claude reader and a Codex reader. Six replies drew a disagreement. Two adjudicators, one per family, settled each point
against the passages and the format rules (the D741 rulings included). A point counts as settled when both agree.

**Settled as not defects (both adjudicators reject):**
- every "plus or minus 2%" guidance given as its midpoint (R06 F7, R09 F4, R10 F3). The format permits this.
- R11 F4 ("up to" stands before the $3B total in e1919's quote, not before the $1B tranche).
- R11 F12 (42 + 25 = 67 with "more than" kept on the source).

**Unsettled: the families split** (in every split, the Codex adjudicator upholds and the Claude adjudicator rejects). They fall into
two classes.
1. **O's "$18 billion" (R07, R11).** e2889: "it has $18 billion committed to equity investments for the remainder of its fiscal year".
   Both O writers read it as the part of e2620's $25B balance funded by year-end, stated that reading as their assumption, and built
   the reference as 25 − 18 = 7. The rung depends on that reading: without the deduction the balance starts at $25B, which is rung 2.
   - **R07, "own estimate passed off as the market's reference" on F3.** D741 ruling 2 does not settle it. The ruling names what can
     be the market's reference (an outside figure for the member's own quantity, or a calculation that carries no past share). That is
     a condition, not a guarantee. F3 = 25 − 18 still rests on the writer's reading that the $18B is part of the $25B and will be paid
     by year-end, and the passages do not state that reading (Council round 56 corrected my first draft here).
   - **R07, "two forecasts of one quarter" on F3 and F10.** F3 has the outcome's key but is the July balance still unfunded, a part of
     the year-end total. The Claude adjudicator calls it the company-schedule baseline beneath the forecast, which the format allows.
     The Codex adjudicator calls it a part labelled as the whole.
   - **R11.** The Codex family calls F2's "guidance to fund in Q3–Q4" an unsupported schedule and the forecast not supported. The
     Claude family says "for the remainder of its fiscal year" gives the timing and the answer states the reading.
   - **R11 F13** also split. It attaches a period and a funded-and-unfunded scope to Bank of America's $70B figure, which e1732 says
     was "not specified". F13 feeds neither the outcome nor the reference.
   - The first test split the same way on the same passage (D740, R02).
2. **Statements in the answer's prose that no figure carries** (R03, R09, R11). Codex upholds them as "number misread" or "wrong
   arithmetic". Claude rejects them because those types are defined on source and computed figures. I read each one against its
   passage:
   - R11: "if the $18B funding slips into FY2028 … probably keep it below $25B" is wrong on the answer's own numbers: a full slip gives
     25 + 7 = 32, rung 2.
   - R09: "$115bn, then 20% sequential growth" is offered as reaching rung 1, but it gives 430.8 against the 431.2 edge.
   - R09: "both 6 GW" drops e1041's "up to".
   - R03: "Vera Rubin is already about 20%" states e2721's expectation as achieved.
   - R03 "flat second half" is disputed: the Claude adjudicator shows a reading under which it holds.
   None of these enters a figure, an outcome or a rung. They are what the card would show an analyst. Code does not check prose
   (D737), and the registered defect types do not cover it.

**Support.** Every forecast is supported by both adjudicators except R11 (O, Claude writer), where the families split as in class 1.

## 4. What the test shows

- **The request and the rulings hold.** There were no schema refusals and no unstated rule. D741's three rulings were applied by the
  writers and are visible to code (S5) and readers.
- **The request contradicted itself on one rule.** The system text invited carrying the guided growth forward directly. The schema
  and the code allow a guidance rate only as an estimate's benchmark, which is Alex's ruling 1 as written. Two attempts to loosen the
  code failed review, so the request was fixed instead (D742).
- **The reader families still split on two things.**
  - One is a source reading: what "$18 billion committed … for the remainder of its fiscal year" covers.
  - The other is whether a wrong number in prose is a defect.
  - Neither is a registered stop, because neither was settled. Both reach the product: the first decides O's rung, and the second is
    what an analyst reads.
- **One draw per writer.** P's six replies are 413–419 (v4) and 382–389 (v8), all rung 2. That is no evidence about gpt-6-luna.
