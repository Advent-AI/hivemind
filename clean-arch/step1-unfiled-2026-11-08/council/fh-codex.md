**BLOCKER: the new cap can still undercount a paid call.**

For example, if the provider returns a valid response without `usage`, [budget.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/budget.py:38) charges **$0** and releases the full reservation. The provider may still bill that call, and subsequent calls can then take actual spending past the cap. Missing or invalid usage needs to retain the full reservation or stop further sends.

The reservation also assumes one input token per request character and uses locally recorded prices. Those are conservative estimates only if the tokenizer and current billing rates support them; the code does not establish that they are strict bounds.

The other changes check out:

- The proof binds the listed settings and `budget.py`; bytecode writing is disabled in the harness.
- I checked the reference archive: it has 1,018 rows, 1,018 distinct stored hashes, and 1,018 distinct base hashes. The proof records 1,018 matches and zero byte differences.
- The locked reservation handles concurrent attempts and charges failed attempts conservatively. The reported archive replay and tests do not exercise a valid response with missing usage.

I reviewed the code and stored proof; I did not rerun tests or paid calls.

**BLOCKER**