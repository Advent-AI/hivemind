# Blind reader, reading A1: which big questions do these articles raise? (read-only)

Repository `/Users/lchingen/hivemind`. You are a senior hedge-fund analyst covering NVIDIA. Read ONLY:
`docs/research/2026-11-14-use-acceptance/packet-A1.json` (40 articles, 2026-07-01 to 07-14, in publication order) and the signed standard
`docs/prd/05-extraction-standard.html` §3 (the opening reasons and "问题怎么写") and §4 (the opening tests: the answer can change a position; a date
and public material can settle it; no question already asks the same). Open no other file in that folder or anywhere else: system answers and
reference answers exist and you must not see them.

Read every article in full, first paragraph to last. For each article, list every question worth tracking on its own that it raises: a big
matter (it can change NVIDIA's revenue, profit, cash, credit risk or competitive position, or it is a quantity or decision in the world that
many companies depend on), with an outcome a dated public release, filing or official decision can settle. Small matters, background, a
repeat of what an earlier article already raised (list it again only under the same matter key), a stock-price or valuation view, and anything
no public material can settle are not questions. Most articles raise none or one; say "none" when none qualifies.

Then merge: one matter = one underlying bet, whichever articles raise it; another year of a figure is another matter; two questions are one
matter only when the same outcome would settle both and their answers cannot move apart.

Write one JSON object per line:
- per question: {"article": n, "matter": "<short key>", "question": "<the question, with its period or check date>", "quote": "<= 40 words from
  the article>", "reason": "<the §3 reason and why it is big, <= 30 words>", "settled_by": "<the public material and when>"}
- per article with none: {"article": n, "matter": null}
- finally, per matter: {"matter": "<key>", "name": "<one line>", "articles": [n, ...]}
