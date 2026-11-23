You are an independent reviewer, read-only. Do not run model calls or start runs; do not write files. You have not seen this
work before; form your own view from the files, then answer. Cite files and lines.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`. Working rules `AGENTS.md` (read §2 on design tables,
§3, §4 on tests, §5, §9 on paid runs). Step 4 design: `clean-arch/step4-2026-11-10/DESIGN.md` §5.4 ("What is written, and who
reads it": the adapter's "new mode"), §6, §7.1 (state × event, including the stop rule and the due-day guard), §8 "### Stage B".
Alex's decision D429 (`docs/DECISIONS-log.md`, search "## D429"): build the adapter's ladder mode; once a review finds nothing
serious, send Stage B's three draws without asking again, capped at $2. Stage A has not passed (D426).

**This is the sixth review.** Five earlier reviewers found the build not ready (`council/ko-codex.md` to `kt-codex.md`). The
fifth (`kt-codex.md`) found one serious point: a crash between writing a terminal failure to `run.json` and writing the stop to
the ledger could let a later launch start the redo. Since then a terminal stop reaches the ledger before the attempt reaches
`run.json` (`run_stage_b.py`, the exception path), with a test that kills the process at that write and checks a later launch
sends nothing (`test_a_crash_right_after_a_terminal_stop_cannot_lead_to_a_redo`) and a mutant that reverses the order; a
thesis with no ladder keeps the model's answer and reason in `checked_answer`; the mutant count is corrected (20 mutants and the
control, `stage_b/mutants.output.txt`). 27 tests. Review the files as they now stand, cold, then check each point of the fifth
review.

**What to review:**
- the plan of the send: `clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md`;
- the code: `clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py` and `run_stage_b.py`, over the unchanged Stage 2 adapter
  `clean-arch/e2e-2026-11-09/adapter.py` and `budget.py`;
- the tests `stage_b/test_ladder_adapter.py`, the mutants `stage_b/mutants.py` and `stage_b/mutants.output.txt`;
- the inputs as before (`poc/data/clean-ladder-stage-a-2026-11-10/run-4/send-1/`, `stage_a/cases.json`, the draws under
  `poc/data/clean-unseeded-2026-11-10/`), the frozen judge `src/hivemind/views/judging.py` and store `src/hivemind/views/store.py`.

**Questions.**
1. Is each point of the fifth review closed? One by one: closed, partly or not, with the line that shows it.
2. Can the paid send spend past $2 in any ordinary case (a crash, a redo, a second launch, threads inside the judge)?
3. Does anything in the code or plan make the paid run's result unreadable, misleading, or different from design §5.4, §7.1 and
   §8 in a way that matters?
4. Is anything serious left? If only refinements remain, or limits already disclosed (a billing cap that rests on the
   reservation covering the charge; identity by case name; no test that kills a live process), say so plainly: this is the
   sixth round on this build.

End with one line: **Ready** (the three draws may be sent), or **Not ready**, with the changes needed, most serious first.
