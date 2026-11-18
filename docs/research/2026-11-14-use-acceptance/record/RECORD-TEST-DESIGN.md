# Can the figures the new system already keeps form a faithful, usable company record? A $0 test on the stored week (D492, D493; council mx)

**What it can decide.** Whether the company figures the clean path kept over the fresh week (the statements its request files as conditions:
measure, period, value, kind, basis, with speaker, date and passages) can be assembled by code into a record that is faithful to the
articles and from which a reader can answer what the company says, what the market expects and what differs, for revenue and gross margin.
This is the use Alex approved in words on 2026-11-08 (`clean-arch/step1-unfiled-2026-11-08/LOG.md` §17: a kept figure "labelled actual,
guidance or expectation, with who said it and the period"); D382 and D384 are untouched. The system sends nothing; the readers are the two
reader families used all along (a read-only Codex session and Claude subagents; no charge on the project's ledger).
**A pass shows** that this stored week's selected figures can be assembled and read faithfully under the questions and lines below. It
does not show complete extraction, a record ready for production, an effect on any judgement, or that questions on these numbers are not
needed. **A failure** names a defect to trace; it does not show that standing questions are the remedy.
Version 2, after council mx round 2 (`mx-codex-3.md`); written before any figure entry was read for this purpose.

## The record (`build_record.py`, code only)

- **Full-week record** (`record-week.json`): every figure entry of every kept statement of the clean week draw
  (`poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1/trace.sqlite`), one row each: measure, basis, period and value as stored, kind, the
  statement's original party, reporting speaker, statement date and its text, tier, the article (step, day, title), its passages, and its
  Step 2 group. Used for the counts and the fidelity sample.
- **The reader's view** (`record-view.md`), built from the **40 sampled articles only** (`week/packet-A1.json`; the article numbers are the
  packet's), so that the record reader and the reference reader have the same source population: the rows whose stored measure names
  revenue, sales or gross margin, grouped by the stored measure and period after a fixed text normalisation (case, spacing; "fiscal 2028",
  "FY2028", "FY28" as one form, and only when the year is written; a period with no year stays as stored). Rows are merged only when
  measure, period, value, kind and original party are all equal after that normalisation; a merged row lists every article and date it
  came from. Nothing is edited by hand; if the view cannot be built without a hand decision, that is the result.

## Checks (frozen now)

1. **Fidelity** (full-week record). Two strata, their sizes printed by the builder: R, the rows whose measure names revenue, sales or gross
   margin; O, every other row. A seeded sample (seed 20261119) of 20 from each (all of a stratum if it has fewer). Two blind reader
   families, each with the row and its article, mark every field: measure, basis (scope), period, kind, value, original party, date, as
   `right`, `wrong`, `missing` (the article states it and the row leaves it empty) or `unknown_ok` (the article does not state it and the
   row leaves it empty). They also mark whether the row is the company's own figure, and, for a row of O, whether it is in fact a revenue
   or margin figure the view's filter leaves out.
   - A row is **wrong** when any field is `wrong`; **incomplete** when none is wrong and one is `missing`.
   - A mark the two families give differently is settled against the article by a third blind reader before the verdict.
   - **Line, per stratum (not a rate for the whole record):** at most 1 of 20 wrong in R and at most 2 of 20 in O after settling;
     incomplete rows, rows that are not the company's own, and revenue or margin rows the filter leaves out are counted and listed.
2. **Usability** (the view; cut-off: the last article of the week, 2026-09-28). Six questions with their required parts:
   - Q1 Fiscal 2028 revenue growth: (a) the company's guide; (b) what analysts expected before the guide; (c) the latest market estimate
     for fiscal 2028 revenue or its growth in the articles.
   - Q2 Fiscal 2027 total revenue: (a) each market estimate in the articles with its source.
   - Q3 Fiscal third-quarter 2027 revenue: (a) the company's guide; (b) the market's estimate.
   - Q4 Gross margin: (a) the last reported quarter (fiscal Q2 2027); (b) what is guided or estimated for the rest of fiscal 2027;
     (c) the outlook for fiscal 2028. Asked also, not required: what is said to drive the change (the view holds figures; a missing
     explanation is reported as a limit of the view).
   - Q5 The last reported quarter: (a) total revenue with its growth; (b) data-center revenue with its growth.
   - Q6 The same measure and period given different values by different sources in the week (not a revision over time): each pair.
   The **record reader** sees only the view and answers each part from the rows it cites, or says the record does not hold it. The
   **reference reader** sees only the 40 articles and answers the same parts, citing article numbers; it never sees the record. Two
   **comparers** (a blind reader of each family) get the two answer sets under shuffled labels with the articles and mark each part: the
   two agree and are supported; one is wrong or unsupported (which); one lacks what the other gives; or neither has it.
   - A part **neither has** is unexercised and counts for nothing. A question is **exercised** when the reference answers at least its
     first required part.
   - A question is **the same** when every required part the reference answers is answered by the record reader with the same figure,
     period and attribution, and the record reader states nothing the articles do not support.
   - **Line:** at least five questions exercised; of those, at most one not the same; no part where the record reader states something
     wrong. Wrong statements, omissions and comparer differences are counted apart; a comparer difference that could change the verdict
     is settled against the article first.
3. **Reported:** rows by measure and kind; missing periods and bases; repeats before and after Step 2 grouping, and whether any merged
   group held different figures, periods, qualifications or sources; the same measure and period with different values.

## Refutation

The fidelity line missed in either stratum; or the usability line missed; or the view not buildable by code alone. Then the record is
not ready as the next improvement, and the defects are listed as what would have to be fixed first.

## What is decided and what is not (council mx, D493)

The order is agreed: this test first. The standing-question comparison (the adopted request unchanged, read against a library that already
holds revenue and margin questions) stays a candidate diagnostic of library state; its questions would be presets in the ordinary sense,
which Alex removed from production (D370), and D490 does not cover them as a product design; it goes to him with that stated before any
send. Any change to what the product shows or sends is his choice, with this test's evidence.
