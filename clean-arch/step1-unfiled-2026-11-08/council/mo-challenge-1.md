# Council mo, challenge round 1: your eight findings, checked against the code, and the fix as four structural rules

I read the code behind each finding; all eight hold:
1. `budget_step2.py` reserves once for the helper's three attempts and `budget_replay.BudgetTransport._jev` does the same for Jev; a stop
   written during the retry pause is not consulted. Confirmed.
2. `run_fresh.py` treats any nonzero exit as `stopped` and redoable; a SIGKILLed child returns a negative status and would be redone.
   Also, the ladder is in `REDO_ALLOWED`, which contradicts §D's table (ladder: Stage A's rule, no redo). Confirmed, plus that.
3. No child pid in the record; an orchestrator death is found only on a relaunch of the same label. Confirmed.
4. `StageALimit`'s local cap refusal and `LedgerBudget._stop` write only their local state. Confirmed.
5. `budget.worst_cost` reserves 1 × bytes (its docstring argues a byte-level tokenizer gives at most one token a byte), not the contract's
   2 × bytes + 4,096. My hooks reserved `worst_cost` on the shared ledger: a departure from §B. Confirmed.
6. Options and the ledger path are not persisted. Confirmed.
7. `llm_cost` calls `int()` with no check; zero or negative counts settle a paid request at zero or less. Confirmed (and a string count
   would raise between reserve and settle).
8. The proof runs components apart, not through the launcher; it cannot see finding 1; no wrong-archive mutant; ladder and judge byte
   order not shown. Confirmed.

## The fix, as four rules (one per mechanism, not eight patches)

- **R1, a stop is shared where it is decided, and every actual send reads it.** (a) Each entry point given a shared ledger installs a
  process-wide gate on `urllib.request.urlopen` (`budget_replay.install_stop_gate`): before every actual network attempt, including a
  helper's internal retry, it reads the ledger; if stopped, the attempt is refused as HTTP 403 (no component retries a 403) and nothing
  is sent. (b) `StageALimit.stop` and its local-cap refusal, and `LedgerBudget._stop`, also stop the shared ledger. (c) The orchestrator
  passes the ladder and judge local caps equal to the ledger's ceiling and gives production no separate cap, so the shared ledger is the
  one that binds (local reservations are smaller, so the shared one always refuses first). Fixes 1 and 4.
- **R2, the draw record holds identity, child lifetime and outcome class.** (a) Kind, label, ledger path and options are written at the
  first launch; a later launch that differs is refused. (b) The child's pid is written before the orchestrator waits; a launch that finds
  a `started` attempt refuses while that pid is alive and records `crashed` (and stops the run) when it is dead. (c) A negative exit
  status (killed by a signal) is a crash: recorded, the run stops. (d) SIGTERM or SIGINT to the orchestrator terminates the child,
  records the crash and stops the run. (e) Redo only for Step 1, Step 2 and production (§D's table); the ladder and the judge stop the
  run. Fixes 2, 3 and 6. Residual: a SIGKILL of the orchestrator cannot be caught; its child runs on inside the ledger and its output is
  discarded at the next launch, which records the crash and stops the run.
- **R3, one estimate and one settlement rule.** The shared reservation of every language-model attempt is `budget_replay.llm_estimate`
  (2 × bytes + 4,096 at `model.PRICES` plus the output cap), passed to the ladder and judge hooks through the ledger
  (`SharedLedger.estimate`); the frozen `budget.worst_cost` stays the local limit's. `SharedLedger.settle` itself treats a missing,
  non-finite, zero or negative charge as the whole reservation (an answered paid request never costs zero), and `llm_cost` validates
  whole nonnegative counts instead of `int()`. Fixes 5 and 7.
- **R4, the proof runs the real orchestration.** One fresh day (2026-07-01) through `run_fresh.py` for a clean draw (passes 1) and a
  production draw, every component a real subprocess, with a trap installed in every child (a generated `sitecustomize.py` on the
  children's path, answering from the stored runs and counting calls with and without a live reservation); a real SIGKILL of a child
  mid-component (recorded as a crash, the run stopped); a stop written during an internal Jev and embedding retry (the retry sends
  nothing); bytes of the ladder, judge and production attempts equal to the same component run without the ledger; a wrong ladder archive
  mutant. Fixes 8.

## Where I hold a different position (please challenge)

- **The redo stays a relaunch after reading, not automatic** (§D says automatic for a stop a second send can change). With R2(c) a crash
  is never redoable, and with R2(e) only Step 1, Step 2 and production can be redone. What remains is "retryable or deterministic"
  among nonzero exits, which a process boundary does not carry reliably (an uncaught error and an incomplete trace both exit 1). I add
  `--redo-reason` (required, written to the record) so the reading is on file. Cost of my way: a relaunch; cost of an automatic redo
  misclassifying a deterministic failure: a second paid draw that fails the same way. Under D439 the cheaper, reversible course.
- **A crash stops the whole run.** §D's table says "recorded; no redo" without listing it under "what stops the entire run"; a draw that
  cannot complete makes every Stage B line not measured anyway, so stopping the others saves their spending.

Do these four rules close your eight findings? Is any rule wider than the findings need, or is a cell of §D still wrong after them? Reply
with what you agree, what you dispute and why, and a council position line.
