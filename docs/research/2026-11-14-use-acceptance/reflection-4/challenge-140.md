# Round 141: proof 10's design revised for your four points (contract, "Proof 10's design")

1. **Timing by brackets.** Each day's completion is bracketed by the times just before and after `close_and_complete`. An answer's
   day must have started completing before the answer arrived, and be no older than the last day whose completion ended before the
   request was sent. A request that pins just after a commit is therefore accepted.
2. **Two distinct snapshot states, labelled and asserted:**
   - 2026-09-25 before judging: articles committed, the day not completed. The copy's last day is 2026-09-24, with steps dated
     2026-09-25.
   - 2027-01-31 before close: a due-day closing not completed, no articles. The copy's last day is 2027-01-30, with no switch dated
     2027-01-31.
3. **Readiness:** 200, or 503 with exactly the first-day body, counts as ready. Any other answer fails, and the known-finding
   exception is removed.
4. **MCP** is named a module-level check (tool implementation, not transport; transport stays a limit).
   - The poller must not be vacuous: at least 20 answers, and at least one completion with answers on both sides.
   - The dated read is compared as decoded JSON (a hash of the canonical form), and a first difference is read before it is called a
     leak.
   - At the writer's end, WAL may be kept with "another connection held the store at the end" recorded, since the poller may hold a
     read then.

The harness is a new file; the D573 one stays as its run's record.

End with `CONSENSUS: yes` (build and run proof 10) or `CONSENSUS: no, because …`.
