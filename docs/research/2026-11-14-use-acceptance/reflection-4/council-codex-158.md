Version 4 is ready for the **$0 scratch build**, with the D397 departure recorded as a reversible proposal before the build. The split remains diagnostic; it does not change the frozen control line.

Two checks need particular attention before any send:

- **Budget:** the existing [Stage A limit](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/stage_a.py:68) reserves before sending, but charges the returned cost afterwards. The $0.40 bound therefore depends on each charge staying within its reservation; already-started workers can finish after a stop. Test an over-reservation charge as well as ordinary concurrent stopping, and report the bound’s assumptions.
- **Readers:** the named refusal checks must also accept historical stores that lack the new `period` column, with their existing results unchanged. On a split store, each applicable reader must refuse before producing a partial count.

Keep the crash and partial-result proofs in the build, and bring the prompt audit, tests, mutants, actual reservation calculation and resulting files back for a separate send decision.

CONSENSUS: record the reversible proposal and build the $0 checks; send nothing yet.