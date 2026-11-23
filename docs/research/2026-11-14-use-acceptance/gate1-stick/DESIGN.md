# Does gate 1's reading give the same answer twice? A repeatability check of the measuring stick (D567's next step), version 3 for the council (rounds 27 to 29)

**Why.** Gate 1 (Alex's six lines, D400) has been missed in all nine readings, by a few sends a line, with no one fault class
(D557; `carried-run/faults_by_topic.py`). Lines 1 to 3 allow no fault on any written answer choice. Whether a second reading of
the same answer choices, by the same method, names the same faults has never been measured (searched D396 to D567; Stage B had
`stage_b/line_chance.py`, Stage A none). This check measures that: how much of each line's verdict and of its failing sends
changes when the identical sends are read again. It does not establish which reading is right, does not apportion the nine
misses between the step and the reading, and changes no line (council round 27).

**The re-reading.** The fortnight's gate-1 reading (`poc/data/clean-carried-run-2026-11-16/stage-a/`, 39 sends) is read again from
the start by the unchanged tooling and the unchanged briefs, in a new folder: the same packets (`build_reader_packets.py`, same
seed), two fresh first-reader sessions of each family, the disputes and named W faults sent to two fresh third readers, one of
each family (`collect_readings.py disputes`, `ladder/stage-a-third-reader-brief.md`), and the report with both treatments of
unresolved points (`collect_readings.py report`). The first reading's files are copied, never edited.

**Controls** (`controls.json`, frozen before any re-reading; checked by Claude against the article and the brief:
author-checked, not independent; reported, deciding nothing): three sends whose fault Claude confirms (Q: `c1/clean-1` pass 3, the
question leans on an unnamed lab; R: `c1/clean-7` pass 1, "and" in the question against "or" in the Yes rung; L: `c1/clean-13` pass
1, two of the thesis's checkpoints neither asked nor listed as not judged) and three sends Claude reads as sound on Q, L and R
(`c1/clean-5` pass 1, `c1/clean-9` pass 2, `c1/clean-11` pass 3). The fresh readers see the same items as before, with no mark of
the first reading and no sign of which items are controls.

**The comparison** (`compare_readings.py`, written and tested before the re-reading on a copy altered in known ways: a new fault
appears as "second only", a removed one as "first only", a missing ruling makes the reading "not measured" and stops the comparison
of its sends; `compare-selftest.txt`). It runs the gate's own accounting (`accounting.account`, as `collect_readings.py report`)
on each reading under each treatment of unresolved points and reports, without a conclusion of its own: each line's verdict in
each reading, "not measured" kept apart from met and missed; for lines 1 to 3 the failing sends in both readings, in the first
only and in the second only, each with its size and the union's (an empty union said so); per send the Q, L and R values that
changed; the W faults upheld in each reading with their reasons; line 5's counts of topics right (the accounting's counts, not
their identities); the dispute shares; the controls against each reading. It refuses two readings of different sends and a reading
without third readers of both families (no one-reader fallback).

**What is said afterwards:** what the comparison shows, in those terms (the two readings agreed or differed on a line's verdict;
how many failing sends recurred, against each denominator). Nothing is concluded about which reading is right or about how much of
the nine misses the reading caused; no probability is computed.

**Limits.** One re-reading of one fortnight (39 sends, 13 topics, related sends); the same two model families, whose standards
recur, and the same packets in the same order, so shared order effects can make agreement look stronger; the briefs as used. Reader sessions are outside every ledger ($0).
