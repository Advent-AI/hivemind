**No-go until the comparison and its interpretation are fixed.** A second reading is worthwhile: it can show whether the same method identifies the same failures on this fortnight. It cannot tell which reading is right or how much of the failure was caused by the reader.

The proposed “fewer than half recur” line is underspecified. Half of which set: the first reading’s failures, the second’s, or their union? For example, if two of three original failures recur but the second reading finds seven additional failures, those denominators tell different stories. Predefine and report **both / first only / second only** for each line, with the denominators and an explicit treatment of empty sets. Avoid concluding that the failed sends are “largely set by the reading”: the observation is that the two readings differed. [DESIGN.md:22](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/gate1-stick/DESIGN.md:22)

One fortnight and one repeat can establish a concrete difference—or stability—on these 39 sends. The same packets and order make this a repeat under the same conditions, but shared order effects and the two families’ recurring standards can make agreement look stronger; fresh sessions do not make their judgements independent. Keep the same order for this test, state that limit, and keep the earlier marks and control identities hidden from the fresh readers.

Before reading, make the comparison executable and reviewable:

- Freeze the six author-checked controls and their expected marks; report misses without treating them as independently proven errors.
- Require complete, valid rows and third-reader rulings, and preserve **not measured** as distinct from met or missed. Compare both unresolved treatments separately and keep W’s named reasons visible. [accounting.py](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_a/accounting.py:128)
- Build and check the comparison script on known examples, including a changed failure set and a missing ruling. The directory currently contains only the design, so I cannot verify that comparison yet.

CONSENSUS: no, because the recurrence denominator and conclusions need definition, and the comparison and its checks must be prepared before the reading.