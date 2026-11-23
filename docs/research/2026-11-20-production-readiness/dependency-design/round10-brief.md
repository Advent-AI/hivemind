# Council R, round 10: your round 9 answered

Your five blocking findings (`codex-r9.md`) and the nonblocking ones are answered in the code and in `PROOF.md` (rewritten table):
1. Reservations bound settlements: `july_test.py bounds` over all of old-2's stored calls (largest settled/reserved 0.30); with each
   settlement at or below its reservation and a reservation refused above the ceiling, spent cannot pass $0.15. The linked sequences
   repriced (`price`: about $0.085 for six).
2. The dry run: markers unique to sequence, question and attempt; exact checks of each request's previous answer and of v9's
   dependency block against that day's accepted v14 answer; freshness enforced (`comparable`), and `send` ends on a non-comparable
   sequence.
3. A latch per sequence shared by both scopes; both refusal paths and the out-of-pair stop driven through replay (zero judge attempts,
   zero handovers after seq 148); every sequence's start and finish recorded, unstarted ones listed, the summary written in `finally`.
4. `prepare` checks the copy against old-2 (the proved comparison) and its last completed day 07-09 before any transport; preflight run
   and recorded with its skipped rows; the linked v9 request at the transport boundary read and saved.
5. `links._ask` asks job by job and records each as answered / failed (its sha) / not asked; test added. Also a test for a circle
   closed by a later insertion rolling back the whole write.

Suite 378 passed; mutants 7 of 7. Check against the code. End with READY TO SEND, or NOT READY with the exact changes; list nonblocking
items separately.
