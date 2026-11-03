# D182: fifteen days through the parallel day, against the serial path, with no network

**Answer.** Over August 1–15 (221 items, 15 consecutive days, $0), the parallel day built a ledger identical to the
serial path's in every product table plus handovers and match decisions, and its turns accepted exactly the serial
run's 221 extraction requests. A deliberately broken runner was caught. At recorded call durations the fifteen days
take an estimated **2.79×** less time end to end (3.66× for item work); a day gains between 1.5× (4 items) and 4.5× (19
items). This is an estimate from recorded durations, not a live measurement; the live measurement is D181's 4.46× on
July 27.

## Why an oracle, not the recorded answers

The recorded run (`poc/data/english-v23-jev-2026-10-25`, poc-v23) predates D168. Its Jev requests lack one relation
option and carry the older replace wording, and D168 also changed the matching and writing rules, so the current
ledger, and with it every later request, departs from the recording after the first item. The recorded answers can
therefore not answer the current code's requests for fifteen days. Each call is answered instead by one deterministic
oracle, a function of the request bytes only, so the same request gets the same answer in every mode:

- extraction: the recorded answer for the same item (221 of 221 found), each evidence line tagged with the request's
  digest, so a ledger built from an answer to any other request differs;
- Jev: each question's choice drawn from the request digest and question id, mostly "different" or "false";
- judging: rung 1, nothing cited, changed.

The fifteen days wrote 1,458 rows (39 new theses, 231 evidence links, 2 successions, 8 groups, 107 judgements), so later
items do depend on earlier ones: 121 early requests were changed by an earlier commit and prepared again.

## Correctness

| Check | Result |
|---|---|
| Parallel (16 extraction workers, 8 Jev) ledger equals the serial ledger | 12 of 12 tables identical, 3,418 rows; recompared after the D183 review with all 20 product tables: identical, 5,805 rows |
| Requests the parallel turns accepted equal the serial run's extraction requests | 221 of 221 |
| Mutant without re-preparation and without the turn check | caught: 11 of 12 tables differ (16 of 20) |
| Inputs (start ledger, recorded archive, items) unchanged | yes (digests) |

The same checks also passed with answers served instantly (no delay), a different interleaving of the same work.

## Speed, estimated at recorded durations

Calls wait 0.25 × their recorded duration (the item's recorded extraction time; the recorded median Jev and judging
time), at most 32 at a time. Times below are scaled back ×4 to recorded durations; local work is not scaled, which
slightly favours the serial path.

| Day | Items | Serial s | Parallel s | Speed-up |
|---|---:|---:|---:|---:|
| 08-01 | 8 | 140 | 64 | 2.18× |
| 08-02 | 3 | 32 | 16 | 2.02× |
| 08-03 | 8 | 70 | 27 | 2.62× |
| 08-04 | 21 | 228 | 118 | 1.93× |
| 08-05 | 12 | 172 | 69 | 2.50× |
| 08-06 | 14 | 168 | 69 | 2.43× |
| 08-07 | 8 | 95 | 31 | 3.07× |
| 08-08 | 4 | 66 | 44 | 1.51× |
| 08-09 | 4 | 51 | 27 | 1.91× |
| 08-10 | 22 | 258 | 62 | 4.14× |
| 08-11 | 44 | 473 | 125 | 3.78× |
| 08-12 | 24 | 239 | 67 | 3.56× |
| 08-13 | 19 | 241 | 54 | 4.48× |
| 08-14 | 18 | 169 | 67 | 2.52× |
| 08-15 | 12 | 112 | 61 | 1.83× |
| **Total** | **221** | **2,512** | **900** | **2.79×** |

Item work: 2,218 s → 605 s (3.66×). Daily judging: 295 s in both (the same code). A small day gains little because its
own chain of dependent items and its judging round dominate; the busy days gain 3.6–4.5×, in line with D181's live 4.46×
on the 53-item July 27.

Cost: the parallel day sent 342 extraction requests for 221 items (+55%). Its oracle's matching answers are not the
model's, so this share is indicative; live on July 27 it was +15% to +45% (D181).

Files: `summary.json`, per-mode `result.json`; script `poc/concurrency_study/multi_day.py`. Ledgers and archives stay on
disk (`*.sqlite` is ignored here).
