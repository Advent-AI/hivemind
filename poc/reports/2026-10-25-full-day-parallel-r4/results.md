# D180: complete-day concurrency proof and live matching measurement

The existing implementation plan has now been exercised on the complete July 27 workload: **53 items**, sequential and eight-worker execution, with **all 10 compared logical tables identical**. Every one of the **106 accepted handovers** binds to its exact preceding-state request and recorded answer. A separate live same-input Jev comparison measured **3.34×** at the matching phase. This is not a whole-pipeline 10× result.

## Implementation-plan checklist

| Planned work | Result |
|---|---|
| Immutable requests and concurrent preparation | Full day executed; parallel provider peak was 8 |
| Ordered validation and one writer | All 53 accepted requests reconstruct from their committed prefixes |
| Stale preparation handling | 10 stale preparations recomputed; no synthetic speculative answer accepted |
| Independent matching requests | Existing Jev worker pool used; live phase reached 5 simultaneous provider calls |
| Complete-day storage equivalence | Views, rungs, evidence, sources, links, dependencies, succession, groups, memberships and judgments all match the sequential control |
| Source and database isolation | All 138 protected database files unchanged |
| Existing checks | 156 product, corpus and diagnostic tests passed |
| Negative control | Replacing a nonempty accepted handover with an empty one was detected |

The full-day run uses real SQLite, request builders, checks, matching, writer, judgment scheduler and day completion, with recorded external responses. Timed external responses use a 0.01 scale solely to exercise overlapping execution. Its 7.50-second sequential and 3.13-second parallel wall times are **synthetic** and must not be presented as API performance.

The source fixture first needed completion under current code: the historical archive contains pre-D168 Jev criterion wording. Exact request hashes differ after that recorded correction. Existing exact answers were reused; only missing requests were sent. This completed the current-code day with 82 fresh Jev calls and four fresh judgment calls, while retaining all 53 stored extraction answers. That partially cached completion is not a latency baseline either. Earlier incomplete fixture attempts remain in their dated directories; no stored data was deleted. The final proof uses exact requests, without the abandoned criterion-normalization adapter.

## Live API comparison: identical matching work

Source: `gnews:77407f8ee20f4ae125475c46`, first matching phase. Each sample runs the same five original requests, with the same state, question IDs, schemas, model and snapshot, through `jev_matching.decide`. Every sample has a fresh archive. No product records are written by this measurement.

| Sample | Seconds | Peak provider calls |
|---|---:|---:|
| Serial 1 | 4.121 | 1 |
| Parallel 1 | 1.719 | 5 |
| Parallel 2 | 0.614 | 5 |
| Serial 2 | 3.471 | 1 |
| Serial 3 | 3.959 | 1 |
| Parallel 3 | 1.185 | 5 |

Medians: **3.959 → 1.185 seconds**, ratio **3.340×**. Thirty fresh Jev calls cost an estimated **$0.005448** at the repository's list price. See live summary (local artifact: `../2026-10-25-within-item-parallel/summary.json`) and its per-sample archives.

One of the six resulting evidence decisions varied: `e1 → v3` was a repeat in all three serial samples and parallel sample 2, but new in parallel samples 1 and 3. The **original provider responses**, for the identical request hash, already differ: the repeat probability ranges from 0.46 to 0.53 around the unchanged 0.50 threshold. The other five decisions agree across all six samples. This is not completion-order corruption in our result application. These samples do not establish whether service load influences the provider's answer; no threshold, prompt or identity rule was changed to hide the variation.

## Budget and scope

The initial study's unknown-use request still holds its $0.517 reservation. Fixture completion and the live comparison use only the remainder of the original cap. Combined totals: **140 of 144 allowed attempts**, conservative known charges **$0.088577**, unknown reservation **$0.517**, total held **$0.605577 of $1.50**. No cap was raised, reservation erased, provider switched or working library rewritten. Final isolation/accounting (local artifact: `final-isolation-and-budget.json`).

The delivered result is the working parallel implementation, full-day deterministic storage equivalence and real within-item parallel API throughput. A fresh full-day end-to-end speed comparison remains necessary before claiming a whole-pipeline speedup or promoting the mode. Existing extraction findings do not become a new work order in this slice.
