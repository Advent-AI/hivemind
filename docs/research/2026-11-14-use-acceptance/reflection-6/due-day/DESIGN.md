# The due-day probe (council rounds 19 to 22): design

**The candidate.** `candidate-system-v2.txt` is the frozen system text with one clause changed. "for an obligation already taken on,
its next annual filing" becomes "for the **amount** of an obligation already taken on, its next annual filing".
- **Sources:** D210 (the next-annual-filing rule is for "a financing_amount question on the amount") and D403 (an event takes its
  stated date or period end, and "the model chooses no other day").
- **Blind audit** (`audit.md`): the changed clause is consistent; the frozen one keeps wider than D210 and conflicts with D403.
- **Outside the change, recorded:** the reader brief's D row still holds the wide rule (the reading form stays unchanged), and a
  pre-existing D414 tension.

**The arms.** Astra on the frozen request (a fresh control) against astra on v2, interleaved, 2 draws.
- **The 9 topics:**
  - a signed completion, with a stated date and with a closing window (one matter, two forms);
  - a guarantee with a stated date;
  - three obligation amounts;
  - an unsigned acquisition;
  - two period-end events.
- **Spend:** a cap of $3.20, against an estimate of about $1.5.

**The verdict, fixed before.** It is read on the **stored** day, the view's due_day, which code sets for a year's figure (D414).
- **Inconclusive** when the frozen arm does not store the fortnight completion in Feb or Mar 2027.
- **Moves**, when all of these hold:
  - v2 stores 2028-03-24 and 2027-06-30 for the two completion forms, in both draws;
  - the guarantee stays at 2028-04-03 and the amounts at 2027-04-01 (basis expected_publication), in both arms;
  - the event controls stay within every stored draw's outcomes.
- **The review,** two blind reviewers, Codex and Claude, over all 36 answers mixed (`review-brief.md`, key outside the repository):
  - no topic has more material defects in v2 than in the frozen arm;
  - v2's completion questions have none;
  - no new v2 decline is flagged unjustified.
- **Counting:** "agreed" (both reviewers) and "either" (one reviewer). When they lead to different verdicts, the result is
  inconclusive.
- **Closes:** otherwise.
- **What it is:** one matter in two forms, a small diagnostic, not a gate pass.

**Proofs:** tests 11 of 11; seven mutants each caught by a failing assertion (`mutants.txt`); the check passes (`check-output.txt`).
