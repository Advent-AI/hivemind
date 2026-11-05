# Pull mode

> Status: decided and built (D54, D356; day-end scope confirmed by D368). English edition: November 4, 2026.
> Design page: `docs/system-design.html` → New → Pull mode. Recorded decisions take precedence.

## Purpose

The only time-driven module. The incoming stream handles one item at a time and never reads the calendar; pull mode owns what depends on the date.

## What it does

- At the end of each day, with the day passed in (real time in production, the replayed day in tests), it closes every open question whose due day has come, at the rung it stands on. See [Closing at the due day](07-final-verdict.md).
- It does not re-judge open questions without new evidence (D356), and it does not wait for the day's items (D54).
- It opens nothing: an event question that falls due unresolved closes at its state, and no next-deadline successor is opened at the due day (D248 boundary 2's step dropped, D368).
- Due days are set when a question is opened, on or after the day its result is published (D356). A question whose result is still unknown on its due day closes at its state like any other.
- Upstream delivery is a separate thing and is not pull mode.

## Example

"What will Nvidia's total revenue be in FY2027?" is due on February 28, 2027, after the annual results are published. The results arrive as evidence and move the question's state before that day. At the end of February 28, pull mode freezes the question at its rung and closes it; questions that depend on it read the closed conclusion. An FY2028 successor question continues the tracking.

## Not built

- Fetching settlement figures (prices, filings) from a source, and whether they would enter through dispatch.
- Claude's earlier daily duplicate check among open questions: not decided (D356; library PRD, proposals).

## Related decisions

- D12, D13: the stream does not read the calendar. D14: the two modes are designed apart.
- D31: the day is passed in.
- D54: freezing at the due day; nothing waits.
- D356: what pull mode does and does not do.
- Code: `src/hivemind/pull.py` (`end_of_day`), called by `src/hivemind/replay.py` at the end of each replayed day.
