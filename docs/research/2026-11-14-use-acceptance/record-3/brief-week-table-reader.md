# Blind reader: what does this financial table give on three matters? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-3/financial-table-week.md`. Open no other
file in that folder or anywhere else, and use nothing you know from elsewhere: the point is what this table alone lets a reader say.

The table lists financial figures a system stored from the news articles of one week (2026-09-22 to 09-28) about NVIDIA (its fiscal
year ends in late January: fiscal 2027 is the year to January 2027, fiscal 2028 the year after). Its opening lines explain the layout.
Every line has an id in square brackets.

- M01: NVIDIA's revenue for fiscal 2027, the year to late January 2027 (total, or its data-center segment).
- M02: NVIDIA's revenue for fiscal 2028, the year to late January 2028 (total, or its data-center segment).
- M03: NVIDIA's gross margin for fiscal 2028.

For each matter, list every figure the material gives that someone tracking the matter would need, in three groups:
(a) the company's own outlook or guide that bears on it; (b) each market or analyst estimate of it; (c) the latest reported figure it
builds on. Give each figure with its value, its period and whose figure it is. Where the material holds nothing for a group, say so.
Answer from the table's lines only, citing the id of every line you use. Say whose figure each one is as the section and the line's
stored source give it, and give the period as the line stores it.

Write one JSON object per line and nothing else, with no code fence, one line per figure:
{"matter": "M01", "group": "a", "value": "...", "period": "...", "whose": "...", "lines": ["T-012"]}
and, for a group with nothing, {"matter": "M01", "group": "a", "value": null, "note": "not in the table"}. Then a last line
{"matter": "use", "note": "<= 60 words on how hard the table was to use for this and why>"}.
