You are an independent reviewer, read-only. Do not run model calls or start runs; do not write files. You have not seen this
work before; form your own view from the files, then answer. Cite files and lines.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`. Working rules `AGENTS.md` (read §2 on design tables,
§3, §4 on tests, §5, §9 on paid runs). Step 4 design: `clean-arch/step4-2026-11-10/DESIGN.md` §5.4 ("What is written, and who
reads it": the adapter's "new mode"), §6, §7.1 (state × event, including the stop rule and the due-day guard), §8 "### Stage B".
Alex's decision D429 (`docs/DECISIONS-log.md`, search "## D429"): build the adapter's ladder mode; once a review finds nothing
serious, send Stage B's three draws without asking again, capped at $2. Stage A has not passed (D426).

**What to review, before a paid send:**
- the plan of the send: `clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md`;
- the code: `clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py`, which subclasses the Stage 2 adapter
  `clean-arch/e2e-2026-11-09/adapter.py` (unchanged) and its spending limit `budget.py`;
- the tests: `clean-arch/step4-2026-11-10/stage_b/test_ladder_adapter.py`; the mutants:
  `/private/tmp/claude-501/-Users-lchingen-hivemind/f1ea972d-85a1-4f27-8010-cf0b60054109/scratchpad/mutants-stage-b/run.py`;
- the inputs: the stored ladders `poc/data/clean-ladder-stage-a-2026-11-10/run-4/send-1/outcomes.jsonl`, the cases
  `clean-arch/step4-2026-11-10/stage_a/cases.json`, the draws under `poc/data/clean-unseeded-2026-11-10/`; the frozen judge
  `src/hivemind/views/judging.py` and store `src/hivemind/views/store.py`; the ladder step's view writer
  `clean-arch/step4-2026-11-10/ladder/ladder_step.py` (`write_view`).

**Questions.**
1. Does the code do what design §5.4 and §7.1 specify for the new mode, and what `STAGE_B_RUN.md` says? Name every
   departure (for example: the ladders come from a stored file rather than a live call; the order of writes at an article;
   one commit a day; the counts' names; `created_from_input`; the `clean_ladders` columns and values against §5.4's table).
2. Walk the state × event table of §7.1 against the code: which cells does the code meet, which not, and does any matter for a
   paid run (a crash, a refused judgement, the cap, a transport failure, the due-day guard, a view with no opening evidence)?
3. The spending: is the ledger correct (each attempt's reserve and charge written under the lock; the total from the ledger;
   no attempt can be sent without a reserve line)? Is the cap of $0.66 a draw sound against the estimate, and can three
   processes at once exceed $2 in all?
4. The frozen judge and the store: does the mode change any frozen behaviour (judging, selection, theme block, quote cut,
   refusals)? Does any value the ladder mode writes reach a reader it should not (search the fields)?
5. Tests: does each test name a requirement, fail without the code under test (see the mutants), and avoid credentials and
   paid calls? What is not tested that a paid run would exercise?
6. Anything that would make the paid run's result unreadable or misleading (for example a thesis whose ladder view collides
   with another id, a theme view judged with company labels, a due day inside the window)?

End with one line: **Ready** (the three draws may be sent), or **Not ready**, with the changes needed, most serious first.
