# Reflection council K (cold read, read-only, $0)

You are reviewing a research line cold. Read in this order:
1. `docs/research/2026-11-20-hybrid/PLAN.md`;
2. `docs/research/2026-11-20-hybrid/DESIGN-J2.md`, all of it;
3. `docs/research/2026-11-20-hybrid/census/CENSUS.md`;
4. `poc/data/hybrid-2026-11-20/diag-score-H1.json`;
5. `docs/research/2026-11-19-merge-council/RESULT.md`, the section "Where the old system loses on the 32 matters";
6. in `docs/DECISIONS-log.md`, the records D198, D382, D439 and D681–D684 (search `## D198`, and so on).

**The goal (Alex, D681):** build and test a hybrid of the old and new systems that serves an analyst better than the old one. Problems
must be found early, not at the end.

**Answer, in under 350 words:**
1. **The lessons**, at the level of mechanism.
2. **Which conclusions are weaker than they look.**
3. **The remaining problems, ranked by product impact on the 32 matters.**
4. **The one next angle and its falsifier.** Choose between:
   - continuing the judge line within D198, for example placing the previous conclusion before the evidence;
   - taking D198's options to Alex;
   - starting phase 2, the census of the 17 never-opened matters;
   - something else.

   Say what result would change the plan.

**Out of scope:**
- changing the frozen ruler or gold;
- the c8 reading arm;
- anything that pushes, deploys or commits.

End with `CONSENSUS-READY: <one sentence>` or `OPEN: <the disagreement>`.
