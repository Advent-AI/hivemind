# Round 100: the exact launcher proved at $0 (`unlisted-parts/fresh-a2/launcher_proof.py` → `launcher-proof-output.txt`). Decide the send.

Through `clean-arch/step1/run_live.py --shared-ledger` with its LiveTransport and stop gate, frozen inputs, only the network send
replaced by a stored "nothing kept" answer of the 10-06 week (with its usage):
- L1: 25 of 25 test-week articles complete; ledger spent $0.0648 = 25 × $0.00259 at usage (`live.ledger_cost`), reserved back to $0 at
  the end; reservations $0.120–$0.157 with the 13-topic library.
- L2: a network loss on attempt 3 is sent again (after the real 30 s wait); 6 attempts for 5 articles; the lost attempt charged at its
  reservation ($0.124); run complete.
- L3: a $0.17 ceiling stops the run midway: ledger stopped ("a reservation of $0.139364 would pass the $0.17 ceiling"), launcher exit 1,
  13 of 25 articles complete, read as incomplete (no verdict).
- L4: largest reservation $0.157, so a $6.50 ceiling holds charges up to $6.34.
- L5: without --shared-ledger the cumulative reservations (mean $0.126) would hit a $6.50 max_usd after ~51 attempts: your round-99
  finding, confirmed. Mutant no-shared-ledger fails L1 (nothing reaches the ledger).
Design updated to $6.50. The send, if agreed: network checked; nothing else live; `budget_replay.py --init-ledger <root>/ledger.json
--ceiling 6.50`; detached under caffeinate with log + pid: `run_live.py --source <items> --output <root>/step1/trace.sqlite --manifest
fresh-a2/inputs/manifest-2026-10-13-10-19.json --initial fresh-a2/inputs/initial-10-06-library.json --settings fresh-a2/inputs/settings.json
--limits <root>/limits.json (max_seconds 28800, max_calls 700, prices as the stored run) --shared-ledger <root>/ledger.json`; root
`poc/data/clean-fresh-a2-2026-11-16/`. A ledger stop or crash = incomplete, no verdict, back to you. After it: $0 build of the cases,
the blind population classing and the control-vs-A2 harness, back to you before the ~$0.10 answer-choice send.
Yield risk unchanged (≥ 5 topics per population and ≥ 2 control L failures needed). End with `CONSENSUS: yes` (send) or `CONSENSUS: no,
because …`.
