# Blind audit of a candidate prompt change against its signed standard (read-only)

Repository `/Users/lchingen/hivemind`. Compare `clean-arch/step1-unfiled-2026-11-08/arms/c20-system.txt`, `c20-closing.txt` and
`c20-schema.json` with the current `c8-system.txt`, `c8-closing.txt` and `c8-schema.json` (run `diff`; for the schema compare the parsed
JSON). This is version 2: version 1 was audited in `docs/research/2026-11-14-use-acceptance/main-numbers/audit-c20-blind.md`; read it and
check whether each material point is resolved (the scope beyond revenue and margin, the missing date for an item that gives none, the
growth example, measure and scope), and whether anything new is wrong. The test's scope is revenue and gross margin on purpose (D490);
the narrowing from the standard's row A is disclosed in `PROBE-DESIGN.md` beside that file and is not a finding. The change adds a fifth reason to section 3's closed set (`main_driver`: the company's main annual quantity as a question) and
rewrites one row of the do-not-open list. The decisions on this boundary are D382, D384 and D490 in `docs/DECISIONS-log.md` (read them; D490
opens this as a test, for revenue and margin). Read the whole changed request as the model reads it (system text, then the closing check,
then every schema description), and the signed standard `docs/prd/05-extraction-standard.html` §3 (the table of question types, row A
"主驱动量", and "问题怎么写") and §4 (the opening tests and "同一题、续期，还是另一题" in full).

Report, sentence by sentence of the change: consistent / contradicts / keeps wider / keeps narrower / no source, quoting the standard's
line or the decision. Then:
1. Does the change contradict any other sentence of the request? Check at least: the role paragraph; section 2's CONDITION bullet ("inform
   an open thesis about its revenue or earnings path"); "A thesis asks one quantity for one period, or one event"; the date rule ("Give the
   date the item supports …"); the do-not-open rows "another estimate, source or wording of what an open thesis tracks" and "an annual
   quantity after next year"; `closest_open_thesis` and `why_a_separate_bet`; every sentence of the closing check that speaks of figures,
   conditions or reasons.
2. Do the examples read the same for any industry, name no covered company, product or number, and agree with the standard and the schema?
3. Could the new text make the model (a) open a question on every statement line it meets (EPS, net income, cash flow, a small segment),
   (b) open a question for a quarter or for a year after next fiscal year, (c) open two questions for one quantity and year (its level and
   its growth; the total and its main segment), (d) open a question on another company's figures, or (e) stop opening what the other four
   reasons open? Name the words that would do it, and the smallest wording that would stop it without adding a rule the standard lacks.
4. Is anything the model needs to write such a question missing from the request (which measure, which fiscal year, the settling
   material, the date)?

Out of scope: other prompts; changing the standard; whether the test should be run at all.
