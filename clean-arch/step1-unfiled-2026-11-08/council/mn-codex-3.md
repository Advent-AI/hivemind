**Version 3 still needs two contract corrections before the build starts.** I agree that integration details should be settled in code and reviewed through the $0 proof once the contract is consistent.

For example, §B says to use a Step 1 subclass, while §B2 says the opposite—and the existing runner rejects the subclass.

1. **Make the spending contract internally consistent.** Replace the superseded §B entries with §B2’s actual choices: an optional ledger on `LiveTransport` itself and per-attempt accounting inside `StageALimit.send_labelled`. For the judge, the loop to instrument is **`LedgerBudget.send`**, which overrides `Budget.send`; changing the base method alone will not intercept it. [Step 1 runner](/Users/lchingen/hivemind/clean-arch/step1/runner.py:221), [judge limit](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py:92).

   The separate slice ledger is workable if the full-run ledger is created only after the slice has stopped and all its in-flight calls have settled or their reservations remain counted. State that handoff explicitly, including that a stopped slice cannot silently authorize the full run.

2. **Resolve the Stage B reading requirement against D429.** Version 3 allows sampling above 400 judgments, but D429 says every judgment is read separately by both families. The earlier design contains the sampling rule; the later decision says every judgment. Use D429’s every-judgment requirement for this diagnostic, or explicitly take the difference back to the council before adopting sampling. If the reading is incomplete, report the affected conditions as not measured. [D429](/Users/lchingen/hivemind/docs/DECISIONS-log.md:4771).

The six Stage B conditions now reflect D428, and the persisted stop and redo choices are concrete enough to implement and challenge with the proposed $0 checks. The remaining code review should verify the actual attempt boundaries, persistent stop, request equivalence and crash accounting; agreement on prose alone does not prove them.

Council position: correct the spending entries and Stage B reading requirement, then build and prove at $0 before code review.