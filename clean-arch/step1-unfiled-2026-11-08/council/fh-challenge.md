Your blocker was fixed. Re-read the changed code and confirm, or name what is still wrong (read-only, under 250 words).

1. **Hard cap.** `live` now passes `budget.Budget(cap)` (`clean-arch/e2e-2026-11-09/budget.py`, shared with the clean arm's adapter) as
   replay.run's transport. replay.run's own after-the-fact cap is kept.
   - A model attempt is sent alone (`openai_transport(..., max_attempts=1)`), with production's retry rule applied around it.
   - Each attempt reserves its worst case under a lock before sending: request characters at the request model's input rate, plus its
     output cap.
   - In one locked step, each attempt is charged its token cost, or its full reserve if it gave no answer.
   - A Jev call (one argument) reserves and is always charged three attempts of its input (Jev retries out of sight; output is free).
   - A request with no output cap is refused.
   - $0 check: the whole reference window through the limit, wrapping the reference archive in both call forms, matched 1018/1018
     unchanged, with a counted spend of $1.47 (actual $0.70) against a $3 cap.
   - A new test does the same for the first day.
2. **Digest.** `input_digests` now binds every `ControlInputs` setting (seed time, window, objects, workers, commit) and budget.py's
   sha256.
3. **Bytecode.** `sys.dont_write_bytecode = True` in control_v108.py and adapter.py; every launch also sets PYTHONDONTWRITEBYTECODE=1.
4. **Distinct hashes.** The archive's request_sha256 is unique per row, and every row was used once, so 1018 distinct hashes means 1018
   sends.

`prove` re-ran on the current code into `poc/data/clean-e2e-2026-11-09/stage2-control-proof`: passed, 1018 matched, 1018 compared as
sent, 0 differing. Tests: control 5 passed, adapter 8 passed.

SEND or BLOCKER?
