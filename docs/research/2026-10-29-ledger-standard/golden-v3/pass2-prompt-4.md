Read-only task, independent reader. Repository: /Users/lchingen/hivemind-extraction-quality-2026-10-28. Do not edit any file. Read ONLY:
1. docs/research/2026-10-29-ledger-standard/standard-v2.14.md (the standard, Chinese)
2. docs/research/2026-10-29-ledger-standard/golden-v3/pass2-articles-4.json (articles about NVIDIA; the covered company is NVIDIA)
Do not open any other file (no golden, draft, batch, reference, simulation or review file).

For each article, walk the text from the first paragraph to the last and apply the standard:
- items: every statement the standard keeps (one item per matter). For each: span (an exact substring of the text, the shortest that carries the meaning), weight_current (core / supporting / optional under §6.1, the signed rule in force; write "excluded" if the signed rule does not keep it but a proposal would), tier (§5.5), and a one-line reason.
- must_open: questions the standard says this article should open (§3, §4), each with type A-E, opens_as and a one-line gist.
Answer with one JSON array and nothing else: [{"input_id": ..., "items": [...], "must_open": [...]}, ...] covering every article of the file in order.
