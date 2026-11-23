# Challenge 16: the complementary screen is prepared at $0; send or not? (`reflection-6/astra/DESIGN-REST.md`)

Read `astra/DESIGN-REST.md`, `astra/astra_rest.py`, `astra/test_astra_rest.py`, `astra/check-output-rest.txt`,
`astra/mutants-rest.txt` and `astra/preflight-rest.txt`.

**Your round-15 conditions, one by one:**
- **Exact complement frozen and verified against the first 12:** it is computed from the first draw's own seed and size, checked
  against the first run's sent topics, and the union is checked to equal the 26.
- **Launcher adapted and tested:** the same launcher, re-pointed by `astra_rest.py`. 4 tests pass, plus the first screen's 16 in their
  own process.
- **Spending guards:** the same, at caps of sol $1.20 and astra $5.00.
- **Blind packets:** 84 sends and the same six controls, a new shuffle seed and a new key outside the repository.
- **Preflight:** `preflight-rest.txt`.
- **The memory-aggregation concern:** I read astra's ladder against its topic and article. The topic asks "the change in HBM/DRAM
  contract prices over calendar 2027"; neither the topic nor the article defines an aggregation. Astra's "equal-weighted mean of
  matched AI-server HBM and DRAM quotations" is its own construction. Both families held it. I record it as a concern, not a counted
  fault, and will read any such construction in this half.

**One defect found and fixed at $0:** the first draft drew the "first 12" with the overridden size and got 14. A test caught it; it is
now mutant R3.

**Cost:** about $1.8 expected, $6.20 at most. That leaves at least $1.25 of D439's $40.

**Asked:** send or not?

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
