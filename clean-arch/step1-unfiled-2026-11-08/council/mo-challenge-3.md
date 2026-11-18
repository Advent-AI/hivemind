# Council mo, round 4: the code and the $0 proof, built to the four rules (D449 recorded)

Please read the code itself (read-only) and the recorded proof outputs, and say whether the eight findings are closed and whether anything
serious remains before the slice. Scope and out-of-scope as in `mo-handoff.md`.

**Where each rule sits:**
- R1: `budget_replay.install_stop_gate` and `SharedLedger.stop_if_a_launcher_is_gone` (`clean-arch/e2e-comparison-2026-11-13/budget_replay.py`);
  installed in `clean-arch/step1/run_live.py`, `stage_a/stage_a.py` `main`, `stage_b/run_stage_b.py` `main`, `budget_step2.main`,
  `budget_replay.main`. Shared stops: `StageALimit.stop` and its local-cap branch, `LedgerBudget._stop`.
- R2: `run_fresh.py` (`Draw.launch`: the dead-launcher check before the lock, then the lock, then `register_launcher`, signal handlers,
  `remove_launcher` in `finally`; `_launch`: identity check, attempts found `started` → crashed, `REDO_ALLOWED = {step1, step2, prod}`,
  `stopped-run` for the cases, the ladder, the judge and a configuration mismatch; `_call`: a negative exit status → `crashed`;
  `child_environment` keeps an existing import path after `src`).
- R3: `SharedLedger.estimate` (= `llm_estimate`), used by the ladder and judge hooks; `SharedLedger.settle`'s rule for missing, zero,
  negative, non-finite or boolean charges; `llm_cost`'s validation.
- R4: `proof_end_to_end.py` (output `proof_end_to_end.output.txt`), `proof_interception.py` (`proof_interception.output.txt`, now with
  `retry` and `bytes`), `proof_wiring.py` (`proof_wiring.output.txt`, now with the wrong-archive mutant).

**Results:** `proof_end_to_end` 3 of 3: one day through the real orchestrator (a clean draw with ladder pass 1 and a production draw: 5
child processes, 55 trapped calls, 0 unreserved, 0 misses, ledger attempts 55; Step 1's results and states, the cases and the ladder
outcomes as stored); a SIGKILLed child (crash, run stopped); a SIGKILLed orchestrator (its child's sends admitted after the kill: 0; ledger
stopped "the launcher of o1 is gone"; another draw refused; the relaunch records the crash). `proof_interception` 8 of 8 (retry: one
actual send per helper, the retry refused by the gate; bytes: ladder 48, judge 80, production 19 request bodies identical with and without
the ledger). `proof_wiring` 10 of 10 (the wrong ladder archive caught by the row comparison: `clean_ladders` differs). `test_run_fresh.py`
23, `test_shared_ledger_hooks.py` 5, `check_budget.py` 16; mutants caught for every new rule (no stale check before the lock; the gate
without the launcher probe; a signal exit not a crash; an interruption unhandled; no unregistering; no identity check; a ledger accepting
a zero charge; `int()` usage; the retry without the gate: 3 sends each). Full suite 287 passed; frozen pieces 21 passed.

**What I know is not covered:** the killed-orchestrator scenario's detector has no mutant run end to end (the children load
`budget_replay.py` from its repository path, so a mutant would edit the real file); its unit-level mutant (the gate without the probe) is
caught, and the scenario's first run flagged a delayed admitted send, which shows the detector can fire. The stale-registration relaunch
race is covered by `test_a_relaunch_of_a_dead_launcher_catches_its_own_stale_entry_before_taking_its_lock` and its mutant.

End with: "Council position: <ready for the slice | not ready, because ...>".
