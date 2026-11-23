# Council round 57 (Council B on the third blind run): independent read, read-only

You are an independent reviewer. Do not edit any file. The repository is /Users/lchingen/hivemind. Cite what you read. Treat my
documents as claims to check.

## Scope and material
The third judging-v13s blind run (D742).
- My result: `docs/research/2026-11-22-number-answers/BLIND3-RESULT.md`.
- The run: `poc/data/judging-v13s-blind3-2026-11-22/`:
  - `CHECKED.json`, `reader-key.json`, `TALLY.json`;
  - `reader-packets/R*.{md,claude.json,codex.json}`;
  - `adjudication/R*.{md,claude.json,codex.json}`;
  - each case's request files and answers.
- The registered lines: `SMALL-DESIGN.md` §5, including the [D742] block at its end.
- The reader brief: `blind_test.py`, `READER_BRIEF`.
- The schema: `render_v13.py`, `v13s_schema`, `answers/rung` description.
- The code: `calc_small.py`, S6.
- The earlier council: `codex-r56.md`, `codex-r56b.md`, `codex-r56c.md`.

Out of scope: the frozen ruler, the production configuration, any paid run.

## Questions
1. **Is the verdict right as registered?** Two readers marked R01 "broken structure" on F14 (a range across a rung edge, rung 4
   chosen with a reason). Both adjudicators rejected the mark, citing the schema's "for a range outcome, a band it overlaps, with the
   reason in reasons". Score the registered line "an accepted reply with a named defect (marked by both readers, or by the third
   reader) is a stop" as written. Is my reading of the cause right (the reader brief omits the range clause)? Do the counts reconcile?
2. **R07** (S, Codex writer) is accepted and publishable but settled "not supported": its 90% data-center share decides rung 3, against
   passages that point near 100%. Is that correctly outside the registered stop lines? What should it mean for the next step?
3. **The next step.** I see three options:
   - (a) Correct the reader brief's definition to the schema's range clause. Then re-read the same 12 replies with fresh readers and
     the registered adjudication. The writers are not re-run, because the request did not change. If clean, the result goes to Alex
     for the paid re-send.
   - (b) Run a fourth full blind run with the corrected brief.
   - (c) Go to Alex now with this result and the disclosures, and let him rule whether the instrument stop counts.
   Which is honest, and which is not moving the goalposts? If (a), does re-reading the same replies after seeing them bias it, and how
   would you guard against that? Under the standing rules, a stop the cause of which is the measuring instrument, with a clean
   substance, still goes back to council, and Alex is active.
4. **Anything I missed** in the replies, readings or adjudications that a registered line should have caught.

Return a numbered report: findings marked serious / minor / wording, with citations, then one recommendation for the next step and its
falsifier.
