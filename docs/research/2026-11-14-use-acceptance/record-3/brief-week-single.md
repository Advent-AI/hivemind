# Blind reader: does this figure bear on this matter? (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-3/week-single-packet.json`. Open no other
file in that folder or anywhere else.

The packet holds two `matters` (things an analyst tracks about NVIDIA, whose fiscal year ends in late January), a few `articles` and
`items`: each item is a figure from one article, with its period and whose figure it is, proposed as bearing on one matter in group
"a" (the company's own outlook or guide that bears on the matter) or "b" (a market or analyst estimate of the matter).

For each item decide, from its article alone:
- `stated`: yes when the article states that figure with that period and that source; else no;
- `bears`: yes when, as the article gives it, the figure is the company's outlook or guide for THAT matter's period, or a market or
  analyst estimate of THAT matter (its revenue for that fiscal year); no when it is a figure about another period that the matter
  only builds on.

Write one JSON object per line and nothing else, with no code fence:
{"id": "M01-S1", "stated": "yes", "bears": "no", "note": "<= 30 words: the article sentence that decides it>"}
