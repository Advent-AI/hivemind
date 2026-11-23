# The table on the fresh week: can a reader find the figures of the three matters the new system had no question for? Result (D503), 2026-11-15

Design: `TABLE-WEEK-DESIGN.md` (version 2, frozen before any reader). Tallies: `tally-week.txt` (`tally-week-first.txt` before the fresh
pair). The table: `financial-table-week.md` (trace `table-rows-week.json`), built by `build_table.py --trace` from the new system's stored
answers of the fresh week of D489 (2026-09-22..28, 235 articles). The key: `week-key.json` (sha256 in `week-key.sha256`). Cost: $0.

**This is a separate question from D489's and changes nothing in it.** D489 counted a matter covered when a tracked question was
opened or a narrower one carried the outcome: the new system 2, production 4. A table line is not a tracked question.

## The verdict, by the line written before any reader

| Matter | Key figures (from the seven articles) | Outcome by the line |
|---|---|---|
| M01 fiscal 2027 revenue | 5 | **undecided**: all five found by all four readers; the comparers split on whether an extra figure two readers gave is misleading |
| M02 fiscal 2028 revenue | 4 | **not findable**: one key figure was never stored; one was found by the two Claude readers and neither Codex reader |
| M03 fiscal 2028 gross margin | 3 | **not findable**: one key figure, a line of its own in the table, was found by the two Claude readers and neither Codex reader |

In plain words: of the twelve figures the articles give on the three matters, eleven are in the table and one was never stored; two
readers found all eleven, the other two found eight and nine. Why those two missed them was not measured (a 146-line table is a
plausible cause, not a diagnosis). The line (at least one reader of each family for every figure) is not met for two matters. The
table also passes on wrong or misleading stored sources (below). Seven articles, four readers and one stored draw: a lead.

## Every key figure

The key: every company outlook (a) or market estimate (b) both reference readers listed from the seven articles, each quote checked
in its article by code. Three figures only one reference reader listed for a matter were read by a fresh reader of each family: stated
in the article, not bearing on that matter (they are key figures of the other matter); kept beside the key.

| Key figure | Whose | In the table (by code) | Found by (of 4) | Readers who did not find it |
|---|---|---|---|---|
| M01-K1 third-quarter guide $108 billion, plus or minus 2% | the company | a line of its own, key article | 4 | none |
| M01-K2 fiscal 2027 revenue $406.05 billion | Zacks consensus | a line of its own, key article | 4 | none |
| M01-K3 fiscal 2027 revenue around $412 billion | analysts' consensus | a line of its own, key article | 4 | none |
| M01-K4 revenue growth of roughly 90% this fiscal year | not attributed | a line of its own, key article | 4 | none |
| M01-K5 next quarter $109.0 billion, up 91.2% | consensus | a line of its own, key article | 4 | none |
| M02-K1 revenue growth of about 70% in fiscal 2028 | the company | a line of its own, key article | 4 | none |
| M02-K2 chip sales to double in the coming year | the company (its CEO) | a line of its own from another article only | 2 | both Codex readers |
| M02-K3 the 45% growth analysts had expected | analysts | a line of its own from another article only; from the key article only inside a note | 4 | none |
| M02-K4 fiscal 2028 revenue around $700 billion | the article's own calculation | **nowhere** | 0 | all (not stored) |
| M03-K1 gross margin 72% to 73% in fiscal 2028 | the company | a line of its own, key article | 4 | none |
| M03-K2 a low of 71% to 72% in the fiscal fourth quarter | the company | a line of its own, key article | 3 | Codex reader 1 |
| M03-K3 under 72% by the fourth quarter | analyst estimates compiled by Bloomberg | a line of its own, key article | 2 | both Codex readers |

The two comparers gave the same mark on every one of these 48 cells, and so did the fresh pair.

Traced to the stored answers:
- **M02-K4** ($700 billion, article 121's own arithmetic on the consensus and the 70% outlook): the system kept five statements of
  that article and none holds this figure. A figure the reading step did not keep cannot be in any table.
- **M02-K2** (the CEO's "double its chip sales in the coming year", article 73): the statement was kept, with no figure stored in
  it (the claim is in the summary only), so the table of figures has no line from that article; the Claude readers found the same
  claim on a line from another article (article 99: "Huang, who said that Nvidia would double its chip sales next year").
- **M02-K3** (the 45%): from its own article it is only inside the note of the company's 70% line (T-093); its own line (T-114, from
  another article) stores the CFO as its source and so sits in the section "stored as NVIDIA's own estimate". All four readers
  found it and said the stored source clashes with the line's own words ("Wall Street model previously expected").

## Misleading extras: the comparers split, on every matter

The first Codex comparer flagged an extra for every reader and the first Claude comparer for none; the fresh Codex comparer flagged
one (the "+91.2%" line's year for the two Claude readers on M01) and the fresh Claude comparer two others (the Codex readers passing
on "Keithen Drury (fool.com)" and "24/7 Wall St." as the forecasters of figures the passages attribute to no one). No extra is flagged
by both comparers of a pair, so by the rule they stay open. Read against the whole articles by Claude (the author; not deciding):
- the flagged stored sources and periods of the Zacks, consensus and "fiscal Q3 2027" lines (T-124, T-131, T-134, T-139, T-140,
  T-143, T-146) are each supported elsewhere in their article; the short stored passage does not repeat them. The comparers were
  told to judge lines from outside the seven articles by the stored passage alone, which cannot settle this: a fault of the brief.
- T-125, T-137 and T-141 are real limits of the stored labels: the articles state a figure with no source ("Gross margins are
  expected to ... 72% to 73% in fiscal 2028"), and the system stored the outlet or the author as the forecaster, so the company's
  own guide appears a second time as an outside forecast.

## What the table showed of the stored labels (seen by the readers themselves)

- **Two market consensus figures filed under the company** (T-114 the 45%; T-115 the $92.37 billion second-quarter consensus): the
  one-party-per-statement fault of D494, reaching a reader's table on a key figure this time. All four readers noticed the first
  and said so; the two Claude readers also listed the second.
- **One article's own wrong year carried faithfully** (T-104: "For FY 2027, Nvidia estimates its revenue growth will be around 70%",
  two syndicated copies): the table shows a 70% growth outlook under FY 2027 beside the fiscal 2028 lines. Two readers passed it on
  as a fiscal 2027 outlook; two flagged the clash.
- **Periods:** 95 of 186 rows sit under a fixed period key; the rest under the period as stored ("current quarter", "next year",
  "this year"). All four readers named this, and the same figure repeated over many lines, as what made the table slow to use.

## The joined lines the readers relied on

Nine of the table's eighteen joined lines are cited for a company outlook or a market estimate. Both families read each member
against its whole article: all nine are one claim. Five of their 26 members carry a fiscal year their article only implies (both
families); none is unsupported.

## What this result may and may not be said to show

- Shown, for three matters, one week, the figures of seven articles and four readers: most of the figures that bear on the matters
  were kept and can be found in the table with their periods and sources; a reader who does not read all of it misses some; one
  figure was never kept; the table passes on the stored labels' faults.
- Not shown: that the matters are covered in D489's sense or their outcome answered; a revised comparison count; that the table
  carries every important figure of the week; that it gives what a tracked question with a judgement gives; that either system
  should carry forward.

## Council (thread mx, round 17; `clean-arch/step1-unfiled-2026-11-08/council/mx-challenge-16.md`, `mx-codex-17.md`): consensus, with three of Claude's points withdrawn

- The frozen outcomes are reported as they are: M01 undecided, M02 and M03 not findable, for these seven articles, four readers and
  one stored draw.
- Withdrawn by Claude after the council's challenge: (1) "a thorough reader finds all eleven" (two did; why two did not was not
  measured); (2) that c22's per-figure source "would have filed T-114 and T-115 under the market" (c22 was not run on this week;
  that needs a comparison, not an inference from its schema); (3) that the new system is "ahead" on the fresh week and that the
  three financial matters are "its only large loss" (D489's own rule gave **not clear**: 6 of 7 against 10 of 15 judgements is one
  judgement from a 14-point swing and the readers split on the supported controls; production also missed a matter and had
  duplicates).
- The table carries more than reader omissions: wrong or misleading stored sources (T-114, T-115; T-125, T-137, T-141). Nine joins
  read as one claim does not make every label source-faithful, and the comparers' split on extras stays visible.
- Tracked revenue and margin questions are a legitimate option for Alex, not established as the remedy: c20's failed stop line is
  real and its cause cannot be read out of the stored reasoning (it gives two reasons; only a controlled comparison could separate
  them, on a constructed state).
- **To Alex, one question:** for the company's major financial numbers, what should a reader be able to do: see the kept figures
  with their sources, get a tracked question with a judgement, have kept figures reach the judgements of related questions, or
  several of these. The options are not exclusive.
- The cheapest next step that decides something concrete: a $0 check of the stored judgement requests against the kept figures:
  for an existing question, is a financial fact it should have received absent from its request. It cannot show the value of annual
  financial judgements or choose a system.

## Lessons

1. **A conclusion stays what its pre-written rule gave.** Claude proposed telling Alex the new system was "ahead" on a comparison
   whose own rule said "not clear". The council caught it. Before any summary to Alex, each earlier result is quoted by its recorded
   verdict, not by its most favourable count.
2. **A brief that tells comparers to judge by the short stored passage cannot settle a source or period the article gives
   elsewhere.** Every comparer flagged different extras. Give the whole article for every cited line, or do not ask for the mark.
3. **With four readers, how many found a figure is the result.** A line of "at least one of each family" hides that half the
   readers missed three figures; report the count first.
4. **A stored reason is not a cause** (again, after D491): a diagnosis that the stored data cannot give is not offered as a next step.

