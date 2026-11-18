# Council mo, round 7: the fail-closed rule's premise widened to "work began", not "an attempt is started"

Your round-6 finding held: the rule was right but its premise was too narrow. `Draw.close` now treats as abnormal any exit of a launch that
began work (`self.working`, set once the refusals are passed and just before the component loop) other than a normal return, as well as any
exit leaving an attempt `started` on disk. On such an exit the shared stop is the first write; then the child is ended; then
`mark_crashed` marks the draw `stopped` (and a `started` attempt `crashed`); the registration is removed only after that stop, after a
normal return, or after a refusal before any work. A normal return from `_launch` always leaves a terminal state saved (complete, awaiting
a redo decision, stopped), and no attempt `started`.

Tests (`test_run_fresh.py`, 30): `test_an_interruption_between_components_or_before_the_end_is_saved_stops_the_run` (parametrized: a
signal right after Step 1 is saved completed and before Step 2 starts; and right after the judge is saved completed and before the draw is
saved complete): the draw is `stopped`, the ledger stopped, the registration removed after it, and another draw starts nothing;
`test_a_refusal_before_any_work_unregisters_without_stopping_the_run`. Mutant ("only when an attempt is started") caught (2 tests).
Reruns: `proof_end_to_end.py` 3 of 3, touched suites with the frozen checks 283, full suite 287.

The exits I walked: a refusal before work (identity, awaiting, preconditions, the claim) → unregister, no stop; a stopped ledger at launch
→ a terminal refusal recorded, no stop needed (already stopped); each component outcome → a saved terminal or awaiting state, normal
return; any exception or signal after `working` → stop first; any exit with a `started` attempt on disk → stop first; an error inside
`close` before the stop is written → the registration stays (gate); an error after the stop → the run is already stopped.

Is there any exit left that removes the registration while the run is open, or leaves a child sending with no stop written? If not,
anything else serious before the slice?

End with: "Council position: <ready for the slice | not ready, because ...>".
