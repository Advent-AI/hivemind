# Can an affordable comparison tell the two systems apart? The sizing (D516, under D439), 2026-11-15, $0

**Answer: at the proposed size the comparison may miss differences that matter, and its reliability cannot yet be calculated from the
stored readings. It was not run.** Under simple assumptions (independent answers, the fresh week's question counts, the shares seen
so far) the smallest difference such a comparison would detect four times in five is between about 22 and 38 points for the shapes
the money allows, and more if repeated draws add little; these are illustrations, not a measured boundary. The differences seen so
far are 6, 19 and 26 points on one run each, which neither establish the true differences nor rule out larger ones. By the stop
condition written in D516 this design is not sent. That stops this design at this size; it does not show that the systems are
equal, or that no comparison could ever decide.

Scripts: `draw_counts.py` (what each stored draw holds, by code; `draw-counts.json`), `sizing.py` (the calculation, its inputs printed
with their sources, the closed form checked by simulation).

## 1. What each reading has, per draw (nothing here is made comparable that is not)

| Reading | July window, 14 days (2026-07-01..14) | Fresh week (2026-09-22..28) | Draws of one system on the same news |
|---|---|---|---|
| Big matters covered, both teams (outside the company's own financial level) | trial, one draw each: new 6 of 7 (one team: the seventh missed; the other: folded into another question), old 7 of 7 | one draw each: new 2 of 2, old 1 of 2 | **none** |
| Questions that are trivia or duplicates, both teams | not read | one draw each: new 1 of 7, old 6 of 15 | **none** |
| Answers supported by what the judge was shown, both teams | trial, one draw each: new 7 of 9, old 10 of 12 | one draw each: new 6 of 7, old 10 of 15 | **none** |
| Cited statements whose summary departs from the passage the judge was shown (neither reading checked them against the full articles) | trial: 4 of 201 flagged by both teams (the two systems together, unconfirmed) | one in each system | none |
| Delivery (facts that reached the judge of their question) | trial, the gold's 62 facts, one draw each: delivered new 31, old 22; never delivered though judged later: new 8, old 19; no known "would change" control | the new system only: three confirmed pairs, 23 open (D508) | none |
| Agreement with the frozen reference, seven graded questions | **three draws each**: new 2, 1, 0; old 1, 1, 1 | not applicable | the only reader-based line with repeats: the new system's own spread (0 to 2) is wider than the gap between systems |
| By code: questions opened | new 9, 8, 12; old 12, 13, 14 | new 7; old 15 | three draws each in July |
| By code: statements with no question (new) | 347, 286, 310 of about 550 | 382 of 567 | three draws in July |
| By code: share of links on the largest question | new 0.20, 0.25, 0.20; old 0.53, 0.32, 0.39 | new 0.26; old 0.28 | July: the ranges do not overlap; the fresh week shows no gap |

Sources: `TRIAL-RESULT.md`; `week/WEEK-RESULT.md`; `clean-arch/e2e-comparison-2026-11-13/CENSUS-FULL-RESULT.md`; `draw-counts.json`.

What this table says before any calculation:
- For the three reader-based lines a choice would rest on (matters covered, question quality, answers supported) there is **one draw
  of each system on each of two windows, and no repeat**: the spread between draws of one system is unmeasured for them.
- Where repeats exist (the frozen reference; counts by code), a system's own spread is as wide as the gap between systems, except
  for the share of links piled on one question in July, and that gap is absent in the fresh week.
- On answers supported, the sign of the difference flips between the two windows (6 points for the old system, then 19 for the new).

## 2. How large a difference a comparison could detect

Inputs (all from the fresh week, and all estimates): at the end of one week the new system holds 7 questions with a latest answer
and the old system 15; a week costs about $2.52 a draw for the new system (charged) and about $0.50 for the old (its token count at
listed rates, rounded up; not a separately charged amount). The article database holds articles for three later weeks (2026-10-06
to 10-26); **no exposure census has been run on them and no article list priced**, so their being unread and their cost are
assumptions here. The week of 09-29 has 40 articles already read once by the reading step.

The smallest true difference detected four times in five (two-sided, 5%):

| Shape | Cost | Answers supported | Trivia or duplicates |
|---|---|---|---|
| 1 week, 3 draws each | about $9 | 31 points if repeated draws were as good as new weeks; 54 if they add nothing | 34; 60 |
| 2 weeks, 3 draws each | about $18 | 22; 38 | 24; 42 |
| 3 weeks, 1 draw each | about $9 | 31 | 34 |
| 3 weeks, 2 draws each | about $18 | 22; 31 | 24; 34 |
| 4 weeks, 3 draws each (more unread news and money than there is) | about $36 | 16; 27 | 17; 30 |

- The calculation assumes independent answers, fixed weekly question counts and particular starting shares. Questions within a
  week, and repeated draws of the same week, are correlated to a degree the stored runs do not measure for these readings. "As good
  as new weeks" is an upper bound on what repeated draws can give.
- The simulation checks the formula under the same assumptions; it does not validate the assumptions. For 3 weeks and 1 draw (21
  and 45 answers): a 31-point difference is detected in 82% of 20,000 simulated comparisons, a 10-point difference in 12%, and a
  20-point difference in roughly 40 to 60% depending on the starting shares (about 37% at 83 against 63, about 57% at 97 against
  77, the council's own runs).
- Big matters covered cannot be sized this way at all: a week gives two to seven such matters.

## 3. The stop condition of D516, applied

- **A stated difference the comparison is meant to detect:** none can be defended. Under the simple assumptions the shapes the
  money allows detect differences of roughly 22 to 38 points or more; one draw of each system does not tell us whether the true
  differences are that large (the largest seen is 26 points, on one week), and on the one line with two windows the sign flips.
- **A defensible size and cost for it:** the reliability of a $9 to $18 comparison cannot be calculated from the stored readings
  (no repeated draws of the reader-based lines; correlation unmeasured). Spending the remaining money on a test whose power is
  unknown and plausibly low is not defensible.
- **The readers' controls:** the delivery reading still has no known single-fact "would change" case (the six calls of D511 did not
  give one), so that line could not be exercised either.
- **So this design is not sent.** What is unmeasured and would have to change for a comparison to decide: many more independent
  weeks of unread news than the database holds (seven to nine weeks for a 20-point difference at one draw each), or a line that does
  not depend on the handful of questions a week produces.

## 4. What this means for the decision page

The page's section 5 offered Alex "one comparison written down before it runs" as the way to choose by measurement. The page now
says, in plain words: at the proposed size the comparison may miss differences that matter; we cannot yet calculate its
reliability from our stored readings; we did not run it.

## 5. Council (reflection thread "my", round 7): consensus, with corrections

The council ran the script and reproduced its figures, and corrected this page's first wording: "only about 30 points or more" (the
table gives 22 to 38), "nothing seen suggests a 30-point difference" (one draw does not establish it), the single 40% figure for a
20-point gap (it depends on the starting shares), the row that claimed a check of cited statements against their articles (both
readings used the passages shown to the judge), and the unread weeks and costs stated as facts (they are estimates until an
exposure census and an article list exist). **Decided under D439 (D517): this comparison is not sent.**
