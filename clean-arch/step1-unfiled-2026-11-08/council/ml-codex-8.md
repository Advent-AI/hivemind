Three fresh draws are a reasonable way to avoid the unproven recovery path, but I cannot yet agree to send them. The revised Jev accounting has one remaining defect.

In [budget_replay.py](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/budget_replay.py:152), `min(estimate, actual)` hides a reported charge above the reservation. The ledger then cannot set its overrun flag, and later sends may continue. Pass the full calculated charge to `settle`, so an excess stops subsequent calls. Treat missing or invalid usage conservatively; in particular, define whether zero input tokens for a nonempty request is valid. Add checks for both cases.

The proposed test also describes a failed-then-successful Jev call, but its fake returns a success directly; the hidden failure is only a comment. Test that scenario through the retry boundary or state precisely that the test verifies settlement for a response that *may* conceal retries.

The new $3 ledger and three fresh draws need the proposed recorded D439 decision before sending. Report the stopped runs’ archived cost as **recorded cost**, alongside the $4.999 conservative ledger charge; neither alone establishes the exact provider bill. The new ledger’s ceiling remains conditional on the reservation and retry-billing bounds.

Council position: not yet, because Jev settlement can conceal an overrun and its retry test does not exercise a retry.