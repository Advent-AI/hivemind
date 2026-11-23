# Does a missing figure explain the unsupported answers? Sizing on the census's ten settled cases (D530, under D439), 2026-11-15, $0

Script: `search_missing_inputs.py` (`candidates.json`): for each settled unsupported answer of the two earlier readings, the statements
in that run's store by the judgement's sequence that were not printed in the judge's request and match the matter by pattern.
The two later answers (the trial's and the fresh week's) were searched the same way by hand. A pattern search lists candidates;
each was then read against the question and the request. Nothing was sent and nothing changed.

## The answer

**Three of the ten answers the census settled as unsupported, on two matters (one in each system), coincided with a relevant
candidate figure that was in the run's store and absent from the judge's request. For the other seven the search and the reading
found no qualifying figure** (a pattern search can miss one). This does not show one common mechanism, or that the omissions
caused those answers (council round 22). The two answers on the custom-chip matter rest on the same stored statements and are
not independent.

## Case by case

| Answer (reading) | Matter | A sized figure in the store, absent from the request? | Withheld by |
|---|---|---|---|
| fresh week, old system, data-center revenue, last answer | data-center revenue, fiscal 2027 | **yes**: the next quarter's revenue guidance ($108 billion) and the year's consensus (about $406 to $412 billion), in none of its seven requests | **filing**: sixteen statements of the guidance under the total-revenue question, none under this one (`d375-measure/SAME-DAY-CASES-RESULT.md`) |
| baseline, run 2, custom-chip spending, first answer (07-06) | cloud companies' spending on custom chips, 2026 | **yes**: "Broadcom guided third-quarter AI semiconductor revenue to $16.0 billion" (`e151`, article 63), in the store before the judgement at article 76 | **a later-linking decision** (corrected after the council's round 22: the new system's own question on this matter opened at article 65, after the statement; the hand-written question of the baseline stood in for it). When the question opened, the statement was checked against it and not linked (`FILING-TRACE-RESULT.md`). The next day a repeat (article 92: $10.8 billion for the second quarter, $16.0 billion guided) was filed under the question by the reading step; the second answer used it and was settled as supported after a split. Other statements arrived that day too: not a controlled before and after. The question names four buyers; Broadcom's figure is not broken out by buyer |
| Stage B, run 2, custom-accelerator spending, first answer (07-06) | the same matter, the same stored statements | **yes**: the same `e151` (the same stored statements: not an independent case) | the same later-linking decision |
| baseline, run 3, credit support, first and fifth answers (07-01, 07-05) | total of credit support | none found: no dollar amount for the programme in the run before 07-06 | neither |
| baseline, run 1, credit support, fifth answer (07-05) | the same | no sized figure; the answer counted money already spent | neither |
| trial, old system, credit support, last answer (07-14) | the same | no: the statements not shown were capacities already in its request in other words, or carried by its previous answers; nothing sizes the share committed by the report date | neither (the one-fifth is the judge's own) |
| Stage B, run 3, memory capacity added in 2027, first answer | wafer capacity | no: one unfiled statement speaks of demand for DRAM wafers, not of capacity added | neither |
| Stage B, run 3, supply commitments, third answer | purchase commitments | no | neither (the scaling by revenue is the judge's own) |
| Stage B, run 1, Kyber shipping, fifth answer | an event | no: six unfiled-here statements repeat a report the request already holds from other outlets | neither |

The relevance of Broadcom's figure to the custom-chip question is the frozen judgement reference's own (D354, known defect 4:
"the gold's basis for custom-chip spending"). The relevance of total-revenue guidance to data-center revenue rests on one
statement in that question's request ("roughly 92.5% of total revenue"); no reference exists for the fresh week.

## What it adds up to

- The census's kinds (`unsupported/UNSUPPORTED-CENSUS.md`) now divide by cause: answers given when **no figure exists yet** in the
  news (credit support before the first disclosed amount; memory capacity; the judge's own fractions), and answers given when
  **a figure exists in the system and was not delivered to the question** (2 of 6 distinct matters; 3 of 10 answers).
- The second cause is the delivery relation of PRD 10 §2, seen in both systems: in the old one the figure sat under a sibling
  question; in the new one it was kept with no question (the open defect D506/D508).
- **The stored runs already hold the before and after for one of the two:** the custom-chip question answered the lowest band
  without Broadcom's figure (settled unsupported) and a higher band the next day with it (settled supported, after a split).
  One question, two runs sharing the same statements; a pair of consecutive answers is not a controlled test (other statements
  arrived that day too).

## What this result may and may not be said to show

- Shown: for ten settled unsupported answers, by pattern search then reading, which had a sizing figure in the store and absent
  from the request; three did, by filing.
- Not shown: that delivering the figure would make any answer supported (one natural before-and-after, not a controlled one);
  a rate (ten answers, six matters, repeated days and shared statements among them); which rule produced each filing; that a
  search by pattern found every candidate (a figure worded outside the patterns is missed); the 26 answers settled as "too
  little to prefer a band" (not searched).
