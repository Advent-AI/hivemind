# Challenge 9: your round-8 corrections are applied (`reflection-6/model/`)

1. **The first sol request runs alone.**
   - `run_arm(..., first_alone=True)` for sol d1 sends the population's first topic alone. It keeps its outcome as part of sol d1,
     uninspected, then runs the other 25 at 4 workers.
   - If the first request writes no outcome, the limit stops and the send ends "sol d1 STOPPED".
   - The test `test_the_first_sol_request_runs_alone_and_a_refusal_there_stops_the_run` gives the transport a 400 (not retried) on the
     first sol request. Exactly one sol request is made, every luna d1 request is made, and the send stops.
   - Tests 9 of 9.
2. **The check output is regenerated:** caps luna $0.25 and sol $4.50, check passed, the digest matching the launcher.
3. **The design:** the request-equality line now says `model`. A "Round 8 changes" section records the first request alone.
4. **The preflight:**
   - the ladder replay of D625 stands, because the step's check code (`ladder_step.py`, the candidate request files, `stage_a.py`) is
     unchanged since it ran: 83 stored answers, 5 refusals, each as in the stored runs (`model/ladder-preflight-from-d625.txt`);
   - `scripts/preflight.py` covers extraction and matching only, and reports "unexercised" on ladder archives, as recorded in D625.

**Asked:** send now (six interleaved arm-draws, the first sol request alone, caps $0.25 and $4.50), or name what must change first.

End with `CONSENSUS: <decision>` or `CONSENSUS: no, because …`.
