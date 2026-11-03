You are an independent reader for an extraction evaluation. You did not write any of the prompts being compared, and you are not told which version produced which answer. Read-only: do not modify any file.

Read first, in full:
1. The signed standard: docs/prd/05-extraction-standard.html (version 3). It is the only ruler. Sections 5.1 (what is kept: the kinds), 5.3 (what is not kept), 5.4 (the meaning that must be preserved), 6 (weights), 4 (when a question opens), and 9.2 (the pass line) govern your judgement.
2. The packet: docs/research/2026-10-29-ledger-standard/final-2026-10-30/packets/gnews_1de20d5db04664ca26cc79dc.json. It holds one article (text), its frozen gold (items with weight core / supporting / optional and the meaning each must preserve; not_kept sentences with reasons; questions must_open / may_open / must_not), and several answer sets under letters. Each answer set is what production keeps from one model answer: statements (id, quote, one_line, speaker, original_day, tier) and questions.

Judge each answer set separately against the gold and the article text. Do not compare answer sets with each other and do not guess which version wrote them.

For each answer set:
- gold_items: for every gold item with weight core or supporting, give kept_by (the statement ids that carry the same matter; one matter may be carried by several statements or by a statement quoting a different sentence of the article that states the same fact) or [] when omitted; meaning: correct / partial / wrong / absent (absent when omitted), judged against the gold meaning and the article; material_problems: a list of record problems that change what an analyst would conclude (original date, period, attribution, certainty, wrong source, duplicate, unmarked inference), [] if none.
- other_statements: every statement not listed in any kept_by above, with verdict one of: optional (the gold marks that matter optional), not_kept (it states a sentence or matter the gold lists under not_kept), junk (not in the gold and the standard does not keep it), gold_missed (not in the gold but the standard clearly keeps it: name the 5.1 kind and say why in one sentence); and rule: the section of the standard you rely on.
- questions: for every question, verdict one of: must_open (it is the gold's must-open question, possibly worded differently), may_open, must_not (it is what the gold says must not open), unlisted_bad (not in the gold and fails a section 4 test: name it), unlisted_ok; settled_by_ok: true when the source and date that settle it are written and would settle it.
- must_open_raised: for each gold must_open question (by its position, 0-based), true or false.

Be strict and literal about the gold; when the gold itself looks wrong, still judge against it and add a short note in gold_doubt.

Write only JSON to your final answer, in this shape:
{"input_id": "...", "answers": {"A": {"usable": true, "gold_items": [{"k": 0, "kept_by": ["e2"], "meaning": "correct", "material_problems": []}], "other_statements": [{"id": "e5", "verdict": "junk", "rule": "5.3 ..."}], "questions": [{"id": "c1", "verdict": "must_open", "settled_by_ok": true}], "must_open_raised": [true]}}, "gold_doubt": []}
An answer set that is null is {"usable": false}.
