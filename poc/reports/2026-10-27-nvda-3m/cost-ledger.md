# Cost ledger: the three-month NVDA run (2026-07-01..2026-10-27)

Alex, 2026-10-27: "不要设价格上限，但是清楚的帮我记录成本". Every paid step is a row; token counts come from the archives, prices from
`model.PRICES` (gpt-6-luna $0.10 / $0.01 cached / $0.50 per M; Jev $0.042 per M input), `scripts/cost_report.py`.
The provider's bill is the measurement; these are estimates from tokens.

| step | what | calls | USD (estimate) | source |
|---|---|---|---|---|
| corpus backfill, 2026-07-01..07-23 and 10-23..10-27 | Google News RSS, link resolution, page fetches, NVIDIA blog and newsroom, EDGAR, TrueNorth stories (token, no per-call price) | — | 0.00 | public endpoints; DeepSeek search/fetch not used (probe: plain day queries return nothing, fetch fails on most news sites) |
| DeepSeek search probe (can it resolve Google News headlines?) | 8 searches | 8 | 0.006 | $0.75 per 1,000 successful requests |
| three-month run launched 04:25 (pid 13313), `run-all.sh`, poc-v29, `--only NVDA`, no cap | 3,852 NVDA items 2026-07-01..10-27 (copies excluded; 2026-10-27 empty) | — | filled by `scripts/cost_report.py` at the 25-minute check and at the end | archive `english-v29-nvda-3m-2026-10-27/archive.sqlite` |
| 25-minute check (04:50): through 2026-07-20, 20 days | extract 598 calls (3.67M in, 1.24M cached = 34%, 0.35M out) 0.432; judge 84 calls 0.162; match: collision judge 10 calls 0.003, Jev 727 calls 0.127 | 1,419 | 0.724 | `cost_report.py`; rate ≈ 24 items/min, ≈ $0.0012 per item so far |
| pause/resume proof (04:54–04:56): `pause.sh` stopped the replay during 2026-07-23's judging; `launch.sh` resumed after the last completed day 07-22 | 2026-07-23 re-entered: 33 items, 0 re-extracted (all 30 already handed over), judging finished with 16 calls | 16 | 0.02 | the only cost of a pause is the calls in flight at the stop; both databases `integrity_check` ok before and after |
| stall at 2026-08-07 judging (05:30): v11 refused twice (first answer named 7 theme ids as dependencies; the retry pushed on an id not shown); day finished on the serial path after the fix (05:37) | 25 judge calls for 08-07 re-sent (the closing line of the request changed, so no archived answer matched) | 25 | 0.05 | `finish-0807-1.out`; cost of the stall: the two refused answers ($0.03) plus this re-send |
| hourly check (05:51): through 2026-08-10 | extract 1,185 calls (8.05M in, 2.46M cached = 31%) 0.966; judge 376 calls (3.96M in, 0.85M out) 0.810; collision judge 27 calls 0.011; Jev 1,576 calls 0.317 | 3,164 | 2.105 | `cost_report.py`; judging is now 38% of spend and rising with the evidence lists |
| network failure (06:24): DNS lookup failed during 2026-08-11 judging; run ended, day resumable; relaunched 06:28 | — | — | 0 | `run-all.log` |
| arm beside control for D198 (06:38): v6, v11, v22 under judging-v4 (fresh) and judging-v5 from the same ledger state | 6 judge calls, scratch archive `docs/research/2026-10-27-evidence-in-view/ab-archive.sqlite` | 6 | 0.031 | `ab-results.md`: same rungs; request tokens cut to 16–33% |
| switch to poc-v30 (06:42–06:46): paused after 08-17; 2026-08-18 finished serially under poc-v29 in three attempts (Jev HTTP 451 once, one empty judge answer, then done: 15 calls) | the two failed attempts cost their calls before the failure (archived, reused) | — | ≈0.05 | `finish-2026-08-18-*.out`; relaunched 06:46 under poc-v30 from 08-19 |
