# Blind reader, packet two: is each figure's fixed period right? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/figure-fields/reader-packet-2.json`. Open no other
file in that folder or anywhere else.

The packet holds `articles` (title, publisher, publication date, text) and `answers`; each answer lists `figures` a system stored from
its article about NVIDIA (its fiscal year ends in late January: fiscal 2027 is the year to January 2027). Each figure has its `measure`,
its `period` as the article words it, and a `fixed_period`: either a code such as `FY2027` (the company's fiscal year 2027), `FY2027-Q3`
(the third quarter of that fiscal year), `CY2027` or `CY2027-Q2` (a calendar year or quarter), or empty (null).

For every figure, judge against the article only, and mark:
- `established`: `yes` only when the article itself supports a period for this figure that the code can hold in full: a fiscal or
  calendar year, or a quarter together with its year (the article may name it anywhere, for example "the fiscal second quarter of 2027"
  in one sentence and "last quarter" in another); `no` for a quarter with no year anywhere in the article, a relative period the article
  does not pin down ("next year" with no year named), a range of years, a deadline ("by 2029"), or no period at all. Do not use the
  publication date or outside knowledge to decide.
- `fixed`: `right` (the code is the period the article establishes for this figure; or it is empty and `established` is `no`), `wrong`
  (a code for another period, or a code where `established` is `no`), `empty_missing` (it is empty although `established` is `yes`).

Write one JSON object per line, one line per answer: {"answer": "B01", "figures": [{"statement": "...", "n": 1, "established": "yes",
"fixed": "right"}], "note": "<= 30 words, required when anything is wrong"}
