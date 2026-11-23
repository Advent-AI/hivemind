Both remaining points were fixed. Re-read `clean-arch/e2e-2026-11-09/adapter.py` and `test_adapter.py` and confirm, or name what is
still wrong (under 200 words, read-only).

1. **Library check.** `load_draw` now compares every library copy (originals and members) with the trace's record on ten fields: article,
   input_id, summary, passages, parties, tier, dates and thesis_ids. It also refuses revisions and later links that name unknown groups
   or records. On the stored dev draw all 277 copies match. A test edits one member's summary and is refused; a scratch mutant that
   skips the check fails that test.
2. **Cap.** Each call reserves its worst case under a lock before it is sent: request characters as uncached input tokens, plus the
   16,000-token output cap at gpt-6-luna's rates. It refuses when spent plus in flight plus this reserve would pass the cap, releases
   the reserve after the call, and adds the actual cost, bounded by the reserve. A test with about $0.007 per call checks that the
   final spend is at most the cap and nothing is left in flight; a mutant that checks only past spending fails it.
   Retries in model.call each pass through the transport, so each reserves.

End with SEND (clean arm, pending the control harness) or BLOCKER.
