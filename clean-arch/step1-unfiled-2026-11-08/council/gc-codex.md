**BLOCKER: one opened question cannot be matched to two reference questions.** MATCHING-v2 explicitly allows a question covering both 2026 and 2027 to match q04 and q13. But [adapter.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:320) turns repeated `--map` entries into a dictionary, so one match silently replaces the other. That can undercount opened and answered questions.

The remaining checks:

1. Mapped clean questions feed their reference views; several clean questions can feed one view. The 22 seed views start at sequence 0. q23 starts at 0 **only if mapped**, although MATCHING-v2 says to create all 23. The existing leakage checks remain in place.
2. Merging several confirmed matches into one reference view follows the stated rule.
3. The launcher uses the same manifest, settings and limits with an empty start. The continuation still supports numbered Stage 2 paths.
4. Live adapter output remains restricted to the seeded Stage 2 output root; an output inside the unseeded draw folder will be refused. The new tests do not cover one clean question matching two reference questions.

**BLOCKER**