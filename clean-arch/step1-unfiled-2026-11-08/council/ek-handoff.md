Council review, read-only, fresh reader. Repository /Users/lchingen/hivemind, branch clean-arch.

Read `clean-arch/step1-unfiled-2026-11-08/council/ej-claude.md`, a plan for the clean system's first end-to-end measurement. Verify it
against the primary sources it cites:
- `docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py`;
- `scripts/replay.py`;
- `src/hivemind/views/judging.py`, `store.py` and `round.py`;
- `src/hivemind/seeding.py`;
- `clean-arch/step2/run_forward.py` and `clean-arch/step3/library.py`;
- `docs/prd/10-filing-phase.md`;
- AGENTS.md §§5 and 7;
- D370 and D391 in `docs/DECISIONS-log.md`;
- `docs/research/2026-11-04-filing-end-to-end/` (diagnosis.md, oracle-design.md, acceptance-measure.txt).

Out of scope: changing the frozen ruler, judge or c8.

Answer, under 500 words:
1. Is each stage necessary and correctly ordered? Is Stage 1 decisive for what it claims?
2. Is the adapter contract faithful to how production feeds the judge (seq per day, evidence selection, quote shape, dependencies)? Name
   any mapping that would bias the score.
3. Are the pass and fail lines sound against the ruler's own noise (readers A and B differ on 3 of 23)?
4. What is missing, wrong or overclaimed?
5. Does the plan respect every constraint: same-day control, frozen pieces, D370, who authorizes what?

End with READY TO PUT TO ALEX, READY WITH CHANGES, or NOT READY.
