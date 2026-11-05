Found **one remaining issue**. The r1/r2 fixes hold.

1. **[P2] Preflight silently skips committed judgements whose archived answer is missing.** [preflight.py:309–311](/Users/lchingen/hivemind/scripts/preflight.py:309) continues without reporting incomplete verification. Reproduced by removing one accepted answer from an **in-memory copy** of the archive: F reported **215 checked, zero refused, two unverifiable**, versus 216 checked beforehand. The missing judgement appears in neither error count. An incomplete or mismatched archive can therefore look clean. Count and report these missing records, and fail incomplete verification.

No further storage, resume, prompt/schema, or v7 behavior findings. Nine card tests passed in memory, including the earlier fixes; additional refusal, rollback, cached recovery, and same-sequence checks passed. Against `HEAD`, 77 v7 requests were byte-identical and 630 answer-check results matched on the same stored states.

The full suite could not start because the sandbox has no writable temporary directory. No files were edited and no paid calls were made.