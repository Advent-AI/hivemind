**No serious findings remain in the revised design. Both round-2 blockers are addressed.**

1. **Resolved — seeded-question visibility (previously serious).**  
   Mapping sequence 0 to the first processing day makes seeded questions and dependencies visible from coverage start ([design:46](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/production-design.md:46)). In-memory checks showed all 22 questions, 17 dependencies, and correct evidence, source and arrival dates; everything stayed hidden before coverage start. The served ledger’s complete library output was identical across all **59 completed days**. Its records contain no sequence-0 values affected by this change.  
   **Fix:** No further design change needed; preserve positive-sequence mappings and the existing cache.

2. **Resolved — interrupted initialization (previously serious).**  
   Requiring the coverage-start day to finish before advancing closes the lost-first-judgement path ([design:49](/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end/production-design.md:49)).  
   **Implementation requirement:** Check that **that exact date exists in `days_completed`**, before the existing-baseline shortcut. Apply the guard against replay’s effective start: replay can advance beyond the requested `--from` ([replay.py:56](/Users/lchingen/hivemind/src/hivemind/replay.py:56)), while `last_completed_day()` returns only the latest appended completion ([store.py:475](/Users/lchingen/hivemind/src/hivemind/views/store.py:475)). A later completion alone does not prove the coverage-start date completed.  
   **Fix:** Implement the stated exact-date condition; retain the planned entry-point checks for interrupted initialization and normal later resumption.

No files were edited and no model requests were sent.