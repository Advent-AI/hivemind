# Blind reader: the article from which an analyst would write each question's answer choices (read-only)

Repository `/Users/lchingen/hivemind`. File: `clean-arch/e2e-comparison-2026-11-13/ladder-cost/article-candidates.json`: for each of eight research
questions, up to ten articles (in date order) whose statements an extraction step linked to it, with those statements. The article text is in
`poc/data/items-nvda-2026-07-01-10-27.sqlite`, table `items`, column `text`, by `input_id`.

For each question, pick **the earliest article whose own text states the question's subject itself** — its quantity, plan, schedule or decision,
with a figure, a date or a named step — so that an analyst could write the question's answer ranges and say where the market stands from that
article. An article that only mentions a neighbouring matter (another company's deal, a product's component, a general theme) does not qualify.
If none of the ten qualifies, say so. You are not judging any answer.

Return one JSON object per line:
{"question": "v4", "input_id": "<chosen or null>", "day": "...", "passage": "<= 40 words copied from the article, the decisive sentence", "why": "<= 30 words"}
