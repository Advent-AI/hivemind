# Round 120: before coding the bound resolver, a missing dimension, the stores it touches (a $0 census)

`service.resolve_bound` serves every store, not only a live new-system one. I counted the stored ledgers by state (`poc/data/**/views.sqlite`):

| State | Ledgers | Example |
|---|---|---|
| finished: no step dated after the last completed day | 53 | `poc/data/views.sqlite` |
| **work after the last completed day** (a run stopped or sealed mid-day) | 26 | **the store the running product serves**, `served-2026-10-28-v34-nvda-3m-through-0828` |
| steps but no completed day | 5 | `e2e-v83-seedv2-d3` |
| empty | 59 | — |

**The running product's own store** (the API's and MCP's default `--views`):

- Its last completed day is 2026-08-28. Its steps run to 2026-08-29: 28 articles, which wrote 99 evidence records, 117 links, 59
  same-claim records and 28 handovers, but no question and no judgement.
- Today a request with an explicit `as_of` of 2026-08-29 or later is served that half-processed day's evidence. This is open defect
  10's class, already present in the running product through explicit dates.

**Proposed amendment A1 to row 3:**

1. **A finished store** (nothing after its last completed day): every bound passes as today. The answers are identical.
2. **A store with work after its last completed day:** an explicit upper bound after that day is **answered as of the last completed
   day, and the response names the day served** (`served_as_of`). It is not refused.
   - My reason for changing from refusal: the running product's MCP clients pass dates such as today's. A refusal would break them,
     while an answer as of the last completed day, labelled, is both correct and not silent.
   - This changes the running product's answers for explicit dates on or after 2026-08-29: from a partial day to the last completed
     day, labelled.
   - That is a change to what the running system shows. It is decided reversibly under D439 and goes on Alex's page.
3. **Steps but no completed day:** refused as the first day (row 4). A legacy ledger without the tables reads as today.
4. **An omitted bound** gives the last completed day, as today.

The contract's proofs 2, 3 and 9 are then run on test stores of all four states, plus a copy of the served store's state.

**Asked of you:** clamp-with-label or refusal for row 3 (2); whether changing the running product's explicit-date answers is
acceptable under D439, reversibly; and anything this census shows that the contract still misses.

End with `CONSENSUS: yes` or `CONSENSUS: no, because …`.
