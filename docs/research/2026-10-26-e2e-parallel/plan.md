# D181: live end-to-end measurement of the ordered concurrent day

Alex, 2026-10-26: "finish the entire POC of parallelization ... the results are correct compared to the golden that we
ran sequentially and the speed up end-to-end is measured and benchmarked ... 我是要你真的implement 下去跑". D180 left
exactly this open: its full-day proof used recorded answers and its live measurement covered one matching phase.

## Workload and arms

- The complete July 27 day: 53 items, the start-of-day ledger and the items database of D180's fixture
  (`poc/reports/2026-10-25-full-day-parallel-r4`), configuration `poc-v23`, unchanged prompts, checks, matcher, writer
  and judging.
- Serial arm: the product's default replay path. Parallel arm: the D172 runner with 16 extraction workers and 8 Jev
  workers per matching phase. Both share one outbound limit of 32 calls; daily judging keeps its own six workers in
  both arms.
- Order `serial-1, parallel-1, parallel-2, serial-2, serial-3, parallel-3`; each trial gets a fresh ledger copy and a
  fresh archive, so every answer is a fresh live call. A failed trial stops the study.

## One scheduling change before the run

D180's recorded replay showed where the parallel day spends its time: 74 s of its 154 s ingestion chain re-extracted
stale requests at their turn. The runner now re-prepares a waiting request right after the commit that changed it,
not at its turn; the turn still validates the exact request. The recorded full-day replay stays identical to the
serial ledger in all ten tables at 8 and 16 workers (ingestion chain 154 s → 128 s → 95 s at recorded durations).

## What is measured and what counts as correct

- Speed: wall time from the first item to day completion, split into ingestion (items extracted, matched, written)
  and daily judging; medians of three per arm.
- Correctness, per trial: (1) the audit rebuilds every accepted extraction request from its committed prefix and binds
  it to the exact archived answer, and checks judging population, day completion and memberships; (2) the trial's own
  answers are replayed through the other mode with no network (parallel answers through the serial path; serial
  answers through the parallel runner) and the ledgers must be identical in all ten product tables plus handovers and
  match decisions.
- Drift census, not an identity check: per-item agreement of each trial with the recorded sequential golden and with
  every other trial. Serial-to-serial and serial-to-golden agreement are the sampler's floor; parallel trials are
  read against it.

## Budget

A new journal for this study: $4.00 conservative accounting (request-size input bound at the highest reviewed
Standard rates), at most 2,000 attempts, up to three attempts per call on network, rate-limit or server errors, each
failed attempt's reservation held. Published-rate estimate: about $0.08 per trial. The D173–D180 journal and its
held reservation are not reused.

## Result

[Results](../../../poc/reports/2026-10-26-e2e-parallel/results.md): median 501.8 s → 112.5 s, 4.46× end to end, 5.91×
for item work; all six trials pass the audit and the cross-replay; drift inside the serial spread. One more live run
through the product entry point (`scripts/replay.py --workers 16`) took 135.5 s with the same checks clean. The
read-only code review ([findings](review.txt)) led to five fixes and two recorded non-changes (D181).
