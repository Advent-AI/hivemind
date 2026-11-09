**BLOCKER: the UTF-8 byte bound is not applied to Jev.**

[budget.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:90) counts Unicode characters for Jev, while [Jev sends UTF-8 bytes](/Users/lchingen/hivemind/src/hivemind/jev.py:32). This affects the reference window: **488 of 545 Jev requests** contain non-ASCII text. One has 1,566 characters but 1,570 bytes. Its reservation is therefore below the claimed byte bound.

The model-call fix does charge the full reservation when the two token counts are missing or invalid, and the new test covers missing usage. The request-body byte calculation also matches the model transport.

I inspected the code and archive; I did not rerun the tests.

**BLOCKER**