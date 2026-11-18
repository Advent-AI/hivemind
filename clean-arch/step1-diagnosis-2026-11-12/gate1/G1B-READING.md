# G1-b read by hand (change 2 alone: c15c against c8), 2026-11-13

Run: `poc/data/clean-step1-gate1-2026-11-13/g1b/` (24 sends; 23 answered; one c8 send on the Gulf state lost to the network, a
connection cut after one byte; the Gulf state has no line). Every record read whole with `gate1/print_records.py`.

**Result: G1-b passes.** The pass line holds and no stop fires.

| state | line | c8 (3 sends) | c15c (3 sends) | verdict |
|---|---|---|---|---|
| positive: the capex article, d1 step 42 | the candidate retains a capex thesis in 3 of 3 | 3 of 3 | 3 of 3 | **pass** |
| negative: Goldman's $765bn estimate, the capex thesis (clean-4) open, d1 step 66 | bad: opened as a new thesis, or not kept | kept and linked to clean-4 in 3 of 3; no new thesis | kept and linked to clean-4 in 3 of 3; no new thesis | **no stop** (0 against 0) |
| single customer: the Firmus and Sharon AI announcement, d1 step 1 | bad: a thesis on a customer's own deployment or capacity | 0 of 3; each send opens a thesis on NVIDIA's own credit support to AI clouds | 0 of 3; the same credit-support thesis in each send | **no stop** (0 against 0); the credit-support thesis is line 110's allowed exception |
| Gulf buyers' combined spending, d2 step 237 | reported, no line | 1 of 2 answers opens a combined Humain and G42 spending thesis; 1 send lost | 0 of 3 open a thesis | reported |

**What the reading shows beyond the lines.** On the positive state, the year defect is visible under change 2 alone, as expected: c15c
send 2 holds both years in one thesis, send 3 asks 2027 only; c8 send 2 holds both years, send 3 asks 2027 only. That is change 1's
case (G1-a). On the Gulf state the scoped counterexample did not make the model open the aggregate (0 of 3), so change 2 does not by
itself open a doubtful aggregate.
