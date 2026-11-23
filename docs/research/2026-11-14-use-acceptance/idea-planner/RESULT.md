# The Idea planner on new-system answer shapes: the $0 check D580 asked for (2026-11-16)

**Answer: the falsifier does not hold in full.**

- The page computes no composite from an event or an undirected range: its UI tests show that, but this trace did not run the page,
  and what external API clients compute is unknown.
- The planner hands the model an event's two ends as "Yes" and "Still open", and it can record "Still open" as the end that raises
  the outcome.
- The page shows no composite for any Idea that has a new-system event or theme range among its drivers.

Trace: `trace_planner.py` → `trace-output.txt`. Run on the fortnight's page store (`poc/data/clean-carried-run-2026-11-16/page-store-2026-11-16/views.sqlite`)
with the API's default configuration (`poc-v118-idea.json`: `idea-summary-v8`, which shows the planner endpoints only). The three
drivers were an event (v3), a theme range with no favourable end (v5) and a company figure whose lower end is favourable (v2). The
answers are realistic and written by hand; there is no model call.

| Shape | All choices | Shown to the planner | What the plan records |
|---|---|---|---|
| event, three outcomes | Yes, Ruled out, Still open | **Yes and Still open** (positions 1 and 3) | `first` for Yes; `last` when the model names "Still open" |
| theme range, no favourable end | five ranges | the lowest and the highest range | `first` or `last`: a direction relative to the Idea's own outcome, meaningful for a range |
| company figure, lower favourable | five ranges with bullish-to-bearish labels | the two end ranges | `first` or `last` |

**The consumers (read from the code; this trace did not run the API or the page):** only the page's composite
(`poc/ui/src/idea/composite.js`) reads `supporting_end`.

- It computes from the investment scores (±2).
- Since D570 it refuses any undirected driver (an event, an unrecorded shape, a range with no favourable end), with a note on the
  card; this was shown by its UI tests, not by this trace.
- The API's Idea route returns the reader's card with the plan in it, so by the code path an API client can read an event whose
  "last end" (Still open) raises the outcome. The MCP server has no Idea-planning tool.
- The synthetic answers show what the contract permits, not what the model would choose or how often.

## What this means

1. **The request misdescribes an event.** An event here has three stored outcomes: Yes, Ruled out (a formal decision against it) and
   Still open (neither, on the due day). The planner is shown only Yes and Still open, as if they were the two ends of one scale. Ruled
   out is left out, though it is not the same as Still open. Neither of the two outcomes left besides Yes is the whole opposite of
   Yes.
2. **Coverage.** In the new system most theme questions are ranges with no favourable end: 4 of the 12 questions open in this store at
   its default date, beside 6 events and 2 directed company figures. Any Idea that uses one as a driver gets no composite on the page, although the planner gives each range a direction
   relative to the Idea's outcome. The page's composite scale is the investment score, which such a range does not have.

These are integration gaps; neither passes a quality gate. A narrow design would decide two things, each a choice of what the product
shows:
- how an event can be a driver: shown all three outcomes, with Yes or Ruled out as the end that raises the outcome, or kept as context
  only;
- whether a range's own positions, with the planner's direction, may form the composite scale.
