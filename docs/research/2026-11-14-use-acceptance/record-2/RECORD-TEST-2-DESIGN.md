# The company record on unread articles: the adopted request against the second figure-fields arm, version 2 (D499), 2026-11-15

**What it can decide.** Whether, on articles no arm has read, a company record built by code from what each request keeps lets a reader
answer what the company says and what the market expects for revenue and gross margin without being led to a wrong statement; and
whether the arm's record (a source and a fixed-form period on each figure, c22) does that better than the adopted request's (one party
per statement, c8), which in the first test led its reader to one wrong attribution (D494). It shows nothing about judgements, about a
forward run, or about what the product should show: those stay Alex's.

**Alex's word (D499):** "直接做记录测试", on the option "用现在的第二版在没看过的文章上做财务记录测试：新旧两版各读约 40 篇，看读者能否正确回答六个问题、会不会被误导". He
waived the one-figure miss of D498 for this step; the council's position that a pass should come first is recorded there.

## Material

- **Articles** (`sample-unread.json`): forty, drawn by seed (20261122, by day) from the 81 articles of 2026-09-29..10-05 that no run or probe
  has sent, that the clean path's own rule selects, and whose text carries a revenue or gross-margin figure (a text screen, fixed before
  any answer, so that the record has something to hold; the population is that screened one, not the week, and the figure may be
  another company's: the screen does not ensure the six questions can be answered). The population, the seed and the sample are kept;
  no article is replaced after a result is read.
- **Requests** (`build_trace_record.py`, the reviewed builder; a stored request rebuilt byte for byte first): each article read once by c8
  and once by c22 against the library the clean week draw left on 2026-09-28 (seven questions). A labelled constructed state: the same
  week-end library for every article. 80 sends, about $1.00 (dry run $1.17 at the script's estimate); ceiling $2.00. One answer an
  article and arm: a difference between the arms on one article may be ordinary variation; individual outputs are reported and no
  general claim rests on them. **Matched articles:** an article for which either arm has no valid answer is left out of both records
  and listed; a missing answer is never an empty record.
- **The two records** (`build_views.py`, code only, the same code for both): the rows whose stored measure names revenue, sales or gross
  margin, each with its value, kind, basis, its source (c8: the statement's party; c22: the figure's own) and the article; grouped under
  the stored measure and, where the arm gives one, the fixed period, else the period as stored. Rows are merged only when measure,
  period, value, kind, source and basis are all equal; a merged line lists its articles. Every line has an id, and a side file keeps
  each id's statements, passages and articles, so an answer is traced to its rows. Checked before the send on the second probe's stored
  answers (ten articles, both arms): every line id traces to statements with passages. The two views go out as record A and record B,
  the letters drawn by seed, the key outside the repository.

## Checks (frozen now)

1. **Usability**, the six questions of D494 with their required parts, with the gaps its review named closed:
   - Q1 fiscal 2028 revenue growth: (a) the company's guide; (b) what analysts expected before the guide.
   - Q2 fiscal 2027 total revenue: (a) each market estimate in the articles with its source.
   - Q3 fiscal third-quarter 2027 revenue: (a) the company's guide; (b) the market's estimate.
   - Q4 gross margin: (a) the last reported quarter; (b) what is guided or estimated for the rest of fiscal 2027; (c) the outlook for
     fiscal 2028.
   - Q5 the last reported quarter: (a) total revenue with its growth; (b) data-center revenue with its growth.
   - Q6 revenue or gross margin only: the same measure and period given different values by different sources (not a revision): each pair.
   **Record readers:** a reader of each family (Codex, a Claude subagent) answers the six questions from record A alone, and, in a
   separate session that sees nothing of the first, from record B alone: four answer sets, so that a record is not judged through one
   reader. Each answer cites the line ids it rests on, or says the record does not hold the part.
   **Reference readers:** a reader of each family answers the same parts from the forty articles alone (title, publisher, text), citing
   articles; for Q2 and Q6 they list every estimate and every pair the articles hold.
   **Comparers** (one of each family), given the questions' wording, the forty articles, the two reference sets and the four record
   sets under labels drawn anew for each question, and each record answer's cited lines:
   - first fix, per part, what the articles hold (for Q2 each estimate, for Q6 each pair, as a list of items), from the articles and
     the two reference sets;
   - then mark every part of each record set: `supported` (every item the articles hold is given, with figure, period and attribution
     the articles support, and resting on the lines it cites), `incomplete` (what it gives is supported but an item the articles hold
     is missing: name it), `wrong` (a figure, period or attribution no article supports, or one the cited lines do not hold: say which),
     `none` (it says the record does not hold the part).
   - A part is *exercised* when both comparers find the articles hold it; a part one comparer finds and the other does not is open.
   - For one record set, a question is *the same* when every exercised required part is `supported` by both comparers; an `incomplete`
     or `none` on an exercised part is an *omission*; a part both mark `wrong` is *wrong*. Marks the comparers give differently are
     settled against the articles by a fresh reader of each family and stay open if those differ.
   - **Line, per record:** in both of its readers' sets: at least five questions exercised, at most one not the same, and no part
     wrong. Omissions and wrong statements are counted apart and each wrong statement is traced to its line. Fewer than five questions
     exercised is **inconclusive** for both records, not a failure of either; open marks that could change a line leave it undecided.
2. **Fidelity of the source**, twenty seeded rows of each record's revenue and margin rows (seed 20261123), read against the article with
   its publisher by two blind families under shuffled labels: the source right, wrong, missing or unknown_ok, by the definitions used in
   the second probe; measure, period, kind and value right or wrong. Reported per record, with both arms' differing marks settled alike;
   a count, not a line (the probes measured the line).
3. **Reported:** rows and headings per record; rows with a fixed period; the parts each record's reader could not answer; every wrong or
   open part with the row it came from.

**Verdict:** per record: meets the usability line, does not, undecided or inconclusive; and the comparison in plain words (what each
record's readers got wrong or could not answer, and from which line). A clean result would describe these screened articles, this
constructed library, one answer an article and these readers: not complete extraction, not a forward week, not an effect on a
judgement, and not that the product should show the record. Nothing is adopted by this test: c8 stays the adopted request, and whether to adopt c22 or to
show a record is put to Alex with the result.

**Method, from the lessons of this path:** the tally prints every line at the grain stated here; packets go to Codex readers in parts
of ten; readers' files are joined by parsing; both records' disputed marks are settled alike; the publisher is in every packet.
