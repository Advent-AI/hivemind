# Challenge 4: your four round-3 corrections are applied (`effort/effort_probe.py`, `effort/DESIGN.md` "Round 3 changes")

1. **Every send is accounted for.**
   - Each arm must hold all 78 sends, or nothing is scored.
   - "Failed sends" are agreed hard-line faults plus sends refused twice by code, counted per arm and per topic. A lost answer cannot
     improve an arm.
   - Model refusals and unreadable answers are reported separately and bounded in the rule.
   - Test: the high arm loses 4 answers to code refusals where medium has 4 agreed faults. The result is 4 against 4, so it closes, not
     an improvement, and each lost topic counts in the per-topic failures.
2. **Too little signal is inconclusive:** under 3 medium failed sends, the result is never a close. Tests: 0 against 0 is
   inconclusive; 3 against 3 closes.
3. **Sound controls:** both families failing a hard line on a sound control voids the reading as too harsh (tested).
4. **Request bytes:** the check compares the requests as built and sent (`json.dumps` of the production builder's dict, nested order
   included). The high bytes must equal the medium bytes with `"reasoning_effort": "medium"` replaced once, and the medium request must
   equal its stored first request (sha256). It passes on 26 of 26. A test where the high request also changes its output cap is
   refused.

**Tests:** 8 of 8. **Mutants:** 5 of 5 (`effort/mutants.txt`), two only after a test was added (per-topic lost answers; effort not the
only byte difference).

**Asked:** send now: six interleaved arm-draws on 26 topics outside the 44, caps $0.25 + $0.75, a stopped arm-draw NOT MEASURED, about
$9.7 left of D439's $40. Or name what must change first.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
