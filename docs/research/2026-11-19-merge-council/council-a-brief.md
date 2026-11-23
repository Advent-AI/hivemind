# Independent design: merge the best of two systems, and a small test to validate it (read-only, $0). Read the material cold.

**Context.** Alex has two pipelines that read the same NVIDIA news and hold research questions an analyst tracks.
- The **old** system is production `poc/config/poc-v118.json`, replayed by `clean-arch/e2e-comparison-2026-11-13/budget_replay.py`.
- The **new** clean system is `clean-arch/PRD.md`: Step 1 c8, then Steps 2 and 3, the ladder, and the same frozen judge.
- A release comparison (2026-11-17..19) scored both on 32 frozen matters. The old system served 10, the new one 2–3.

**Read first:**
- `clean-arch/PRD.md` §1.3–1.4: the measured problems of the old system, and what the new one does differently.
- `docs/research/2026-11-19-comparison-review/PATH-TO-PASS.md`: why the new one lost, including the refusal cascade.
- `docs/research/2026-11-19-comparison-review/DESIGN-refused-not-open.md`.
- `docs/DECISIONS.md` D382, D383, D505 and D676.

**Stored runs** (all finished):
- `poc/data/comparison-2026-11-17/run/old-1..3/prod/views.sqlite`;
- `.../new-2`, `.../new-3`: `step1/trace.sqlite`, `step2/`, `cases/`, `ladder/`, `judge/`;
- the readings in `poc/data/comparison-2026-11-17/reading-diagnostic/`.

**Design, from the evidence:**
1. **The merge.** Which piece comes from which system, and why, citing the measured strengths and weaknesses. This covers:
   - opening questions;
   - answer choices;
   - reading and extraction;
   - repeats and earlier versions;
   - judging.
   Name the wiring needed between the pieces, and any decision of Alex's it touches (D382, D505).
2. **The smallest test that would validate it**, using stored runs wherever possible:
   - its window and inputs;
   - what it compares against;
   - its pass lines, written now;
   - its cost, priced from the stored ledgers;
   - the result it can attainably reach, computed before any send.
   - Say what the test can and cannot decide.
3. **The main risk of the merge.**

Under 500 words. Separate what you checked from what you infer. Do not open `~/.hivemind-keys`.
