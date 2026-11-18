# Blind reader, packet two: is each figure's fixed period right? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY the packet file named at the end of this brief. Open no other file in that folder or
anywhere else.

The packet holds `articles` (title, publisher, publication date, text) and `answers`; each answer lists `figures` a system stored from
its article about NVIDIA. Each figure has its `measure`, its `period` as the article words it, and a `fixed_period`: either a code such
as `FY2027` (the company's fiscal year 2027), `FY2027-Q3` (the third quarter of that fiscal year), `CY2027` or `CY2027-Q2` (a calendar
year or quarter), or empty (null).

For every figure, judge against the article's own words only (not the publication date, not what you know of the company), and mark:
- `written`: `yes` only when the article itself writes the year of this figure's period and that year belongs to this figure: for a year
  figure, the article writes that fiscal or calendar year for it; for a quarter figure, the article says which quarter it is and ties it
  to a written year (in the figure's sentence or another one: "the second quarter of fiscal 2027" once, "that quarter" afterwards).
  `no` when the article never writes that year for this period: a quarter or "the full year" with no year anywhere; a year that could
  only be worked out from another year the article mentions ("next fiscal year, fiscal 2028" does not write the current one); a range
  of years; a deadline ("by 2029"); no period at all.
- `deducible`: only when `written` is `no`: `yes` when a careful reader could still work the period out from the article's own
  statements (for example from "next fiscal year, fiscal 2028"), `no` otherwise.
- `fixed`: `right` (the code is the period the article writes for this figure; or it is empty and `written` is `no`), `wrong` (a code
  for another period, or any code where `written` is `no`), `empty_missing` (it is empty although `written` is `yes`).

Write one JSON object per line, one line per answer and nothing else, with no code fence: {"answer": "B01", "figures": [{"statement":
"...", "n": 1, "written": "yes", "deducible": null, "fixed": "right"}], "note": "<= 30 words, required when anything is wrong"}

The packet file: `docs/research/2026-11-14-use-acceptance/figure-fields-2/reader-packet-2-part1.json`
