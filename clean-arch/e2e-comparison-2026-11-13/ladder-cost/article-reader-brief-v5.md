# Blind reader, second pass for one question (read-only)

Repository `/Users/lchingen/hivemind`. File: `clean-arch/e2e-comparison-2026-11-13/ladder-cost/article-candidates-v5.json` (up to 25 articles in date
order, with the statements linked to the question; texts in `poc/data/items-nvda-2026-07-01-10-27.sqlite`, table `items`, column `text`).

The question: "How will server DRAM and HBM contract prices in calendar 2027 compare with calendar 2026?" Pick **the earliest article whose own
text states the level or the direction of server DRAM or HBM contract prices (or of memory contract prices generally, with server or AI demand)
with a figure, a period or a forecast**, so that an analyst could write ranges for the 2027-against-2026 change from it. If none qualifies, say so.

Return one JSON object: {"question": "v5", "input_id": "<chosen or null>", "day": "...", "passage": "<= 40 words copied", "why": "<= 30 words"}
