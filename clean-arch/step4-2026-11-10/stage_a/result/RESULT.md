# Stage A of the clean ladder step: the result (2026-11-10)

**Every one of Alex's six lines (D400) is missed as the third reader ruled. Three are missed whoever reads (3, 4 and 6); three
depend on which of the two reader families is followed (1, 2 and 5).** Stage A does not compare the step with production
(D400). By D401 the work stops here and goes to Alex.

The step as built (design version 31): the request as first sent (D407), gpt-6-luna at medium effort, the code checks, one
resend. 44 stored theses, three sends each.

- Sent: `poc/data/clean-ladder-stage-a-2026-11-10/run/` (132 sends, 200 calls, $0.1659 from tokens; with the slice $0.1716 of
  the $3 of D401).
- Read on: `poc/data/clean-ladder-stage-a-2026-11-10/run-rechecked-2/`, the stored answers replayed at no cost through check 6
  as corrected after the send (design §5.3, check 6; round log §69). Three sends change against the stored run, all of
  u2/clean-8: refused twice as stored, ladders here. Counted on the stored run those three would be "refused twice"; no line's
  verdict changes with it. The replay shows what the stored answers do under the corrected check; it is not three new sends.
  Its reach: all 141 references of the run, first and second answers, were put through both rules: 75 accepted by both, 6
  newly accepted, 60 refused by both, and none the old rule accepted is refused by the corrected one.
- Generated beside this page: `report.txt` (the lines, the shares, every refusal, every named fault upheld), `tables.txt` (by
  kind of answer and by thesis, and line 5 under each reading), `code-counts.txt` (what code counts across the three sends).
  `own-read-before-rulings.md` is my read of the disputed marks behind lines 1 to 4, written before the rulings.

## Outcomes

| | sends |
|---|---|
| a ladder written | 111 (yes/no 24; five states for the company 17, for a theme 3; a figure for the company 30, for a theme 37) |
| declined by the model | 17 |
| refused twice by code | 4 |

As sent, 68 of the 132 first answers were refused by a check and sent back, 62 of them for a reference that was not the
article's words; 61 second answers passed and 7 sends ended refused twice. Under the corrected check the three first answers
of u2/clean-8 are accepted as they came: 65 sent back, 61 passed, 4 refused twice.

## The lines

Readers: reader 1 is the Codex family, reader 2 the Claude family; the third reader is a fresh Codex session, with the two
sides unnamed and shuffled. The two readers differ on 73 of 908 applicable marks (8%), far below the third at which the
reading would not count.

| line | as ruled | if every differing mark had held | my own read (decides nothing) |
|---|---|---|---|
| 1. no ladder asks another question (Q) | **missed**: 11 of 111 | 0 | 0: I differ from all 11 rulings |
| 2. no ladder leaves a part unlisted (L) | **missed**: 4 | 0 | 2 |
| 3. no outcome with no rung or two (R) | **missed**: 16 | **missed**: 7, failed by both readers | 12 |
| 4. no refusal without a justified reason (N) | **missed**: 2 of 17 | **missed**: 1, failed by both readers (see the note) | 1 |
| 5. 35 of 44 theses right in two of three sends, 28 by a ladder | **missed**: 21 right, 16 by a ladder | met: 36 and 30 | not read |
| 6. favourable end the same in three sends, every company figure | **missed**: differs in 2 of 8 theses | by code | by code |
| 6. due day the same in three sends, nine theses in ten | **missed**: 21 of 32 | by code | by code |

Note on line 4: the one refusal both readers fail is of a thesis whose outcome joins two things with "and" ("Global HBM
shipment growth and whether HBM supply remains short of demand"). Both readers take the first for the main thing; the thesis
does not say so (council `iu`). The miss stands as counted, and the thesis's wording is part of its cause.

The third reader ruled with reader 1 on 54 of the 73 differing marks and with reader 2 on 19; it upheld 13 of the 20 faults
named under `W`. Reader 1 holds every firm mark on 47 of the 111 ladders, reader 2 on 84; as ruled 49 are sound, and 86 if
every differing mark had held. The two families read the form at different strictness, as every practice reading showed, and
the third reader is of the stricter family: I chose it because I wrote the step and am of the other.

**The reference reading beside it, a lead and not a comparison (D400):** of the 36 ladders production wrote for other
questions, two readers held every firm mark on 19 and on 25, unadjudicated (`readings_summary.md`).

## What both families agree is wrong (25 of 111 ladders, 1 of 17 refusals)

| kind of answer | ladders | with a fault both readers mark | the marks |
|---|---|---|---|
| five states, for the company | 17 | 10 | direction or the Neutral state 7, the object 5, a gap or an overlap 5 |
| five states, for a theme | 3 | 1 | a gap or an overlap 1 |
| yes/no | 24 | 2 | a gap 1, the object 1 |
| a figure, for the company | 30 | 7 | a quarter's figure or the wrong year and unit 4, the reference 3, the object 1 |
| a figure, for a theme | 37 | 5 | the object 2, the reference 2, the due day 1 |

## The classes, by mechanism

1. **Five states for an event are where the step is weakest.** 15 of 17 company five-state ladders are unsound as ruled, 10
   by both readers. The states leave a case out or let two hold (a prohibition in force while a review is pending; "broad"
   against "narrower" with no line), the labels run against the business (an investigation that lapses with no fine labelled
   Strongly bearish), the Neutral state names no baseline, and a regulator's decision is filed under the company in one send
   and under the theme in the next. Seven theses change shape between sends (yes/no in one, five states in another).
2. **A yes/no whose Yes needs a confirmation and whose No does not** (3 as ruled, 1 by both): shipped and not yet confirmed
   fits neither rung.
3. **The reference** (16 as ruled, 5 by both). Two things: an amount already reported is carried as what the market expects
   (the $119 billion of supply commitments, 8 sends of 3 theses; the thesis itself says "compared with the $119 billion cited in
   this item"); and an expectation the article states as a range ("approximately 50%-60%") has no place in a field that holds
   one number, so the judge is told there was no reference figure (2 sends, a fault upheld on both).
4. **A figure's due day is the model's estimate of a publication day** and differs between sends in 11 of 19 theses whose three
   sends are figures (24 February, 28 February, 31 March). The 13 theses whose three sends are events all keep their day
   (D403's rule).
5. **Direction** differs between sends for two theses, both a commitment's amount (supplier commitments; commitments for future
   investments): "more secures supply" in one send, "less keeps flexibility" in the next. This is the reference's direction
   problem, unchanged.
6. **A company's figure for a quarter written as a ladder** (2 sends of one thesis; its other send declined it, rightly), and
   an industry quantity filed under the company with its fiscal year (2 sends of one thesis). Production's quarterly pattern,
   which the design left to the readers, matches exactly the two.
7. **A group named and not listed** ("the big four AI hyperscalers", 8 of the 11 Q failures as ruled). The form asks that a
   question lean on no name it does not give. Reader 1 and the third reader read a group name as names not given; reader 2 and
   I read it as a name given, the thesis's own. This class is a difference in reading the form, and it is Alex's to rule.
8. **The same thesis declined in one send and laddered in another** (5 theses), and two refusals not justified (one by both
   readers: a thesis whose main figure is plain was declined as having none).

## Where I differ from the rulings (lines 1 to 4)

- Q: all 11. Eight are class 7. The three others: "versus the prior period" is the thesis's own wording; "by December 31,
  2028" for a system delayed to 2028; revenue above zero from the sales as the measure of the sales.
- L: two of four. A comparison with the reference in the middle rung is not a part left out; "or slips to 2028" is the No of
  the same question.
- R: four of nine. The cases named (a fine with no concluding decision; a conclusion that neither finds nor clears) are not
  ones an analyst would meet.
- N: one of one. Chinese firms' split of their budgets between domestic chips and Nvidia is no listed theme's figure.

On my read line 1 would be met and lines 2, 3 and 4 missed, with fewer answers behind each.

## What the checks did

- The check on pointing at the item refused nine answers, each a true instance. One wording passed it ("at the item date").
- Check 6 refused the article's own words where a footnote marker stood before the full stop; corrected after the send (design
  §5.3). The marker set aside is one thing more than D405's record names: for Alex.
- Four sends ended refused twice: a reference figure outside the middle range twice (1), a quote reworded twice (1), a
  reworded quote and then "in the item" (2).

## The council on this result (`council/iu-*`, `iv-*`; round log §69)

An independent Codex read of the raw material, then a challenge of my reading. Agreed: the acceptance failed; lines 3 and 6
do not depend on the reader, lines 1, 2 and 5 do; the answers to events are the largest class; nothing is designed or sent
before Alex decides. It asks that Alex rule the boundary cases the two families read differently before any second reading,
and that the third reader become two, one of each family. It challenged my lean to ask every event as yes/no: cleaner in each
of the five theses the run wrote both ways, and in two of them it drops what an analyst holds the card for. Of the seven gaps
both readers found, six sit in the division of an event beyond three outcomes and one in a Yes that needs a confirmation its
No does not.

