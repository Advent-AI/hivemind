You are an independent reader testing whether a written standard is clear enough that different readers reach the same classifications. Read ONLY these two files (do not read anything else in the repository, do not look at any other reference, gold, prompt or decision file; the point is to test the standard on its own):

1. docs/research/2026-10-29-ledger-standard/standard-v2.1.md  (the standard, in Chinese)
2. the cases: docs/research/2026-10-29-ledger-standard/sampled-statements.json, cases-v1.json, sampled-statements-r2.json and cases-r2.json (all in that folder)

Context for the cases:
- S01–S42 (sampled-statements.json) are sentences sampled from news and blog pages about NVIDIA; the covered company is NVIDIA. Some are page clutter or unrelated text; classify them as the standard says.
- B01–B26 are statements from NVIDIA articles; the covered company is NVIDIA.
- T01–T42 (sampled-statements-r2.json) are sentences sampled from other NVIDIA news and blog pages; the covered company is NVIDIA.
- X01–X16 (cases-v1.json) and Y01–Y12 (cases-r2.json) are statements from other industries; the covered company is the company the statement is about (the bank, the drug maker, the retailer, the airline, the utility, the miner, the insurer, the software vendor).
- Q01–Q22 (cases-v1.json) and P01–P10 (cases-r2.json) are candidate questions an extractor proposed. For P01–P10 the covered company is the company the question is about. Unless a case says otherwise, assume no question is open yet in the library except where the case text says one is open. The covered universe is NVIDIA plus the companies named in X01–X16; AMD, Alphabet and Sharon AI are not covered companies. Assume each Q comes from an article published in July 2026 (NVIDIA's fiscal year FY2027 ends late January 2027; FY2028 ends late January 2028).

For every statement (S, T, B, X, Y) decide, by the standard alone:
- keep: true or false
- if false: reject_row = which row of §5.3 (quote its first words), or "not a statement" for page clutter
- if true: kind = 1, 2, 3 or 4 (§5.1); weight = core, supporting or optional (§6); tier = fact, party_statement, third_party_view or rumour (§5.5); driver = which of the seven drivers (§1) makes it matter, or "none"
- section: the section numbers you relied on
- reason: one sentence

For every question (Q) decide:
- open: true or false
- if true: type = A, B, C, D or E (§3.1); opens_as; kind = asset or theme
- if false: not_open_row = which row of §4.3 (quote its first words), or failed_test = which §4.2 test fails, or same_as = which other question it is the same as
- reason: one sentence

Then list every place where the standard was ambiguous, silent, or contradicted itself for some case: for each, the case id, the sections involved, and what two readings were possible.

Answer with one JSON object and nothing else:
{"statements": [{"id": "S01", "keep": ..., "reject_row": ..., "kind": ..., "weight": ..., "tier": ..., "driver": ..., "section": ..., "reason": ...}, ...],
 "questions": [{"id": "Q01", "open": ..., "type": ..., "opens_as": ..., "kind": ..., "not_open_row": ..., "failed_test": ..., "same_as": ..., "reason": ...}, ...],
 "ambiguities": [{"case": ..., "sections": ..., "readings": ...}, ...]}
Cover all 138 statements and all 32 questions. Use null for fields that do not apply.
