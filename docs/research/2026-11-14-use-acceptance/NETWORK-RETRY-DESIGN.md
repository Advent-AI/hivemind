# Clean Step 1 stops on one dropped connection: diagnosis and the fix, design for the council (lean step 2), 2026-11-14

**Class ($0, every stored Step 1 trace, 52):** 7 steps failed on a network error ("IncompleteRead", "Connection reset by peer"), and each
stopped its run: clean-e2e 2026-11-09 d1, d2 and d3; unseeded 2026-11-10 d3; the full run's c2 (D453); this week's c1 twice. Long runs (about
200+ items) hit one in most attempts; earlier rounds worked around it with "segment-2" restarts.

**Mechanism (traced):** `clean-arch/step1/live.py` `LiveTransport.__call__` sends with `max_attempts=1` ("the single network attempt",
kept so that every attempt is reserved and settled on the ledger, D448); `runner.run` treats any failure other than a format failure as the
end of the run. Production's transport (`model.openai_transport`) tries a network failure up to three times. So the clean path, alone, ends
a two-hour serial run on one dropped connection.

**Fix (one owner, the transport):** `LiveTransport` retries a network loss — a `model.TransportError` with no HTTP status, or 429 or 5xx — up
to three attempts in all, waiting 30 s and then 60 s; every attempt is checked against the time and call limits, reserved on the ledger before
it is sent and settled after (its reservation when it fails), so the ledger contract of D448 holds per attempt. Not retried: any other HTTP
status, a limit refusal, anything raised after an answer arrived (format failures stay the runner's one resend). The retries of a step are
recorded: the transport keeps the step's network errors, and the runner writes them into that step's `retry_reason`. A resend after no answer
is the same request with nothing seen, so it adds no sampling choice.

**Tests (fake sender, fake ledger, no network):** two network losses then an answer → the answer, three sends of `max_attempts=1`, three
reservations and three settlements (the first two at their reservations), waits of 30 and 60; an HTTP 400 → one send, raised; three losses →
raised after three sends; a call limit of one → the retry is refused with the limit error, not swallowed; the runner records the retries in
`retry_reason`. Mutant: three attempts set to one fails the first test. The existing ledger tests stay green.

**After:** the clean week draw relaunched in a new root (`week-r2`) from empty on the same frozen manifest, with a new ledger whose ceiling
keeps the step's total under the agreed $8 (spent $2.17: ceiling $5.80); production's completed week draw is kept as it is.

## Addendum, 2026-11-15 (D552): two rows the table lacked

| Event | Before D552 | Since D552 |
|---|---|---|
| A connection goes silent during a call (no error, no data) | the call waited for the run's whole remaining time; no retry started; the run sat until its own limit | the wait ends after at most 600 seconds (`CALL_WAIT_SECONDS`), or the run's remaining time when that is less; the timeout is a network loss, sent again under the rule above, each attempt reserved and settled |
| The machine sleeps with a call in flight | as the row above after waking: the run of 2026-11-15 stopped this way at article 121 of 272 | after waking, the call times out within ten awake minutes and is sent again; a lost attempt is charged its reservation |

Limits: the bound is on each wait for data, not on the whole call; an answer that keeps arriving is never cut. A machine that
stays asleep past the run's time limit still ends the run. Counted when the bound was set: 4,718 answered calls in 53 stored
traces, the longest 220 seconds.

