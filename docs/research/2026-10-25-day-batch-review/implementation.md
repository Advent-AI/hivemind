# D172: isolated concurrency POC, first slice

D180 execution update: the [complete-day and live matching results](../../../poc/reports/2026-10-25-full-day-parallel-r4/results.md) now exercise this implementation on all 53 July 27 inputs. Eight-worker recorded-response execution preserves all 10 logical tables; a six-sample live Jev phase comparison measures a 3.34x median ratio. These are distinct proofs, not a fresh full-pipeline speed measurement.

Alex accepted the D171 recommendation and asked to flag ordering or production contradictions immediately. This slice implements the offline coordinator and tests. It does not enable concurrent ingestion by default or launch paid calls.

The controlling rule is unchanged: an item's accepted extraction must be a response to the exact request built from the committed preceding items. Speculative calls may run early; their answers are not handovers until their turn and validation. This deliberately changes the experimental call schedule, not committed knowledge. D159's default no-later-call-on-failure test continues to hold on the default path. In the experimental path, earlier failure cancels pending work and drains already running requests without accepting later handovers or writes.

## Shape and ownership

- `poc/concurrency_study/runner.py`: opt-in callable day runner, bounded extraction lookahead, request validation, immutable worker inputs, manifest and cleanup. Invoked through `replay.run(day_runner=...)`; default remains serial. The POC uses a single coordinator/writer and does not claim support for other processes writing this ledger.
- `model.request_identity`: one exact serialization/hash function shared by normal calls, Jev calls and validation. Same bytes and keys as before.
- `extraction.request_for`: one owner for extraction setting, complete prompt and schema; both extraction and validation use it.
- `round.run(extractor=..., matching_workers=...)`: dependency injection for the POC; the existing checks, two matching phases, writer, completion records, failure handling and daily judging remain the owners.
- `jev_matching.decide(workers=1)`: plan independent questions on the coordinator, send only immutable state/questions to threads, collect answers and mutate candidates/totals in original order. The default remains serial. A refused answer fails the item; successful concurrent responses remain archived for retry.
- The Jev coordinator submits at most the worker count at a time. It checks all completed requests for failure before filling open slots; on failure it submits no more work, cancels what has not started, and drains running requests. Completion order never controls output order.
- Identical Jev requests within a batch share one future, keyed by the complete request hash. Every logical consumer reads that same answer and archive ID. Later uses are accounted like cache hits, preserving the existing logical request order and aggregate hash. No second network answer may claim the first answer's call ID.
- Every new Jev matching record includes the ordered individual call IDs and request hashes in `shown_json.requests`, alongside the existing candidate/evidence lists. Existing readers select those list keys; legacy records remain readable without the new metadata. This makes concurrent matching traceable without inferring call ownership from arrival order.
- Persistent POC manifest: ordered input identities and source digests, sequence numbers, configuration, universe and code/prompt digests per day. Resume must match. A changed source/configuration is refused before speculative submission. Interrupted manifest creation refuses with a clear error rather than guessing.

No writable thesis connection is passed to a worker. No worker writes handovers, memberships, matching records or completion markers. Archive access already has a lock; the network runs outside it. Local IDs remain scoped by input because the writer still handles one item at a time.

## State × event

| State | Event | Transition and write |
|---|---|---|
| Before day | Same manifest on resume | Reuse; default dispatch retains original sequences |
| Before day | Changed/corrupt manifest | Refuse before launching calls; no source or ledger rewrite |
| Prepared | Worker available | Submit bounded extraction with copied item/context and frozen configuration/universe |
| In flight | Later result returns first | Archive only; never an accepted handover |
| In flight | Failure | Retain exception until this request's turn; if stale, it does not invalidate a different current request |
| Item's turn | Same complete request and frozen semantics | Accept its prepared handover through the normal round |
| Item's turn | Changed request/schema/context | Cancel if pending; otherwise drain and keep the old archive record. Re-extract with current context; never remap old IDs |
| Item's turn | Changed configuration/universe/source | Refuse the run; do not combine contracts |
| Matching | Independent questions | Read on coordinator, run API calls concurrently, apply results in planned order |
| Matching | Identical complete request appears twice | One in-flight future and archive result; both consumers receive the same data/ID, with only one fresh-call cost |
| Matching | One question fails | Drain remaining calls; fail the item without a write; resume can reuse completed archived requests |
| Writing | Exception | Existing savepoint rollback and failed-step record; no later accepted item |
| Earlier item fails | Later speculative calls exist | Cancel queued calls, drain running calls, archive only; do not mark later items extracted or written |
| Restart | Saved accepted handover exists | Use normal resume; do not speculatively re-extract it |
| End of day | All items committed | Existing dependency-ordered judging and pull, then day completion |
| End of day | Any failure | Existing day remains incomplete |

Dates in accepted records remain source publication days; ordering remains dispatch sequence. Wall time describes calls only.

## Value × reader and old checks

| Value | Writers/readers | Proof |
|---|---|---|
| Exact request JSON/hash | Model/Jev, validation, archives | Existing hash bytes unchanged; schema included |
| Prepared handover | Worker → coordinator → normal round | Used only for the same item, source, universe, settings and current request |
| Jev result | Worker → coordinator | Completion order cannot change candidate decisions, evidence decisions, group refs, call aggregation or request hash |
| Individual Jev call IDs/hashes | Jev coordinator → matching record → preflight/trace/recall readers | Ordered request metadata is additive; existing list readers retain candidate/evidence keys |
| Per-day manifest | POC coordinator → restart | Exact source/configuration/order match; no silent config or source replacement |
| Final IDs and writes | Existing writer → all readers | Identical fixture ledger to serial control after metadata/call IDs are removed |
| Failure/retry | Existing round and replay | No later authoritative progress; completed prefix reused on restart |

Tests use real temporary databases and real stored source material where available; only model/provider responses are faked. Cases: independent overlap; schema-only invalidation; same-day new thesis; changed group membership; failed earlier call; out-of-order completion; accepted-handover resume; writer failure; no later-day work; Jev response ordering and partial failure/cache reuse; manifest mismatch. Positive controls and scratch mutants must fail for stale-answer acceptance and completion-order mutation. The default sequential tests remain unchanged.

The first read-only design review found one serious missing row: concurrent identical Jev calls can return different sampled answers but share the archive's winning call ID. The complete-request shared-future rule above closes this row before implementation. The network remains outside the archive's SQLite lock.

The first code review found a second failure dimension: submitting all Jev jobs up front allowed queued jobs to start after another request failed. The bounded submission rule above closes it. A ten-job/two-worker control holds one request in flight, fails another and checks that no remaining request starts. Day cost is read from the archive delta, including discarded speculative calls; accepted-item costs alone undercount the new path.

## Limits before a live POC

The existing spend check runs after an item and is not a reservation for concurrent requests. Therefore this first POC entry uses explicit offline transports in tests. Before any live concurrent run, account for in-flight worst-case cost and timed-out unknown usage, and register the comparison's cap. Existing completed-run budgets are not reused. This is a live-launch prerequisite, not a claim that concurrency has been measured.

The coordinator is single-writer, as the current POC is. It does not make the production system safe for uncoordinated external writers. No such guarantee is claimed; that would require a separate ownership/transaction design.

## Result

The offline implementation is complete. [Results and evidence](../../../poc/reports/2026-10-25-concurrency-poc/results.md): 143 tests passed, five scratch mutants caught, and 3,595 historical request identities unchanged. The focused follow-up review found no serious issue after the duplicate-request and queued-work corrections. Live accounting and a fresh performance/quality comparison remain outstanding.
