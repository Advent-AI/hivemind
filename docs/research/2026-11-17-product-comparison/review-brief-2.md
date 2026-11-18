# Review round 2 of the comparison's run plan (read-only, $0)

**Read:**
- `RUN-PLAN-v2.md` in this folder.
- Round 1:
  - `review-codex-1.md`;
  - the Claude reviewer's points, summarised at the top of `triage-1.md`, with my verification of each against the code.

**Governing records:**
- in `/Users/lchingen/hivemind/docs/DECISIONS-log.md`, search "## D665 ", "## D666 ", "## D505 ", "## D431 ", "## D449 " and "## D613 ";
- `/Users/lchingen/hivemind/clean-arch/PRD.md` §1.5.

**Code it names:**
- `/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py` and `budget_replay.py`;
- `/Users/lchingen/hivemind/clean-arch/step1/live.py` and `run_live.py`;
- `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/stage_a.py`;
- `/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/run_stage_b.py` and `ladder_adapter.py`;
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/reflection-6/gate1-candidate/gate1_candidate.py`;
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/fresh_week_inputs.py`;
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/week/` (brief-A1.md, brief-A2.md, tally_week.py);
- `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/pilot-deck-1/council-marking/`.

Do not open anything under `/private/tmp` or `~/.codex/memories`, or any file named `review-claude-*`.

**Report only what would change what is built, run or measured,** each with file and line:
1. Is each round-1 point resolved? Name any that are not.
2. Two decisions made here:
   - the company's own figures counted in N, with the subgroup printed beside (§1.3 item 5);
   - the exposure narrowing for the old system's sealed production replays (§1.1 item 3).

   Are they faithful to D665, D505 and D431? Argue against them if you can.
3. Anything new that would stop a stage, move the finish line after results are seen, or let a run go wrong unseen.
4. Is anything here wider than D665 requires (scope drift), or missing that D665 requires?

End with `READY` or `NOT READY: <the smallest changes>`. Keep it under about 800 words.
