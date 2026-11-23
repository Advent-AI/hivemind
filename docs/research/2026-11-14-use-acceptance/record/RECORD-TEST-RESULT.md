# The kept figures as a company record: result of the $0 test (D493), 2026-11-14

**Answer: not ready: the usability line is missed, and parts of the rest are unsettled (council mx round 3).** From the record alone a blind reader answered five of the six questions as a second reader
did from the articles, and the stored measures and values are right in all 40 sampled rows. The usability line is missed because the
record made its reader say one wrong thing: that the CFO stated the last quarter's 75% gross margin. The record stores who said it and
when once per statement, and a statement can hold several figures; here it held the CFO's two outlook figures and the reported 75%, so
the 75% carries her name. The defects are few and structural; they are listed below as what would have to be fixed first.

Material: the clean week draw's kept statements with figures (`record-week.json`: 341 figure rows from 179 statements of 74 articles; 186
name revenue, sales or gross margin, 155 do not); the reader's view built by code from the 40 sampled articles (`record-view.md`).
Readers: Codex (read-only) and Claude subagents, blind; keys outside the repository; $0. Tally: `tally-record.txt`.

## Usability: six questions, the record reader against a reference written from the same 40 articles

| question | result | detail |
|---|---|---|
| Q1 fiscal 2028 growth: guide, earlier expectation, latest estimate | the same | 70% guided, 45% expected before; the latest estimate is in neither the record nor the articles (part not exercised) |
| Q2 fiscal 2027 revenue estimates | the same | $406.05 billion (Zacks) and about $412 billion; the record reader also gave the "about 90%" growth expectation the reference left out |
| Q3 fiscal Q3 revenue: guide and estimate | the same | $108 billion ± 2% against $109.0 billion |
| Q4 gross margin: last quarter, rest of the year, fiscal 2028 | **a wrong statement** | figures and periods the same (75%; 71%–72% in the fourth quarter, Bloomberg's "under 72%"; 72%–73% in fiscal 2028); but the reader, following the record, attributes the 75% to the CFO, which no article says (both comparers) |
| Q5 last quarter: total and data-center revenue | the same | $96.2 billion, up 106%; $89 billion, up 117% |
| Q6 one measure and period, different values | the same | $406.05 billion against about $412 billion |

Six exercised; five the same on the required parts as tallied; one with a wrong statement. **Line (at least five exercised, at most one not the same, nothing wrong): not
met, on the wrong statement.** One comparer marked Q2 as not agreeing only because the reference was the shorter answer. Limits of the comparison (council): the
comparers were not shown the questions' wording, so "neither has Q1's third part" rests on the two answers; Q6 asks for each pair, and
the two readers listed different sets beyond the shared one (the reference added acquisition prices, outside the view; the record reader
added pairs the reference left out), so Q6's completeness is not settled. Neither changes the verdict.

What the record reader said of using it: "Usable but slow": one measure and period under many spellings (the quarter's revenue under seven
headings), periods that are relative or missing ("last quarter", "fourth quarter" with no year), the 45% earlier expectation held only in
a basis note, and no line for what drives the margin (the memory cost is in other statements, not in the figures).

## Fidelity: 20 rows of each stratum, each read against its article (not a rate for the whole record)

| | revenue and margin rows (R, 186) | other rows (O, 155) |
|---|---|---|
| measure, value | right in 20 of 20 | right in 20 of 20 |
| period | none wrong | none wrong |
| rows wrong | **0** (line: at most 1) — met | **1** by both families: an earnings base "today" stored as an estimate (line: at most 2) — **undecided**: with the two rows below counted wrong it is 3 |
| still differing | none after a fresh pair of readers (three "missing" marks became "the article does not say") | 2 rows: "Consensus analysts" where the article says "Analysts" (the Codex readers call it wrong, the Claude readers right, twice each); counted wrong they would make 3 and miss the line |
| a rejection that was the packet's fault | | 1 row: "Yahoo Finance" as the party of the outlet's own projection; the readers called it wrong because the name is not in the article text, but the request showed the model the item's publisher (finance.yahoo.com) and the readers' packet did not |
| date | stored for 71 of 341 rows; in the sample the article gives no date for 23 to 25 of 40, and gives one the row lacks for 4 to 6 | |

## The defects, counted

1. **Who and when are stored once per statement, not per figure.** 93 of the 179 statements hold several figures; 15 hold figures of more
   than one kind (50 rows). Of 201 rows of kind "actual", 9 carry a party other than the company's name (a named executive, an outlet).
   The Q4 error is one of these (clean Step 1, step 121, statement ev-5).
2. **Measure and period are free text.** The view's 44 rows fall under 42 headings; code that changes only case, spacing and the written
   fiscal year merges none. 52 of 341 rows have no period.
3. **A figure's reason is elsewhere.** What drives a change sits in other kept statements, which the record of figures does not carry.
4. **Mine:** the readers' packet left out the item's publisher, which the model had; one "wrong" mark came from that.

## What it shows and does not

- Shown, on this week's stored data: the kept figures are faithful in measure, value and period, and hold what a reader needs to answer
  the six questions; attribution is the weak field and grouping is absent.
- Not shown: complete extraction, a record ready for a product, any effect on a judgement, or that questions on these numbers are not
  needed.

## The census the council asked for (Claude's own reading of the stored rows against their passages; $0; not blind)

- **Attribution, the 15 statements that hold figures of more than one kind (50 rows):** in 5 of them at least one figure is not the
  statement's party's, at least 6 rows (the council found a seventh, a percentage the article calls the author's own calculation, and
  doubts one of the six; the count is a floor from one reading, not a complete census): a market estimate filed under the company's or the CFO's name (the 45% consensus beside the 70%
  guide; the $92.37 billion and $2.09 consensus beside the reported quarter), an author's own estimate under the company's name, and a
  person's name carried to a neighbouring figure (the 75% under the CFO; the 70% guide under the CEO). In the other 10 every figure is
  the company's and the party is right. The stored measure often names the true party in words ("Consensus revenue estimate"), so a
  display that says "statement by" and shows the passage would let a careful reader see it; the stored party of those rows stays wrong
  and code cannot correct it. The pairs it hits are the ones a reader most wants: the company's number beside the market's.
- **Period, the 186 revenue and margin rows:** most write a fiscal quarter or year in one of a few forms a general parser could bring
  together; about 31 are relative ("last quarter", "next fiscal year", "current quarter") and 11 have none, and those cannot be grouped
  without inventing a year. The measure is written in 66 spellings.
- **What it means:** a display rule can make the record honest about what it does not know; a faithful, groupable record needs each
  figure to carry its own party and a period in a fixed form where the record is written, which is the Step 1 schema: a new version of
  a frozen piece, Alex's to open.

