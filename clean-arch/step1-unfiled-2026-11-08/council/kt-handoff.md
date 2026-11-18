You are an independent reviewer, read-only. Do not run model calls or start runs; do not write files. You have not seen this
work before; form your own view from the files, then answer. Cite files and lines.

**Context.** Repository `/Users/lchingen/hivemind`, branch `clean-arch`. Working rules `AGENTS.md` (read §2 on design tables,
§3, §4 on tests, §5, §9 on paid runs). Step 4 design: `clean-arch/step4-2026-11-10/DESIGN.md` §5.4 ("What is written, and who
reads it": the adapter's "new mode"), §6, §7.1 (state × event, including the stop rule and the due-day guard), §8 "### Stage B".
Alex's decision D429 (`docs/DECISIONS-log.md`, search "## D429"): build the adapter's ladder mode; once a review finds nothing
serious, send Stage B's three draws without asking again, capped at $2. Stage A has not passed (D426).

**This is the fifth review.** Four earlier reviewers found the build not ready (`council/ko-codex.md`, `kp-codex.md`,
`kq-codex.md`, `ks-codex.md`), the last three on the stop paths. After the fourth, the stops follow one rule instead of case-by-
case fixes: the first stop of any kind (the cap refusing a request, a draw ending incomplete, a redo left unfinished by a crash)
is written to the ledger under the limit's lock before it is raised (`LedgerBudget._stop`, `ledger_stop`), so no other judge
thread sends after it; a limit built later on the same ledger starts stopped and the launcher sends nothing (`run_stage_b.py`,
`Stopped`); any incomplete draw ends the send; the design's one redo is the only second chance. 26 tests, 19 mutants
(`stage_b/mutants.output.txt`), and a $0 replay of the whole send with a judge that always picks the last rung (three draws
complete). Review the files as they now stand, cold, then check each finding of the fourth review.

**What to review:**
- the plan of the send: `clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md`;
- the code: `clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py` and `run_stage_b.py`, over the unchanged Stage 2 adapter
  `clean-arch/e2e-2026-11-09/adapter.py` and `budget.py`;
- the tests `stage_b/test_ladder_adapter.py`, the mutants `stage_b/mutants.py` and `stage_b/mutants.output.txt`;
- the inputs as before (`poc/data/clean-ladder-stage-a-2026-11-10/run-4/send-1/`, `stage_a/cases.json`, the draws under
  `poc/data/clean-unseeded-2026-11-10/`), the frozen judge `src/hivemind/views/judging.py` and store `src/hivemind/views/store.py`.

**Questions.**
1. Is each finding of the fourth review closed? One by one: closed, partly or not, with the line that shows it.
2. Can the paid send spend past $2 in any ordinary case (a crash, a redo, a second launch, threads inside the judge)?
3. Does anything in the code or plan make the paid run's result unreadable, misleading, or different from design §5.4, §7.1 and
   §8 in a way that matters?
4. Is anything serious left? If only refinements remain, or limits already disclosed (a billing cap that rests on the
   reservation covering the charge; identity by case name; no test that kills a live process), say so plainly: this is the
   fifth round on this build.

End with one line: **Ready** (the three draws may be sent), or **Not ready**, with the changes needed, most serious first.
