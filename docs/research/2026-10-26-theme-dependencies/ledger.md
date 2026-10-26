# Ledger: the theme block (D191 → D195)

Task 1: zero-cost census (`theme_block_census.py`) on r3 and r4; first version double-counted propagation pairs and read tags from the day marker (Codex finding 7), corrected: 141 additional calls on r4, tagged 14 of 175.
Task 2: design §8 with the AGENTS §2 tables; Codex read-only review (12 findings) read against the code; §8 revised (resume recovery from the ledger, closure row, version gates, readers). Alex chose propagation A: "A 但是仔细思考怎么做才是正确的".
Task 3: tests first (`tests/test_theme_block.py`, 4 tests, all red for the intended reasons), then `judging.py` (block, schema, check, record, round order, propagation, ledger-derived queue), `store.py` (column + migration), `vocabulary.py`, `service.py`; suite 184 pass. Ruling: the block names a theme by its universe id, not its name (judging has no universe handle; the id reads) — cost if wrong: one line of plumbing later.
Task 4: three r4 theses re-judged under v4 ($0.0088): signs as an analyst would give; prompt 1643 → 2264 chars (the block's reading rules, a new input). preflight unchanged. r5 launched detached (`run-all.sh`, pid file) under `poc-v29` over the r4 window.
