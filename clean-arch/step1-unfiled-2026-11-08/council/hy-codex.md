NOT READY.

For example, after the spending limit refuses one request, another worker may finish and free enough money for a waiting request to go out. The design says the test stops, but does not say how concurrent workers stop sending.

1. **The stop rule does not settle what happens to concurrent work.** [DESIGN.md:767](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:767) says a refused reservation stops Stage A. The existing limit raises only in the worker making that reservation; it has no shared stop flag ([budget.py:63](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:63)). A different worker can finish, release its reservation, and let a queued call or transport retry send before the runner observes the failure. Two engineers could therefore send different numbers of requests after the stop. The fix must specify when the stop becomes shared, what happens to queued calls and retries, how already-sent calls finish and are charged, and when the final spend is read. Test that interleaving.

2. **The binding-obligation exception is contradicted in the no-question table.** [DESIGN.md:485](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:485) says a figure beyond next year is refused if a ladder is written, while [check 5](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:383) and [production](/Users/lchingen/hivemind/src/hivemind/extraction.py:629) except binding obligations. One engineer could reject such a ladder and another accept it. State the exception in the table’s code cell and test both sides.

The previous review’s three findings are addressed: Stage A no longer resumes a stopped folder, the boundary is explicitly 548 days, and the surviving-evidence admission check has its own row. Under the stated assumptions that reservations bound actual charges and the synced ledger writes succeed, I did not construct a reserve/send/charge/process-death interleaving that passes $3 or understates the reported amount: an uncharged reservation is counted in full. The concurrent-stop issue above concerns **additional sends after a stop**, not a demonstrated cap overrun.

Wording: [DESIGN.md:623](/Users/lchingen/hivemind/clean-arch/step4-2026-11-10/DESIGN.md:623) still says the old pattern matches “quarter” anywhere; it excludes the start of “quarterly report.”

I walked §7.1 and §7.3, the Stage A spending text, and the named code paths. I did **not** read the individual rows of `dryrun/`, `dryrun2/` packet A, `dryrun3/`–`dryrun8/`, or `reference/`; nor did I finish every fixture in `examples.json` or every sentence of the Stage A reading form. Their evidence is therefore not independently verified in this review.

