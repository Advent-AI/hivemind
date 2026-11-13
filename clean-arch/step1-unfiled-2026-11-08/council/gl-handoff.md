# Council gl: review of the Step 4 design, version 2 (fresh reviewer; read-only: do not edit files, run model calls or start runs)

You have not seen this work before. Review `clean-arch/step4-2026-11-10/DESIGN.md` (version 2) as a design that must be READY before
any code is written. Read `AGENTS.md` first (§1, §2, §6 and §7 govern a design and its test). Do not assume the design's claims are
right: open the code and the data behind every claim you rely on.

## Scope

- In scope: the design page; the draft request `clean-arch/step4-2026-11-10/ladder/candidate-system.txt`; the census files in
  `clean-arch/step4-2026-11-10/census/` (packet, reader brief, `production_ladders.py` and its output, `tally.py`,
  `reader-codex.jsonl`).
- Governing documents: Alex's decisions in `docs/DECISIONS.md` and `docs/DECISIONS-log.md` (D38, D46, D185, D186, D191, D195, D198,
  D248, D260, D354, D356, D359, D368, D370, D378, D382–D396); `docs/prd/11-production-experiments-from-split.md` (E3, E4);
  `clean-arch/PRD.md` §§1–7 and §12; the earlier verdict `clean-arch/step1-unfiled-2026-11-08/council/gg-codex.md` (its four
  blocking items).
- Code the design leans on: `src/hivemind/extraction.py` (`sift`, `check_ladder`, `check_bounds`, `check_admission`,
  `beyond_next_year`), `src/hivemind/views/judging.py`, `store.py`, `matching.py` lines 320–340, `src/hivemind/universe.py`,
  `clean-arch/e2e-2026-11-09/adapter.py`, and the sealed split's `ordered_ladder`, `render`, `empty_rung` in
  `/Users/lchingen/hivemind-no-preseed-evidence-review/src/hivemind/split.py`.
- Out of scope: the frozen ruler, the frozen production prompts and judge (report a defect in them as a finding, do not propose an
  edit), c8, Step 2 and Step 3, `clean-arch/step2-validation-2026-11-07/LOG.md`, `reports/step2-*`, the frontend.
- Known to be pending, do not report: the second blind reader's column in §2.1 and the third reader's decisions; the whole-request
  audit of the draft request, which follows Alex's answers to C1 and C2.

## Angles (answer each)

1. **The earlier blocking items.** For each of gg's items 1–3, is it now answered completely? Quote what is still missing.
2. **Facts.** Check at least eight factual claims of §2 and §5 against the code or the stored data (name the file and line). List any
   that are wrong or overstated.
3. **State × event (§7.1).** Walk a thesis through every state against: success, a refusal, a refused retry, a transport failure, a
   crash midway, a run that ends with work in flight, a later run on a later date, changed configuration, another writer, two
   theses at once. Name each cell that is blank, wrong, or names no date.
4. **Value × reader (§5.4) and new path × old checks (§7.3).** Search the code for each value's readers. Name a reader the table
   misses and an old check the new path fails without saying so.
5. **Rules and their sources.** For each sentence of the draft request and each code check of §5.3: is it sourced to a decision or a
   production rule, or is it a new rule? Is any rule wider or narrower than its source? Is anything in the request fitted to the
   covered company or to the test articles?
6. **Could an engineer build §5 from the text alone?** Name each place where two engineers would build different things.
7. **The test (§8).** Can Stage A and Stage B each fail? Are the denominators complete? Is any line unfalsifiable, unfair to an arm,
   or decided by a number with no basis? Does the hold-out really lie outside what tuned anything?
8. **The choices for Alex (§4).** Are C1 and C2 stated fairly, with the option the decisions favour named? Is anything listed as
   "settled by existing decisions" really a choice that changes what the system does?

## Deliver

A verdict on the first line: READY, READY WITH CHANGES, or NOT READY. Then the findings, most serious first, each with its file and
line and what a complete fix must contain. Keep wording-level points in a short list at the end. Under 1,300 words.
