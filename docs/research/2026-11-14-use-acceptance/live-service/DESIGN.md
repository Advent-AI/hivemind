# A live new-system service: design for the council (D574), 2026-11-16, $0

**What it is for.** The new system's daily loop writes a store day by day (D567); the product's API and MCP server read it while it is
written; the page reads the API. Open defect 10: before any day completes, the readers' default date falls back to the latest judgement's
day, so the first day is served in progress; a per-read check races the writer unless the check and the read share one state.

**Fact the design turns on:** the stores are in SQLite's rollback-journal mode (`pragma journal_mode` = `delete` on the fortnight's
store). There, a reader's transaction holds a shared lock and the writer waits for it at commit (Python's default busy timeout, 5 s),
so pinning a request to one snapshot can delay or fail the writer (the 2026-10-28 lock halt). In WAL mode readers never block the
writer and each read transaction sees one committed state.

## The design

1. **The new loop's store in WAL mode.** `ladder_adapter.LadderAdapter` sets `pragma journal_mode=WAL` on the store it creates (the
   new system's own writer; production's `store.open_db` and its run stores are unchanged). A read-only reader then reads one committed
   state per transaction while the writer commits.
2. **One snapshot per request, readiness checked inside it.** The API's `Connections.__enter__` begins a read transaction on the
   ledger, checks `service.first_day_unfinished` (a processing step and no completed day) in it, and answers **503** "the store's first
   day has not completed" when true; the request's reads use the same transaction; `__exit__` ends it. The MCP server does the same
   around each tool call (`read_snapshot` on its connection). An explicit `as_of` does not bypass it. An empty store (no step) and a
   legacy ledger read as today.
3. **MCP's start.** Its object list is computed per call from the snapshot's last completed day (not once at start); its index build at
   start reads a snapshot too and refuses an unfinished first day like any read.
4. **The streamed Idea response.** The handler opens its connections and checks readiness before it sends the stream's headers; an
   unfinished first day is answered 503 like any other route.
5. **The page when the live library is unavailable.** Today it keeps the embedded snapshot silently, as `thesis-ui.md` specifies.
   Proposed, a presentation choice for Alex (recorded, not built in this slice): the library's existing stats line names a collected
   snapshot ("collected snapshot of <day>") when the live read failed.

## State × event (the writer's state × a reader's request)

| Writer's state at the request's snapshot | `/days` | `/library` (default or explicit `as_of`) | other routes, MCP tools |
|---|---|---|---|
| empty store (no step) | none | refused: no completed day (as today) | as today on an empty ledger |
| first day in progress (steps, no completed day) | 503 | 503 | 503 |
| first day completed, later day in progress | completed days only | the last completed day's view (the partial day is outside it: shown by the paused-writer check) | as of the last completed day |
| after a due-day closing completes | includes that day | closing visible from that day | same |
| crash left the first day unfinished | 503 until a day completes or the store is replaced | 503 | 503 |

The race closed: a request's check and read see one committed state, so a writer's commit between them is invisible to that request.

## Proof ($0)

1. The store's journal mode is WAL after the loop creates it (test); production's stores unchanged.
2. The API through its real entry point, one process, on a store driven through the loop's real writes: empty → refused; a request held
   **between its readiness check and its read** (a hook in the test) while the writer commits the first processing steps and judgements →
   the held request's response is the empty-store answer, not the partial day; first day in progress → 503; first day completed → the
   view as of it. The writer completes while a request is held, with no lock error.
3. MCP: the same three states through its tool functions; its object list after a later day completes includes that day's objects.
4. The streamed Idea route: 503 on an unfinished first day before any stream header.
5. The paused-writer harness (`page-contract/serving_while_writing.py`) re-run: the first-day case now passes; every other check holds.

## Prior decisions and limits

D567 (the loop), D574 (the open defect and this design's scope), the 2026-10-28 lock halt (AGENTS §9: never open a live run's databases;
that rule stays for production's runs, whose stores are not in WAL mode). Not covered: the Idea planner on a new-system ledger (a separate
item); a long-running service's operations (restart, monitoring).
