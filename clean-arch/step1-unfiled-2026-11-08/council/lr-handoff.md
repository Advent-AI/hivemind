You are an independent reviewer, read-only. Do not run model calls, start runs, or write files. Cite files and lines.

Context: repository `/Users/lchingen/hivemind`, branch `clean-arch`; rules in `AGENTS.md` (§2 incl. "No case-fitted fix", §6
prompts incl. "move the rule to its owner" and "Never grow a prompt to fix quality", §7.3 incl. "Several fixes on one base are each
proved on stored data in minutes and then run together once", "Small first", "Name the effect on the judgement first"). Alex chose
(D434 in `docs/DECISIONS-log.md`): finish diagnosing Step 1's other defects, then combine the changes into one version; the plan goes
to him before any send. c8 stays in force (D387, D391; c14 stopped, `clean-arch/step1-diagnosis-2026-11-12/STAGE1-RESULT.md`).

The plan (version 2, after a review that said not ready: `clean-arch/step1-unfiled-2026-11-08/council/lq-codex.md`): `clean-arch/step1-diagnosis-2026-11-12/COMBINED-PLAN.md`. Check first that each finding of lq-codex.md is closed. Its evidence: `DIAGNOSIS.md`, `STAGE1-RESULT.md`, the blind shape
readings in `second-thing/` (`packet.json`, `reader-brief.md`, `reader-codex.jsonl`, `reader-claude.jsonl`, `my-classification.json`),
Stage A's per-thesis table `clean-arch/step4-2026-11-10/stage_a/result-4/tables.txt`, the stored c8 runs
`poc/data/clean-unseeded-2026-11-10/draw-d*/trace.sqlite` (read-only; reasoning in `raw_response`), c8's files
`clean-arch/step1-unfiled-2026-11-08/arms/c8-*`, the frozen standard `docs/prd/05-extraction-standard.html`, decisions D38, D386,
D388–D391, D397.

Challenge:
1. Is each of the three defects real and counted right on the cited data (the 9 aggregate citations and the 1 collision; the
   16-versus-26 crossing)? Does the evidence support the cause stated for each?
2. Is each change sourced (the standard, a decision, c8's own text), general across companies, and the smallest lever for its
   defect? Could change 3 (the `outcome` schema description) suppress theses c8 rightly opens, or move error to the description?
3. Are the proofs' pass and stop lines adequate and fixed before results; is anything missing (controls, variation, cost)?
4. Is anything larger missing from the plan, or should one of the three not be in it?

End with one line: the plan is ready to put to Alex (yes / yes with changes / no).
