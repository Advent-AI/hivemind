**BLOCKER: successful retries can still make the $3 cap undercount spending.**

For example, an attempt may be billed but lose its response; a retry then succeeds. The adapter reserves for three attempts, but afterward records only the successful response’s cost and releases the rest. Later calls can spend money already used by the lost attempt. See [adapter.py](/Users/lchingen/hivemind/clean-arch/e2e-2026-11-09/adapter.py:231).

The locked release and cost update fixes the concurrency gap. The launcher’s stamp also checks that the trace bytes match, though it does not detect a later change to the library itself.

**BLOCKER**