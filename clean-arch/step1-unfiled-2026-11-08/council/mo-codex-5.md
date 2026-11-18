**Not ready for the slice:** the two reported paths are substantially improved, but the crash handler still leaves the shared run open while it waits for the child to exit.

1. **The stop is written after child cleanup.** In [run_fresh.py](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py:188), an unexpected launcher error calls `end_child()` before `record_crash()` stops the ledger. The interruption path does the same at [line 257](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py:257). `end_child()` can wait up to ten seconds before killing the child. During that wait the launcher still holds its lock and the ledger is active, so another draw—and a child slow to terminate—can pass the gate and send after the crash was detected. If cleanup itself raises, the `finally` block can still remove the registration without recording the stop.

   **Smallest fix:** persist the shared stop first, then terminate and wait for the child, then record the attempt. Keep the registration if stopping or cleanup cannot be completed. Add a test that holds child cleanup open and checks that another draw’s send is refused during the wait.

2. **An interruption can land just after `started` is saved but before it is recognized.** At [lines 252–254](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py:252), the attempt is written as `started` before `started_any` becomes true. A signal in that interval reaches the outer handler with `started_any == False`; it unregisters without stopping the ledger, although the persisted attempt is unfinished. **Smallest fix:** make crash handling cover this transition as well, and test an interruption at that point.

The new ledger-locked claim does close the stale-registration race I raised last round: the probe, lock acquisition and registration share the ledger lock, and the still-registered check covers a death between probe and acquisition. The new unexpected-error test also proves the ordinary cleanup path reaches a stopped state; its fake child exits immediately, so it does not exercise the delay above.

I read the updated code, tests and recorded proof output. I did not rerun them in this read-only review.

Council position: not ready, because crash cleanup must stop the shared ledger before waiting and must cover the transition into a started attempt.