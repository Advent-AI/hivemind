**Not ready.** A second launch can run alongside the first with its own view of the $2 limit. For example, each process can believe $1 remains and send calls against that same dollar. The reading plan also leaves a control rule unresolved before the send.

Stage A has **not passed**. D429 nevertheless permits Stage B once review finds nothing serious, with $2 for all three draws together. [D429](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4771)

### 1. The first review, finding by finding

| Finding | Status | Evidence |
|---|---|---|
| $2 across draws and redos | **Partly closed.** One launcher shares a limit across its draws and redo, and a later launcher reads the ledger. Overlapping launchers do not share a lock or refresh each other’s spending. | [Launcher](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/run_stage_b.py:33), [ledger limit](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:55) |
| A newly opened, already-due view could be judged | **Closed.** The guard runs after the day’s writes and before judging. The new test checks that the view has no judgement. | [Replay](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:264), [test](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/test_ladder_adapter.py:158) |
| Configuration checksum named the answers file | **Closed for the reported issue.** The value now comes from the ladder archive’s configuration; the answers file gets a separate hash. | [Configuration lookup](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:211), [replay counts](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:249) |
| Counts misnamed or missing | **Closed for the two identified counts.** Links to laddered views and views without opening evidence have separate names. | [Links](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:167), [opening evidence](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:260) |
| Identity check used only description | **Partly closed.** It also checks outcome, period and opening day. The three thesis fields are compared only when present in the trace, and the check still identifies an outcome by case name rather than independently proving the stored answer came from that complete case. | [Identity check](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:185) |
| Failure paths untested | **Partly closed.** Tests now exercise refusal and redo, a deterministic stop, and cap refusal. They do not demonstrate overlapping processes, a crash with calls in flight, failed ledger writes, or the judge’s partial commits after a failure. | [New tests](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/test_ladder_adapter.py:174), [judge’s concurrent calls and commits](/Users/lchingen/hivemind/src/hivemind/views/judging.py:317) |
| Mutants counted any failure as a catch | **Partly closed.** The runner now requires the named test to appear as failed and excludes pytest errors. It still does not verify the failing assertion or preserve its traceback; the saved output is truncated. I did not run it. | [Mutant runner](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/mutants.py:63), [saved output](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/mutants.output.txt:1) |
| Preflight not addressed | **Partly closed.** The plan explains that preflight judges zero cases on this stored replay and says what the fake-judge check exercises. It does not give a preflight result with its skipped cases, as the standing rule requests. The fake judge does not replay real judge answers through preflight. | [Plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:44), [rule](/Users/lchingen/hivemind/AGENTS.md:174) |

The design table’s earlier `reference_status` omission is also corrected: it now lists `last reported figure`. [Design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:944)

### 2. Can it exceed $2?

**Yes, with overlapping launches.** Each process reads the ledger once when it constructs its limit and uses its own `threading.Lock`. The launcher has no process-wide exclusion. A second launcher can also skip an existing draw folder and start its redo while the first is still working. Both can allocate the same remaining money and reuse attempt numbers, making the ledger total unreliable as well. [Limit initialization](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:55), [lock](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:53), [folder handling](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/run_stage_b.py:42)

For the other cases:

- **Threads within one launcher:** reservations and charges use the same lock, so they cannot each reserve the same remaining balance. [Ledger](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:67)
- **A crash, followed by a launch after the first process has ended:** an in-flight call has a synced reservation, which the next limit counts if no charge was recorded. The stopped folder is skipped. This depends on a readable, intact ledger and on the reservation covering the eventual charge. [Ledger writes](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:61), [ledger total](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:101)
- **A redo in the same process, or a later non-overlapping launch:** it uses the shared or reconstructed balance, so the original fresh-allowance problem is addressed. [Launcher](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/run_stage_b.py:38)
- **Reservation size:** the limit assumes its request-size estimate and output cap bound the charge. It does not check that returned usage is within that reservation before adding the actual charge. That is a limit to the hard-cap claim, rather than evidence that these ordinary requests will exceed their reservation. [Cost calculation](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:30), [charge](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:84)

### 3. Result readability and departures from the design

The main replay follows the intended path: stored first-send ladders create the views before the opening article’s evidence, and the frozen judge runs after the day’s commit. The plan correctly states that live ladder calls and their retry cells do not apply to this replay. [Run plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:9), [replay](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:251)

Two things need attention before relying on the result:

1. **The control’s date rule is unresolved.** The design requires the judged question’s period and due day to equal the frozen question’s. The draft reading plan proposes treating different due dates as equal when they refer to the same annual publication, and explicitly leaves which reading decides the line to reviewers and, if they differ, Alex. That can change whether five figure controls qualify and therefore whether Stage B can pass. The rule needs resolving before the send; it should not silently replace the design’s literal rule. [Design](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:1471), [reading plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_READING.md:48)
2. **Per-draw cost labels are misleading.** Each draw writes `judging usd` from the shared limit and shared ledger, so the second and third draw’s values include earlier draws’ spending. They must be labeled cumulative or calculated per draw. [Replay counts](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:269)

The plan’s last-rung dry run is useful evidence that the new shapes can pass the frozen judge’s checks, but it is not evidence of the real judge’s quality or a substitute for the requested preflight. [Run plan](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/STAGE_B_RUN.md:31)

### 4. What remains serious

The overlapping-launch cap failure is serious because it can exceed Alex’s explicit limit. The unresolved control rule is serious because it can change the test’s verdict. The incomplete failure-path evidence and preflight record should also be closed before sending; the cumulative cost label is a reporting fix.

This was a read-only review. I did not run tests, model calls, or Stage B.

**Not ready — prevent overlapping launches from spending against the same $2, resolve the control’s due-date rule, then verify the failure paths and preflight record and correct the cumulative cost labels.**