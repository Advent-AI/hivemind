# Round 62: design version 2 and the $0 harness checks, against your six points. Go or no-go for the send.

`unlisted-parts/DESIGN.md` v2; `make_arm.py`, `arm-a/`, `probe.py`, `check-output.txt`, `check-mutants.txt`.
1. The fourth place (line 13, events: "when the topic's wording names it, list it in not_judged") is changed too; `make_arm.py`
   refuses an arm in which "wording" remains. Arm B stays an idea needing its own audit.
2. Regression watch: L there is reported both ways and does not veto; the veto is every other mark.
3. Rule 2 now covers every mark other than L in every group, the motivating topics included, H among them; H has "cannot tell";
   three planted H controls (two should fail, one, a cap on an approval, should hold), a miss stops the reading.
4. The population is fixed: all 18 stored first requests rebuilt byte for byte by the production builder (July's three included);
   the harness refuses a missing topic or a check record that does not match the arm files; a stopped arm reads NOT MEASURED.
5. What the probe can resolve is stated (about half to about one in ten; not a smaller change); the rule is by topic: inconclusive if
   the control fails L on fewer than 3 of 7 topics; a lead needs the changed arm to fail L on at most 1 topic in at most 1 send.
6. The cap is held by Stage A's limit (worst-case reserve before every attempt at the full output cap, missing usage charged at its
   reserve, concurrency 8, $0.25 an arm, NOT MEASURED on hitting it); the changed request equals the control plus exactly the
   replacements (18 of 18), and the check fails on two mutants (an arm changed beyond the replacements; a control one byte off).
End with `CONSENSUS: yes` (send the probe; then read it as designed) or `CONSENSUS: no, because …`.
