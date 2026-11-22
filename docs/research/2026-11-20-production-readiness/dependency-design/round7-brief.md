# Council R, round 7: version 4

Your round 6 (`codex-r6.md`, NOT READY, three blockers) is answered in `DESIGN.md` version 4 (§0, §1 step 6, §6; §10 maps each
finding) and `TEST-PLAN.md`:
1. poc-v119 has one entry point, the July harness: `scripts/replay.py` and `budget_replay.py` refuse `jev-links`; the harness holds
   the store lock, refuses a store whose last day is unfinished, never resumes a stopped sequence; an attempt that dies before the
   archive keeps its reservation charged (`SharedLedger.reserve`), and the stopped sequence is final.
2. `link_selections` is append-only per attempt: `proposed` before the write savepoint (survives a failed write: `round._fail` commits
   the open transaction), `committed` in the article's commit, `failed` after the rollback, with a Jev error's computed request sha.
3. An allow-list wrapper sits before the budget transport and refuses any miss other than the v9/v14 judge requests and the seq-148 link
   questions, before reservation; fresh first attempts asserted; an out-of-pair reader stops the sequence at inspection; both stop paths
   exercised with the recording fake.
Nonblocking items taken: examples, effective targets in the checker, the admission rule in Table 4, the tests named.

Check each answer against the code it names. End with READY TO BUILD, or NOT READY with the exact changes; list nonblocking items
separately.
