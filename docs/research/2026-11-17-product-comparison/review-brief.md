# Review of the comparison's run plan (read-only, $0)

The plan is `RUN-PLAN-v1.md` in this folder. It carries out D665, the release comparison: search `/Users/lchingen/hivemind/docs/DECISIONS-log.md` for
"## D665 ", "## D664 " and "## D663 ", and read `/Users/lchingen/hivemind/clean-arch/PRD.md` §1.5. Alex's word is: "write a run plan and monitor it
carefully and don't scope drift".

**Check it against the code it names:**
- `/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py` and its `budget_replay.py`;
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/fresh_week_inputs.py`;
- `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/stage_a.py`, whose `SETTING` uses luna;
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/pilot-deck-1/council-marking/` (the reading protocol);
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/week/brief-A1.md` and `brief-A2.md`;
- the cost and time records cited in its §6.

Do not open anything under `/private/tmp` or `~/.codex/memories`.

**Report only findings that would change what is built, run or measured**, each citing file and line:
1. Does the plan carry out D665 exactly, and nothing wider (scope drift)?
2. Will each stage run as written with the named code? Look for blockers such as:
   - run_fresh's window, configuration check or per-component logic over 82 days rather than 14;
   - the generalised article list;
   - the astra variant;
   - the judge across a long span.
3. Can the finish line move after results are seen? Check the census, the mapping, the cards, the controls and the scorer.
4. Are the monitoring and stop rules enough to catch a run going wrong early?
5. Are the estimates sound enough for the slice's 1.5-times check?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 900 words.
