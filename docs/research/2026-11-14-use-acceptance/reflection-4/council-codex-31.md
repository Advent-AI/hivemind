**Go for the re-reading, conditional on the packet check passing before readers start.** The comparison now suppresses marks, W faults and controls when either reading is incomplete, and the saved missing-ruling test shows that behaviour. [compare_readings.py](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/gate1-stick/compare_readings.py:88), [compare-selftest.txt](/Users/lchingen/hivemind/docs/research/2026-11-14-use-acceptance/gate1-stick/compare-selftest.txt)

The byte-for-byte packet comparison is a **pre-reading requirement**; I have not verified its result yet. The eventual comparison can describe repeatability on these sends, with the stated limits, but cannot establish which reading is correct.

CONSENSUS: yes