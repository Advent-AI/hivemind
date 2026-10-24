No serious blockers.

In the supplied case, `q1 → g1` remains intact. Unused `t1` is filtered before writing, and the [stored proof](/Users/lchingen/hivemind/poc/reports/2026-10-25-membership-free-01/unused-definition-proof.json) shows two theses in one group.

- The [process](/Users/lchingen/hivemind/poc/hierarchy_study/extraction_membership.py:68) and [writer](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_threads.py:132) preserve referenced memberships.
- The proposal retains every candidate-reference check. It broadens raw-answer acceptance only for unused declarations; semantic acceptance remains unchanged.
- Exact-request replay, reuse labels, and the shared budget remain required. The budget records 38 of 48 calls used.

No edits or model calls made.