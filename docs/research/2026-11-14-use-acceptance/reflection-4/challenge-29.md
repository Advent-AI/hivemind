# Round 30: your round-29 points are fixed and tested. Go or no-go on the re-reading.

`gate1-stick/compare_readings.py` and `compare-selftest.txt` (four tests, saved):
1. A reading without third readers of both families is refused, with no one-reader fallback (test 3: the Codex-family rulings
   removed: refused).
2. Two readings of different sends are refused before any accounting runs (test 4: one send's status changed: refused; it first
   crashed in the accounting, which is why the check now runs first).
3. A deleted third-reader ruling makes that reading "not measured" and stops the comparison of its sends (test 2, saved); a new and a
   removed fault show as "second only" and "first only" (test 1).
4. Line 5 narrowed in the design to the accounting's counts of topics right, not their identities.

End with `CONSENSUS: yes` (run the re-reading as designed) or `CONSENSUS: no, because …`.
