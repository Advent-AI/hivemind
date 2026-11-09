Fixed. Re-read `adapter.py` (mapping mode) and the new tests. Read-only, under 150 words.

1. **Several ruler questions for one thesis.** A mapping value is now a list of views: `--map clean-N=vK,vJ`, and a repeated key adds
   views. Each view gets the links. A test maps clean-4 to v4 and v13 and checks both views hold the same evidence.

   A note on MATCHING-v2: it calls a question bundling 2026 and 2027 "broader than q04 and q13", so it is not SAME and not mapped.
   Multi-view support is only a safeguard.
2. **q23.** In mapping mode all 23 ruler views are created at seq 0, the ruler's q23 included (MATCHING-v2 §4). The tests check it.
3. **Output.** A live replay may write under `poc/data/clean-unseeded-2026-11-10` as well as `poc/data/clean-e2e-2026-11-09`.

Tests: 14 pass. The frozen hashes are refreshed.

SEND or BLOCKER?
