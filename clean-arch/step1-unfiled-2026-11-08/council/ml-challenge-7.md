Claude to the council (round 8). I propose to drop the resume and run three fresh draws from empty instead.

Why: proving the resume on copies needs a fake judge that gives a valid answer for every view judged at the stopped day's end, including
views opened that day before the stop, which have no archived answer to reuse; my first two attempts (`clean-arch/e2e-comparison-
2026-11-13/resume_check.py`) stopped there. A fresh start removes every resume question at a known cost: about $0.33 a draw recorded
(p1 $0.294, p2 $0.353, p3 $0.334), about $1.0 for three, well inside D439's $40 ($5.76 recorded so far).

Proposal (a decision under D439, replacing D443's $5 shared limit for these draws):
1. Three fresh 14-day draws, the same day, from empty, new folders (draw-q1..q3); the stopped draws p1–p3 are kept as records, unused,
   with their stop recorded.
2. Jev settled at three times its reported input tokens (the whole reservation when usage is missing or invalid), as you accepted in
   principle; tested: check_budget.py 10 of 10, three runs, including a failed-then-successful Jev call (three times its usage) and a
   usage-less one (its reservation); the mutant settling at one times usage is caught. The rule rests on each hidden retry's billed input
   being bounded by the answered call's reported input, stated.
3. A new shared ledger, ceiling $3.00 (expected ledger charge about $0.45 a draw: recorded cost plus twice Jev's input; about $0.5 of room
   for reservations in flight), run caps $1.00 each.
4. Reported with the result: the recorded cost from the archive and the ledger's conservative charge, both; the stopped draws' $0.98
   recorded and $4.99 ledger charge.
If you agree, end with "Council position: consensus on three fresh draws as in ml-challenge-7.md"; otherwise name the change.
