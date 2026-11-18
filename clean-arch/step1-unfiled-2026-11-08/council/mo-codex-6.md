**Not ready for the slice:** the new `close` rule fixes both round-5 cases, but it misses an abnormal exit *between* components.

In [run_fresh.py](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py:280), a completed component is saved before the next component is marked `started`. If SIGTERM or an unexpected exception arrives in that interval, [close](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_fresh.py:197) finds no started attempt and removes the registration without stopping the ledger. The run record remains `running`, other draws can continue, and a later launch can resume it. The same gap exists after the final component is saved and before the draw is marked complete.

**Smallest fix:** distinguish an abnormal exit after work has begun from an ordinary refusal or normal return, even when no component is currently marked `started`. Persist the shared stop before unregistering on that abnormal exit. Add a test that interrupts immediately after a completed component is saved and verifies that another draw is refused.

For an attempt that is still `started`, the revised order holds in the paths I inspected: the ledger stops before child cleanup, and a failed stop or record read leaves the registration for the gate. The recorded end-to-end proof covers a killed child and a killed orchestrator, but not the between-components interruption above. I did not rerun the tests or proofs in this read-only review.

Council position: not ready, because an abnormal exit between components can unregister while the shared run remains open.