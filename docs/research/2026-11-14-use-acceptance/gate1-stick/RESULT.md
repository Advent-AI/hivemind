# Gate 1's reading, repeated: result (D568), 2026-11-16, $0

Second reading: `poc/data/clean-carried-run-2026-11-16/stage-a-reread/` (packets and key byte-identical to the first; fresh first
readers and third readers of both families; every row valid, every ruling present; its own report `report.txt`). Comparison:
`compare_readings.py` → `comparison.txt` (tested beforehand, `compare-selftest.txt`).

## What the comparison shows

| | Unresolved counted for the answer | Unresolved counted against it |
|---|---|---|
| Line verdicts, first / second | 1, 2, 3, 5 missed and 4 met in both | the same |
| Line 1 (Q) failing sends | 3 / 2: both 2, first only 1 (`clean-1` pass 3) | 5 / 2: both 2, first only 3 (`clean-1` p3; `clean-3` p2, p3) |
| Line 2 (L) failing sends | 7 / 7: the same 7 | 7 / 7: the same 7 |
| Line 3 (R) failing sends | 4 / 5: both 4, second only 1 (`clean-4` pass 2) | 7 / 5: both 5, first only 2 (`clean-3` p2, p3) |
| Line 5 (topics right of 13) | 7 / 7 (by written choices 6 / 6) | 5 / 5 (4 / 4) |
| Q, L, R values that changed | 2 of 108 | 5 of 108 |
| Dispute share | 25 / 16 of 281 | the same |

The three `clean-3` changes under the second treatment are points the first reading's two third readers left unresolved. Controls
(author-checked): five of six read as expected in both readings; the Q fault on `clean-1` pass 3 (the unnamed lab) held in the
second reading (its Claude-family third reader read the focus line as naming the lab's support).

## What it shows and does not

- Shows: on these 39 sends, read again by the same method and families from identical packets, every line's verdict is the same and
  most failing sends recur; line 2's seven are identical. The misses of this reading are not an artefact of one reading session.
- Does not show: which reading is right, how much of the nine readings' misses the method causes elsewhere, or anything about
  independent readers (same families, same order).

## Found while reading the result: which marks reach a reader of the product

`not_judged` (line 2's mark L) and an event's reference (XR) are stored in `clean_ladders.checked_answer`; no judging request
shows them (the judge's request is built from the view, its rungs and its evidence: `src/hivemind/views/judging.py`) and the
product's page and service do not read them (searched `src/` and `poc/ui/`: no reader of `clean_ladders`, `checked_answer` or
`not_judged`). The marks that reach a reader are the question and the rungs (Q, R), the due day (D, W) and the figure ranges (X).
Recounted on the first reading's per-topic map (`carried-run/faults-by-topic.txt`) without L and XR, line 5 would read 9 or 7 of
13 (needed 11): gate 1 would still be missed; that recount is a reading of stored marks, not a change of any line.
