# Closing at the due day

> Status: decided and built (D54, D356). English edition: November 4, 2026.
> This page replaces the final-verdict draft (D29), which D356 retired; Git keeps the earlier text.
> Design page: `docs/system-design.html` → New → Closing at the due day → Details. Recorded decisions take precedence.

## What it does

At the end of each day, pull mode closes every open question whose due day has come. The question's state freezes where it stands, and that rung is its conclusion. There is no separate final verdict and no separate result.

- The closing record names the rung the question froze at. A question that was never judged closes with "no data to verify", neither a pass nor a fail.
- Decisive information, such as an annual report or an official decision, arrives as evidence by the end of the due day and moves the state like any other evidence. Nothing waits for it.
- A question that depends on a closed one reads its frozen state and reasons in its next judgement.
- A closed question is not closed again and is not judged again. Further tracking uses a successor question under the library's rules.

<!-- generated: closing -->
```
Closing at the due day | Has this open question's due day come? (Pull mode, at the end of each day, with the day passed in)
├─ No → Stay open (Evidence keeps moving its state)
├─ Yes, and it has been judged → Freeze at its rung and close (The closing record names the rung; dependent questions read the frozen state and reasons)
└─ Yes, and it was never judged → Close with no data to verify (Neither a pass nor a fail)
```
<!-- /generated: closing -->

## Rules

<!-- generated: rules -->
1. A question has one state and no separate result: the rung it stands on at the end of its due day is its conclusion (D54).
2. There is no separate final review: each day's judgement already reads the evidence in force (D356).
3. Nothing waits. Decisive information arrives as evidence by the end of the due day; a question whose result is still unknown closes at its state (D54).
4. Due days are set when a question is opened, on or after the day its result is published (D356).
5. The closing record is shown, never a gate; a question never judged shows “no data to verify” (D356).
6. The day is passed in: real time in production, the replayed day in tests. The system owns no clock (D31).
<!-- /generated: rules -->

## Example

"Will Nvidia begin shipping its Rubin generation by December 31, 2026?" stands on Yes at the end of December 31, 2026. Pull mode closes it at Yes, with the closing record "due 2026-12-31, frozen on 2026-12-31 at rung 1 Yes". The revenue question that depends on it reads the closed question and its last reasons.

A check on a copy of the first frozen draw, with the day set to March 1, 2027, closed the thirteen questions due by then at their last rung. Two of them had never been judged (operating margin and the company's capital spending); they now close with "no data to verify".

## What is tracked and shown

The closing record and the question's judgement history are stored and served. The question page shows the closing record from the closing day on ("Closing record" under "About this thesis"), and a closed question that was never judged shows "No data to verify" in place of "Not assessed yet". A closing is dated on the day it happens, also on a day without items: pull mode then records the day under a sequence number of its own. Tracking never gates a judgement.

Not built yet: telling a closing rung that reflects the published result from one that is still a forecast. The first real due day, December 31, 2026, will give the first case.

## Not built

- Fetching settlement figures (prices, filings) from a source.

## Related decisions

- D29: the earlier final-verdict draft, retired by D356.
- D31: the day is passed in; the system owns no clock.
- D54: one state, frozen at the due day; nothing waits.
- D356: no separate final review, no day-end re-judging, due days on or after publication, the closing record shown.
- Code: `src/hivemind/pull.py` (`closing_reason`, `end_of_day`); test: `tests/test_pull.py`.
