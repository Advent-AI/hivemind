NOT READY.

For example, if Stage A sends a request, stops before saving its result, and sends it again after a restart, both attempts receive the same spending-record ID. A second restart can then count only one of the two charges.

1. **The spending cap is not guaranteed across repeated stops.** [DESIGN.md:729](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:729) identifies an attempt by case, pass, request and transport try. After a stop, [line 737](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:737) resends a case without an outcome, reusing that ID. The total is calculated by ID, so duplicate reserves or charges have no defined pairing. For example: a $1 attempt is charged but its outcome is not saved; the restart sends and charges it again; another stop occurs. Counting one charge leaves $2 available despite $2 already spent.

   The fix must give every physical send a durable unique ID across restarts, define how all attempts are counted, and prevent two runner processes from independently using the same remaining balance. Test two stops on the same case, including a stop after charge but before outcome, and competing starts. The existing [budget.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:63) only locks one process’s in-memory balance.

2. **The 18-month boundary allows different builds.** [DESIGN.md:362](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:362) says the production check is kept, but does not specify its calculation. Production uses **548 days** in [extraction.py:529](/Users/lchingen/hivemind/src/hivemind/extraction.py:529); another engineer could add 18 calendar months. Those differ at some dates, so the same answer can pass one build and be resent in another. Specify the 548-day rule and test its boundary.

3. **One old candidate check has no row.** [DESIGN.md:602](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:602) says “the evidence checks” are unchanged, but [extraction.py:595](/Users/lchingen/hivemind/src/hivemind/extraction.py:595) and [line 693](/Users/lchingen/hivemind/src/hivemind/extraction.py:693) also refuse a candidate without surviving evidence, except for an owner’s memo. The new path can create a view when its opening article kept no record ([DESIGN.md:522](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:522)); the judge then waits for evidence. Add an explicit row saying this candidate-admission check is dropped or replaced, why, and what happens before and after a later link.

The previous review’s failed-judge-resend finding is answered: the new row matches the individual commits in [judging.py:319](/Users/lchingen/hivemind/src/hivemind/views/judging.py:319). Its quarterly finding is also answered as a risk rather than a measured number of refusals; the constructed annual question in [dryrun9’s packet](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/dryrun9/packet.json:20) provides the requested example. Its restart finding remains open as described above.

Wording: [DESIGN.md:367](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:367) says the old pattern matches “quarter” anywhere; [extraction.py:435](/Users/lchingen/hivemind/src/hivemind/extraction.py:435) excludes `quarterly report`.

I walked every row of §7.1 and §7.3, the Stage A cap and restart text, and the named code paths. I did not independently inspect the individual packets in `dryrun/`, `dryrun2/` packet A, `dryrun3/`–`dryrun8/`, or `reference/`; their reading evidence remains unreviewed for this angle.

