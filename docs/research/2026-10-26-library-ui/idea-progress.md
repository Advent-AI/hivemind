# D187: live Idea progress timeline

The pending card currently has one Reading chip and one static status sentence. The service returns only final JSON, so the browser cannot know when stages change. Replace this entire pending presentation with a vertical connected list. These are public task stages, never model reasoning text or invented timed steps.

## Contract and state × event

Keep JSON POST /ideas unchanged. A caller accepting application/x-ndjson receives ordered records: progress(stage), result(data), or error(status,message). The actual read_idea boundaries emit search, decompose, retrieve, map and optional summarize. The browser adds cards only when it starts the existing bundle request. No prompt, selection, score, model or database semantics change.

| State/event | Transition, writes and date |
|---|---|
| Submit | Clear prior progress; show initial search; use selected library as_of |
| Service enters next stage | Append one known stage; mark prior nodes complete; current glimmers |
| Cached stage / duplicate notification | Same real boundaries, duplicate ignored; no artificial delay |
| No recorded coverage / no summary setting | Only stages actually visited; result then existing card handling |
| Final result | Prepare cards during the existing bundle fetch, then answered card |
| Refusal / transport error / incomplete stream | Existing failed-card path; no fake completion |
| Cancel, navigate away, replacement request | Abort reader; request number excludes late callbacks; no cross-request progress |
| Client disconnect | Stop writing; next progress boundary raises and prevents subsequent stages |
| Legacy JSON server/caller | Existing final JSON still supported; no simulated internal progress |
| Two simultaneous requests | Per-request callback and connection; stages stay local |
| Reduced motion | Same current node, no shimmer or entry animation |

## Value × reader

read_idea owns stage boundaries; HTTP writes the NDJSON envelope; readIdea parses chunked UTF-8; bootstrap owns request-local history and updates its leading card; progress renderer owns sentence-case labels and visual current/completed states. No model token, private reasoning, source text or credential enters a progress event. Final JSON stays unchanged.

## New path × checks and prior decisions

D184/D186 own answered-card analysis; D185 composite is untouched. D135/D145/D186 model requests remain exact. Test real stored-ledger stage order and unchanged result; HTTP streaming at its public entry; stream framing across chunk and Unicode boundaries, errors/early termination, JSON fallback; UI list append/current state; abort/stale response handling stays bootstrap-owned. Use cached model calls or fake external model/HTTP only, no paid experiment. Verify pending preview and completed card in the browser, no header chip, connected nodes and motion. Source hashes must stay unchanged. Run touched/full suites once and docs/check.py after the reasoning refresh.

## D22 reasoning refresh

In the required order: universe and classification retain scope and input contracts; Config retains all settings; dispatch retains ordering; extraction and thesis-library writes remain unchanged; final verdict, pull mode and human review are untouched; the system overview retains its model and data boundaries. Their page/PRD examples and acceptance criteria still agree. Only the Idea read-service and UI documents needed an optional streaming contract and pending-card presentation update. No frozen business rule or model prompt changed.

## Verification

155 Python tests, 37 UI tests and 12 mutation checks pass. Real HTTP testing holds the fake external model and proves progress arrives before it finishes; the final data is unchanged. Client tests split every UTF-8 byte, preserve the stored result, refuse truncated/error streams and accept JSON fallback. The browser preview uses the real UI with a controlled recorded-response server, then verifies cancellation and a subsequent completed request. The actual API emits all five server stages on a cached request, costs $0 and leaves the six archived model calls unchanged. The three protected database hashes are unchanged. See [results](../../../poc/reports/2026-10-26-idea-progress/results.md).
