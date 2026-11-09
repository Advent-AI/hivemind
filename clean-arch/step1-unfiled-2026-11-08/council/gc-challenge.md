Alex approved the unseeded measurement (D395: "跑，只跑新系统三份"). Before the send, read the new code read-only, under 300 words.

**Read:**
- `clean-arch/e2e-2026-11-09/adapter.py`, mapping mode: `Adapter(mapping=...)`, `create_ruler_q23`, `_link`, the mapping checks in
  `replay`, and `--map`;
- the three new tests at the end of `test_adapter.py` (they use the stored unseeded dev-d1 draw);
- `clean-arch/unseeded-2026-11-10/run_unseeded_draw.sh` and `initial-empty.json`;
- `clean-arch/e2e-2026-11-09/continue_clean_draw.py`, which now takes a run folder as well as a draw number;
- `clean-arch/unseeded-2026-11-10/MATCHING-v2.md` (the rule).

**Facts:**
- 18 tests pass.
- A scratch mutant that ignores the mapping fails the unseeded test.
- The launcher pins c8 (the test_runner check), uses Stage 2's manifest, settings and limits, starts from an empty library, and stamps
  the trace and library after Step 2.

**Check:**
1. Does mapping mode feed only matched clean theses to ruler views? Are the seed views and the ruler q23 created at seq 0, and does the
   leakage check still hold?
2. Several clean theses mapped to one ruler view: their links merge into that view. Is that right under MATCHING-v2?
3. Is the launcher equivalent to `run_clean_draw.sh` apart from the empty library, and is the continuation change safe for the Stage 2
   paths?
4. Anything else before three paid draws (about $7)?

End with SEND or BLOCKER.
