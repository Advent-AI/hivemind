# Council mo, the slice, round 3: the measurement record made independent of the ledger, and split by call kind

Both findings held. Changes (`budget_replay.py`, `budget_step2.py`, `spend_by_component.py`):

1. **The attempt line never blocks a stop, a charge or an overrun.** `SharedLedger._note` is now called only after the ledger's state is
   saved (after the `_locked` block in `reserve` and `settle`), and is best-effort (an `OSError` is swallowed). A crash between the two
   writes leaves the lines short of the ledger, never ahead; `spend_by_component.py` reports the ledger's spent minus the lines as
   "unaccounted". Check 18 (`check_budget.py`, 18 of 18): with every append failing (the lines path a directory), an overrun and the stop
   are still saved and a later reservation is refused; mutant "the line may raise" caught.
2. **Each line carries its call kind and reported tokens.** `settle(reserved, actual, kind='llm', tokens=None)`; the Step 2 wrappers pass
   `embeddings` or `jev` with the reported tokens (failure paths with their kind), production's Jev path `jev`; the tally splits each
   component by kind. `proof_end_to_end.py` now also requires Step 2 split into embeddings and Jev with tokens reported: 3 of 3 (Step 2:
   embeddings 1 call, 6,555 tokens; Jev 18 calls, 67,372 input tokens).

Reruns: touched suites with the frozen checks 283, full suite 287, `proof_interception.py` stop/retry/step2 3 of 3.

Launch the slice exactly as in `mo-slice-proposal.md`, with the preflight and these measurement records?

End with: "Council position: <launch the slice | change ... first>".
