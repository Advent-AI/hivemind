# Blind reader: were these stored figures rightly put on one line? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-3/week-joined-packet-1.json`. Open no other file
in that folder or anywhere else.

The packet holds `articles` (number, title, publisher, publication date, text; they concern NVIDIA, whose fiscal year ends in late
January: fiscal 2027 is the year to January 2027) and `joined_lines`: each is a set of figures, stored by a system from different
articles, that a program put on one line of a table because their stored measure, value, kind, period and source looked the same. Each
member gives its `article`, the `passages` the system quoted, and the stored `measure`, `period`, `value`, `kind`, `basis` and `source`.
The stored labels are the system's, not the article's own words: check them against the whole article, not only the passages.

For each joined line:
- `mark`: `same` when all members state one and the same claim (the same measure, e.g. total revenue and not a segment's; the same
  period; the same value; the same source), judged from the articles; `different` otherwise (name the members that part and why:
  another period, another measure or scope, another source);
- `periods`: for each member, how its article supports the stored period: `written` (the article writes that fiscal year and quarter
  for this figure, in the figure's sentence or another), `implied` (the article gives the quarter or year only by its own sequence or
  context, without writing the stored year), `unsupported` (the article gives this figure another period or none that fits).

Write one JSON object per line and nothing else, with no code fence, one line per joined line:
{"line": "T-004", "mark": "same", "periods": {"<article number>": "written", "<article number>": "implied"}, "note": "<= 40 words: the article sentences that decide it>"}
