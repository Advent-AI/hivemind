You draft golden reference entries for an extraction test set. Work in /Users/lchingen/hivemind-extraction-quality-2026-10-28. Do not edit any file except the one output file named below. Do not send any model request.

Read:
1. The standard: docs/prd/05-extraction-standard.html (Chinese, signed, version 3). It is the only rule source. Read all of it, especially section 3 (five question types), 4 (opening), 5 (evidence: 5.1 keep rule, the cautious lean and the claim rule for typical claims and background, 5.3 reject list with its boundary column, 5.4 meaning cells, 5.5 tiers), and 6 (weight). Do not read DECISIONS, prompts, other golden sets, model answers or any run's output.
2. Your batch: docs/research/2026-10-29-ledger-standard/test-set/batches/batch-N.json: articles with full text and metadata.

The covered company is NVIDIA for every article; the research list also has macro and industry themes, so a macro article can bear on NVIDIA's questions or a theme question. Lean cautious: most of a page is noise; keep what an analyst following NVIDIA would note this week as new information; a typical claim or background line that such an analyst already knows is not kept unless it carries a number and a specific narrative; never miss a new increment (a new deal, figure, decision, delay, a named party's specific action, D240: a named party's action is kept even without an amount, usually supporting).

For each article, walk the text from the first paragraph to the last and write:
- items: every statement the standard keeps or allows, one item per matter (a headline that repeats the body is the same item). Each: span (an exact substring of the article text, the shortest that carries the meaning; checked by code), kind (1-4, section 5.1), weight (core / supporting / optional, section 6), tier (fact / party_statement / third_party_view / rumour, section 5.5), who (the original speaker), meaning (only the cells that apply, section 5.4: who, what, how_much, period, condition, status = happened / plan / forecast / claim / rumour), rule (the section and sentence of the standard that decides it).
- not_kept: sentences a model might plausibly keep but the standard does not (product specs, share-price moves, typical claims and background, framing, page clutter, general verdicts), each with span, row (the 5.3 row or the 5.1 reason) and weight ("not_kept", or "optional" where section 6 makes it optional, e.g. the covered company's valuation multiple or market value, a restated past actual).
- questions: must_open (each with type A-E, opens_as, kind asset/theme, gist, settled_by, rule), may_open (another reasonable writing, or a question the standard allows but does not require), must_not (questions a model might propose that the standard rules out, with the section 4 row or test).
- notes: anything the standard did not decide clearly (quote the sentence and the two readings).
An article with nothing to keep has an empty items list; that is a valid answer.

Output: write one JSON file docs/research/2026-10-29-ledger-standard/test-set/draft-batch-N.json:
[{"input_id": ..., "items": [...], "not_kept": [...], "questions": {"must_open": [...], "may_open": [...], "must_not": [...]}, "notes": [...]}, ...]
covering every article of the batch in order. Then reply "done" with the number of articles and items.
