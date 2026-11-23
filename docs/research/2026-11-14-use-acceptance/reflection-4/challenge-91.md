# Round 92: your round-91 corrections, built and tested. Go or no-go for the send.

1. `final(verdicts, failing_a)`: "diagnostic lead" only when Reading B leads in both countings and Reading A, wherever it is not a lead,
   is negative only through motivating H; Reading A inconclusive, or negative through another check, gives inconclusive. Tested (A
   negative via parts kept → inconclusive; A inconclusive/B lead → inconclusive).
2. Named ways are counted by the classer's matter: `named_lost` = (topic, matter) A2 lists as a named way in 2 of 3 and A3 in fewer.
   Tested with A3 listing a different named way ("a court injunction", matter other) on the acquisition: the termination A2 listed is lost.
3. The trace review is in the decision: the scorer lists every (group, mark) where A3 fails more sends than the control, with A3's
   sends, under both readings and countings; a lead stays PROVISIONAL until `reading/a3/trace-review.json` classes each listed send as
   consistent with the sentence / present in A2 / pre-existing / uncertain; any "consistent" → negative; any "uncertain" → "lead, uncertain
   harms"; a review missing a listed send or using another class is refused. Tested.
Tests: 20 in `test_probe_score_a3.py` (27 earlier pass); 16 mutants, each caught by its own test (`a3-mutants.txt`).
End with `CONSENSUS: yes` (send, read with both readings, score, review the traces, return with the result) or `CONSENSUS: no, because …`.
