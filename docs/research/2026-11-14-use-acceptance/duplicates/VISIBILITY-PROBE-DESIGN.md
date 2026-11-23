# An isolated same-day visibility probe on stored articles: design, version 2 (D522, under D439), 2026-11-15; WITHDRAWN, nothing sent

**Withdrawn (D523).** The council's round 14 found that the pass condition contradicts the frozen reading prompt, which tells the
reader to propose a question even when it is already open because the comparison step folds it in afterwards. The trace that
followed (`DUPLICATES-RESULT.md`, "Where each second question was let through") shows the opening is decided in the comparison step.
The text below is kept as the record of what was proposed; its $0 checks (section 1) stand.

Version 1 (adding one question's two lines by hand) was reviewed by the council (round 13) and not sent. This version answers each
of its five points after a $0 check. It is an **isolated probe of what the reading step does when shown the earlier questions of its
day**, not a replay of D375: the later articles of the day, the comparison step and the re-sending of waiting requests are not run.

## 1. What the $0 check established (`historical_check.py`, `historical-check.json`; `visibility_probe.py` dry)

- **The stored request is reproduced by the production code.** For every case below, `extraction.shown_views` and
  `extraction.request_for` on the stored article and the run's store, read at the day's start, give a request with the stored
  archive key. So the state of that day is reconstructible from the stored run, and the request is in the form production sends.
- **The list "committed before the article" is built by the same code,** with one input changed: the sequence number the store is
  read at (the article's own minus one, in place of the day's start). It holds every question committed before the article with
  the groups, other names and parent questions each had at that sequence. Nothing is typed in by hand. It differs from the
  day-start list by more than the earlier question: in the Rubin case two questions are added and another question's line changes.
- **The answer checks and filing run in isolation on explicit lists.** Each stored answer, put through
  `extraction.sift_with_groups` and `extraction.file_reading` on the day-start list, gives exactly the stored handover (four of
  four checked). A synthetic answer whose statements are linked to the earlier question is kept under it on the per-article list
  and is refused or left homeless on the day-start list.
- **The third duplicate pair of the fresh week is a same-day case too** (fiscal 2028 revenue: the amount question opened at article
  11 and the growth question at article 22 of 2026-09-22). It was absent from the first list of candidates because those two
  questions share no research group. So all three pairs both reviewing teams called duplicates were opened by a later article of
  the same day that was read without the earlier question.
- Known mismatch, disclosed: the block's heading still reads "[Open questions at the start of <day>]" (the frozen prompt's words)
  in both arms.

## 2. The question

When the article that opened the second question of a duplicate pair is read with the questions committed before it on its list,
does the reading step file its statements under the earlier question and propose no second question on that matter, without
suppressing questions that should open?

## 3. Cases (all from the old system's fresh-week run; fixed before any send)

| Case | Article | Role | The list gains |
|---|---|---|---|
| rtx | 175 of 09-27 (opened `v15`) | scored: both teams call `v15` a duplicate of `v14` | `v14` |
| rubin | 103 of 09-24 (opened `v11`) | scored: duplicate of `v9` | `v9`, `v10` |
| fy2028 | 22 of 09-22 (opened `v5`) | scored: duplicate of `v3` | `v1`, `v2`, `v3`, `v4` |
| control-revenue | 11 of 09-22 (opened `v2` and `v3`, fiscal 2027 and 2028 revenue) | should stay separate: the only earlier question is the financing total | `v1` |
| control-margin | 98 of 09-24 (opened `v10`, fiscal 2028 gross margin) | should stay separate: the only earlier same-day question is Rubin shipping | `v9` |

The two July pairs are left out: whether each is one matter asked twice has not been read by reviewers.

## 4. Arms and sends

Control: the request as stored (rebuilt, stored key). Changed: the request the production code builds from the per-article list.
The frozen reading prompt, schema, model (gpt-6-luna, low effort) and output allowance (8,000 tokens) are untouched. Three sends
an arm a case: 30 calls, one HTTP attempt each, every reply saved before it is read.

## 5. What is read in each answer (written before any send)

Every answer goes through the production checks and filing on its own arm's list. Then, for each send:
1. **Second question:** is a kept candidate on the matter of the question the stored answer opened? Marked twice: by me, and by a
   blind reader given the kept candidates of all sends in shuffled order without arm or case labels beyond the matter's
   description. A send on which the two marks differ is reported as unsettled.
2. **The case's statements:** the statements the stored answer filed under the question it opened are fixed now, with their
   passages (`cases.json` at the send; 2, 1, 1, 2 and 3 statements). In each answer: how many of those passages are kept (a kept
   statement whose passage overlaps the fixed one by at least half of the shorter), and under which question.
3. **Everything else:** kept and dropped statements with reasons, and every other candidate, printed for each send.

## 6. The rule (written before any send)

- A scored case is **exercised** when the control arm proposes the second question in at least two of its three sends.
- An exercised case **supports** when, in at least two of the three changed sends, no second question is proposed and at least one
  of the case's passages is kept under the earlier question and none of the case's passages that the control kept is lost.
- A separate control **holds** when the changed arm still proposes each of its questions in at least two of three sends.
- **Supports:** at least two scored cases exercised, every exercised case supports, both controls hold.
  **Does not support:** at least two exercised and none supports.
  **Inconclusive:** anything else (fewer than two exercised; mixed cases; a control that does not hold; unsettled marks that would
  change a case). All three outcomes of each arm are reported for every case whatever the verdict.
- A result that does not support says only that listing the earlier questions did not change the reading step's proposal in these
  cases. It is not read as a finding about the comparison step.

## 7. Cost

Sized on the rebuilt requests: 30 calls; if every call used its whole output allowance, $0.159 at the published rates ($0.10 and
$0.50 a million tokens). Ceiling $0.25. Recorded under D439 (about $18.42 of $40 so far).

## 8. What it cannot show

That any answer to a question improves; how a whole day runs with per-article lists; that D375 is ready (its implementation and
acceptance are Alex's, pending); a rate. Three cases of one week of one run, three sends each.
