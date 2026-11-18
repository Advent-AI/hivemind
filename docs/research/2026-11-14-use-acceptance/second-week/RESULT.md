# One more week through the new system, read for its answer choices: result (D550 to D553; under D439), 2026-11-15

**Label: continued, answer-choice diagnostic only.** The run stalled once and was continued as a second part; only the topics
and the answer choices were run; the matching and the judge were not. It passes no gate and reverses nothing (design, section
6). One week, one run.

## The answer

**Not clean, on both counts of topics and whichever way the open points are counted.** The step that writes answer choices
declined 9 of 39 attempts on 4 of the week's 13 topics, two of them in all three attempts, and three of the registered
zero-fault lines are missed on faults both reader families agree on. The fresh week's picture (no refusal in 21 attempts) did
not repeat.

One concrete picture: an article says the five largest cloud companies plan to spend about $800 billion in 2026 and about
$1.3 trillion in 2027. The first step opened one topic for both years. The answer-choice step declined it three times out of
three ("two yearly figures, neither named as the main one"), so in this diagnostic no answer-choice question was written for the cloud
companies' spending. The fresh week, where the first step had opened the same matter for one year, got its question in all
three attempts.

## 1. What was run

| | |
|---|---|
| News | 2026-10-06 to 10-12, 272 articles, in order (`manifest-2026-10-06-10-12.json`) |
| First part | launched 05:24 EST; 120 articles complete when the laptop slept at about 06:24 with a call in flight; the call could not recover (the first step gave each call the run's whole remaining time as its wait); frozen at Alex's word, then ended through the launcher's own handler (`RUN-STALL-2026-11-15.md`, D551) |
| Change between the parts | each call now waits at most 600 seconds on a silent connection (D552; `clean-arch/step1/live.py`); no request or answer is changed by it |
| Second part | the remaining 152 articles from the library after article 120, the cut call sent again (a new sample), limits reduced to what the first part left (177 calls, 25,200 seconds); 8 attempts lost on a poor network and to a second sleep, each sent again; the bound worked: the run went on by itself after waking |
| Merge | `continuation.py merge`: 272 articles, each complete and in order, the library carried unbroken; proved beforehand on the stored fresh week (`split_proof.py`, 20 of 20, three mutants) |
| After the first step | the topics and the answer choices only, through the unchanged runner, three attempts a topic; the matching and the judge recorded as not run (D553; proofs `choices_only_entry_proof.py`, `choices_full_control.py`) |
| Ledger | first part $1.1305 charged and $0.1199 in flight counted in full; second ledger $2.4203 of its $2.6996 ($2.3817 the second part, $0.0386 the answer choices): **$3.6707 of D550's $3.95**. Of it $1.11 is lost or cut attempts charged at their whole reservations; what the provider bills for those is unknown |
| Readings | two reader families apart (2 sessions each), then a third reader of each family on the 43 marks and 5 named faults they differed on (3 packets, so 3 sessions each: six third-reader sessions against the two the design planned, inside its bound on tokens; the Claude-family sessions used 0.11 to 0.20 million tokens each). Claude's own marks on all 39 attempts were stored before any reader's answer was opened (`own-marks-before-the-readers.json`) |

## 2. The topics the week opened

13 topics (`topics-opening-articles.json`; the opening article's id taken from the trace row that opened the topic). One was
opened by an article seen before (left out of both counts); two by articles on the review pages of the offline source-page work
(left out of the strict count). **Wider count 12 topics, strict count 10.** Both are above the 6 the rule needs.

| Topic | What it asks | Opening article | Three attempts |
|---|---|---|---|
| 1 | the maximum of Nvidia's guarantee on the SB Energy and OpenAI affiliate leases at the next annual report | counted | answers ×3 |
| 2 | Nvidia's supply and capacity commitments at the next annual report | counted | answers ×3 |
| 3 | the change in memory contract prices over 2027 | counted | answers ×3 |
| 4 | the five cloud companies' capital spending in 2026 and 2027 | counted | **declined ×3** |
| 5 | whether the Hugging Face acquisition closes by mid-2027 | strict count leaves it out | answers ×3 |
| 6 | whether the U.S. licence still bars Nvidia's chips from China at the fiscal year-end | counted | answers ×3 |
| 7 | whether the Rubin chip reaches volume by late January 2027 | counted | answers ×3 |
| 8 | Nvidia's loss-share exposure on customer financing at the next annual report | counted | answers ×3 |
| 9 | whether the Groq 3 LPX system ships in volume in the current quarter | strict count leaves it out | answers ×3 |
| 10 | the hourly rental price of a B200 chip at the end of 2026 | counted | answers ×2 (under two different themes), **declined ×1** |
| 11 | whether Nvidia signs and completes an acquisition of Reflection AI | seen before: left out | answers ×3 |
| 12 | global AI capital spending in 2026 and 2027 | counted | **declined ×3** |
| 13 | how much of Nvidia's $25 billion of equity-investment commitments remains at the next annual report | counted | answers ×1, **declined ×2** |

## 3. The registered rule (design, section 5), on the new week alone

Both families' rows are complete and valid (39 of 39 each); they differ on 43 of 244 marks. The two third readers differ on 41
of the 48 points put to them, so every line is given twice: with each open point counted for the answer, and against it
(`proofs/reading-report.txt`, `proofs/second-week-account.json`).

| Line | Wider count, 12 topics | Strict count, 10 topics |
|---|---|---|
| 1. No question other than the topic's | **missed** either way (3 attempts agreed; 5 with the open points) | **missed** either way (3; 5) |
| 2. No part left unlisted | **missed** either way (3 attempts, all agreed) | **missed** either way (3) |
| 3. No outcome with no range or two | met either way | met either way |
| 4. No unjustified refusal | **missed** either way (2 refusals agreed; 4 with the open points) | **missed** either way (2; 4) |
| 5, scaled. Right in two of three attempts; by written choices | **missed**: 9 right of 12 (needs 10), 6 by written choices (needs 8); with the open points against, 3 and 1 | **missed**: 7 of 10 (needs 8), 4 (needs 7); against, 3 and 1 |
| Same favourable end, company figures (by code) | 3 of 3 | 3 of 3 |
| Same due day across attempts (by code; nine in ten needed) | **missed**: 7 of 8 topics with three written answers | **missed**: 5 of 6 |

The two counts fall on the same side, and no line the third readers left open would change the verdict: the three missed
zero-fault lines are missed with every open point counted for the answer.

**The fresh week beside it** (2026-09-22 to 09-28, 7 topics, its existing marks by Claude and one Codex reader, no third
readers; D545 to D547): no refusal in 21 attempts; line 2 failed on six attempts of three questions in both readings (after
D547's recount two of the six stand, on one question); right in two of three attempts on 4 of 7 topics by Claude's marks and 1
of 7 by Codex's, the gap being the due-day reading below. Pooled, as description only: 20 topics, 60 attempts, 9 refusals.

## 4. The faults both families agree on

| Line | Topic, attempts | What is wrong, in the reader's words |
|---|---|---|
| 1 | topic 1, attempts 1 and 3 | "What maximum potential guarantee liability does Nvidia disclose in its FY2027 annual report" names no guarantee: it can be read as the total of all Nvidia's guarantees, another figure than the one the topic asks about. The second attempt names the leases and holds |
| 1 | topic 7, attempt 1 | it asks whether the chip reaches volume "during the fiscal quarter ending in late January 2027", where the topic's quarter is the one the article calls "this quarter" (ending late October 2026) |
| 2 | topic 1, attempts 2 and 3; topic 3, attempt 2 | further figures the topic's `outcome` names (amounts paid or accrued and the remaining term; the memory makers' selling prices and margins) are left out of the question and not listed. Other attempts on the same topics list them |
| 4 | topic 13, attempt 2 | declined for "several figures, none the main one", where the remaining balance is plainly the main one: the first the outcome names, and the amount the topic was opened on. The first attempt wrote sound choices for it |
| 4 | topic 4, attempt 3 | the case it names (a figure for two years together, with no publication day) does not apply: the topic names two yearly figures. Its other two attempts declined for the case that does apply |
| a named fault, upheld by both third readers | topic 3, all three attempts | "HBM/DRAM contract prices" are two separately priced products and "over calendar 2027" gives no start and end readings: no single percentage is settled. The vagueness is the topic's own wording, carried into the question |

Claude's own marks, stored beforehand, found the same faults on topics 1, 3 and 13 and on the due day of topic 7; they held the
question of topic 7's first attempt and the refusal of topic 4's third, where both families fail them
(`own-marks-before-the-readers.json`: 29 of 39 attempts with no fault).

## 5. The refusals, read and traced

| Topic | Declined | The step's reason | Ruling | Trace |
|---|---|---|---|---|
| 4, cloud companies' spending in 2026 and 2027 | 3 of 3 | two yearly figures, neither the main one | justified in two attempts by both families; the third names a case that does not apply | the first step wrote one topic for two years; its `outcome` names both figures |
| 12, global AI spending in 2026 and 2027 | 3 of 3 | the same | justified, both families | the same shape; also a figure only one bank's forecast settles |
| 13, equity-investment commitments | 2 of 3 | the outcome names several figures (the balance, the cash paid, the change) with no main one | one unjustified by both third readers; the other open between them | the same request gave sound choices once and a refusal twice |
| 10, rental price of a chip | 1 of 3 | no listed theme covers a rental-market price | open between the third readers | the other two attempts put the same figure under "AI capital spending" and under "Semiconductor cycle"; the readers split on which, if either, covers it. July's class (the H100 rental price), repeated |

**The same reasons over every stored run** (60 topics: July's three runs, the fresh week, this week; 180 attempts, 37 refusals):
"several figures, none the main one" 22 attempts on 9 topics; a period that is not one year, 8 attempts (July only); "no
listed theme covers it" or the rental price in other words, 7 attempts. Within the first class: a topic whose own question
asks two things (two years, or "how much A, and how much B") was declined three times out of three, on 6 topics; a topic
whose question asks one thing while its `outcome` lists several was declined in 1 or 2 attempts of 3, on 3 topics.

**What the decisions already say about this class.** Declining a topic with no main part is Alex's own rule (D397, "只判主要那件":
a thesis with no main part gets no judged question), taken with its cost stated: such topics get no answer "until splitting
is built", recorded then as an open defect to be sized. He also ruled that a second side of one bet stays in the same topic
(D436) and that periods of one bet are one question (D248). So these refusals are the step doing what was decided; what this
week adds is the size of the defect on news outside the tuned days (2 of 13 topics with no question at all, both worth one in
a reader's eyes, and a third decided by chance) and where it starts: the first step's field for what a topic tracks, which
its schema describes in one line ("the outcome or event being tracked") and which it fills with two years or a list.

## 6. Where the two reader families part, and what that does to the numbers

- **The due day, 23 of the 41 open points, of three kinds.** Ten are a company's annual figure due on 2027-04-01 (topics 1,
  2, 8 and 13): one family reads "the next annual report, around February", the other holds the day. For these the day is not
  the model's: code sets it, 60 days after the fiscal year-end, by Alex's decision (D414), and the reading form says that day
  is right, while the note the step and the readers are given says "published around 2027-02; use that day". Eleven are an
  event's day (topics 5, 7, 9 and 11): the end of a month the topic gives approximately, or the closing window of a signed
  deal against "its next annual filing"; D414 does not settle these. Two are the rental price at a year's end (topic 10),
  where the question is whether a day's price is a year's figure. The split is the same as in the fresh week; it is why "right
  in two of three" falls to 3 topics when the open points are counted against the answer. The marks stand as given; nothing
  here re-reads them.
- **Whether a rental price belongs to a listed theme** (topic 10: object, year and refusal all open).
- **Whether an expectation about another quantity is the reference** (topics 3 and 7: Micron's fiscal-year price guidance for
  a calendar-year contract price; a revenue share this quarter for a ramp by January).
- **Whether "sign and complete" is one event** (topic 11, left out of the counts).

None of these changes the verdict: section 4's faults stand without them.

## 7. What a reader of the product would notice, beyond the lines

- No answer-choice question was written for the cloud companies' spending or for total AI spending. That both are worth a
  question is a reader's judgement (Claude's), not a measured result: the matching and the judge were not run.
- Topic 8 and topic 10 ask for an amount the article gives no figure for; the ranges are the step's guess and differ between
  attempts (a middle range of $5 to 10 billion in two attempts and $1 to 5 billion in the third; $8 to 12 an hour against $4
  to 6). This is the fault D546 recorded: the six lines do not see it.
- Topic 7's due day differs between attempts (February 28, February 24, February 28).
- The week has no library and no judgements: nothing here says how these questions would be answered.

## 8. What this is evidence of, and what it is not (design, section 6)

- **It is evidence that** on a second week outside the tuned days the frozen step shows the faults July showed: refusals of
  topics a reader wants answered, a question that drops a name, parts left unlisted. With the fresh week, two weeks give
  opposite pictures of refusals (0 of 21 attempts; 9 of 39). For the two spending topics the shape the first step gave them
  (two years in one topic) explains the refusal under the present rule; it does not explain the other three refusals (the
  commitments topic decided by chance, the rental price's theme).
- **A left-out part, agreed by both families, on two more questions** (topics 1 and 3): under the design this is a lead. The
  earlier audit (D547) found a place in the request that could produce it (the instruction says to list every other part of
  "the topic's wording" and never says whether the `outcome` field is part of that wording); it did not show that this caused
  each omission, and these new ones have not yet been traced against their requests. This week 27 of the 30 written answers list at
  least one such part; the three that list none are the three agreed faults of line 2.
- **A topic declined:** a lead. Section 5 counts the reasons the step gave; the earlier boundary check of this class (D469,
  D470: a candidate that takes the first-named figure as the main one was rejected as wider than Alex's rule, and a blind
  reader found it risked joining separately tracked things) stands, and this result does not reopen it.
- **It is not** a measurement of a rate (two weeks, 20 topics, not independent draws), not a pass or a fail of Stage A (Alex's
  lines are on 44 topics), and not a reason by itself to reverse the direction (D544) or to reopen a stopped line.
- **Limits:** continued after a stall, one call sent twice, a changed wait and reduced limits between the parts; one run;
  7 of the ten strict-count topics were opened in the week's first two days; the exposure search works by article id; the reading's
  third readers disagree on most of what was put to them, which is a finding about the form as much as about the answers.
