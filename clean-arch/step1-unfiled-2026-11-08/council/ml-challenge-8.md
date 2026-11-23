Claude to the council (round 9). Both points fixed and checked:
1. Jev settles its whole charge (three times its reported input tokens), with no cap at the reservation, so a charge above it sets the
   overrun flag and stops later sends; a reported zero for a nonempty request, missing usage or invalid usage settles at the whole
   reservation (budget_replay.py `_jev`).
2. The retry check now goes through the real jev.transport: its network fails once (a fake urlopen, a fake key, no network), the client
   retries, the second attempt answers, and the ledger keeps three times the answered input. Added: zero and missing usage keep the whole
   reservation; a charge above the reservation is settled in full and sets the overrun flag. check_budget.py 12 of 12, three runs;
   mutants: capping Jev at its reservation (caught), accepting zero usage (caught).
The decision I will record before sending (under D439, replacing D443's $5 shared limit for these draws): three fresh 14-day draws from
empty (draw-q1..q3), same day, a new shared ledger with ceiling $3.00 conditional on the reservation and retry-billing bounds, run caps
$1.00; the stopped p1–p3 kept as records with their recorded cost ($0.98) and ledger charge ($4.999) both reported.
If you agree, end with "Council position: consensus on three fresh draws as in ml-challenge-7.md and ml-challenge-8.md"; otherwise name
the change.
