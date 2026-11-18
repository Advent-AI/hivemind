# Blind comparer: four readers answered from a table; mark every answer against the key and the articles (read-only)

Repository `/Users/lchingen/hivemind`. Read ONLY `docs/research/2026-11-14-use-acceptance/record-3/week-compare-packet-settle.json` and
`docs/research/2026-11-14-use-acceptance/record-3/week-articles.json` (seven news articles of 2026-09-22 to 09-28, numbered, with day,
publisher, title and text; they concern NVIDIA, whose fiscal year ends in late January: fiscal 2027 is the year to January 2027,
fiscal 2028 the year after). Open no other file in that folder or anywhere else.

The packet holds three matters. For each: `key`, the figures the seven articles give that bear on it (each with an id, its group:
"a" the company's own outlook or guide, "b" a market or analyst estimate; its value, period, whose figure it is, its article and a
quote), and `sets`, four readers' answers under the labels S1 to S4 (drawn anew for each matter). The readers answered from a table
of figures a system stored from the whole week's articles; every figure an answer gives comes with the table lines it cites: where
the line sits, its text, and `stored_passages`, the passage the system quoted from each article on that line. A cited line may come
from an article outside the seven: judge it by its stored passage.

For every key item and every set, one mark:
- `found_same_article`: the answer gives the figure with the value, the period and whose figure it is as the key gives them, and
  rests on a cited line from the key item's own article;
- `found_elsewhere`: the same, resting only on cited lines from other articles, and those lines' own stored passages give that
  figure with a source and a period that agree with the key (an equal value alone does not earn this mark);
- `misstated`: the answer gives the key's figure with another value, period or source than the key and the article support (for
  example a market estimate given as the company's own), or rests on lines whose passages do not hold it;
- `not_found`: the answer does not give it.
And for every set, `other_misstatement`: null, or a short description when the answer gives, for this matter, a figure outside the
key with a source or a period that its cited lines' stored passages do not support (name the figure, the line and what is wrong). An
answer that reports a line's stored source or period as stored, and says so, does not misstate; an answer that passes on a wrong
stored source as fact does.

Write one JSON object per line and nothing else, with no code fence, one line per matter:
{"matter": "M01", "items": {"<key id>": {"S1": "found_same_article", "S2": "not_found", "S3": "found_elsewhere", "S4": "misstated"}}, "other_misstatement": {"S1": null, "S2": "...", "S3": null, "S4": null}, "notes": {"S4": "<= 30 words on any mark that is not found_same_article>"}}
