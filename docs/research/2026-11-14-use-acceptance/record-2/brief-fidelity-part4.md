# Blind reader: is each stored figure right against its article? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-2/fidelity-packet-part4.json`. Open no other
file in that folder or anywhere else: keys, designs, records and other readers' answers exist and you must not see them.

The packet holds `articles` (each with its number, title, publisher, publication date and text) and `rows`: figures a system stored from
those articles, in shuffled order, from more than one version of the system; you are not told which is which and must not guess. The
articles concern NVIDIA (its fiscal year ends in late January: fiscal 2027 is the year to January 2027). Each row names its `article`,
the `passages` the system quoted, and the stored `measure`, `period`, `value`, `kind` (actual = reported; guidance = the company's own
outlook; estimate = someone's forecast), `source` (whose figure the system says it is), `basis` and `said`.

Judge every row against its article (text, title and publisher), nothing else. Mark:
- `source`: `right` (the article gives this figure to that source, in the figure's sentence or another one; another wording of the same
  source is right; the company is right for its own reported result even where the article names no spokesperson; for a forecast or
  outlook the company is right only where the article says the company, its management or an executive gave it, and an executive only
  where the article gives that figure as the executive's statement), `wrong` (the article gives the figure to someone else: a market or
  analyst estimate given to the company or its executive; the article's own calculation given to the company; a reported result given
  to an executive who did not state it), `missing` (the source is "not stored" or empty though the article says whose figure it is),
  `unknown_ok` (not stored and the article does not say);
- `measure`, `value`, `kind`: `right` or `wrong`. For `kind`: a forecast is `guidance` only where the article says the company, its
  management or an executive gave it; any other forecast is `estimate`; a reported figure is `actual`;
- `period`: `right` when the article gives this figure that period (the article's own wording, such as "current quarter", is right; a
  code such as FY2027-Q3 means the third quarter of fiscal 2027, CY2026 the calendar year 2026, and is right only where the article
  itself ties this figure to that year and quarter), `wrong` when the article gives the figure another period or none that supports it.

Write one JSON object per line and nothing else, with no code fence, one line per row:
{"row": "F01", "source": "right", "measure": "right", "value": "right", "kind": "right", "period": "right", "note": "<= 30 words, required when anything is not right>"}
