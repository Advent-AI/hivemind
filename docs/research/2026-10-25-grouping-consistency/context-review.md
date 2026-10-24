No serious blockers to the proposed 3-control/3-context-arm diagnostic.

For example, showing the stored SK → Rubin membership gives the model prior context without supplying the desired OpenAI answer.

- **The intervention fits the code.** [retained_membership.process](/Users/lchingen/hivemind/poc/hierarchy_study/retained_membership.py:53) currently omits memberships from existing theses. [thread_members](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_threads.py:53) stores those relationships. Filtering them to already-offered groups stays within the IDs the [existing validator accepts](/Users/lchingen/hivemind/poc/hierarchy_study/retained_membership.py:31). No prompt or output-schema change is needed.
- **The comparison answers the narrow question.** The [revised plan](/Users/lchingen/hivemind/docs/research/2026-10-25-grouping-consistency/plan.md:23) fixes the two-article prefix, uses fresh third-article samples, and separates extraction coverage, identity errors and missed memberships. This matches [revised D148](/Users/lchingen/hivemind/docs/DECISIONS.md:2167).
- **Cache and failure behavior are compatible.** [Calls.stage](/Users/lchingen/hivemind/poc/hierarchy_study/ingestion_groups.py:237) checks complete-request equality before reuse. Its [inherited call path](/Users/lchingen/hivemind/poc/hierarchy_study/study.py:268) refuses automatic resending of incomplete or failed records.

Limits: this is a small, case-specific diagnostic. Missing OpenAI extractions cannot count as correct membership, and inconclusive samples must remain inconclusive. This assessment assumes the runner implements the promised **18-request/$2 cap**, fresh sample isolation and rollback behavior; it does not verify that future implementation.

Read-only review completed. No edits, model calls or corpus/history re-audit.