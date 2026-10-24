No serious concrete blockers found in the requested design scope.

For example, `t1` and `t2` can appear together in one `local_ids` list and resolve to one new group without either pointing to the other.

- **Same-batch consolidation and closed destinations:** the contract requires a complete, nonduplicated partition; old destinations must have been shown for every member. [plan.md:21](/Users/lchingen/hivemind/docs/research/2026-10-25-direct-subjects/plan.md:21)
- **Memberships and evidence:** the reused writer resolves candidates to final view IDs, preserves memberships, and reads evidence through actual, sequence-filtered links. Merged candidates retain the second evidence-matching pass. [ingestion_threads.py:132](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_threads.py:132), [ingestion_threads.py:217](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_threads.py:217)
- **Transaction boundaries:** view, evidence, group, membership and completion writes share the final commit; the runner rolls back failures. Dispatch’s initial record remains separate as specified. [ingestion_threads.py:232](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_threads.py:232), [ingestion_threads.py:316](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_threads.py:316)

This reviews the specified design and reused helpers, not a completed direct-group implementation or model quality. No edits or model calls were made.