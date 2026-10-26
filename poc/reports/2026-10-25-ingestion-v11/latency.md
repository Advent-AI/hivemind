# Why this three-item run still takes 43 seconds

The completed concurrent trial did not demonstrate useful scheduling speedup for its accepted extraction work. Both later-item preparations became stale and were re-extracted in sequence. Each matching phase had only one Jev request. Most of the observed 60.65 → 43.03 second difference comes from a smaller judgment workload, not demonstrated parallelization.

This is a read-only analysis of saved calls, with no new API requests or runtime changes. profile_calls.py (local artifact: `profile_calls.py`) produces latency-profile.json (local artifact: `latency-profile.json`). A request hash can recur across trials, so each archive row is joined only to journal attempt IDs belonging to that trial; usage is cross-checked. Mixing trials would produce false durations.

## Account for the elapsed time

| Component | Sequential control | Concurrent trial |
|---|---:|---:|
| Three accepted extraction requests, provider time summed | 31.82 s | 28.36 s |
| Matching requests, provider time summed | 2.94 s | 2.57 s |
| Daily judgment phase, reconstructed wall time | 25.76 s | 11.95 s |
| Remaining local/scheduling time, by subtraction | 0.13 s | 0.16 s |
| Measured end-to-end | **60.65 s** | **43.03 s** |

Provider request time includes network/service waiting and generation; these records do not separate those components. Judgment wall time is reconstructed from saved request durations, their actual dispatch order and the shared two-request limit. Both ledgers have zero dependency edges, so these judgments are independent. The reconstructed total differs from measured wall time by less than 0.2 seconds in each trial.

The control judged four theses; the concurrent trial judged two. That reduces the judgment phase by about 13.81 seconds, or 78% of the 17.61-second total difference. Accepted extraction calls also returned faster in the concurrent sample. These are workload and sampler differences, not a controlled measurement of scheduler benefit. The supposedly sequential control already judges independent theses concurrently.

## Where parallel preparation failed to help

The coordinator first prepared SK and NAVER together. SK then created a new question/group. NAVER's full request consequently changed, so the earlier NAVER answer could not be accepted. The coordinator re-extracted NAVER with the correct preceding state.

The same happened to the follow-up: it had been prepared before the NAVER question existed. Once NAVER was written, the follow-up required a different request and another extraction.

Thus there were five physical extraction calls for three accepted answers. Both later-item lookaheads missed; the first item is not an acceleration opportunity because it has no earlier work to overlap. The two discarded requests consumed **19.57 provider-seconds** in total. That time overlapped other calls and must **not** be added to the 43.03-second wall time.

This follows `DayRunner.accepted_extraction`: a changed complete request cancels/discards the preparation and invokes normal extraction. Keeping that validation is necessary to preserve correct ordering and context; removing it would recreate the stale-reference loss measured in D171.

All three concurrent matching phases had one physical Jev request each. The configured two-worker matching pool therefore had no independent jobs to overlap in this trial. Even making its 2.57 seconds instantaneous would improve 43.03 seconds by only about 6% on this workload.

## Same-work counterfactual and limits

Using the concurrent trial's own accepted responses and saved durations, a serial extraction/matching schedule followed by the already-parallel judgment phase takes an estimated **42.88 provider-seconds**. The actual concurrent trial took 43.03 seconds. This is a schedule reconstruction, not another live test or a claim about all workloads. It explains why the observed 1.409x ratio does not establish useful concurrency speedup here.

The sample is useful for proving stale-input handling. It is a chain of related announcements, not evidence of day-level throughput acceleration. The current approach cannot obtain 10x on this sample merely by adding workers. A useful next design investigation would target the expensive whole-call recomputation or identify truly independent work, while retaining ordered matching/writing and validating any changed extraction contract separately. No extraction, matching, model or provider change is made by this report.
