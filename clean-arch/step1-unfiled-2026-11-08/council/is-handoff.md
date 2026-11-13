# Council is: read of the built ladder step and its Stage A runner, before the first paid run of the built code (read-only)

Do not edit files, run model calls or start runs. You may run the two test files (they reach no network).

Context: `clean-arch/step4-2026-11-10/probe-2026-11-10/READING-claude.md` (one page) and decisions D397 to D407 in
`docs/DECISIONS-log.md`. By D407 the step uses the request as first sent in the probe (`clean-arch/step4-2026-11-10/ladder/candidate-system.txt`,
`candidate-closing.txt`, `candidate-schema.json`), and code refuses and sends back once: a reference whose words are not the
article's (D405), a theme's state named with a company label (D404), a question that says "this item" (D407). The design the code
follows is `clean-arch/step4-2026-11-10/DESIGN.md` §5.3 (checks 1 to 8) and §8 ("Stage A": the cap, one stop for all workers, the
spend on disk, a case and its files, three sends as three samples). Where the design still describes fields of an answer shape
that D407 dropped (`named`, `main`, `company_states`, `theme_states`), D407 governs: the schema has one `states` field.

Read:
- `clean-arch/step4-2026-11-10/ladder/ladder_step.py`, `model_calls.py`, `test_ladder_step.py`;
- `clean-arch/step4-2026-11-10/stage_a/stage_a.py`, `build_cases.py`, `test_stage_a.py`;
- the production code they call: `src/hivemind/model.py` (`call`, `build_request`, `check_schema`, `Archive`),
  `src/hivemind/extraction.py` (`repair_quote`, `normalise`, `beyond_next_year`, `BINDING_HORIZON_DAYS`),
  `src/hivemind/universe.py`, `clean-arch/e2e-2026-11-09/budget.py`.

Answer in under 700 words, most serious first, each with file and line:
1. **Would Stage A misstate what happened?** Any path by which a send is counted twice or not at all, an outcome row is written
   for the wrong case or pass, an answer comes from a cache unnoticed, a cost is missed, or the cap can be passed.
2. **Would a check accept a wrong answer the design says it refuses, or refuse a right one?** Walk checks 1 to 6 in
   `check_answer` against §5.3. In particular the order of the checks, the early returns, and what `write_view` does with an
   answer `check_answer` accepted.
3. **The text the model is sent on a refusal:** `RESEND_NOTE` and every reason string in `check_answer`. Does any reason tell the
   model something the request contradicts, or fail to tell it what to do? Is any fitted to the covered company or a test article?
   (AGENTS.md §6.) Quote the string and give the words you would use.
4. Anything in the tests that asserts less than its name says (a test that would pass with the code under test removed).
First line: "run the slice" or "hold", with the one thing to change first.
