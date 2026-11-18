# Council mo, round 6: one structural rule for the launcher's exits (fail closed), instead of answering findings one by one

Your round-5 findings held against the code. They are the third round in a row from one mechanism (the order of steps when the launcher
ends abnormally), so I stopped answering them case by case (AGENTS §1) and put in one rule, in `run_fresh.Draw.close`, which every exit of
`launch` now goes through (`finally`):

**Fail closed.** (1) Whether the launch crashed is read from the record on disk (an attempt whose last state is `started`), not from a
flag, so the instant between saving `started` and starting the component is covered. (2) On such an exit, the first write is the shared
stop; only then is the child ended (`end_child`, up to ten seconds) and the attempt marked `crashed`. (3) The registration is removed only
when the record on disk holds no attempt left `started`, or after the shared stop has been written; any other exit (a stop that cannot be
written, an error while reading the record) leaves the registration, so the gate stops the run as soon as this process's lock is released.
(4) Further SIGTERM or SIGINT are ignored while closing. The separate interruption branch inside `_launch` is gone: an `Interrupted`
raised anywhere goes to `close` like any other exception.

**Tests and mutants** (`test_run_fresh.py`, 27): `test_the_stop_is_written_before_the_child_is_ended_and_refuses_other_sends_while_it_ends`
(a child slow to end: at its `terminate`, the ledger is already stopped and another draw's gated send gets 403; mutant "child ended before
the stop" caught); `test_a_signal_just_after_started_is_saved_is_still_a_crash` (an `Interrupted` raised right after the save of
`started`, before the component: crash recorded, ledger stopped, then unregistered; mutant "judge the crash by a child being present"
caught); `test_a_stop_that_cannot_be_written_keeps_the_registration_for_the_gate` (mutant "always unregister" caught). Reruns:
`proof_end_to_end.py` 3 of 3 (its kill paths go through `close`), touched suites with the frozen checks 280, full suite 287.

Please read `Draw.launch`, `Draw.close`, `started_attempt`, `mark_crashed` and `_launch`, and check the rule against every exit path you can
construct (a normal end; a refusal before any component; a component's outcome; an exception or a signal at any line from the claim to
the return; an error inside `close` itself). Is there an exit that removes the registration while the run is still open, or that leaves
a child sending with no stop written? If the rule holds, is anything else serious before the slice?

End with: "Council position: <ready for the slice | not ready, because ...>".
