# Round 91: A3 built at $0 (DESIGN-A3.md v11, section "Built and checked"). Go or no-go for the send.

- Arm files: system and schema byte-identical to A2; closing +398 characters (the one sentence).
- `probe.py --arm a3 check`: all 28 controls equal their stored first requests; the A2 arm equals control + A2's replacements and A3
  equals control + A3's; 18 stored answers accepted; synthetic accepted, mutant refused; 252 sends, $0.25 an arm by reservation; A2's own
  check output unchanged.
- Synthetic answers following A3 (a restated delay removed ×2; "MIIT blocks or delays" reduced to its named way): all accepted by code.
- Readings: classer packet built from the first readers' packets (topic, choices as shown, entry, matters, no arm); dry run on a copy of
  A2's stored reading: 48 entries, Ruled out shown with "or any other decision against the event of rung 1"; named-way packet from the
  classer's answers; briefs `a3-class-brief.md`, `a3-named-way-brief.md`; `run_readers.py` runs both.
- Scorer `probe_score_a3.py`: Reading A = probe_score unchanged (loading moved into `load_reading()`; A2's score output byte-identical
  after the move); Reading B and every check as v11 states.
- 18 tests (Reading B's four cases, removal range ×6, named ways kept, parts kept, H bar at 2 and 3, unexercised removal, outcome
  mapping, a mismatched A2 arm refused, the whole three-arm pipeline through a fake transport); 27 earlier tests pass; 11 mutants all
  caught by their own tests (`a3-mutants.txt`).
- Preflight: as before, the ladder archive has no extraction rows; the ladder answers are replayed by `probe.py check`.
- Cost ≈ $0.23; spend so far ≈ $26.33 of $40.
What can the send still change: whether one closed-set sentence removes A2's restated outcomes on events without losing a named way or a
part (removal and keep checks), and whether motivating H then sits within control + 2 under either reading. Read the files you need.
End with `CONSENSUS: yes` (send, read with both readings, score, return with the result) or `CONSENSUS: no, because …`.
