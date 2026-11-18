# Round 29: the stick check, version 3. Go or no-go.

`gate1-stick/DESIGN.md` (version 3), `controls.json` (frozen), `compare_readings.py` and `compare-selftest.txt`:
- The "fewer than half recur" line and its conclusion are gone; the comparison reports, per line and treatment, both / first only /
  second only with each set's size and the union's (an empty union said so); afterwards only what it shows is said, no apportioning,
  no probability.
- The comparison runs the gate's own accounting on each reading; "not measured" kept apart; tested on a copy altered in known ways:
  a new agreed Q fault on clean-5 pass 1 shows as line 1 "second only", the R fault removed on clean-7 pass 1 as line 3 "first only",
  and a deleted third-reader ruling makes that reading "not measured" with no comparison of its sends (both runs in
  `compare-selftest.txt` and above).
- Six controls frozen with expected marks (three faults I confirmed, one each of Q, R, L; three sends I read as sound), author-checked,
  reported, deciding nothing; the fresh readers see the same items, no first-reading mark, no sign of the controls.
- Limits stated: one re-reading of one fortnight; the families' recurring standards and the same order can make agreement look
  stronger.

End with `CONSENSUS: yes` (run the re-reading as designed) or `CONSENSUS: no, because …`.
