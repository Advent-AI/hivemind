# Round 75: DESIGN-A2 v2, built and checked to your round-74 points. Go or no-go.

`unlisted-parts/DESIGN-A2.md` v2, `make_arm2.py`, `arm-a2/`, `check-output-a2.txt`, `test_probe_score_a2.py`, `test-mutants.txt`.
- Clause rewritten: D436's three examples only (as examples); "A second side is not by itself a reason to decline; decline only when no
  part is the main one, or when the main part itself meets a case below." The "two bets leave no main part" sentence and the checkpoints
  example are gone.
- Two arms (control and A2), the attribution limit stated; 28 topics: D577's 18, four refusal controls, four recovery leads, two disputed
  (reported only).
- Rule: per-topic refusal retention on every refusal control the control exercises (2 of 3), inconclusive if fewer than 3 are exercised;
  recovery requires a gain of at least 3 correct written answers (no Q, O or R settled failing), inconclusive if the control already
  writes 10 of 12; each recovery's question printed beside both blind readers' named main parts and read by me; rule 2 skips expected
  refusals in those two groups; D577's other rules unchanged.
- $0 checks: 28 of 28 controls equal stored; 28 of 28 changed = control plus exactly the arm; tests 7 new + 17 old pass; five mutants of
  the new rules each fail their test (a first mutant run errored at import for a missing copied module; recorded, rerun).
End with `CONSENSUS: yes` (send A2's probe; read as designed) or `CONSENSUS: no, because …`.
