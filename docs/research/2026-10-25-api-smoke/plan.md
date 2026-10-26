# Isolated API smoke test, October 25

Alex asked for an isolated small test before any larger run, and for actual API documentation to be checked. This is a test of provider requests, accounting and completion order. It does not adopt concurrency, change extraction or grouping, change a gold, or measure end-to-end acceptance. D159, D171 and D172 still govern committed order. Existing databases are read-only inputs; all new files are under a fresh report directory.

## Verified API contract

Official pages read on October 25:

- [OpenAI Batch guide](https://developers.openai.com/api/docs/guides/batch): asynchronous JSONL upload, Files API then Batches API, unique `custom_id`, results need not be in input order, `24h` completion window. A failed/expired job can contain billed completed requests. This is not the transport implemented in D172.
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna): pinned model supports Chat Completions, structured outputs and Batch. Max input 922,000, max output 128,000. Batch support does not establish account access or a seconds-level turnaround.
- [OpenAI pricing](https://developers.openai.com/api/docs/pricing): standard short input/output $0.10/$0.50 per million; long input/output $0.20/$0.75; highest listed long cache-write input $0.50. Regional premium may apply. The accounting reservation below deliberately exceeds ordinary charges.
- [TypeSafe API](https://docs.typesafe.ai/api/system-one) and [models](https://docs.typesafe.ai/models): POST `/v1/systemone`, named questions and named answers, billable input usage, pinned `jev-1.14.0`, $0.042/million input, free output, default 64k/request and 32k/question. There is no OpenAI Batch transport for these calls. This test does not pack additional questions or enable long context.

## Fixed scope and measurement

Read exactly calls 574, 575 (extraction) and 577, 578 (Jev) from the existing v23 Jev archive through SQLite read-only mode. Resend their unchanged full requests. Each of three samples has fresh serial control A, fresh serial control B, and a fresh two-worker arm. Each arm has its own empty archive. Total maximum: 36 provider requests; no retries; global $1.50 ceiling using conservative reservations. Estimated ordinary token charges from the saved usage are below $0.10; that estimate is not the ceiling or the eventual bill.

Serial controls establish provider variation on these requests. Record every request identity, raw response, usage, schema validation, latency, completion order, answer equality and Jev choice differences. A smoke pass requires every response to validate, match its original request, and have billable usage; persistent unknown usage, API rejection or validation failure stops the study. Differences between fresh answers are reported, not automatically classified as pipeline defects. No gold score or 10x claim is made. A larger end-to-end comparison is a separate next step.

## State × event

| State | Event | Transition and durable write |
|---|---|---|
| Before first call | New absolute output directory | Hash all existing `poc/data` database files and sidecars; write immutable test manifest; create independent archives and accounting database |
| Before first call | Output already exists or input hash changed | Refuse; never reuse or overwrite a prior experiment |
| Ready | A permitted request arrives | In one lock/SQLite transaction, reserve worst-case cost and consume one of 36 dispatches before network I/O |
| Ready | Cap/count exhausted or earlier failure | Refuse before network I/O |
| Reserved | Local HTTP preparation completes | Under the same lock as cancellation, check admission is still open and durably mark dispatch committed. Only then may socket I/O start. Cancellation before that point marks `not_sent`, charges zero and makes no HTTP call. Cancellation after that point drains it as in-flight work; no claim that a physical socket write is atomic with cancellation |
| Reserved | Valid response and usage | Persist raw response and measured time in accounting row; replace reservation with conservative usage-based charge |
| Reserved | Timeout, network/API error, malformed/missing usage | Preserve reservation, mark usage unknown and halt new dispatch; drain already-running calls; no retry |
| Reserved | Process crash | Reservation stays; reopening a database with unresolved work refuses all new calls |
| Any active state | Cancellation or downstream validation failure | Close admission durably before cancelling unsent futures and draining sent calls. Unsent work makes no HTTP request; sent work retains its reservation until valid usage is persisted. Record cancelled/failed study outcome |
| Completed | Schema refusal downstream | Keep response/cost; stop study; no broader test |
| Study end or failure | Other call in flight | Drain it, persist whatever is known, then compare protected database hashes |
| Study end | A protected hash differs | Report failure and path; do not claim the files were unchanged |

The sequence of call/attempt rows is owned by SQLite, not wall time. Elapsed time uses a monotonic clock. Source dates and request bodies do not change. This smoke test never writes a product ledger, so there is no day-completion or publication-date transition.

## Value × reader

| Value | Writer and readers | Rule |
|---|---|---|
| Request body/hash | Existing archive → smoke adapter → provider/accounting/new archive | Complete body remains identical; model, prompt, schema and output cap do not change |
| Reservation | Transport → admission and final report | OpenAI $0.70/call exceeds all documented context/output limits at highest listed Standard rates including 10% regional premium; no Fast/custom tier accepted. Jev reserves 65,536 input tokens times `(question count + 1)` at its price, conservatively allowing repeated state billing. Unknown usage never releases funds |
| Usage charge | Provider → accounting | Nonnegative integer usage required; conservative published rate, not a claim about the bill; may not exceed reservation |
| Response | Provider → accounting → existing `model.call`/`jev.ask` validation | Persist even if downstream schema validation refuses it; secrets never persisted |
| Protected hashes | Read-only census → final comparison | Every existing database and sidecar in `poc/data`, not only the selected archive |
| Arm results | Existing validators → report | Separate archives prevent cached controls; completion order cannot change logical response order |

## New path × old checks

| Check | Proof |
|---|---|
| Exact request serialization | Rebuild each stored request through current builders and require matching hash before paid calls |
| Extraction schema | Existing `model.call` and current stored schema |
| Jev named-answer checks | Existing `jev.ask` / `jev.validate` |
| Admission is before send | Fake external HTTP transport and real temporary SQLite; cap refusal asserts no call |
| Concurrent admission | Two requests reserve under one lock; third cannot exceed cap |
| Unknown billing/crash | Timeout and reopen tests retain reservation and refuse later calls |
| Cancellation | Close admission while one request is held in flight; a subsequent request must not reach the fake service; drain the first and retain its usage |
| Ordinary output accounting | Usage recorded before downstream JSON/schema validation |
| Database isolation | Read-only inputs, new directory, before/after hashes |

Tests use no credentials. The live HTTP function loads configured credentials only after preflight, uses fixed documented endpoints, and makes exactly one attempt. The POC guard does not replace production accounting or change the default transport. No OpenAI Batch endpoint adapter is added in this slice.

The code review identified two timing windows before live calls: cancellation after reservation but before dispatch, and a later worker's schema failure waiting behind an earlier result. Local request preparation now precedes an atomic dispatch/admission check. Each worker closes admission on failure itself, independent of result collection order. Both have direct tests with a held earlier request; all unsent requests must remain unsent.
