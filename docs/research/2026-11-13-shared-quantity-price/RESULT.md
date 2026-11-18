# Production's opening rule with a price (D480): result, 2026-11-13

**Answer: it fails. With "quantity or price" in its rule, production still proposed no memory-price question in any of 45 sends on the five
memory articles across three draws (neither arm did; no candidate was proposed and dropped). The model's own account: it reads the new
rule, says such a question would need industry_aggregate, and declines because the article gives "no defined price measure or calendar year
… and does not report a specific memory contract price": it wants a stated figure and period before it will write the question and its
ranges.** The change also cost elsewhere: fewer candidates overall (target articles 5 → 0, the supply-commitment obligation question; capex
articles 20 → 12) and more statements dropped with no home (target articles 91 → 114, capex 7 → 18, random articles 19 → 28).

180 sends, all valid; $0.25 at published rates (ledger, every attempt settled); the byte check holds (every answer's keys in production's
order: evidence, candidates, new_groups). Records `answers.jsonl`; accounts `accounts.json` ($0.004).

| line (frozen in `PROBE-DESIGN.md`) | price | stored | result |
|---|---|---|---|
| target: a kept memory-price candidate (15 article-draws × 3 sends) | 0 of 45 | 0 of 45 | **not met** (0 of 15 hold) |
| noise: kept candidates `price` adds on 12 random articles | none (the same Kyber and H200 questions both arms keep) | — | no regression |
| aggregates: the capex aggregate kept (p1 / p2 / p3) | 2 / 2 / 3 of 3 | 3 / 3 / 3 | met (no draw fewer by two) |
| reported: kept candidates, all cases | 16 | 29 | fewer |
| reported: statements dropped with no home | 160 | 117 | more |
| reported: kept statements | 262 | 274 | about the same |

**What it shows.** The price was not what stopped production; its one-call design is. Production writes a question's ranges when it opens it,
and the model will not write ranges for a price the article describes only as "climbed sharply" or "skyrocketed". That is the same pattern
c19 showed when the clean path's first step was made to write outcomes in the opening call (memory opened less). The standard's own example,
"2027 年 DRAM 合约价相对 2026 年的变化", is a change against the year before, which needs no stated level; the request does not say a price question
may take that form.
