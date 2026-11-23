# Council: do the six lines still make sense, and what should decide that the new system is ready? (read-only, $0)

You are an independent reviewer for the hivemind project, repository `/Users/lchingen/hivemind`. Read-only: edit nothing, run no model call and
start no run. Every claim cites the file and line it rests on.

**Alex** (2026-11-17), asked whether the six lines of the answer-choice gate should still block release: "what are the rules, does it make sense
now run your council to determine". He also set no budget for the product comparison and deferred the new control-line reference (D664). Your
consensus with Claude will be recorded as the decision.

**Read:**
- the decisions, searching `/Users/lchingen/hivemind/docs/DECISIONS-log.md` for:
  - "## D400 " (the six lines);
  - "## D428 " (gate 2's lines);
  - "## D484 " (use on unseen news);
  - "## D544 ", "## D560 ", "## D623 ", "## D649 ", "## D650 ", "## D656 ", "## D657 ";
  - "## D662 ", "## D663 ", "## D664 ";
- `/Users/lchingen/hivemind/clean-arch/PRD.md` §1 (the goal and the five gates, §1.5);
- `/Users/lchingen/hivemind/docs/prd/10-filing-phase.md` §1;
- `/Users/lchingen/hivemind/AGENTS.md` §7.3 ("Name the effect on the judgement first");
- in `/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/`:
  - `comparison-feasibility/RESULT.md`, with D613's correction;
  - `comparison/COMPARISON-SIZING.md`;
  - `pilot-deck-1/council-marking/RESULT.md`;
  - `reflection-9/` (the drift council, and `own-reflection.md` there).

Do not open anything under `/private/tmp` or `~/.codex/memories`.

**Answer, in order:**
1. **For each of the six lines:**
   - what product harm it guards against, and how much that harm matters to an analyst's final record;
   - whether it can be measured reliably today (reader agreement, draw-to-draw noise);
   - whether a zero-fault or fixed-count form is achievable at the measured rates.

   Then say whether it should stay a release-blocking gate, become a diagnostic that is reported, or become a code check.
2. **What should decide readiness instead,** if anything. Propose the finish line in numbers:
   - what is compared (the product comparison of D663: the new system run fresh on unread weeks 2026-07-20 to 08-24, against the old system's
     stored output for those weeks, both read as cards by the council, with Alex spot-checking splits);
   - which quantities count (for example: answers agreed supported; questions worth tracking; big matters covered; planted controls caught);
   - the margin that counts as "the new system is better", "no worse" and "worse";
   - the minimum size for the result to mean anything, given about 7 new and 15 old questions a week.
3. **Gates 2 to 5** (`PRD.md` §1.5): which still gate release, which fold into the comparison, which wait. D658 waits by Alex's word.
4. **A reconsideration point:** what result, or what amount of work, sends the direction back to Alex.
5. **Anything in the comparison design that must be settled before it runs,** so the finish line cannot move after the result is seen.

End with your proposed decision in five lines or fewer.
