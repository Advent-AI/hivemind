# Round 99: the $0 proofs (D587) are done. Decide the paid run on their numbers.

`unlisted-parts/fresh-a2/fresh_a2_proof.py` → `proof-output.txt` (ALL OK; mutants dropped-thesis and truncated-not-flagged both FAIL):
- F1: the week 10-13..19 = 383 items, same set and order through both systems' entries and today's census.
- F2: the starting library = the 10-06 week's completed state (272 articles complete from empty, window to 10-12), 13 topics = its 13
  cases.
- F3: today's run loop rebuilds stored 10-06 requests byte for byte (first, middle, last) from their stored libraries.
- F4: for the test week's first 3 articles, carried vs empty requests differ only in the open questions (13 vs 0).
- F5: one system text (15,828 chars) across all 272 stored requests; settings deepseek-flash, high, 64k.
- F6: a run cut after 100 of 272 reads as incomplete with only its completed articles' topics (8); no verdict.
- F7 cost: the 10-06 continuation charged $0.0094 an article for normal attempts; 8 of 201 attempts were cut and charged at their
  reservation (~$0.12 each), the cause being the laptop sleeping (RUN-STALL-2026-11-15; since then each call waits at most 600 s, D552).
  383 articles: $3.60 with no cut attempt, $6.06 at that cut rate. Reader workload: n·6+3 items per family (n=5: 2 packets; 10: 3; 15: 5),
  third readers on about 2 in 3 sends.
- Frozen inputs: `fresh-a2/inputs/` manifest `587c0647…`, starting library `b85458ff…`, settings `7716a85d…`.
Yield unknown: from empty the 10-06 week opened 13 topics in 272 articles (8 in the first 100); from a carried library fewer.

My proposal: send the first step on the whole week, detached with caffeinate, network checked, a new ledger ceiling $6.50 (D439 after
≈ $33 of $40), the frozen Step 1 (`clean-arch/step1/run_live.py --manifest --initial --settings --limits`), nothing else live; then at $0
build the opened-topic cases, the blind population classing, and the control-vs-A2 harness (checked as the probes were) and return to
you before the answer-choice send (~$0.10). Stop rule: a ledger stop or crash = incomplete, no verdict, back to you. Is the run worth it
given the yield risk? End with `CONSENSUS: yes` (send the first step) or `CONSENSUS: no, because …`.
