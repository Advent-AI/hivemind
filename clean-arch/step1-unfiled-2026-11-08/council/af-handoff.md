# Council: complete review of the proposed final configuration before freezing (independent; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs. Read cold.
Repository /Users/lchingen/hivemind. Read AGENTS.md (§§1–7) and `.claude/skills/council-loop/SKILL.md` first. Do NOT read
`council/af-claude.md` until your answer is written.

Alex's decisions in force: D380–D386 in `docs/DECISIONS-log.md` (K6b + DeepSeek with one retry, cut answers included; Step 2's three
lines; figures are conditions and a thesis is a view with a reason; material statements with no home are kept unlinked and linked later;
theses only for the signed standard's big matters as the frozen gold applies it; target prices and valuation conclusions not kept;
acceptance on fresh articles read by readers against the source). Alex, today: every decision in this goal goes through the council.

The proposed final configuration:
- Step 1 prompt `clean-arch/step1-unfiled-2026-11-08/arms/c7-system.txt`, `c7-closing.txt`, `c7-schema.json`; settings DeepSeek Flash,
  high effort, 64k output cap;
- runner `clean-arch/step1/runner.py` with `test_runner.py`;
- Step 2 `clean-arch/step2/compare.py` and `run_forward.py`; Step 3 `clean-arch/step3/library.py`; with their tests;
- measurement tools `clean-arch/step2-validation-2026-11-07/map_reference.py`, `build_merge_packets.py`, `score_final.py`,
  `clean-arch/step1-unfiled-2026-11-08/build_question_packets.py`, `tally_questions.py`.
- Evidence so far: `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§22–39; stored runs under `poc/data/clean-step1-unfiled-2026-11-08/`
  (test-c7-flash; the c7 dev run may still be running, so treat it as partial) and `poc/data/clean-step2-forward-c*-2026-11-08/`.
- The signed standard `docs/prd/05-extraction-standard.html` (§§3–5) and the frozen gold are the references.

Deliver in English, under 1,000 words:
1. Every contradiction between the c7 request (all of it, including unchanged K6b text) and D380–D386 or the standard, with the clause
   quoted and the fix.
2. Every downstream check that could silently do the wrong thing (keep, link, merge, later-link, map, score), with the evidence that
   would show it, at no or low cost on stored data.
3. What must be verified before freezing, at least cost, and what can wait.
4. The acceptance protocol to fix before choosing any article: which fresh NVDA articles (the source is
   `poc/data/items-nvda-2026-07-01-10-27.sqlite`; dev is 2026-07-01..07-14 and test 2026-09-01..10-24), how many, how the starting library
   is set, what readers judge and how, the pass criteria in numbers derived from the agreed lines, the by-design misses stated in
   advance, and the dev repeats for stability.
5. Anything in the current state that you would revert now.
Facts and hypotheses kept apart, with files and lines.
