You are a read-only reviewer. Do not modify any file. Repository: /Users/lchingen/hivemind-extraction-quality-2026-10-28.

Scope (only this): the three schema field descriptions added for extraction prompt version 53, `FIELD_NOTES` in src/hivemind/extraction.py (search "FIELD_NOTES"), read together with what the model reads beside them: the role text src/hivemind/prompts/role-v53.txt (identical to role-v51) and the per-category lines src/hivemind/prompts/categories-v53.json. Out of scope: every other part of the prompt, the rest of the code, the measurements, and any module other than extraction.

Governing documents: the extraction standard docs/prd/05-extraction-standard.html (sections 5.3, 5.4, 5.5 and the 记录约定 block), and docs/DECISIONS.md entries D203, D220, D237, D243 (search "## D203", "## D220", "## D237", "## D243"). AGENTS.md section 6 states the prompt rules: every sentence traces to a line of the standard or a decision; a prompt serves every company (a bank, a drug maker, a retailer, a chip maker) and is never fitted to the bench or to NVIDIA; an example is an instruction and must agree with the standard, the schema and the code that reads the answer (extraction.statement_day keeps an ISO day and blanks anything else).

Report, as a numbered list, each with the exact words quoted and file:line or section:
1. For every rule inside the three descriptions: the standard line or decision it follows, or "unsourced" if none.
2. Contradictions: between a description and the standard; between a description and the role text (for example role-v53.txt line 17); between a description and any categories-v53.json line (for example how T7 or T8 assign tiers or attribution).
3. Wording fitted to one company, one industry or the bench articles.
4. Any case where following a description would remove or mislabel something the standard keeps.
5. Anything an engineer or a model could not apply from the text as written (ambiguity).
Say "none" for an empty item. Findings only; no rewrite of the prompt.
