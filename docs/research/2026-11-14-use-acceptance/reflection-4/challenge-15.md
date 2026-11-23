# Round 16: your three points are fixed and checked at $0. Go or no-go on the one send.

1. **E** is counted with the unresolved (both countings and the more-than-4 limit) and reported apart. Your counterexample run on
   made-up accounts (C on every failed case, E on every passed case): 23 unresolved or E, so **unclear**; 23 false alarms under the
   second counting.
2. **Population:** the scorer refuses unknown or duplicated cases (checked: both refuse) and scores a missing case as unresolved
   (checked: 30 records of 45 lists the 15 missing).
3. **Cost:** the added messages are bounded at one token a byte (a token holds at least one byte) plus 50 each; the original
   input is the provider's recorded count for the same content; output at the full allowance; no cache discount: **$0.403**. A
   usage missing either count is charged at its bound; an output above the allowance is a breach; after each batch of eight the
   script stops on a breach or if spend plus the remaining bounds would pass $0.45.

`self-report/DESIGN.md`, `self_report.py`, `score_self_report.py`. End with `CONSENSUS: yes` (send as designed) or `CONSENSUS: no, because …`.
