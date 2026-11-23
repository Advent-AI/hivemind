# Round 65: both points built, tested and mutant-proved. Go or no-go for the send.

1. H adjudication path: `h_disputes.py` writes the third readers' H packet from the actual disagreements (the item as the first
   readers saw it, the part, both marks as "a"/"b" with sides drawn per point from a fixed seed; plants excluded) and
   `h-third-reader-brief.md` asks for one line per point into `h-rulings-<family>-1.jsonl`. Test: two disagreements on changed
   harm-control sends → the packet holds exactly those two points with both marks unnamed → both families rule `settlement` → the
   changed arm fails H on two sends against none → negative. Mutants (rulings ignored; every part sent) fail it.
2. A missed plant now returns "STOPPED: a planted control was missed" before any verdict; tested with a strong and a weak control;
   the mutant that checks the plant after the inconclusive verdict fails the weak-control case.
Wording: preflight "unexercised, not passed", its 2 skipped matching records noted; the ladder replay "17 written answers, all
accepted; the eighteenth a refusal the replay does not judge".
Tests: test_probe.py 3, test_probe_score.py 14, all pass; every guard's mutant listed in test-mutants.txt fails its test.
End with `CONSENSUS: yes` (send; then read as designed) or `CONSENSUS: no, because …`.
