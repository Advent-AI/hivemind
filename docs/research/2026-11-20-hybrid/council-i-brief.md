# Council I: the fresh test before its first send (read-only, $0)

Alex replied "那你自己持续迭代" to council H's recommendation (D684): run the presentation-only test and keep iterating under the
council loop.

**Read:**
- `docs/research/2026-11-20-hybrid/DESIGN-J2.md`, the section "The fresh test (D684)";
- `docs/research/2026-11-20-hybrid/fresh_test.py`;
- `poc/data/hybrid-2026-11-20/freshpool.json`;
- one census card, `poc/data/hybrid-2026-11-20/deck-fresh-census/C001.txt`;
- the system text `src/hivemind/prompts/judging-v7.txt`, line 3;
- `docs/prd/06-views.md`, line 19 and the State row (line 89);
- `poc/data/hybrid-2026-11-20/account/T-new-2-Q31.json`.

**Done at $0:**
- 116 pooled answers as of 09-06, all rebuilt byte for byte;
- `check pool`: v7 equals the stored bytes; H1 and H2 change only the heading line; the stored answer passes the production check
  under each arm;
- two mutants are caught: an evidence-text change, and a cite of an id that was not shown;
- the census reading is running now. No mark has been read.

**Challenge:**
1. **The pool and the selection rule.**
   - Is there an exposure leak: same-matter chains across draws, or questions the design saw under another label?
   - Is there a selection bias, given that 114 of 116 answers hold the previous rung?
   - Is the scaling to ceil(5n/13) and ceil(8n/13) right?
2. **H1's wording.** It keeps the name "Previous conclusion" so that the system text's three references still point at the block. Is it
   faithful to council H?
3. **H2.** Send it beside H1 as the isolation of the system sentence, or not? Is the restatement sourced, or is it a new rule? Is one
   account in 24 enough reason to spend the arm?
4. **The screen, the falsifier and the blinding.** The cards are built from the v7 text, so the heading is not on them. Is anything
   missing that would let a pass be an artefact?
5. **What here would be a step run for its own sake?**

**Out of scope:**
- the frozen ruler and gold;
- the opening step;
- D382;
- the c8 reading arm;
- anything not in phase 1.

Answer in under 300 words, then `CONSENSUS: …` or `DISAGREE: …`.
