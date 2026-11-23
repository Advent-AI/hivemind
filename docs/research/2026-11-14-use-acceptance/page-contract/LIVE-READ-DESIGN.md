# The page's date on the live read, and the first day of a live store: design version 3 for the council (D573; rounds 46 to 48), 2026-11-16, $0

## A. The page opens on the served snapshot's day (built)

**Defect** (`SERVING-WHILE-WRITING-RESULT.md`, finding 2): at start the page shows its embedded snapshot, then replaces it with the
served library (`bootstrap.loadLibrary` → `library.setDataset`), whose clamp keeps the embedded day. A shell built on one day and opened
on a later one therefore shows the shell's day, not the latest completed day. `thesis-ui.md`: "The supplied snapshot defines the
displayed date."

**Rule:** the library has no date control of its own (its day is set only when it is created and in `setDataset`, searched); the
person changes dates in the explorer and the drawer, which keep their own state. So: the page's one automatic read
(`bootstrap.loadLibrary`, run once at start) shows the served snapshot's `as_of`; every other replacement keeps today's verified clamp
(`verify-library.mjs`, "library day clamps before replacement"); a failed read keeps the embedded snapshot silently, as
`thesis-ui.md` specifies ("Automatic API loading keeps the current snapshot when unavailable"), a limitation recorded for Alex.

**Owner:** `components/library.js` `setDataset(input, { day } = {})`: with a day, the library shows it, clamped to the new history;
without, today's behaviour. `bootstrap.loadLibrary` passes `{ day: next.as_of }`. `thesis-ui.md` says it.

**Proof ($0):** a test of `setDataset` with and without `{ day }`; the existing clamp check unchanged; the paused-writer test re-run
with the page check asserting the displayed day and the question identities against the served response; the production shell against
a new-system store shows the served `as_of`.

## B. The first day of a live store (not built; an operating rule, recorded)

**Finding 1:** before any day of a store completes, `service.default_as_of` falls back to the latest judgement's day, so the default
views serve the day in progress. **Readers of that default** (searched): `bundle.library`, `bundle.thesis_bundles`, `idea.py`,
`search.py`, `service.py` (views, a view, evidence, history, changes, the day's items, the evaluation route), and MCP's start
(`scripts/hivemind_mcp.py`, the object list). Changing the default would change every one of them; a `None` default breaks several that
compare dates. Census: 0 of 143 stored `views.sqlite` files hold processing steps, judgements and no completed day; the state lasts
from a new store's first write until a day completes (longer for a store a crash leaves there).

**Rejected proposal, not built (council round 48: the check and the read can see different states). It read:** *Enforced on every read (version 3, council round 47: a start-time check admits a store that is empty at start and later reaches the
state).** `service.first_day_unfinished(conn)` is true when a store has a processing step and no completed day. It is checked on each
read, at the one place each entry point opens the ledger for a request: the API's `Connections.__enter__` (every GET route and
`POST /ideas`) raises `service.NotReady`, answered **503** "the store's first day has not completed"; the MCP server wraps each tool
with the same check and raises the same error. An explicit `as_of` does not bypass it: until the first day completes nothing is served.
An empty store (no step) is read as today (no judgement: the library refuses for want of a completed day). A legacy ledger with no day
records (no step) is read as today. A crash-left store in that state is refused for as long as it stays in it (until a day is
completed or the store is replaced), not only "to the end of its first day". MCP's object list, computed at its start, stays as today
(stale for objects that appear later: a recorded limitation, not this slice). Every reader of `default_as_of` keeps its default.

**Tests through the real entry points:** one API process started on an empty temporary store: `/library` refused for want of a
completed day; a processing step and a judgement written (the first day unfinished): `/days` and `/library` 503 with the message;
the day completed: `/library` 200 as of that day. The MCP tools called with the module loaded on the same three states (503-equivalent
error, then a library). `docs/poc/service.md` states the rule.

## Status after round 48 (2026-11-16)

- **A built and proved:** `verify-library.mjs` 11 of 11 in headless Chrome (`library-check.txt`); the paused-writer check re-run
  (`serving-while-writing.txt`): a fresh page during 2026-09-25 shows exactly the five questions served as of 2026-09-24, and on
  2027-01-31 after its closing exactly the seven served as of that day.
- **B not built; recorded as an open defect.** A check on every read still races the writer unless the check and the read share one
  database snapshot (council round 48); holding a read transaction across a request can delay the writer's commits (the 2026-10-28 lock
  halt); MCP builds its object list and index at start; the streamed Idea response sends its headers before opening its connections.
  The state arises only on a new store's first day (or a store left there by a crash); 0 of 143 stored stores are in it; no new-system
  store is served live today (the service serves production's sealed ledger). Design input for the fix, when a live new-system service is
  designed: the reader table above, one snapshot for check and read per request, MCP's start, the streamed response, and a test that
  pauses a request between check and read while the writer commits.
