# Review round 4: the reading tools, and the design of the §1.6 tools (read-only, $0; D672's condition)

**Part A, the reading tools.** Rounds 1 to 3 said NOT READY: `tools-review-codex.md`, `-2.md` and `-3.md`, with the Claude readers
summarised in D675 in `docs/DECISIONS-log.md`. Every fix and every reading of the frozen rule is in D675. The tools in `stage0/` are:
- `score_comparison.py`
- `mapping.py`
- `mark_cards.py`
- `build_cards.py`
- `eligibility.py`

Their tests are the matching `test_*.py` files. The mutants are in `mutants_reading_tools.py`, with their output in
`mutants-reading-tools.txt`.

Check, citing file and line:
1. Is every earlier finding fixed, or argued in D675 with a reason you accept?
2. Did a round-3 fix break anything? In particular:
   - the card's request context, its theme rungs and its own place in the opening order;
   - eligibility's identity check against the six live run records (read `poc/data/comparison-2026-11-17/run/<draw>/run.json` only);
   - the scorer's re-reading of its inputs.
3. Is anything left that changes a count, a verdict or what a reader sees?

**Part B, `DESIGN-1.6.md`:** the hard checks and the printed-beside quantities, not built yet except the D400 code part.
- Is each item faithful to `RUN-PLAN-v12.md` §1.6 and `stage0/verdict-rule.json` `hard_checks`?
- Is each runnable on the stores the run writes?
- What is missing or wrong? In particular:
  - Step 2 line 1's labelling, independent of Step 2's own search;
  - line 3's two renderings;
  - D431's reading without the MATCHING-v2 §4 adapter;
  - the reading that a lead with a failed or unmeasured hard check reports as "no release: hard check".

End Part A with `READY TO READ` or `NOT READY: <the smallest changes>`. End Part B with `BUILD AS WRITTEN` or `CHANGE: <the smallest
changes>`. Under about 600 words. Open nothing under:
- `/private/tmp`;
- `~/.codex/memories`;
- `~/.hivemind-keys`;
- `stage0/downloaded_files`;
- `poc/data/comparison-2026-11-17/run`, except the six `run.json` files named above (never a database).
