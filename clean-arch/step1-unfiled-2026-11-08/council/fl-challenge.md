Two events during Stage 2. Read-only check, under 200 words.

1. **Clean draw 3's Step 1 stopped on a cut network reply after 40 completed articles.**
   - It was continued as a segment, per the established practice in round log §30 (`clean-arch/step1-unfiled-2026-11-08/LOG.md`, section
     "Continuation"). The remaining 203 items run in manifest order from article 40's after_state, with the same pinned c8 invocation,
     settings and limits: `poc/data/clean-e2e-2026-11-09/stage2-clean-d3-segment-2/` (`continue.sh`, `continuation.json`).
   - `adapter.py` `trace_articles` and the stamp now accept 'first+segment'. Articles are numbered by the first manifest, an article a
     later segment completes is not failed, and the stamp holds one hash per segment plus the library.
   - A new test splits the stored trace at 40, marks row 41 failed in the first part, and checks the join reads exactly like the
     unbroken trace. A mutant that keeps such rows failed fails it.
2. **Control draw 2 stopped on the frozen judge's own refusal** (v17 cited v8 as a dependency). It was replaced by a fresh draw 4 and
   kept for the report, and the same rule is stated for the clean arm. See the two dated addenda at the end of
   `clean-arch/e2e-2026-11-09/stage2-frozen.md`, both written before any clean result.

Is either handling biased or wrong? Answer SEND or BLOCKER.
