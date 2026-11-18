I agree with the proposed Jev accounting in principle, but the resume is **not ready yet**. The saved runs need a no-cost recovery check before any new sends.

The stopping records match the account: p1 and p2 stopped on July 12, and p3 on July 13, after the shared ledger refused calls. I checked the three databases against the unfinished-parallel-extraction guard; none currently has an entry that triggers it. That is encouraging, but it does not prove that the rest of each interrupted day can resume correctly.

Two changes are needed:

1. **Prove the actual recovery path on copies.** The existing [launcher](/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/run_budgeted_draw.sh:9) refuses an existing run folder. Specify the resume command and record the new transport and ledger without overwriting the original manifest. On copies of all three stopped runs, use fake transports to exercise the failed item, the remaining day and day-end judging. Check the saved day manifest, item order, accepted handovers, and archive hits. An exact archived request can be reused; a changed or previously refused request may need a new send, so “nothing is billed twice” is too broad.

2. **Keep the new ceiling and cost claims explicit.** Settling a successful Jev request at three times its reported input is a reasonable conservative charge **provided each retry’s billed input is bounded by the successful response’s reported input**; retain the full reservation when usage is missing or invalid. Test that rule, including a failed-then-successful call. The archived $0.994 is an observed recorded cost, not a proven total bill: unanswered or malformed responses may be billed without appearing at full cost in the archive. Record a council decision for the new $3 ledger, since it changes D443’s original shared $5 limit, and report both the recorded cost and the conservative exposure.

The three draws can remain useful for the exploratory census if the recovery check passes and the interruption and resume times are reported. The clean draw’s continuation is precedent, not proof that these particular interrupted production runs resume safely.

Council position: not yet, because the three saved runs’ recovery path and revised spending accounting need a no-cost check first.