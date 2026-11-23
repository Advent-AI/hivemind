# Retro council: review the changes made without a council round (independent; read-only)

You are Codex, the second member of a council with Claude Code. Read-only: do not edit files, run model calls or start runs. Read the
record cold; do not assume Claude's conclusions are right. Repository /Users/lchingen/hivemind. Read AGENTS.md (§§1–7, 9) and
`.claude/skills/council-loop/SKILL.md` first.

Alex asked whether these changes were council-reviewed before they were made. Several were not. Review each and say whether it should
be kept, revised or reverted, with evidence from the files.

Read: `clean-arch/step1-unfiled-2026-11-08/LOG.md` §§22–38 (the night's round); the arms `clean-arch/step1-unfiled-2026-11-08/arms/c2-*`,
`c4-*`, `c5-*`, `c6-*`, `c7-*` (diff each against the previous); `clean-arch/step1/runner.py` and `test_runner.py` (git diff); 
`clean-arch/step2/compare.py`, `run_forward.py`, `clean-arch/step3/library.py` and their tests (git diff); 
`clean-arch/step2-validation-2026-11-07/map_reference.py`, `build_merge_packets.py`; the signed standard
`docs/prd/05-extraction-standard.html`; Alex's decisions in LOG §§11, 16, 17, 27, 36. Do NOT read `council/ae-claude.md` until your first
answer is written.

The changes made without a council round before the send:
1. c4 prompt (D209 second amendment wording; closing read-back "not returned"; closing row 6 valuation changed to "not kept").
2. c5 one-party rule and c6's narrowed version; the 64k output cap.
3. Runner: a cut answer treated as a format failure (retried once); an existing test changed on the claim that it misread Alex's rule.
4. Step 2: the clean Jev piece criteria ("main statement"); the tightened later-linking criteria; numbering by manifest position;
   reference mapping by input id.
5. Measurement: carried verdicts for identical merge pairs; one reader per question measure; the test scored for five configurations
   in sequence.

Deliver in English, under 900 words:
1. For each change: is it sourced (Alex's words, the standard, a decision), general (not fitted to the cases that motivated it), and did
   it break anything that was right? Keep / revise / revert, with file and line evidence.
2. Which reported results are not trustworthy because of how they were measured (selection on test, tuning and judging on the same
   cases, one draw), and what would make them trustworthy at least cost.
3. Process errors, ranked, and the structural rule for each that would have caught it.
4. The one next step you would take before any further run.
Facts and hypotheses kept apart.
