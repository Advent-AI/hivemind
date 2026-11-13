# Stage B, the reading: what is read, counted and decided (D428, D429, D430); written before the send

Written 2026-11-11, before Stage B is sent and before any of its verdicts exist. It carries the baseline's reading over
(`BASELINE.md`, reviewed seven times) and adds what Stage B needs: Alex's lines (D428) and the design's control theses (§8,
line 3). **Stage A has not passed** (D426), and every report of Stage B says so. Reviewed before any verdict is read.

## What is read, as in the baseline

- **The judgements:** every judgement the frozen judge makes in Stage B's three draws (about 236 in the dry runs), each with
  the request as sent, the stored answer and the evidence linked by then that the request did not list; read each alone in
  shuffled packets with no two judgements of one question, by the same form (`ladder/stage-b-reader-brief.md`).
- **Readers:** Codex and Claude Opus 5.5, one fresh read-only session a packet, as in the baseline (Opus is the baseline's
  second family as counted); two third readers on every differing verdict; my own read of every stored judgement any reader
  calls UNSUPPORTED, written before the count.
- **Controls:** the baseline's six planted answers, unchanged (they passed their trial and both families caught them in the
  baseline with the stored rung named), placed as single judgements among Stage B's; and three repeats of Stage B judgements,
  drawn with a seed fixed before the run is read. A planted answer missed by both families stops the reading (the design's
  instruction); a family missing more than one in five, more than a third of verdicts differing, fewer than 30 decided
  judgements, or a family's sessions over twice the estimate, read NOT MEASURED.
- **The count:** the baseline's `baseline_count.py`, generalised to Stage B's population and lines, with the same refusals of an
  incomplete record (every packet rebuilt and compared, every row's contract, session logs, third rulings, my own read).

## The lines (D428, in Alex's words: "数字题和是非题分开比")

Each line is computed on the same three readings as the baseline's shares (unresolved left out; counted SUPPORTED; counted
UNSUPPORTED) and compared reading for reading with the baseline.

| line | passes when | the baseline it compares with |
|---|---|---|
| 1 | no draw incomplete after one redo (design §8) | — |
| 2 | at least nine in ten laddered theses judged at least once (design §8); 26 laddered in the first send, so at least 24 | — |
| 3 | the control theses (below) | reader B's frozen answers |
| figure | decided figure-question judgements UNSUPPORTED at most 5 points above the baseline's | 4/52 (7.7%), 4/53 (7.5%), 5/53 (9.4%) |
| yes/no | decided yes/no judgements UNSUPPORTED at most 5% | 0/99 |
| last | of the judged theses whose last judgement in the window is decided, at most one in ten UNSUPPORTED (Alex's "3 in 30", scaled); INSUFFICIENT last judgements reported beside | 16 of 16 SUPPORTED |

What a judgement counts as a figure or a yes/no is its view's shape: a ladder with numeric bounds is a figure; an event (two or
three rungs, no bounds) is a yes/no. In the first send, 12 of the 26 laddered theses are figures and 14 are events
(11 event for a company, 3 event for a theme, 6 figure for a company, 6 figure for a theme); the share of judgements of each shape is reported
beside the lines.

## Line 3: the control theses

The 16 theses of the three draws that the frozen matching rule paired with a ruler question (`unseeded-2026-11-10/
mapping-runs.json`): q07 (three), q08 (three), q09 (two), q13 (two), q18 (three), q04, q16 and q23. All 16 have a ladder in the
first send.

1. **Eligible** when (a) a reader confirms the judged question asks what the ruler's question asks, for the same period;
   (b) for an event, the deadline is the ruler's; (c) reader B's frozen gold holds an answer for it; (d) the view has a
   judgement on or before 2026-07-14. Two readers (one of each family) on each, a third on a difference.
   **The due day of a figure (D430, Alex: "指同一份年报就算相同").** A figure's due day counts as the ruler's when both mark
   the publication of the same period's figure (the ladder step sets a year's figure's due day by code, D414, where the ruler
   gives another day for the same annual report: q09 2027-04-01 against 2027-02-28; q04 and q13 likewise). An event's
   deadline must be the ruler's. The literal reading (every due day equal) is counted beside. Three controls fail either way:
   the two Kyber theses written for "during calendar 2027" with a due day at the end of 2028, and the Ohio thesis due
   2027-12-31 against the ruler's 2027-06-30.
2. **The answer compared** is the view's last judgement on or before 2026-07-14 (the frozen scorer's rule), by outcome: for a
   figure, the chosen rung's band overlaps reader B's range; for an event, Yes against reader B's yes, and "Ruled out" or
   "Still open" against no (both mean the event has not happened by the deadline).
3. **Material shown:** for each eligible thesis, two readers mark each of reader B's decisive items (the gold's own
   `decisive_items`, read in the frozen packet) as shown or not shown to the judge in its last request on or before
   2026-07-14. A disagreement where the material was not shown is a miss of Steps 1 to 3, reported apart.
4. **Line 3 passes** when at least 8 eligible theses have reader B's material shown, and all but one of those agree with
   reader B. Fewer than 8: the control is unexercised and Stage B cannot pass (the design's words).

## What it cannot show

That the ladder step's ladders are sound (Stage A has not passed; their known faults are in them); that the readers catch
subtle errors (no control is known to be sound); anything about the system's other steps. Three draws of 26 laddered theses:
the lines' chance behaviour is in `result/line-chance.txt`.
