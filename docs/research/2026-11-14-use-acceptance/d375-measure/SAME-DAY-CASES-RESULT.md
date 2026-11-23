# Eligible cases for measuring D375: what later articles of a day could have given a question opened that day (D528, under D439), 2026-11-15, $0

Scripts: `same_day_candidates.py` (the pool, four stored runs), `build_same_day_packets.py`, `tally_same_day.py`; `brief-same-day.md`.
Readers: two families, each packet read once by a fresh Codex session and once by a Claude subagent, given only the brief and
the packet; the key stayed outside the repository. The run read: the old system's fresh-week draw. Nothing was sent to the
pipeline's models and nothing changed.

## The answer

**In the fresh week, both reader families mark 37 statement-and-question pairs where a later article of the same day held a
statement that bears on a question opened earlier that day and did not reach it that day; 14 of the 37 had been dropped for want
of a question.** Traced into the actual last judging request of each question (section "The trace into the final requests"): for
most of them a statement of the same fact was in the final request, having arrived one to four days later from another article;
**for one question it was not: the data-center revenue question never received the company's guidance for the next quarter, nor
any market estimate of the year's revenue, in any of its requests.** Whether a per-article list (D375) would have filed any of
these is untested: the stored default omitted them on the first day; what the reading step does on a longer list is not known.

## What was read

For each of the 14 questions opened before the last article of its day: every statement the later articles of that day produced
(728 statement-and-question items in 20 packets): 412 kept under other questions, 301 dropped for want of a question, and, mixed
in unmarked, the 15 the system itself filed under the question that day.

| Kind | Items | Marked as bearing by Codex | by Claude | by both |
|---|---|---|---|---|
| The system filed it under the question that day (known cases) | 15 | 13 | 13 | 12 |
| Kept under other questions | 412 | 31 | 29 | 23 |
| Dropped for want of a question | 301 | 20 | 15 | 14 |

- The readers mark 12 of the 15 known cases: the reading finds most of what the system itself files, not all.
- Of the 23 kept elsewhere, 17 belong to the two RTX questions (the duplicate pair of `duplicates/DUPLICATES-RESULT.md`: each
  holds statements the other lacks). The other six: the quarter's revenue under the data-center question and not the total; the
  70% outlook for fiscal 2028 under the growth question and not the amount; three statements on the cloud companies' spending
  filed under one of two spending questions; one other.
- The 14 dropped items are 9 distinct statements, read by me:

| Day | Question (opened at) | The dropped statement of a later article | A like statement first reached the question (keyword lead) |
|---|---|---|---|
| 09-22 | fiscal 2027 revenue, `v2` (article 11) | article 22: second-quarter revenue of $96.2 billion | article 35, the next day |
| | | article 22: third-quarter guidance of about $108 billion | article 35, the next day |
| | | article 16: market estimates of about 90% growth in fiscal 2027 (also marked for `v3`, `v4`) | article 91, two days later |
| | | article 15: an outlet's estimate of more than 80% growth over the past year | none found (see the trace below) |
| | data-center revenue, `v4` (article 13) | article 22: the same quarter's figures and guidance | data-center revenue of $89 billion was already under it from article 13 |
| | fiscal 2028 revenue, `v3` (article 11) | article 22: the chief executive, chip sales could double in 2027 | article 73, two days later |
| | financing commitments, `v1` (article 4) | two statements | like statements under it from the first day |
| 09-24 | Vera Rubin shipping, `v9` (article 78) | articles 92 and 98: production shipments of Vera Rubin have begun | article 120, the next day |

On its first day the fiscal 2027 revenue question was judged on one statement; the quarter's revenue and the next quarter's
guidance, read ten articles later the same day, were dropped. The Vera Rubin shipping question was judged on its first day
without the two reports that shipments had begun.

## Across the stored runs, by code (candidates only, not read)

Questions opened before the last article of their day: 14 in the fresh week, 11, 13 and 14 in the July runs. Statements of later
same-day articles that reached such a question that day: 15, 11, 8 and 3. Statements kept under other questions: 412, 92, 178,
191. Dropped for want of a question: 301, 108, 156, 182.

## The trace into the final requests (council round 20; $0; read by me in the stored requests)

For the nine distinct dropped statements and the six pairs kept elsewhere outside the RTX pair: the question's last judging
request, every request of the question, and what its judgements cited. The 17 RTX pairs are kept apart (evidence split between
two questions on one matter; `duplicates/DUPLICATES-RESULT.md`).

| Question | The same-day statement that did not reach it | In the question's last request? |
|---|---|---|
| fiscal 2027 revenue (`v2`) | second-quarter revenue of $96.2 billion | yes: `e24` and others, from 09-23; cited |
| | third-quarter guidance of about $108 billion | yes: `e25`, `e30` ("$108 billion, plus or minus 2%"), from 09-23; cited |
| | market estimates of about 90% growth in fiscal 2027 | in substance: a consensus of $406 billion (88% growth) and of about $412 billion |
| | an outlet's "more than 80% over the past year" | no like statement; the request holds the exact reported growth figures |
| fiscal 2028 revenue (`v3`) | the chief executive: chip sales could double in 2027 | yes: `e99`, from 09-24; cited |
| | the 70% outlook for fiscal 2028 (kept under the growth question) | yes: `e132` and others, from 09-23; cited |
| | market estimates of fiscal 2027 growth | in substance: the request holds the fiscal 2027 consensus base |
| financing commitments (`v1`) | guarantees of more than $100 billion; a quarter of fiscal 2028 revenue from financed customers | in substance: the guarantee disclosures; "roughly one-quarter of NVIDIA's business in fiscal 2028" (`e186`, 09-25); the $175 billion figure itself is not there |
| Vera Rubin shipping (`v9`) | production shipments have begun | yes: `e190` (09-25), `e311` (09-27); cited |
| cloud companies' spending 2026 (`v7`) and AI spending 2027 (`v8`) | nearly $800 billion in 2026 and $1.3 trillion in 2027, as Nvidia's estimate | yes: `e270` and others, from 09-23 to 09-26; cited |
| **data-center revenue, fiscal 2027 (`v4`)** | the second quarter's figures | yes: data-center revenue of $89 billion was under it from the first day |
| | a statement that China is largely closed to data-center sales | in substance: "Nvidia's outlook for the year excludes sales from China" and others |
| | **third-quarter guidance of about $108 billion** | **no: not in the last request and in none of the question's seven requests** (checked line by line: no "$108 billion", no third-quarter revenue guidance). Eighteen stored statements name $108 billion (one of them a guarantee cap of $108.5 billion); sixteen are filed under the total-revenue question, none under the data-center question |
| | **market estimates of fiscal 2027 growth** | **no: no consensus or estimate for fiscal 2027 is in any of its seven requests**; its last answer says so: "No full-year FY2027 consensus or annual Data Center guidance is supplied" |

**The positive case.** The data-center revenue question is the one whose final answer both reviewing teams called unsupported
(`side-by-side/SIDE-BY-SIDE-WEEK.md`): about $400 billion, reached by carrying the last quarter's 18% growth into the third
quarter and "allowing" 25% for the fourth. Its own reasons say "The supplied evidence has no full-FY2027 Data Center consensus
or annual company target". The company's guidance for the third quarter and the market's estimate for the year were in the
system all week, under the total-revenue question; one statement in the question's own request puts data-center revenue at
"roughly 92.5% of total revenue" for the latest quarter (`e11`). So this answer rested on the judge's own growth numbers while
figures that may bear on it by one step were never shown to it. They are figures of total revenue: that either is a forecast of
data-center revenue, or that the judge would reach a supported answer on seeing them, is not established (council round 21).

Cautions (the last two from the council's round 21). First, this is not shown to be a same-day matter, and it is not ruled out
either: the first instance was dropped on the day the question opened,
but every stored statement of the guidance was read from the second day on, when the data-center question was on the list, and
none was filed under it.
A per-article list would not by itself have changed those; what a changed reading would have done with the first, dropped
instance, and what an earlier judgement might then have carried forward, is untested. Second, nothing here shows the answer
would differ with the guidance in view. Third, the cause of the filing is not established: "a fact that bears on two questions
is filed under one" describes what happened (PRD 10 §2 names the relation); it does not show which rule or check produced it,
or that the remedy is two homes: the one-home rule (D207, D265, PRD 10) still governs. Fourth, the answer's 25% was already in
the previous answer shown back to the judge.

## What this means for a measurement of D375

- For facts that are widely repeated, the stored week shows a delay of one to four days and a first-day judgement made without
  them; a delayed first answer is a real cost to a reader of a daily product, and it is not what the frozen end-of-window
  measure counts.
- One eligible case for "a fact absent from the final request" was found, on the data-center revenue question; it is not shown
  to be one D375 would recover.
- The 15 statements the system itself filed check the readers' agreement with the system's filings (12 of 15); they are not an
  independent standard.

## What this result may and may not be said to show

- Shown, for one week of one run: 37 pairs both families mark; 9 distinct dropped statements and 6 pairs kept elsewhere traced
  into the final requests; two facts (the next quarter's guidance; the year's market estimate) absent from every request of the
  data-center revenue question.
- Not shown: that D375 would have filed any of them (the reading step's behaviour on a longer list is untested); that any
  judgement would differ; a rate; anything about the July runs (candidates counted, not read).
