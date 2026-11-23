Fixed. Re-read `clean-arch/e2e-2026-11-09/budget.py` (worst_cost, cost, send) and the new test at the end of `test_adapter.py`
(read-only, under 150 words).

1. **Usage.** `cost` returns None unless the answer reports non-negative integer prompt_tokens and completion_tokens. In that case the
   attempt keeps its full reserve. A test sends an answer without usage and checks the charge equals the reserve. Cached tokens are
   clipped to prompt_tokens.
2. **The input bound** is now the body's UTF-8 bytes as sent (json.dumps escapes non-ASCII). Byte-level tokenizers emit at most one
   token per byte, and the body's JSON keys cover the chat template's few tokens; the docstring states this. Rates are model.PRICES,
   the published rates AGENTS §7.2 prescribes. That is the evidence available; it cannot cover an unannounced price change.

`prove` re-ran on this code: passed, 1018/1018 matched and as sent, 0 differing. Tests: 14 passed.

SEND or BLOCKER?
