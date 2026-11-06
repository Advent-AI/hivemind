# The split extraction in the production round: state × event (plan-final C-5)

Code: `scripts/replay.py` → `hivemind.replay.run` (items of a day routed in order, then run one after another; the day's judging; pull mode) →
`views.round.run` (per item) → `hivemind.split.extract` → matching (`views.jev_matching`) → `views.writing.write`. The model archive (`model.Archive`)
keys every request by its identity, so a re-sent identical request is answered from the archive at no cost. D = the item's publication day,
S = its dispatch sequence, E = the day being completed. No read or write uses the computer's clock for order (AGENTS §3).

| State | Success: what is read and written | Refusal, failure, crash, restart |
|---|---|---|
| Routed | `dispatch.route` assigns S in feed order; a `dispatched` step with D | A merged copy or a skipped item writes its route and never reaches extraction |
| Snapshot | `split.latest_library(conn, S)`: every question with created_seq < S whose last switch before S is open, with its key, groups and parents as of S − 1; research subjects restored from the ledger into the universe (`split.load_subjects`) | Deterministic from the append-only ledger: a restart, preflight or audit rebuilds the same list (`scripts/preflight_split.py`) |
| A and B in flight (per section of the item) | Both requests built on the same snapshot; sent together; each answer archived under its request identity | A transport error or schema refusal raises: `round.run` marks `extracted failed` and the day stops resumable. On resume the item re-runs from the snapshot; identical requests come from the archive, nothing is charged twice |
| Record preparation | Built from the archived A and B answers (A's questions and passages, B's version of any statement A also quoted, B's unfiled passages); archived | Same as above; a changed A answer is a changed request |
| Handover | `split.build_handover` (source quotes, one record per statement, checks, analyst check dates); research subjects written with the item (`research_subjects`); `round.run` stores the handover and the `extracted ok` step in one commit | A refusal inside the checks (an unshown link, a subject identity collision) fails the item before the commit; nothing of it is stored |
| Matching | Jev and the analyst review over the saved handover and the snapshot; a match record per call | A failure marks `matched failed`; on resume the saved handover is reused (resume_from) and matching re-runs; Jev answers come from the archive |
| Written | `writing.write` in a savepoint; `written` and `handed_over` steps in the same commit | An error rolls the writes back and marks `written failed`; resume re-runs matching and writing from the saved handover |
| Day judged | After every routed item of E: `round.judge_day` over the questions changed on E, at E's last sequence; pull mode closes due questions with ladders; `days_completed` written | A refused judgement leaves E resumable; resume skips the items already handed over and judges E before any later day. Replay refuses to start before the last completed day (no backdating) |

Events the table covers by construction:
- **A later run on a later date** uses D and E from the items and the ledger, never the run date.
- **Configuration changed between runs**: a changed prompt, schema or setting changes the request identity; the archive cannot answer it and the
  items are re-sent. Preflight against the configuration that wrote the ledger refuses a mismatch.
- **A corrected input** (a new version of an item) is a new item with its own identity and sequence; the old one's records stay.
- **Another writer**: `replay.run` is the only ledger writer; two writers on one ledger are not supported (the runner takes no lock today, like the
  frozen path — named as a gap, not handled).
- **A limited run** (`--max-items-per-day`): replay still judges and completes the cut day, as the frozen path does; the split measurements use whole
  days only (production review §1 named this as a gap of the replay entry point).
- **Analyst check dates and pull mode**: a question gets an estimated check day only when no exact day is supported; pull mode closes a question on
  its due day only when it has a ladder, freezing its last judgement. An annual figure's estimated day is the end of the month after its fiscal year
  ends, when the annual report is expected; if the report comes later, the frozen conclusion is the forecast at that day. This is the risk Alex's
  decision 4 accepted after the table; it is measured, not handled, in the acceptance.
