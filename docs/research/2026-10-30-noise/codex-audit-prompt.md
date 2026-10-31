You are auditing an LLM extraction prompt against the written standard it must carry. Read-only: do not edit any file.

Repository: /Users/lchingen/hivemind-extraction-quality-2026-10-28 (branch fix/extraction-quality-2026-10-28).

THE STANDARD (the only ruler): docs/prd/05-extraction-standard.html, version 4 (signed; Chinese). Sections 2–6 govern the extraction call:
§2 what the ledger records, §3 the question classes, §4 the opening tests and the not-open list, §5 the evidence standard (5.1 the keep rule and
the four kinds, 5.2 incomplete evidence, 5.3 the not-kept table with its "boundary" column, 5.4 the meaning a record must keep, 5.5 source tiers),
§6 weight (judged only in evaluation, not by the model). Also read the "一张图" flow near the top and the 12 + 7 decided items.

THE PROMPT (exactly what the model reads for one item, production configuration poc/config/poc-v69.json, version 53):
- the system text: src/hivemind/prompts/role-v53.txt
- the per-category blocks inserted into the user message: src/hivemind/prompts/categories-v53.json ("what" and "read" for T1–T11)
- the fixed sentences of the user message: function _build_prompt_english in src/hivemind/extraction.py
- the response schema: field descriptions FIELD_NOTES (version 53) and the enums, in src/hivemind/extraction.py (base_schema, admission_schema, schema_for)
- two complete requests as sent, for reference: docs/research/2026-10-30-noise/request-t7.txt (news) and request-t8.txt (analysis)

TASK
1. Go through the prompt sentence by sentence (split a sentence into clauses when its clauses say different things; include every example).
   For each, quote it, quote the standard line(s) it traces to (with section), and classify it as exactly one of:
   CONSISTENT; CONTRADICTS (the prompt decides by a different test or says the opposite); WIDER (keeps or opens more than the standard);
   NARROWER (keeps or opens less); NO-SOURCE (no standard line); EXAMPLE-DISAGREES (an example the standard or its table would decide differently).
   Pay special attention to: what decides keep versus reject (the procedure), escape clauses ("unless ...", "even when ..."), carve-outs,
   definitions that make a class broad ("a size, date or name"), and the order in which the model is told to apply rules.
2. Reverse direction: every rule of §2–§5 that applies to the extraction call and is absent from the prompt, or present only in weaker form.
   Include each row of the 5.3 table and its boundary column, the optional items, the 5.4 cells, the 5.5 table, the §4 tests and not-open list.
3. Contradictions inside the prompt itself (two prompt sentences that pull opposite ways).

Out of scope: matching, judging, placement, the code checks after the answer, weights (§6 is evaluation only). The D248 changes to opening
(§3 class C, §4) are in scope for listing but mark them "opening — next step".

OUTPUT: a markdown report. Part A: a table, one row per prompt clause (id, quote, standard line, class, one-sentence reason). Part B: the
missing or weakened rules. Part C: internal contradictions. Part D: the five findings most likely to change which statements are kept, ranked,
each with one sentence on the mechanism. Quote exactly; do not paraphrase the standard. If unsure, say so.
