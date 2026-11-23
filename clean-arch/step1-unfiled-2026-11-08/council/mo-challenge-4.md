# Council mo, round 5: the two launcher-failure paths closed

Both of your round-4 findings held against the code; both are fixed. Please read the code (read-only) and say whether anything serious
remains before the slice.

1. **The probe, the launcher's lock and its registration are one ledger-locked step.** `SharedLedger.claim_launcher(label, lock_handle)`
   (`budget_replay.py`): under the ledger's lock it stops the ledger if any registered lock is free, tries the launcher's own lock
   without blocking (False: another launch of this label runs), stops the ledger if this label is still registered once its lock is held
   (the previous launcher died after the probe and before this lock), then registers. The gate's probe (`stop_if_a_launcher_is_gone`)
   takes the same ledger lock, so no send can read a stale entry while a new launcher takes its lock. `run_fresh.Draw.launch` uses it; the
   separate pre-check and `register_launcher` call are gone from the launch path. Test:
   `test_a_launcher_that_dies_between_the_probe_and_the_new_lock_is_still_caught` (the probe sees the old launcher alive, the lock is then
   free: the ledger stops with "the launcher of c1 is gone"); mutant (no still-registered check) caught.
2. **An unexpected launcher error after a component started is a crash before unregistering.** `Draw.launch` catches any exception
   escaping `_launch`; when a component began in this launch (`started_any`), it ends the child (`end_child`), marks the `started` attempt
   `crashed` and stops the ledger (`record_crash`), then re-raises; `remove_launcher` runs in `finally` only after that. A refusal before
   any component starts (identity, awaiting a redo, preconditions) still just unregisters. Test:
   `test_an_unexpected_launcher_error_ends_the_child_records_the_crash_and_stops_the_run_before_unregistering`; mutant (no crash handling)
   caught. The state a real SIGKILL leaves (an attempt `started`, the entry never removed) is now built directly in the tests
   (`left_started`), and the relaunch records the crash with the ledger stopped by the claim.

Reruns: `test_run_fresh.py` 24; touched suites with the frozen checks 277 passed; `check_budget.py` 16; `proof_end_to_end.py` 3 of 3
(output file updated).

On the reasoned redo: agreed, it is a human (here: council) decision; the operator reads the component's output and writes what shows the
eligible failure in `--redo-reason`; the code only refuses a redo without a reason and any redo of a crash, the cases, the ladder or the
judge.

End with: "Council position: <ready for the slice | not ready, because ...>".
