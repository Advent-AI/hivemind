The refreshed dry run reached `too small`, and well-formed synthetic reports matched the parent byte for byte across all five verdicts. The round‑15 regression test passed in memory. [Dry run](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/chain-dry-run.txt:1) · [Regression test](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/test_score_comparison.py:321)

Three gaps remain:

- `matter_first_day: null` passes validation and crashes reporting. A null mapping entry or array-valued question ID crashes validation itself. [Container checks](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:195) · [Date lookup](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:389)
- A split containing two identical marks passes. In memory, this reduced the unsplit guardrail count and changed a lead to no winner. The writer emits a settled mark when readers agree. [Split check](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:176) · [Writer](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/mark_cards.py:251)
- `company_figure: 1` passes the frozen-list check against `true`. [Frozen-list check](/Users/lchingen/hivemind/docs/research/2026-11-17-product-comparison/stage0/score_comparison.py:230)

NOT READY: Check container and ID types before access, require different marks in a split, and enforce Boolean company flags.