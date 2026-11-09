**BLOCKER: an unseeded draw with no matches cannot enter mapping mode through the normal CLI.** With no `--map` arguments, [adapter.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:336) passes `mapping=None`, so q23 is not created. An empty set of matches is a valid outcome under MATCHING-v2.

The listed changes otherwise work as described: multiple destinations are retained, q23 is created at sequence 0 when mapping mode is active, and the unseeded output root is allowed.

I also correct my earlier read: MATCHING-v2 treats the bundled 2026–2027 question as broader than q04 and q13, not SAME. I did not rerun the tests.

**BLOCKER**