Read-only task. Do not edit any file in the repository; write only the output file named below. Repository: /Users/lchingen/hivemind-extraction-quality-2026-10-28.

You are an independent reader checking a golden reference. Read the standard docs/prd/05-extraction-standard.html (Chinese, signed, version 3): especially sections 3-6. Then read the 30 articles in docs/research/2026-10-29-ledger-standard/test-set/batches/batch-1.json, batch-2.json and batch-3.json. Do not read any draft-batch file, golden file, prompt, decision log or model answer.

The covered company is NVIDIA; the research list also holds macro and industry themes (poc/universe.json). Lean cautious: keep what an analyst following NVIDIA would note this week as new information; a typical claim or background line the analyst already knows is not kept unless it carries a number and a specific narrative; never miss a new increment (a named party's action is kept even without an amount, usually supporting).

For every article, from the first paragraph to the last, list the statements the standard keeps: span (an exact substring of the article text), weight (core / supporting / optional), tier, and one short reason. Also list the questions that must be opened (type A-E and gist), if any.

Write JSON to docs/research/2026-10-29-ledger-standard/test-set/blind-codex.json: [{"input_id": ..., "items": [{"span":..., "weight":..., "tier":..., "reason":...}], "must_open": [{"type":..., "gist":...}]}, ...] covering all 30 articles in batch order.
