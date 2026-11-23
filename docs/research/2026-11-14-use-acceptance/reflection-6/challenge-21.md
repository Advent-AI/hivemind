# Challenge 21: the due-day candidate, prepared at $0 as round 20 asked (`reflection-6/due-day/`)

Read `due-day/audit.md`, `candidate-system-v2.txt`, `dueday_probe.py`, `test_dueday_probe.py`, `mutants.txt` and `check-output.txt`.

**The blind whole-request audit** (`audit.md`, a fresh Codex session):
- **The changed clause:** "consistent with D210 and D185". The frozen clause "keeps wider than D210" and "conflicts with D403".
- **No gap:** events take D403's stated date or period end, and an event with neither declines.
- **Its "NOT CONSISTENT"** names two things outside the change:
  1. **The unchanged reader brief's D row still holds the wide rule.** D is not a hard line and the reading form stays unchanged.
     In both screens, both families already failed D on the next-annual-filing completion dates and preferred the stated date. The
     gap is recorded for Alex's page, not fixed.
  2. **A pre-existing D414 tension** (the request asks the model to estimate an annual figure's day that code then sets). It is not
     touched here.

**The probe:**
- **Arms:** astra on the frozen request (a fresh control) against astra on v2, interleaved, 2 draws, 36 sends.
- **Topics:**
  - the signed completion, with a stated date and with a closing window (one matter, two forms);
  - the guarantee with a stated date;
  - three obligation amounts at the next annual filing;
  - an unsigned acquisition;
  - two period-end events.
- **Cap and cost:** $3.20, against about $1.5 measured. About $5.3 remains of D439.
- **Requests:** checked to be the stored frozen ones, with v2 differing only in the clause, byte for byte.

**Verdict fixed before:**
- **Inconclusive** if the frozen arm does not date the fortnight completion at the annual filing (no mechanism to fix).
- **Moves**, when all of these hold:
  - v2 dates it at 24 March 2028 in 2 of 2, and the closing-window form at 30 June 2027 in 2 of 2;
  - every amount control stays at the next annual filing, and the guarantee at its stated date;
  - the event controls stay within the outcomes every stored draw gave;
  - v2 makes no more declines than the frozen arm.
- **Closes:** otherwise.
- **Then:** I read every question and its rungs in both arms for any other change before recording anything.
- **What "moves" is:** one matter in two forms, a small diagnostic. It is no gate pass.

**Proofs:** tests 7 of 7, and four mutants each caught by a failing assertion.

**Asked:** send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
