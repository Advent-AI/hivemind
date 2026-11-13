# Council gm: review of the Step 4 design, version 3 (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 3), with the drafts
`clean-arch/step4-2026-11-10/ladder/candidate-system.txt` and `candidate-schema.json`. Read `AGENTS.md` first (§1, §2, §6 and §7
govern a design and its test). Open the code and the data behind every claim you rely on.

## What is already known, do not report

- The design is not READY as a whole: its core contract waits for Alex's answers to C1 and C2 (§4). The request and the schema are
  drafts for the recommended options; their whole-request audit follows his answers.
- The previous reviewer's verdict on version 2 is `clean-arch/step1-unfiled-2026-11-08/council/gl-codex.md`. Version 3 claims to
  answer every finding of it that does not depend on Alex.

## Your question

For everything that does **not** depend on C1 and C2, is version 3 sound enough that, once Alex answers, only the request audit
remains before a build? Answer by angle:

1. **gl's findings.** For each of gl's six findings, is it answered? Quote what is still missing.
2. **The choices (§4).** Are C1 and C2 stated fairly and completely, with what the decisions favour named and each option's cost
   given? Would a product owner reading only §4 and the example in §1 understand what he is choosing? Is any item under "behaviour
   this design takes from production or a decision" misdescribed? Check D38, D186, D248, D368 item 1 and D191 in
   `docs/DECISIONS-log.md`.
3. **State × event (§7.1).** Name each reachable state-event pair that has no row, a wrong row, or no stated date. Check the rows
   against `src/hivemind/views/judging.py`, `store.py` and `clean-arch/e2e-2026-11-09/adapter.py`.
4. **Value × reader (§5.4) and new path × old checks (§7.3).** Search the code for each value's readers and each old check
   (`src/hivemind/extraction.py` `sift`). Name what is missing or wrong.
5. **Checks (§5.3) and the schema.** Is each check sourced as cited? Do the schema's two shapes, the checks and the label rule fit
   together for every rung shape (yes/no; five states of a company event; five states of a theme event; a company figure; a theme
   figure)? Give a concrete answer that passes the schema and the checks and is still a wrong ladder.
6. **The test (§8).** Can Stage A and Stage B each fail? Is any line impossible, unfalsifiable, or unfair to an arm? Are the
   denominators complete? Is the description of the ten fresh theses' exposure accurate
   (`clean-arch/step1-unfiled-2026-11-08/ACCEPTANCE-PROTOCOL.md`; round log §§42–43)?
7. **Facts.** Check six factual claims of §2 against `clean-arch/step4-2026-11-10/census/` (`production_ladders.txt`, `tally.py`
   with `reader-codex.jsonl` and `reader-claude.jsonl`) and the code. List any that are wrong or overstated.

Out of scope: the frozen ruler, the frozen production prompts and judge (a defect in them is a finding, never an edit), c8, Step 2
and Step 3, `clean-arch/step2-validation-2026-11-07/LOG.md`, `reports/step2-*`, the frontend.

## Deliver

First line: for the parts that do not depend on C1 and C2, one of CLEAN, CHANGES NEEDED, or SERIOUS FINDINGS. Then the findings, most
serious first, each with its file and line and what a complete fix must contain; wording-level points in a short list at the end.
Under 1,200 words.
