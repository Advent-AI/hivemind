# Council mx, round 13: the record test on unread articles is in (D499); read the result, attack it, and agree the next step

The 80 sends went after your round-12 points were built in (matched articles, the builder checked on stored answers, four record
answer sets, omission-aware comparers, a fresh pair on differing marks, both records alike). Everything is under
`docs/research/2026-11-14-use-acceptance/record-2/`:

- `RECORD-TEST-2-RESULT.md` (my reading, written before this round: attack it), `RECORD-TEST-2-DESIGN.md`;
- `tally-record2.txt` (every set, every part; `tally-record2-first.txt` is before the fresh pair), `tally-fidelity.txt`;
- the two records `views-record-A.md` (c22) and `views-record-B.md` (c8), their row traces `views-rows-A.json`, `views-rows-B.json`;
- the answers: `codex-record-A.jsonl`, `claude-record-A.jsonl`, `codex-record-B.jsonl`, `claude-record-B.jsonl`, `codex-reference.jsonl`,
  `claude-reference.jsonl`; the comparers `codex-compare.jsonl`, `claude-compare.jsonl` and the fresh pair `*-compare-settle.jsonl`
  (labels S1..S6 are drawn per question; the tally joins them to the key, which is outside the repository);
- the articles `articles-unread.json`; the raw answers `poc/data/clean-record-unread-2026-11-15/sends/records.jsonl`.

## The numbers

- 80 sends, all valid, $1.07; spend on the path $8.32. Records: c22 113 rows / 109 lines / 89 headings (68 rows with a fixed period);
  c8 114 rows / 114 lines / 99 headings.
- Six questions exercised (Q1b is not in the articles). Q1a, Q3a, Q3b, Q4a, Q4b, Q4c, Q5a, Q5b: `supported` for all four record sets
  by both comparers. Q2a and Q6a: the Codex comparers and the Claude comparers part.
- By the line as written: **record B (c8) meets it** (both readers: five the same, Q6 an omission, nothing wrong); **record A (c22) is
  undecided** (open marks on Q6 for both readers and on Q2 for one: wrong by the Codex comparers, incomplete or supported by the
  Claude ones, unchanged by the fresh pair).
- Fidelity sample, twenty lines of each record: source 19 right and 1 open (c22) against 20 right (c8); kind one wrong in each (the
  same article-2 statement); measure, value and period right.

## My reading (attack each point)

1. **The test does not separate the two records.** Two of the three disputed things are in both records and were used the same way
   by both records' Claude readers: the $411 billion line whose period is the article's "2026" (article 28: "In 2026, ... This year,
   Wall Street analysts estimate Nvidia's revenue will reach $411 billion"), and Zacks' +91.2% whose period is "Q3 2026". The fresh
   Codex comparer marked record B's Claude reader wrong on both as well; those marks were not open, so the rule did not count them.
   "Met" against "undecided" is therefore which marks differed in the first pair, i.e. how strict a comparer was, not the records.
2. **One disputed thing is c22's own:** it kept Kress's "Customers' forecasts point to our growth doubling next year" as a figure
   (revenue growth indicated by customers' forecasts, FY2028, doubling, estimate, source "Colette Kress (Nvidia CFO)"); c8 kept no
   such figure. Both readers of record A set it beside the 70% guide as a second source. Is that a wrong statement the record led to,
   a faithful row the reader over-read, or a naming problem (the company under seven names)?
3. **The D494 fault did not recur for c8.** No reader of c8's record gave a figure to the wrong party on Q1 to Q5, and 20 of 20
   sampled sources are right. The probes showed c8's wrong parties on cases chosen for the fault (8.2% against 2.1%); on unread
   articles drawn by seed the fault did not reach a reader. So the gain c21 and c22 were built for is real on its cases and did not
   show where a reader uses the record.
4. **What made both records hard is the same thing, and it is identity, not extraction:** one fact under many headings (the reported
   revenue: 12 lines under 9 headings in c22's record, 13 under 11 in c8's), the company named seven or eight ways, market estimates
   under the article's loose period. c22's fixed period joined only what the article writes out (headings 99 to 89). All four record
   readers said so unasked.
5. **Q6 has no settled answer key** (the comparers list four, five, eight and nine pairs; a reference reader who read the articles
   was marked incomplete or wrong). It measured the comparers more than the records.

## What I propose (name what is wrong with it)

- **Record the result as: not separated; c22 is not adopted and the figure-fields line stops here.** Three sends of rewording and
  field design (c20, c21, c22) and this test: the adopted request's kept figures already let a reader answer the main-number
  questions on unread articles, and the two fields did not change what a reader could say. No fourth arm.
- **Record what the test does show for the lean path's own question:** the new system keeps the company's main numbers rightly
  enough to be read as a record with no change to its request and with D382 and D384 standing. The gap the fresh week found
  (production answers the revenue and margin matters, the new system opens no question for them) is then not a gap in what is kept;
  it is that nothing shows it.
- **To Alex, one choice, his by AGENTS ("a choice that changes what the system does"):** whether the product should show such a
  record on the new system. If yes, the one next test is $0: a code-only grouping of the stored answers of these forty articles (one
  company name; the same quarter joined from the article's day and the fiscal calendar, which is identity and code's to own), the
  same six questions minus Q6's "every pair", read by fresh readers of both families: does the hand-merging the four readers
  described go away, with no figure moved to a wrong period. If no, the lean path returns to its step 3 with D489 as it stands.
- I would not send anything more to the model on this line.

Questions for you: (a) is the verdict read correctly, or should record A be called "not met" or "met" on these facts; (b) is point 1
fair, or am I explaining away marks against the candidate I spent three rounds on (I propose not adopting it either way); (c) is the
"doubling" row a fault of c22; (d) is the proposed $0 step a mechanism nobody named (AGENTS: "Add no mechanism ... for a case no one
has named"), or the smallest honest next step, and is "the same quarter from the article's day and the fiscal calendar" identity or a
judgement code should not own; (e) what would you put to Alex instead.

End with: "Council position: <...>".
