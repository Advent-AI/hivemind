# The memory diagnostic's result (D440): c15yc does not go on; c8 stays (2026-11-13)

**Result under the frozen rule** (`gate2/memory_rule.py`, sha256 `4fd07cb6…`, unchanged): the memory-price thesis outcome is
**inconclusive** and the retention outcome **proceed**; c15yc goes on only if both say proceed, so **c15yc stops and c8 stays.**

| outcome (54 sends a side; 18 per draw) | c15yc | c8 | difference, 90% interval | rule |
|---|---|---|---|---|
| sends with a memory-price thesis (both readings: all 45 theses are price theses) | 17 (d1 4, d2 8, d3 5) | 28 (d1 3, d2 12, d3 13) | -20.4 points, (-34.6, -4.8) | inconclusive |
| sends retaining every listed memory claim (an empty link allowed; mine and the reader's joined, disagreements against c15yc) | 49 | 49 | 0, (-9.8, +9.8) | proceed |
| v5-like thesis (a 2027 price or the 2026-to-2027 change; my marks; reported, not decisive) | 3 | 13 | — | reported |

Runs: `poc/data/clean-step1-gate2-memory-2026-11-13/` (97 sent; 11 held back by the ceiling) and
`…-memory-completion-2026-11-13/` (the 11, sent alone on council consensus before any answer was read); combined
`combined-records.jsonl`, 18 per arm per draw, no duplicates. Spend $1.90 + $0.20. The late c15yc d3 sends (9–18) opened a memory
thesis in 4 of 10 against 1 of 8 earlier, so the timing imbalance did not lower c15yc. Lost statements were all M2 (the $6.7m
self-sourcing figure), 4 c15yc and 5 c8 by my reading.

**What it shows.** The interval excludes zero: c15yc opens a memory-price question less often than c8 on this article, and when it
does, it asks 2026 (12 of 17) where c8 asks 2027 or the 2026-to-2027 change (13 of 28), the shape of the ruler's seed v5 ("How will
server DRAM and HBM contract prices in calendar 2027 compare with calendar 2026?"). The year sentence that separated the two years of
hyperscaler capex (gate 1: 20 of 26 against 0 of 26) moves the memory question away from the ruler's shape: the fix moved its error to
a neighbouring case (D391). The limits the council fixed hold: the 5% is approximate; sends are assumed independent.
