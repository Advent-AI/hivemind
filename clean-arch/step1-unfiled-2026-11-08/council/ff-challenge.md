Both points fixed. Re-read `adapter.py` (send_within_budget, load_draw), `test_adapter.py` and `run_clean_draw.sh` (read-only, under
150 words).

1. **Retries.** Each attempt is now sent alone (`model.openai_transport(..., max_attempts=1)`), and the adapter loops up to three
   attempts with production's rule. HTTP 400, 401, 403 and 404 and undecodable answers are not retried; the waits are 5 s and 10 s.
   - Every attempt reserves its worst case before sending.
   - In one locked step, every attempt is charged its actual cost, or its full reserve if it gave no answer.
   - A test with two failed attempts and a success checks the charge is two reserves plus the actual cost. A 400 makes one attempt and
     leaves nothing in flight.
2. **Stamp.** The launcher writes `step2/inputs.sha256` (trace and library.json) right after Step 2, and the adapter refuses either file
   changing. A test edits the library after stamping and is refused.

SEND (clean arm, pending the control harness) or BLOCKER?
