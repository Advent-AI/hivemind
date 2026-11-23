# A financial table built by code from what the adopted request keeps: a $0 reader test, version 2 (D501), 2026-11-15

**What it can decide.** Whether laying the stored revenue and gross-margin figures out by code (the same figure on one line, whose
figure and which period made plain where the stored text itself establishes them) lets a reader answer the same questions with less
work and no new error, compared with the plain record of the last test (D500). It shows nothing about completeness, a forward week, a
judgement, or whether a table gives a reader what a tracked question gives. Nothing is sent to a model; no request, prompt or package
code changes; nothing is adopted or shown in the product by this test.

**Alex's word (D501):** "试做财务数字表", on the option "不改系统、不花钱（$0）：用这 40 篇已经存下的数字，纯代码把同一个数字归到一行（保留文章原话和来源，时期拿不准的不硬猜），
再请新读者回答同样的问题，看是否更省事且不出错。当天出结果。" The lines below are proposed, not confirmed by him: he set none.

**The council's bounds (D500, thread mx round 13):** join only what the stored evidence establishes; keep the article's wording and
source; leave an uncertain period unresolved; never derive a quarter from the article's day.

**Version 2, after council round 14 (`mx-codex-14.md`), before any reader ran.** The council read the ten joined lines and the key and
asked for five changes, each checked against the files and made: (1) the Q2 key no longer credits the "this year" estimate of
article 28 as a fiscal-2027 estimate (equal amounts do not make it the same period); (2) the third key pair of Q6 is marked as a
qualified pair (article 3 gives no comparison period for its 100%); (3) on a joined line every article keeps its own basis, source
and period (the China exclusion of the $108 billion guide is article 15's alone); (4) a join the two families mark differently is
undecided, never passed; (5) pairs found are coverage, not effort: "less work" is reported and not scored. Also: the sections and the
table's opening say that the labels are the system's stored ones, not the article's sentences (article 22 says "fiscal Q1" with no
year and the stored period is "Fiscal Q1 2027"), and the joined-lines readers mark each member's stored period against its article.

## Material

The adopted request's (c8's) stored answers on the forty unread articles of D499 (`poc/data/clean-record-unread-2026-11-15/sends`); the
same rows as the last test's record B (`record-2/build_views.rows_of`, one owner of the row rule): 114 rows.

## The table (`build_table.py`; code only; closed rules)

| Decision the code takes | Identity or judgement | The closed set that passes |
|---|---|---|
| Is this source the covered company? | identity | the company's name (an argument) alone or with "Corporation", "Corp", "Inc" or "management", a trailing parenthesis set aside (a full match). Everything else stays as written and is joined only with the same spelling. |
| Is this the same period? | identity | the whole stored period, a trailing parenthesis set aside, is one of seven forms that write "fiscal", one year and at most one quarter ("fiscal q2 2027", "q2 fiscal 2027", "fiscal second quarter of 2027", "second quarter of fiscal 2027", "fiscal 2027 second quarter", "fiscal second quarter 2027", "fiscal [year] 2028"). Everything else ("last quarter", "this year", "q3 2026", "twelve months to fiscal q2 2027", "fiscal year ended jan. 25, 2026") stays as written. |
| Are these rows one line? | identity | the same whose-figure (the company, or one spelling of another source), kind, period key, measure and value after normalising case and spacing. The measure is never joined across wordings ("revenue" and "total revenue" stay two lines) and a value never across precision ("$96.2 billion" and "$96.22 billion" stay two lines): whether those are one fact is a judgement, left to the reader, who now finds them side by side. |
| Which figures matter, which period a relative wording means, whether two analysts' estimates are one consensus | judgement | not taken by code |

Layout: a section for what is stored as the company's figures of each kind and one for what is stored as someone else's of each kind
(the stored source is on each line; others' figures are never joined across spellings); inside a section a block for each period key;
lines sorted by measure and value. Every line keeps the source, the period and the basis as stored and its article; on a joined line
each article keeps its own beneath it; `table-rows.json` keeps each line's statements and passages. The table shows the system's
stored labels and says so: it does not verify a stored period or source against the article.

**Checked before any reader ($0):** the builder refuses to run unless eleven stored wordings stay as written (among them "twelve
months to fiscal q2 2027", "year-ago quarter (fiscal q3 2026)", "q3 2026", "fiscal second quarter") and eight are read as their fixed
key, and unless "Wall Street analysts", "AMD", "analysts covering NVIDIA" and "NVIDIA supplier SK Hynix" are not the company; every
row is in exactly one line (asserted). All 47 distinct stored periods and all 17 distinct stored sources were read with the key each
gets (the builder prints them). Result on the material: 114 rows in 99 lines, 5 sections, 39 period blocks; 63 rows under a fixed
period key; 10 lines hold more than one row (25 rows).

## Checks (frozen now, before any reader)

1. **No wrong join.**
   - By code: every row in exactly one line.
   - By readers: every line that holds more than one row (10 lines), each member with its whole article, read by a blind reader of
     each family: are the members one claim (the same measure, period, value and source)? Each member's stored period is also marked
     against its article: written there, implied by the article's own sequence, or not supported. **Line:** every joined line is
     called the same claim by both families. A line both call different fails the check; a line the families mark differently is
     read again by a fresh reader of each family and, if still split, leaves the check **undecided**. Stored periods the article
     only implies are counted and reported: they are the reading request's, not the join's, and decide no line here.
2. **Not less right.** Two fresh readers of each family answer the six questions of D499 (the same wording) from the table alone,
   citing line ids. For a like comparison, one more fresh reader of each family answers from the plain record of the last test
   (`record-2/views-record-B.md`, the same rows), beside the two who did in D500: eight answer sets, four a layout. A comparer of each
   family marks all eight, under labels drawn anew for each question, against **the answer key fixed below** and the articles, with
   each answer's cited lines. **Line:** in every one of the four table readers' sets, each of the eight parts that all record readers
   had supported in D500 (Q1a, Q3a, Q3b, Q4a, Q4b, Q4c, Q5a, Q5b) is supported, and no part is wrong.
3. **Coverage and effort, reported and not scored** (no line: none of these measures a reader's effort well enough to decide):
   - coverage: the key pairs of Q6 each reader finds (below) and each reader's Q2 mark, per layout, the D500 record readers and the
     fresh record readers shown apart (they did not read in the same session);
   - layout, by code (the same patterns as in D500): the reported revenue 13 lines under 11 headings before, 10 lines in 6 blocks
     now; the third-quarter guide 6 under 5, now 5 in 2; the fiscal 2028 growth guide 13 under 7, now 9 in 4;
   - effort as each reader session's harness reports it (tokens and seconds), four sessions a layout, with the spread: a difference
     smaller than the spread inside a layout is not a difference;
   - each reader's own note on how hard the material was to use.
4. **Reported:** every part of every set with its mark; every wrong or open mark traced to its line and article; the lines holding
   more than one row; the periods left as written.

**Settling (the lesson of D500):** a part on which the two comparers differ for any set is marked again, for all eight sets, by a fresh
comparer of each family; the fresh pair's marks are used for every set of that part; a set on which the fresh pair differ stays open.

**Verdict:** no wrong join (met, not met, undecided); not less right (met, not met, undecided); coverage and effort as reported, with
no claim that work was reduced unless the effort figures show it beyond their spread. The table is worth putting before Alex as a
mock when the first two are met. Two readers a family and a layout: a lead, not a rate.

## The answer key (fixed now from what the D500 comparers agreed the articles hold; shown to the comparers, never to the readers)

- Q1a: the company guides revenue growth of about 70% for fiscal 2028. Q1b: not in the articles (the right answer is that the material
  does not hold it).
- Q2a: the articles establish one estimate for the fiscal year: analysts predict more than $411 billion "in the current fiscal year"
  (article 36). Article 28's "$411 billion ... this year", in a passage about 2026, is not established as a fiscal-2027 estimate.
  `supported`: the article-36 estimate given as analysts', with its period as the line gives it; the answer may add the article-28
  figure when it gives that line's period as stored and does not state it as a fiscal-2027 estimate. `incomplete`: only the
  article-28 figure, given with its period as stored. `wrong`: the article-28 figure stated as a fiscal-2027 estimate as fact, or a
  figure or source no line or article supports. The same rule for both layouts.
- Q3a: the company guides $108 billion, plus or minus 2%. Q3b: analysts expect $109 billion for the current quarter.
- Q4a: 75% in the fiscal second quarter of 2027, reported. Q4b: about 74% for the fiscal third quarter and 71% to 72% for the fourth,
  the company's guidance (both items). Q4c: 72% to 73% for fiscal 2028, the company's.
- Q5a: $96.2 billion (also written $96.22 billion or $96 billion), up 106% year over year. Q5b: $89.0 billion, up 117% year over year.
- Q6, three key pairs (those all four D500 comparers listed): **K1** fiscal third-quarter revenue, the company's $108 billion guide
  against analysts' $109 billion; **K2** fiscal third-quarter revenue growth year over year, about 89% implied by the guide against
  the 90% analysts expect; **K3, a qualified pair** the last reported quarter's revenue growth: 106% year over year in most articles
  against "rising 100% to $96 billion in the recent quarter" in article 3, which states no comparison period: found when the answer
  sets the two side by side and keeps the 100% as stored (recent quarter, comparison not stated); stating as fact that the 100% is a
  year-over-year figure from another source is a misstatement. Marked pair by pair: found or not; K3 is reported apart from K1 and
  K2. Other pairs an answer gives are not required and not marked down unless they misstate a figure, a source or a period against
  the cited lines and the articles.
