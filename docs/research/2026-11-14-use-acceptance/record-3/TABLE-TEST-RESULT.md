# A financial table built by code from what the adopted request keeps: result (D501), 2026-11-15

Design: `TABLE-TEST-DESIGN.md` (version 2, frozen before any reader). Tallies: `tally-table.txt` (`tally-table-first.txt` before the fresh
pair). The table: `financial-table.md` (its trace `table-rows.json`), built by `build_table.py` from the adopted request's stored answers
on the forty unread articles of D499. Nothing was sent to a model; no request, prompt or package code changed. Cost: $0.

## The verdict, by the checks written before any reader

| Check | Result |
|---|---|
| 1. No wrong join | **met**: no wrong join was found in the ten joined lines (both reader families); every row is in exactly one line |
| 2. Not less right | **met**: all four table readers meet the written answer line (the eight parts supported, no part marked wrong after the fresh pair) |
| 3. Coverage and effort (reported, not scored) | about the same answers found; **no reliable saving of effort is shown** |

By the design's rule the table is worth putting before Alex as a tested mock: a way to find the kept figures, with the limits of
their stored sources and periods. This is a result on ten joined lines (25 rows) and four table readers, not proof that every join or
answer is safe; it did not make the readers measurably faster or more complete. A lead, not a rate.

## 1. No wrong join

- Ten lines hold more than one row (25 rows). Both families marked all ten `same` (one measure, period, value and source).
- The stored period of each member against its article: no member unsupported. Three of the 25 are a fiscal year the article only
  implies for both families (article 22's two "fiscal Q1" figures, stored as "Fiscal Q1 2027"; article 15's "fiscal third-quarter"
  guide, stored as "Q3 fiscal 2027"), four more for Codex alone. They are the reading request's stored labels, which the table shows
  as stored; the join added no error to them.
- 63 of 114 rows sit under a fixed period key; 51 stay under the period as stored (among them "current quarter", "this year",
  "q3 2026", "recent quarter", and 15 with no period).

## 2. Not less right (eight answer sets, one answer key, two comparers, a fresh pair on the one disputed part)

| Part | Table: Codex 1 | Table: Codex 2 | Table: Claude 1 | Table: Claude 2 | Record: Codex (D500) | Record: Claude (D500) | Record: Codex (fresh) | Record: Claude (fresh) |
|---|---|---|---|---|---|---|---|---|
| Q1a, Q3a, Q3b, Q4a, Q4b, Q4c, Q5a, Q5b | all supported | all supported | all supported | all supported | all supported | all supported | all supported | all supported |
| Q1b (not in the articles) | none | none | none | none | none | none | none | none |
| Q2a (the fiscal-year estimate) | supported | supported | supported | supported | supported | supported | supported | supported |
| Q6a key pairs found (K1, K2, K3) | K1 | K1 | K1, K2 | K1, K2, K3 | K1 | K1, K2 | none | K1, K2 |
| Q6a misstatement | no | no | no | no | no | no | no | no |

With the answer key fixed before the readers, the two comparers gave the same mark on ten of eleven parts for all eight sets. On Q6
they agreed on every pair found and differed on one thing: the Codex comparer called the two Claude table readers' use of the "+91.2%"
line a misstatement and the Claude comparer did not. The fresh pair marked all eight sets again and both found no misstatement in any.
The disagreement stays on record: those two answers set the figure under a fiscal third-quarter heading while giving its stored
period ("Q3 2026"); giving the stored wording does not establish that the two periods are the same, and "no part marked wrong under
this key" is not a claim that no reader made a period error.

## 3. Coverage and effort

- **Coverage.** Q2: all eight supported. Q6 key pairs: the table readers found 1, 1, 2 and 3; the record readers 1, 2, 0 and 2. The
  one reader who set the 100% beside the 106% (K3) read the table; the one who found no pair read the record. A difference of this
  size between single readers is not a difference between layouts.
- **Layout, by code.** The reported revenue: 13 lines under 11 headings in the record, 10 lines in 6 blocks in the table; the
  third-quarter guide 6 under 5, now 5 in 2; the fiscal 2028 growth guide 13 under 7, now 9 in 4. The table file is larger (26.3 kB
  against 22.4 kB): each line carries its stored source, period and basis.
- **Effort, as each session's harness reports it.**

  | Reader | Layout | Tokens | Seconds |
  |---|---|---|---|
  | Claude 1 | table | 97,896 | 289 |
  | Claude 2 | table | 94,806 | 209 |
  | Claude (D500) | record | 93,718 | 157 |
  | Claude (fresh) | record | 94,670 | 183 |
  | Codex 1 | table | 73,324 in | 183 |
  | Codex 2 | table | 75,017 in | 129 |
  | Codex (D500) | record | 72,460 in | not timed |
  | Codex (fresh) | record | 72,441 in | 141 |

  The sessions do not separate the layouts: the table sessions used slightly more tokens; in time, the Claude table sessions were
  slower than the Claude record sessions and one Codex table session was faster than the timed Codex record session. Tokens and
  seconds of a model session are too small and uneven a sample to measure a person's effort. **No reliable saving is shown.**
- **The readers' own notes.** The record readers' main complaint ("one fact repeats under many differently worded headings ... each
  answer needs a full scan") is absent from the table readers' notes ("Company actuals and guidance were easy"; "Sections by whose
  figure help"). What all four table readers still name: market estimates under relative or loose periods ("current quarter",
  "2026", "Q3 2026"), which took inference from the article dates, and the same figure repeated at different rounding. Both are things
  the code leaves alone by rule: which quarter a relative wording means is not established by the stored text, and whether
  $96.2 billion and $96.22 billion are one fact is a judgement.

## What this result may and may not be said to show

- Shown, on forty screened articles, one stored draw and two readers a family: a code-only table of the kept figures joins nothing
  wrongly, loses no answer, and puts the company's reported figures and its outlook where readers find them easily.
- Not shown: that the table saves a reader work; that the kept figures are complete; that a table gives a reader what a tracked
  question with a judgement gives; anything about a forward week.
- Nothing is adopted or shown in the product by this test. `build_table.py` is research code beside the test, not package code.

## Council (thread mx, round 15; `clean-arch/step1-unfiled-2026-11-08/council/mx-challenge-14.md`, `mx-codex-15.md`): consensus

- The two checks meet the written lines; the result is reported as that, with its size, and not as "no error" or "safe in general".
- "Tidier; less work not shown" is fair.
- The table goes to Alex as a tested mock: a way to find kept figures, with their source and period limits. It is not put to him as
  the accepted way the new system handles revenue and margin, and not as a substitute for a tracked question with a judgement.
- A reading of the fresh week's three missed matters (D489: FY2027 revenue, FY2028 revenue, FY2028 gross margin) from a table of that
  week's stored answers is a fair next test **as a separate question** (can a reader find the figures, periods and sources that bear
  on each matter): D489's count (2 against 4) is not changed by it, the articles, required outcomes and line are fixed before the
  read, and what that week's articles support is checked first (its FY2027 revenue articles hold consensus estimates, not a company
  annual guide).
- Tracked revenue and margin questions stay Alex's open choice: the one arm that tried (c20, D491) failed its stop line with the cause
  unsettled, which does not show the approach impossible.
- The report must not say the financial data is complete, that every source and period is right, that the week's missing matters are
  now covered, or that the new system is ready.

## Lessons

1. **An answer key fixed before the readers** took the comparers from splits on two questions (D500) to the same mark on ten of
   eleven parts for eight sets; the one difference was a judgement the key had not worded (a figure set under a heading while its
   stored period is given).
2. **A council read of the joined lines before any reader** caught a display fault (one article's qualification shown as every
   article's) and a key that credited an unestablished period: both cheaper to fix before the read than to explain after.
3. **Do not promise a measure the test cannot take.** The option put to Alex said the test would show whether the table "saves
   work"; model readers' tokens and seconds cannot show that. Name the measure before the promise, or leave the claim out.
4. **A table inherits the stored labels' limits** (three of 25 joined members carry a fiscal year their article only implies): it
   must say that it shows what the system stored.

