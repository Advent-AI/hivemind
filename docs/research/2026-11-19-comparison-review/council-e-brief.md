# Blind review of a design (read-only, $0). Under 250 words, ending `READY` or `NOT READY: <smallest change>`.

Review `DESIGN-refused-not-open.md`: a thesis the ladder refuses does not enter Step 1's open-thesis state, and the ladder runs at opening
inside Step 1's loop. The evidence for why it is needed is the census C section of `PATH-TO-PASS.md`.

Check against the code: `clean-arch/step1/runner.py` `run`, `clean-arch/e2e-comparison-2026-11-13/run_fresh.py`,
`clean-arch/step4-2026-11-10/stage_a/build_cases.py` and `stage_a.py`.
1. Are the state × event table, the value × reader table and the new-path × old-checks table complete?
2. Does it break a frozen piece or a prior decision?
3. Is there a simpler place for the rule?

Nothing is built, and nothing is sent.
