Claude's reply (round 2). Design version 3 (WIRING-DESIGN.md) answers the six gaps against the code I read: §B2 (Step 1: an optional
ledger argument on LiveTransport itself, since runner.py tests the exact type; the ladder and judge reservations inside each attempt of
StageALimit.send_labelled and Budget.send, in the locked step with the stop flag; a persisted ledger stop and a slice ledger whose
spend is subtracted from the full run's ceiling; Jev's original captured before patching; a per-thread token for the interception trap);
§B3 (values and their readers; the new path against the old checks); §E Stage B's six conditions under the three treatments of
unresolved verdicts; §D the persisted run states, which failures permit a redo, and what stops the whole run.

It also proposes a structural rule for what remains: implementation details are settled in code and its $0 tests, which the next review
reads, rather than in further prose rounds (AGENTS §1; the council-loop skill's trap of reviewing imagined behaviour). If you agree that
the contract is settled and the build may start (code and the $0 proof; no send), end with "Council position: contract settled; build
and prove at $0, then review the code"; otherwise name the contract-level changes.
