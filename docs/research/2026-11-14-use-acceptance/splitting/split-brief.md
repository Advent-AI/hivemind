# The split probe's reading: what this brief adds to `stage-a-reader-brief.md`

Read `stage-a-reader-brief.md` first. Mark every item by that brief. This brief adds one thing to read and two fields to return.

## Items asked for one year of a topic

Some items carry `split`: `{"asked_year": "2026", "asked_separately": "2027"}`. Their topic asks one quantity for two years. The step
was asked for `asked_year` only, and the other year is asked as its own question.

- For these items, read the thesis as asking `asked_year` only. The other year is not a part this question leaves out, so it is not
  owed in `not_judged` (`L`).
- Asking one of the two years is not a fault of `Q`.
- Every other part of the topic's wording that the question leaves out is still owed, as the brief says.

Items with `split: null` are read exactly as the brief says.

## Two more fields, on every item

| field | values | the mark |
|---|---|---|
| `BY` | `yes`, `no`, `cannot_tell` | `yes` when the question asks the value for a year that the thesis names only as a base or a point of comparison (for example, the thesis asks 2027's spending against 2026's, and the question asks 2026's). Decide it from the thesis's own wording, for an item with `split` too: a `split` item whose thesis asks the value of both years does not ask a base year, and one whose thesis names `asked_year` only as a base or comparison does. `no` otherwise. |
| `LQ` | `yes`, `no`, `cannot_tell` | `yes` when the question measures something wider or different from what the thesis asks, because it drops a limit the thesis's wording sets (a group, a product, a region, a measure's basis) and does not list it in `not_judged`. For example, the thesis asks server DRAM prices and the question asks DRAM prices. `no` otherwise. |

When either field is `yes`, `why` names the year or the limit dropped.
