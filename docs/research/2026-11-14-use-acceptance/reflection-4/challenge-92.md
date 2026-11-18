# Round 93: your round-92 distinctions, built and tested. Go or no-go for the send.

1. Named ways outside the matter list (classer `other`) are never matched: `named_lost` covers only the listed matters; when A2 lists an
   `other` named way in 2 of 3 sends of a topic, that topic is "unmatched" and the result is inconclusive unless another check fails.
   Tested: A2 "a court injunction", A3 "a shareholder vote against it", both `other` → inconclusive, not a pass.
2. Diagnostic lead also requires Reading B not to raise the control's motivating H count (`control_h[B] <= control_h[A]`) in every
   counting where Reading A is negative; the two readings differ only on named-way entries, so B then passes only by clearing A3's
   named-way marks. Tested: control raised in B → inconclusive.
Tests: 22 (27 earlier pass); 18 mutants each caught by its own test (`a3-mutants.txt`).
End with `CONSENSUS: yes` (send, read with both readings, score, review the traces, return with the result) or `CONSENSUS: no, because …`.
