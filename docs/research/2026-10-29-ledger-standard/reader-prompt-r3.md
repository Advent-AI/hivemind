You are an independent reader testing whether a written standard is clear enough that different readers reach the same classifications. Read ONLY these files (do not read anything else in the repository: no other standard version, simulation file, log, reference, gold, prompt or decision file; the point is to test the standard on its own):

1. docs/research/2026-10-29-ledger-standard/standard-v2.3.md  (the standard, in Chinese)
2. the case files in the same folder: sampled-statements.json, cases-v1.json, sampled-statements-r2.json, cases-r2.json, sampled-statements-r3.json, cases-r3.json
3. docs/research/2026-10-29-ledger-standard/r3-ids.json: the exact list of case ids to answer (111 statements, 12 questions). Answer exactly those ids.

Context for the cases:
- S, T, U, B ids are sentences or statements from NVIDIA news and blog pages; the covered company is NVIDIA. Some are page clutter or unrelated text; classify them as the standard says.
- X, Y, Z ids are statements from other industries; the covered company is the company the statement is about.
- Q ids are candidate questions about NVIDIA (and Q17/Q18 about the bank and the drug maker); P and R ids are candidate questions about the company each names, which is the covered company. Unless a case says otherwise, assume no question is open yet in the library except where the case text says one is open. The covered universe is NVIDIA plus the companies the X, Y, Z, P and R cases are about; AMD, Alphabet and Sharon AI are not covered. Assume each question comes from an article published in July 2026 (NVIDIA's fiscal year FY2027 ends late January 2027; FY2028 ends late January 2028; other companies' fiscal years are calendar years).

For every statement decide, by the standard alone:
- keep: true or false
- if false: reject_row = which row of §5.3 (quote its first words; for the first layer write "第一层")
- if true: kind = 1, 2, 3 or 4 (§5.1); weight = core, supporting or optional (§6); tier = fact, party_statement, third_party_view or rumour (§5.5); driver = which of the seven drivers or "市场预期与估值" (§1)
- section and a one-sentence reason

For every question decide:
- open: true or false
- if true: type = A, B, C, D or E (§3.1); opens_as; kind = asset or theme
- if false: not_open_row (quote the §4.3 row), or failed_test (§4.2), or same_as (another question id)
- a one-sentence reason

Then list every place where the standard was ambiguous, silent, or contradicted itself for some case: case id, sections, the two readings.

Answer with one JSON object and nothing else:
{"statements": [{"id": ..., "keep": ..., "reject_row": ..., "kind": ..., "weight": ..., "tier": ..., "driver": ..., "section": ..., "reason": ...}, ...],
 "questions": [{"id": ..., "open": ..., "type": ..., "opens_as": ..., "kind": ..., "not_open_row": ..., "failed_test": ..., "same_as": ..., "reason": ...}, ...],
 "ambiguities": [{"case": ..., "sections": ..., "readings": ...}, ...]}
Use null for fields that do not apply.
