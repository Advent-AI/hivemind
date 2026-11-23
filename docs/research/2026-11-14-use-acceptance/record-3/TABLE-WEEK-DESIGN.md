# The table on the fresh week: can a reader find the figures of the three matters the new system had no question for? Version 2 (D503), 2026-11-15

**What it can decide.** Whether, in a code-only table of what the new system stored in the fresh week of D489 (2026-09-22..28), a
reader can find the figures, periods and sources that bear on the three matters it opened no question for: M01 fiscal 2027 revenue,
M02 fiscal 2028 revenue, M03 fiscal 2028 gross margin. **It is a separate question from D489's.** D489 counted a matter covered when
a tracked question was opened or a narrower one carried the outcome; a table line is not that, and D489's count (the new system 2,
production 4) is not changed by anything here. It shows nothing about a judgement, about completeness beyond the key, or about a
forward run. $0: nothing is sent to a model; nothing is adopted or shown in the product.

**Alex's word (D503):** "看样表，并在最初那一周再验一次", on the option "用那一周存下的数字排同样的表，请读者盲读，看这三件事的数字、时期、来源在表里查不查得到。原来“2 比 4”的对比结果
不改，这是另记的一项。" The line below is proposed, not confirmed by him: he set none.

**Version 2, after council round 16 (`mx-codex-16.md`), before any reader ran.** Four rules added, each checked against the table: (1)
the two reference readers' lists are reconciled against the articles and a figure only one lists is settled or kept beside the key,
never silently absent; (2) a key figure a reader finds through another article's line is marked apart and credited only when that
line's own passage gives the same figure with its source and period (equal values are not enough); (3) a misleading figure outside
the key counts in the verdict (the table holds one such: line T-114 stores the 45% that "Wall Street had previously modeled" with the
CFO as its source, the per-statement party of D494); (4) before the verdict both families read every joined line a reader relies on
(T-014 joins eight articles' 75% margin). The result speaks of findable figures within the seven articles, never of a matter covered.

## Material (fixed now)

- **The table** (`financial-table-week.md`, trace `table-rows-week.json`): `build_table.py --trace` on the stored Step 1 answers of the
  new system's week draw (`poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1/trace.sqlite`, all 235 articles complete; a missing
  answer refuses the build). The same rules as D501's table, unchanged after seeing this week's wordings ("fy 2027" stays as stored):
  186 rows in 146 lines, 5 sections, 63 period blocks; 95 rows under a fixed period key; 18 joined lines (58 rows). The forty-article
  table of D501 is byte-identical after the builder gained this input.
- **The matters:** M01, M02 and M03 as D489's two reader families named them (`week/matters-A2.json`), worded for the readers without
  their figures (`week-matters.md`).
- **The articles:** the seven sampled articles the families tied to those matters in D489 (sample numbers 3, 6, 13, 18, 21, 29, 39;
  shown to every reader under their place in the week's run: 16, 35, 73, 92, 121, 166, 222; `week-articles.json`).

## Steps, in this order

1. **The required outcomes (the key), before any table reader.** A reference reader of each family reads the seven articles and
   lists, for each matter, (a) the company's own outlook or guide that bears on it, (b) each market or analyst estimate of it, (c) the
   latest reported figure it builds on, each with value, period, whose it is, the article and a quote. These are figures that bear
   on a matter, not its annual outcome (a quarter's guide bears on the year's revenue without being an annual guide). **The key**
   holds every (a) or (b) figure both families list (the same figure under another wording is one figure, decided by reading both
   quotes against the article). A figure only one family lists is read against its article by a fresh reader of each family (is it
   stated there, with that period and source, as the company's outlook or a market estimate bearing on the matter?): both yes, it
   joins the key marked as settled; otherwise it is kept beside the key as unresolved and reported, counted neither found nor
   missing. The key is frozen (`week-key.json`) before any table reader. Group (c) is context and is not required. If the key for a
   matter is empty, that matter is **not exercised** and nothing is concluded about it.
2. **By code, per key item, where its value occurs in the table:** as a line's own value from the key's article; as a line's own
   value from another article only; only inside a basis note; or nowhere. A search by value cannot say whether the figure is
   rightly there (its source and period are the comparers' to read); it separates what was never stored from what was stored and
   not found.
3. **Table readers:** two fresh readers of each family answer the same three-group question from the table alone, citing line ids.
4. **Comparers** (one of each family), given the key, the seven articles and the four answers under labels drawn anew for each
   matter, each answer with its cited lines and each cited line's stored passages: for every key item and every answer,
   `found_same_article` (given with the value, the period and whose figure it is as the key gives them, resting on a cited line
   from the key's article), `found_elsewhere` (the same, resting only on lines from other articles whose own passages give that
   figure with a source and period that agree with the key; equal values alone do not earn it), `not_found`, or `misstated` (given
   with another value, period or source than the key and the article support, or resting on lines that do not hold it); and, per
   answer and matter, `other_misstatement`: a figure outside the key, bearing on the matter, that the answer gives with a source or
   period its cited passages do not support (say which). Figures from articles outside the seven are checked against their stored
   passages only, and the result says so.
5. **The joined lines relied on:** before the verdict, every line holding more than one article that any table reader cites for a
   key item or for a flagged extra is read by a reader of each family, each member against its own passage and article: one claim
   (the same measure, period, value and source) or not. A relied-on join both call different, or one the families mark differently
   and a fresh pair cannot settle, leaves its matter undecided.
6. **Settling:** a matter on which the two comparers differ for any answer is marked again for all four answers by a fresh comparer
   of each family; their marks are used for every answer; an answer on which the fresh pair differ stays open.

## The line (frozen now)

For each exercised matter, one of:
- **its key figures are findable**: every key item is found (in the key's article's line, or corroborated elsewhere) by at least one
  table reader of each family; no key item is `misstated` for any reader by both comparers; no `other_misstatement` on the matter is
  given by both comparers for any reader;
- **key figures found, with a misleading extra**: the first two hold and both comparers give an `other_misstatement` for some reader;
- **not findable**: a key item is found by no reader of a family, or is `misstated` for a reader by both comparers; a key item whose
  value is nowhere in the table (step 2) is listed as a figure the reading step did not store;
- **undecided**: open marks or an unsettled relied-on join could change the above.
Reported per matter and per key item with every reader's marks, each reader's omissions, and how many of the four found each item
(an item two of four find is not "easy to find"). Four readers and one stored draw: a lead.

**What the result may be said to show:** for these three matters, this week and the figures of these seven articles, whether the kept
figures can be found in the table with their periods and sources. Not: that the matters are covered in D489's sense or their main
outcome answered; a revised comparison count; that the table carries every important figure of the week; that it gives what a tracked
question with a judgement gives; that either system should carry forward.
