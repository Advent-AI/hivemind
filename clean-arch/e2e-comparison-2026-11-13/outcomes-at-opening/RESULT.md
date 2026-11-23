# Writing the outcomes at opening (c19 against c8, D478): result, 2026-11-13

**Answer: it fails its frozen lines. Asked to write each new thesis's outcomes when opening it, the first step opened slightly more
ladderable shapes, but the outcomes it wrote are not sound (one list of 21 passes the standard's checks), so no target matter counts as
reshaped; and on one target article it opened the memory question less often (1 of 3 against 2 of 3).** No over-opening regression and no
suppression line fired. Choice 2, in this design (an output contract in the same call), is falsified on these cases.

108 jobs, all valid; $1.88 at published rates. Records `poc/data/clean-outcomes-probe-2026-11-13/records.jsonl`; every answer read by Claude;
two blind Codex readings (`reader-ladderable.jsonl`, arm-blind, both arms; `reader-quality.jsonl`, c19's outcomes), keys outside the repository.

| line (frozen in `PROBE-DESIGN.md`) | c19 | c8 | result |
|---|---|---|---|
| target: H100 price at c1-127, a ladderable thesis | opened 3 of 3; ladderable 2 (year-end, annual average; a quarter is not) | opened 1; ladderable 1 | shape better, but every c19 outcomes list fails quality (middle range uncompared; a top range labelled "at or above the peak" that starts below it) → **not reshaped** |
| target: memory price at c1-127 | opened 2; ladderable 1 (DRAM spot, year-end against mid-year) | opened 1; ladderable 0 | quality fails (the price series unspecified) → not reshaped |
| target: memory price at c2-56 | opened 1; ladderable 1 | opened 2; ladderable 0 | quality fails (ranges overlap at their ends) → not reshaped, and **opened less often** |
| **targets** | | | **not met** |
| should-not-open: Intel, custom chips, the China survey (c3) | 0, 0, 0 | 0, 0, 0 | none |
| should-not-open: Firmus | 1 | 2 | reduction |
| should-not-open: US approval; the China survey (c1) | 1 (three outcomes); 1 (a rolling window, with five outcomes) | 0; 0 | no regression (one send each); the field did not stop a rolling window |
| suppression: capex-open (9) | 8 | 8 | met |
| suppression: memory states (9) | 3 | 5 | met (difference below a third) |
| Ohio (reported) | 0 | 0 | |
| outcomes' quality, all c19 theses | 1 of 21 pass; 20 fail (one list may fail several): no comparison for the middle range (10), overlapping or gapped ends (8), not answering the question's own period or measure (12), wrong count (3); one strict blind reader, not checked by code | — | |

**What it shows.** The opening step can be pushed toward one figure and one year, but in the same call it does not write outcomes that
meet the standard: ranges overlap at their ends, the middle range names no reference, yes/no questions get five ranges, a policy gets three
states. Those are the faults the separate ladder step's code checks catch and send back (D405–D414), which is why that step exists. Adding
the outcomes at opening without those checks moves the work, not the quality. Limits: one design, 18 states, three sends; a strict reader
(the middle-range test fails 10); it does not show that no structural link between opening and the ladder step can work.
