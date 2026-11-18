# Stage-0 freeze review of the release comparison (read-only, $0): is everything the slice needs built, proved and frozen?

**Plan:** `RUN-PLAN-v11.md`. Decisions D665 to D671 are in `/Users/lchingen/hivemind/docs/DECISIONS-log.md`. The build-level items carried from
the design rounds are in `freeze-review-notes.md`.

**Alex** (2026-11-17, after the matter list was frozen): "好，你clean up提交，然后开始跑". Committed as `099f4a8` (clean-arch branch).

**Built, with its proof:**
- **Code** (see `git -C /Users/lchingen/hivemind show 099f4a8 -- clean-arch/e2e-comparison-2026-11-13/run_fresh.py clean-arch/step4-2026-11-10/stage_b/run_stage_b.py`):
  - `run_fresh.py --items/--limits/--ladder-variant astra-frozen/--judge-end-day`;
  - every pass's ladder archive checked;
  - `run_stage_b.py` forwards `end_day`;
  - `stage0/stage_a_astra.py`.
- **Tests and mutants:**
  - `clean-arch/e2e-comparison-2026-11-13/test_run_fresh.py` (33);
  - `clean-arch/step4-2026-11-10/stage_b/test_ladder_adapter.py` (35);
  - `stage0/test_stage_a_astra.py` (4);
  - `stage0/mutants-run-fresh.txt` and `stage0/mutants-stage-a-astra.txt`.
- **Inputs:**
  - the shared items DB `/Users/lchingen/hivemind/poc/data/comparison-2026-11-17/items-comparison.sqlite` (92 excluded window rows
    deleted; `excluded.json` beside it);
  - the two-entry proof `stage0/comparison_inputs.py`, with its output in `stage0/comparison-inputs-output.txt` (1,884 items 07-01..09-20,
    the same set and order, both controls pass);
  - the manifest `poc/data/comparison-2026-11-17/manifest-2026-07-01-09-20.json`.
- **Frozen:**
  - `stage0/kept-articles.json` (410);
  - `stage0/census/matters.json` (N = 32);
  - `stage0/verdict-rule.json`;
  - `poc/data/comparison-2026-11-17/comparison-limits.json`;
  - `stage0/versions-manifest.json` (28 files at `099f4a8`).

**Proposed resequencing** (for this review to accept or refuse):
- The scorer (`score_comparison.py` with tests), the card builder with the generalised `council_mark.py` (change F), and the §1.6 tools
  read only outputs after the run. They would be built and tested during the ~20-hour run, before any output is read.
- The verdict rule itself is frozen now (`verdict-rule.json`), so the finish line cannot move.
- The size check (§1.7) and the preflight (§1.8) would run before the slice.

**Report only what would stop or skew the slice or the run, or let the result move.** Each finding needs a file and line.
- Is the resequencing acceptable under D665's "written before the first send"?
- Do the code changes and proofs hold what `freeze-review-notes.md` asked?
- Does `verdict-rule.json` say exactly what plan §1.4 says?
- Anything that must be done before the slice?

End with `READY FOR THE SLICE` or `NOT READY: <the smallest changes>`. Under about 500 words. Do not open anything under `/private/tmp` or
`~/.codex/memories`.
