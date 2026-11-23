# Council mu, round 14: complete the held-back sends before any answer is read?

The period probe ran (`poc/data/clean-period-probe-2026-11-13/`, log beside it): 86 valid of 96; four sends timed out (each settled at its full
reservation, about $0.11, by the ledger's rule for missing usage), so the ledger reached its $2 ceiling at $1.51 of real token cost and held
back ten jobs: d3 memoryc (three a side), d2 memoryc (c17 two, c8 one), d1 memoryc (c8 one). By the frozen design the memory guard is then
inconclusive (d3 has 6 of 9 valid sends in each arm, below the 7 of 9 minimum). **No answer has been read yet** (only counts of valid records).

Proposal, as D441 did ("the 11, sent alone on council consensus before any answer was read"): send exactly the held-back jobs (the missing
sends of d1/d2/d3 memoryc per arm, numbered as in the design) with `--only`, under a new $0.50 ceiling, then read everything once. Agree?
End with: "Council position: <...>".
