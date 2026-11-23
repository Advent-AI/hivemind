# Blind reader, packet one: is each stored figure's source right, and is each statement filed right? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/figure-fields-2/reader-packet-1-part1.json`. Open no other
file in that folder or anywhere else: keys, designs and other readers' answers exist and you must not see them.

The packet holds `articles` (each with its title, publisher, publication date and text; some with `named_figures` and `open_questions`)
and `answers`: independent answers, several per article, in shuffled order, from more than one version of a system; you are not told
which is which and must not guess. Each answer lists the `statements_with_figures` it kept from the article about the company it covers
(NVIDIA; its fiscal year ends in late January, so fiscal 2027 is the year to January 2027). A statement has a `statement_party` (whose
statement it is), a `statement_date`, and `figures`; each figure has `measure`, `period`, `value`, `kind` (actual = reported; guidance =
the company's own outlook; estimate = a named party's or consensus forecast), `basis`, and `party`: the source this answer gives for
that one figure.

Judge everything against the article (its text, title and publisher), nothing else.

For every figure, mark:
- `party`: `right` (the article gives this figure to that source, in the figure's sentence or another one; another wording of the same source
  is right; the company is right for its own reported result even where the article names no spokesperson; for a forecast or outlook
  the company is right only where the article says the company, its management or an executive gave it, and an executive only where
  the article gives that figure as the executive's statement), `wrong` (the article gives the figure to someone else: a market or analyst
  estimate given to the company or its executive; the article's own calculation given to the company; a reported result given to an
  executive who did not state it), `missing` (empty though the article says whose figure it is), `unknown_ok` (empty and the article
  does not say);
- `measure`, `value`, `kind`: `right` or `wrong`. For `kind`: a forecast is `guidance` only where the article says the company, its
  management or an executive gave it; any other forecast (a named party's, the consensus, or one the article states without saying
  whose) is `estimate`; a reported figure is `actual`.
For every statement, mark `statement_party` and `statement_date` with the same four marks (for the date: right, wrong, missing when the
article states it and the answer has none, unknown_ok when neither has it).
For an article with `named_figures`: for each named figure say where it is in this answer (`statement` id and figure `n`), or that it
is not kept.
For a statement that has `links` (a list, or "none"): mark each link `supported` (the statement bears on that open question, as the
article and the question's wording show) or `unsupported`; for "none", say whether one of the `open_questions` plainly should have
taken it (`should_link`: the question id, or null).

Write one JSON object per line, one line per answer:
{"answer": "B01", "statements": [{"id": "...", "statement_party": "...", "statement_date": "...", "figures": [{"n": 1, "party": "...",
"measure": "...", "value": "...", "kind": "..."}], "links": [{"question": "...", "mark": "supported"}], "should_link": null}],
"named": [{"figure": 1, "statement": "...", "n": 2}], "note": "<= 30 words, required when anything is wrong or missing>"}
Use "named": [] when the article has no named figures; give {"figure": k, "statement": null, "n": null} for a named figure not kept;
leave "links" and "should_link" out for statements that have no `links` entry.

Judge every answer in the file (ten); write exactly one line per answer and nothing else, with no code fence.
