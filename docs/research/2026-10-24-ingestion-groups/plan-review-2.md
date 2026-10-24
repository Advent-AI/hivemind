No serious blockers remain at the plan level. For example, a candidate assigned to an existing view resolves to that view’s real ID; a failed relationship check rolls back the whole write.

- **Retrieval and visibility:** The plan defines extraction and matching retrieval separately, specifies `search_top_n=10`, limits group visibility to retrieved views’ memberships, and records each actual displayed set. Retrieval misses are reported separately from model misses.
- **Adapter and atomic writes:** English enums map in memory to named legacy constants by corresponding order. The plan specifies restoration before writing, retention of legacy values inside `Checked`, candidate/group temporary-ID resolution, validation, and one SQLite transaction.
- **Waves and accounting:** All six streams process one article before advancing. The plan preserves reservation accounting, stops globally at the budget limit, reports completion and failures per stream, and labels results partial when fewer than three controls complete.

These resolve the stated planning blockers; this review does not verify implementation.