# Round 140: proof 10's design (contract, "Proof 10's design")

The harness `page-contract/serving_while_writing.py` is re-run on the built code. Its writer is the real `replay`, now in WAL with
its lock. It runs at $0 (judge answers come from the stored archive), keeps the same seven pauses and runs detached.

**At each pause, through the real entry points:**

1. **The API, `GET /days` and `/library`:** every existing check holds.
   - The first-day case must now pass: both answer 503 at 2026-09-22 before close.
   - A fresh page is rendered at the same two pauses as before, and its checks hold.
2. **MCP,** loaded once at the first pause, lexical, as its entry point builds it:
   - on the first day, its instructions say no day has completed and `thesis_library()`/`views()` refuse;
   - afterwards, `thesis_library()`'s day and question ids equal `/library`'s at the same pause.
3. **Lock and copies:**
   - `live_lock.acquire` and preflight's `store_copies` are refused while the writer runs;
   - `scripts/snapshot_store.py`, at the two pauses where a day's articles are committed but the day is not completed, gives a copy
     whose last day is the previous one, out of WAL, integrity `ok`;
   - the store is in WAL at every pause.

**Concurrent reads.** A poller asks `GET /library` back to back while the writer runs between pauses. Each answer:

- is 200, or 503 before the first completion;
- serves a day completed before the request was sent;
- never goes backwards;
- equals `GET /library?as_of=<that day>` on the finished store, byte for byte.

**After the writer ends:** the lock is free, the store is out of WAL, and the API answers as of the last day.

**Asked of you:** anything missing, or wrong, for row 2 (one state per request), row 3 (dates), row 7 (who writes) and the
first-day refusal. Is the byte-for-byte equality of a concurrent answer with a later dated read right under row 3, or does the
library carry anything time-dependent that would make it fail for a reason other than a leak?

End with `CONSENSUS: yes` (build and run proof 10) or `CONSENSUS: no, because …`.
