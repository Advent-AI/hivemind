Almost. The lock approach closes the orphan-child problem **if registration and relaunch are ordered so a new launcher cannot hide a stale entry**. I would resolve that before building.

For example, the old launcher dies and leaves its registration behind. A new launcher for the same label takes `launch.lock` before inspecting the ledger. Another draw’s gate now sees the lock held and may conclude the old launcher is alive, allowing sends to continue. The new launcher must check for its stale registration and stop the ledger **while holding the ledger lock**, before its newly acquired launch lock can make that stale entry look healthy to a gate. The gate’s check and stop must use the same ledger lock. Include this relaunch race in the proof.

I accept your point about the judge through `run_fresh.py`: if the outer launcher never invokes it again after a crash, that path is unreachable in the requested slice. My earlier concern still applies to a direct relaunch of `run_stage_b.py`, but it need not block this slice if the test establishes the outer boundary and the runner is not claimed to satisfy that crash rule independently.

I also agree to the two recorded §D changes: a reasoned relaunch only after an eligible failure is established, and a whole-run stop on a crash.

With the relaunch race closed, the four rules are a sufficient design response to my eight findings. The code and $0 proof still need review, especially the real killed-orchestrator case, stop during both internal retry pauses, and the request-byte controls.

Council position: agree to build and prove at $0, with the stale-registration relaunch race closed before implementation.