# Council round 41: the probe harness and its $0 rehearsal, before the paid send (read-only)

The design you passed (round 40f, `PROBE-DESIGN.md` v5) is built. Review the harness against the design and the rehearsal against what
it claims, before the paid send of up to $0.50 (D715). Read: `probe.py` (the sender, the request-time check, the order and start rule),
`probe_read.py` (packets and the ordered verdict), `probe_rehearsal.py` (the stub beneath the real budget transport, scenarios, verdict
cases, check equivalence), `rehearsal.log` (41 checks, REHEARSAL PASS), `probe-plan.json`, `probe-targets.json`, `stored-v7-support.json`
(the stored accepted v7 answers' support for the four material targets, frozen before any send), and
`clean-arch/e2e-comparison-2026-11-13/budget_replay.py`. Fixed during the rehearsal (disclosed): the stub first judged the format with
the function under test, so the open-format mutant passed; it now builds the expected formats itself and the mutant is caught. No paid
call; out of scope as before.

Questions:
1. Does the harness implement the design exactly (order, fresh archives per draw, the start rule before any reservation since a refused
   reservation stops the ledger, the A2 condition, request-time checks, records)? Find a defect that would spend money wrongly or let an
   incomplete or wrong run reach "pass".
2. Is the verdict code exactly the §3 order and conditions? Any case the verdict cases miss?
3. Is the rehearsal real (the stub beneath the real budget transport, byte checks independent of the code under test, the stops)?
Answer READY TO SEND or NOT READY with blocking items only.
