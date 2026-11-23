# A live new-system store: the operating contract, version 9, agreed for its $0 proof build (D593; nothing built)

**Status (D593):** agreed by the council in round 119 for a $0 proof build on test stores, after nine versions (rounds 111 to
119). That agreement covers test stores only, not live operation; P1 stays a proposed decision. D575 paused the earlier design (`DESIGN.md`) as recorded input; it was not accepted. Round 110 resumed the work as this
$0 contract. Version 2 answered round 111's six findings; version 3 answered round 112's four; version 4 answered round 113's five; version 5 answered round 114's four; version 6 answered round 115's four; version 7 answered round 116's three; version 8 answered round 117's two; version 9 answers round 118's two. It returns to the council before any build or live run. The new system has
not passed its quality gates, and adopting it is Alex's choice. This contract only states what a live store would have to guarantee.

**Falsifier (round 110):** a required operating case that cannot be served consistently under this contract without blocking the
writer's commits or exposing partial work. The proof plan names one test per case, and one failing test sends the contract back.

## What touches a live store (searched in the code)

- **The writer:** the new system's daily loop through `clean-arch/step4-2026-11-10/stage_b/ladder_adapter.py`.
  - It opens the store with `store.open_db`, today in SQLite's default rollback-journal mode.
  - It commits several times within a day; `close_and_complete` closes due questions, records the day in `days_completed` and
    commits.
  - **A stopped run is never resumed** (the module's docstring; `run_stage_b.py` records a crash as the folder's outcome).

| Toucher | How | When |
|---|---|---|
| API (`scripts/hivemind_api.py`) | `Connections`: one read-only connection per request; `search.ensure_index(ledger, index)` at start, which embeds view text through an outside service (row 4a) | every request; once at start |
| MCP server (`scripts/hivemind_mcp.py`) | one read-only connection at start (`LEDGER`), shared by every call, including overlapping calls under streamable HTTP; `ensure_index` and the object list computed at start | the whole process |
| The page | only through the API | — |
| The page's embedded snapshot (`scripts/mock_build.py` → `bundle.library`) | `service.open_ledger` | one build |
| Idea and evaluation scripts (`idea_probe`, `idea_gold`, `idea_stability`, `agent_day0`, `search_eval`) | `open_read_only` / `open_ledger` | one run |
| Research and census scripts (`docs/research/**`) | `open_read_only` | one run |
| Preflight (`scripts/preflight.py`) | **`shutil.copy` of `views.sqlite`** to a scratch file (row 7: snapshot or finished store only, then the backup API) | before a paid run |
| A run's `snapshot.sh` (a per-run file, not a repository script) | SQLite's backup API | on demand |

## The contract

1. **Journal mode, side files, opening.**
   - The live store is in WAL mode, set by the writer when it creates the store. Production's stores stay as they are.
   - The `-wal` and `-shm` files sit beside the store on a local disk. **No reader reaches a live store through a container bind mount
     or a network share.**
   - **Opening precondition:** every reader runs as the writer's user, and the store's directory is writable by it. SQLite needs the
     `-wal` and `-shm` files readable, or permission to create them, to open a WAL store with `mode=ro`.
   - Readers open with `mode=ro`, never `immutable=1`.
   - A reader that cannot open the store, or cannot begin a read transaction, fails loudly with the store's path. It never serves an
     empty or stale answer in its place. In code (slice 5, D603), `service.open_pinned` raises `StoreUnreadable` for a SQLite failure
     while opening, at `BEGIN` or at the pinning read; a later SQLite error is a separate path, not covered by this rule's tests.
   - Readers set an explicit busy timeout (`store.READ_BUSY_TIMEOUT_SECONDS`, 5 s). SQLite's busy handler retries `SQLITE_BUSY` within
     it; there is no application-level retry (slice 5, D603). SQLite documents rare WAL cases where a read returns busy, for example
     while the WAL index is being rebuilt. The test holds the store with a connection in exclusive locking mode as a stand-in for
     them; those cases themselves are not exercised.
   - The guarantee is that readers do not block the writer's commits, not that the writer never waits.
2. **One committed state per request, one connection per concurrent request** (detailed in council rounds 125 and 126).
   - **Pinned, not only begun:** each API request and each MCP tool call opens its connections and runs `BEGIN`, then a first read,
     which in WAL mode fixes the committed state the later reads see. The bound resolution is that first read.
     - The transaction always ends (`finally`).
     - A failure while opening (for example the items or index file) closes whatever was already opened before the error leaves
       `__enter__`, since `__exit__` is not called then.
   - **MCP opens its ledger, items and index connections per tool call,** as the API does per request, in place of today's
     process-wide `LEDGER`, `ITEMS` and `INDEX`.
     - The index is written during a search (the query-embedding cache, `query_vectors`), so overlapping searches must not share a
       connection.
   - **MCP's object list stays in its server instructions, labelled with its day.**
     - It is computed once at start-up through `idea.object_list`, which resolves its bound; the direct `service.default_as_of` call
       in `scripts/hivemind_mcp.py` goes.
     - The instructions name the day: "objects as of <day>, when this server started; every tool reads the current last completed
       day".
     - On a first-day store the instructions say no day has completed yet, and every tool refuses until one has.
     - No new tool is added, so the public tool list is unchanged.
3. **Every date bound, resolved in one function.**
   - Today 13 places resolve a bound as `x or default_as_of(conn)`: `service.py` ×9 (`summaries`, `views`, `view`, `evidence`,
     `history`'s `to_day`, `record`, `changes`' `to_day`, `evaluate`, …), `bundle.py` ×2, `idea.py` ×1 and `search.py` ×1. An
     explicit date bypasses any check placed in `default_as_of`.
   - **The owner:** one function, `service.resolve_bound(conn, bound)`, receives every upper bound, explicit or omitted, in its
     caller's read transaction.
     - An omitted bound gives the last completed day.
     - An explicit bound later than the last completed day is refused, naming that day.
     - An explicit bound on or before it passes.
   - Every one of the 13 sites calls it. A lower bound (`from_day`, `since_day`) is checked only against its resolved upper bound,
     through `resolve_range` (see the section on row 3's product-facing contract).
   - **A structural check** fails the suite when any module calls `default_as_of` outside `resolve_bound`, or resolves a bound by
     `or`. A behaviour test per caller gives each an explicit future bound and an omitted one.
4. **The first day** (open defect 10).
   - Before any day completes, every request and tool call is refused, including the streamed Idea route before any header.
   - An empty store (no step) and a legacy ledger read as today.
4a. **Search: visibility before ranking and limits; an index of text-keyed vectors refreshed by the service at start** (revised in
    council rounds 127 and 128).
   - **Lexical:**
     - `search.search` ranks the visible candidates' texts (from `service.summaries` at the request's bound) in an in-memory
       full-text table with the same trigram tokenizer;
     - its statistics are those of the visible library only, so a search at the last completed day equals the same search on that
       day's backup;
     - `store.search_views`, which ranks the whole `views_fts`, stays unchanged for its one other caller, production's matching
       (`views/matching.py`), whose behaviour this slice does not touch.
   - **The index holds vectors keyed by (view, the text's sha256, the embedding model).**
     - A vector is used only when all of these hold (`fresh_vectors`, today's check): the sha covers the **complete embedding
       input** (`view_text`: object, kind, what it looks at, the question and every rung's condition), the model matches, the vector
       is usable, and its length matches the others'.
     - Under those conditions a vector is correct whatever store it was built from.
     - Search uses a vector only for a view visible at the request's bound. **The check, the length test included, runs over the
       request's visible candidates only** (round 129). Today `fresh_vectors` walks every view and takes the length from the first
       usable vector, so an invisible view met first could get a visible view's vector rejected. `fresh_vectors` is given the
       visible candidates.
     - **The store identity of rounds 115 to 117 is therefore not needed and is dropped.**
       - A replaced or restored store can at worst find a view without a matching vector. That view counts as unindexed and search
         runs lexically, saying so, as today.
       - It can never be given a wrong vector. The proof keeps the replaced-store and restored-store cases to show this.
   - **Building:**
     - `build_index` embeds only the views visible at the last completed day (resolved by `resolve_bound`), so a view of an
       unfinished day is never embedded and never sent to the embedding service;
     - each batch commits as today. A failure leaves the vectors already stored, all still correct by their keys, and the next
       build embeds the rest;
     - no published day is needed, because correctness is per vector;
     - `build_index` keeps its signature (`scripts/search_eval.py` and the tests call it as today).
   - **What a search sees of the index:**
     - the ledger transaction does not cover the index, a separate file;
     - search reads every stored view vector in **one statement** (`fresh_vectors`), so the set of vectors a search uses comes from
       one committed index state;
     - a build committing during the request can change only later reads, and search makes none of view vectors;
     - the query cache is keyed by the query's sha and model: a cache hit reuses the stored vector for that exact query and model;
       a miss makes an embedding call and stores its answer. No claim is made that a fresh call would return the identical vector.
   - **Who refreshes, and when:**
     - the service (API and MCP) builds the index at start, as today, to the last completed day; on a first-day store it does not
       build;
     - after a later day completes, a newly visible view is served one of two ways until the service is restarted:
       - **a matching vector is already in the index** (the same view, text and model, from an earlier build or another store
         sharing the index): it is used, being correct by its key;
       - **no matching vector:** search runs lexically and lists the view in `missing_vectors`, as it does today.
     - **A service started on a first-day store** builds no index, and does not build one when that day completes. When that day
       completes, its search is semantic only if every visible candidate already has a matching vector in the shared index;
       otherwise it is lexical, listing the views without one, until the service is restarted. Search's rule is unchanged: one missing
       vector makes the search lexical. This holds for the API and MCP alike.
     - The writer never touches the index.
     - An automatic refresh while serving is not built; it is a stated limit.

5. **Checkpoints and disk: what is guaranteed, and the disk-exhaustion behaviour.**
   - The writer sets `journal_size_limit` (proposed 64 MB) and keeps SQLite's automatic passive checkpoint.
   - After each completed day it asks for a truncating checkpoint with a short busy timeout.
   - **Guaranteed:**
     - readers do not block the writer's commits;
     - after a completed day whose truncating checkpoint succeeds, the `-wal` is within the limit;
     - if the truncating checkpoint fails on 3 consecutive completed days, the writer stops before the next day with a recorded
       reason.
   - **Not guaranteed:** a byte bound on the `-wal` within an unfinished day, or across the failed days. Its growth there is the
     day's own writes, which the contract does not bound.
   - **Disk:**
     - before each day the writer checks the free space on the store's disk against a minimum stated in the run's limits file
       (proposed: 20 times the store's size), and stops before the day with a recorded reason if it is below;
     - a write that still meets a full filesystem mid-day (extending the store, its `-wal` or a side file) fails, and the writer
       exits non-zero as in a crash (row 6);
     - its stop reason may then be lost too, if the run's log is on the full disk;
     - **the guarantee in that case is the readers' boundedness** (they keep the last completed day), not the record.
       The process's exit status, seen by its supervisor, is the signal.
6. **A crash.**
   - WAL drops the unfinished transaction. The day's **already committed writes stay** in the store.
   - Readers stay bounded to the last completed day. Every row written during the unfinished day is dated by that day's processing
     steps, after the last completed day, so it is outside every allowed bound.
   - **The writer does not resume** (today's loop). The store is served as of its last completed day until it is replaced.
   - Resuming a stopped live store is a separate design, not covered here.
7. **Who is writing: a signal outside the store, and copies.**
   - **The lock folder: one owner, fixed, fail closed.**
     - One function (`live_lock.lock_folder()`) gives the folder to both the writer and preflight: `~/.hivemind-locks/`,
       created on first use with owner-only permissions (0700).
     - If it cannot be created, opened or written, both refuse and name it. Neither falls back to running without a lock.
     - **Lock files are never deleted or replaced** by any part of the system; only a person removes them, by hand, when no process
       runs.
     - After taking a lock, and again at each later check point (the writer before each day; preflight after its copy), the holder
       checks that the lock file's path still names the inode it locked. If not (someone replaced the file by hand), it stops or
       discards and refuses.
     - A hand deletion while a lock is held is detected at the next check point, not prevented: the rule against deleting lock
       files is what prevents it.
   - **The lock, named by the store file, not its path:** `<device>-<inode>.writer.lock` in that folder. Both numbers are read with
     `stat`, which reads no content of the store.
   - **One name per store:**
     - SQLite finds a WAL store's `-wal` and `-shm` by the path it opens, so a store must be opened by its own path;
     - a symlink is resolved to that path (`realpath`) before anything else;
     - a store file with more than one hard link (`st_nlink` > 1) is refused, naming the reason. A hard link elsewhere would open the
       main file without its WAL and read a stale state.
   - **Operating precondition: a store's path is never replaced in place while it may be in use.** Replacing a store means a new
     path. This is the contract's own precondition, supported by AGENTS §9's working rule that "new stored data gets a new, dated
     name" (round 119), not that rule's wording.
   - **The checks detect a single replacement:**
     - the holder reads the store's device and inode, takes their lock, opens the store, and reads its path's device and inode
       again;
     - preflight checks once more after its copy;
     - any difference discards what was opened or copied, releases and refuses.
   - **What they cannot detect, stated:** a path swapped away and back (A, then B at the moment of the open, then A again) passes
     both checks. The contract does not claim to bind the opened file to the locked one in that case; the rule above excludes it.
   - **The writer locks before it writes:**
     - it creates its store file empty and exclusively (create-new, failing if the path exists);
     - it takes that file's lock without waiting;
     - it opens it as a database and verifies its identity as above, and only then writes;
     - if the lock is held (by preflight), it refuses to start, with that reason.
     - It holds the lock (`flock`) for its whole life; the operating system releases it on any exit, crash included.
   - **Preflight, before it touches a store, always takes that store's lock without waiting,** creating the lock file if it is
     absent. There is no "no lock file" branch:
     - **if the lock is held, a writer is running:** preflight refuses, naming the run's snapshot script (AGENTS §9's sanctioned way);
     - otherwise it keeps the lock through its verified copy (the backup API, from a `mode=ro` source) and releases it after;
     - historical stores and production's are copied the same way; taking a fresh lock on them is harmless.
     - AGENTS §9 remains the only protection for production's own writer, which takes no such lock; changing it is out of scope.
   - **Snapshots:** the snapshot script is the one toucher that copies a store while its writer runs, with the backup API.
     Preflight accepts its snapshots like any store with no writer.
   - **A copy leaves WAL mode** (found in slice 3's build):
     - a backup of a WAL store keeps WAL mode;
     - a read-only reader of that copy then fails with "unable to open database file", since it cannot create the shared-memory
       file;
     - so the snapshot script, and preflight's own copy, set `journal_mode=delete` on the copy before anyone reads it.
   - **Orderly stop:**
     - at its last day the writer tries to leave the store in rollback-journal mode (`journal_mode=delete`, with a short busy
       timeout);
     - if service readers hold it, the store stays in WAL mode and the writer records "stopped in order, WAL kept" in its run's
       outcome;
     - either way it then releases its lock.
     - Journal mode is never used as the sign of a live store; the lock is.
8. **AGENTS §9 ("Never open a live run's databases") stays in force.**
   - **Proposed decision P1, to be resolved before any live-service operation and not assumed by any proof:** the product's API and
     MCP server may read a live WAL store under rows 1 to 7. Every other toucher above uses a backup-API snapshot.
   - The proofs run on test stores made for them, never on a live run.

## State × event (the store's state at the request's transaction × the request)

| State | Bounds omitted | Upper bound ≤ last completed day | Upper bound > last completed day | Start-up reads | Copy |
|---|---|---|---|---|---|
| Empty store | as today | as today | as today | as today | consistent |
| First day in progress | refused (4) | — | refused (4) | wait; requests refused | consistent (an in-progress copy, read under the same rules) |
| A later day in progress | the last completed day | that bound | refused (3) | the last completed day | consistent |
| A day completing during a request | the request's own transaction | same | same | same | consistent |
| Crashed mid-day, not resumed | the last completed day | that bound | refused (3) | the last completed day | consistent |
| `-wal`/`-shm` absent and directory not writable | fails loudly (1) | same | same | fails loudly | — |

## Proof plan ($0, on test stores made for it; nothing built until the council accepts the contract)

1. **WAL mode:** the writer's store is in WAL mode with the size limit set; production's stores are unchanged.
2. **Every upper bound:**
   - the structural check that no bound is resolved outside `resolve_bound`;
   - for each of the 13 callers, an explicit future bound is refused naming the last completed day, an explicit past bound passes,
     and an omitted bound gives the last completed day;
   - lower bounds are unaffected.
3. **One state per request:** an API request, its state pinned by its first read, held between its first and last read while the writer commits a judgement and
   completes a day returns the state at its start, and the writer's commits succeed. Run on a first-day store and a store with one
   completed day.
4. **Start-up and MCP concurrency:**
   - two overlapping MCP calls across a writer's commit each return their own transaction's state, two overlapping **search**
     calls included (each with its own index connection, both writing the query cache);
   - after a later day completes, a tool call on the actual MCP entry point sees that day's views; the instructions still name their
     start day;
   - an error while opening connections leaves none open;
   - a call that fails mid-read leaves no open transaction and no open connection;
   - a service started on a first-day store refuses requests and builds its index after the first day completes;
   - MCP's object list after a later day includes that day's objects;
   - no transaction is open between MCP calls.
5. **Checkpoint and disk:**
   - below the free-space minimum, the writer stops before the day with its reason, and readers serve the last completed day;
   - a database-full error mid-day (a test store with `max_page_count`) stops the writer as a crash, and readers are unaffected;
   - a filesystem-full error mid-day: the store on a small disk image (`hdiutil`, a few MB), filled while the `-wal` grows. The
     writer exits non-zero, and readers serve the last completed day. Whether its reason was recorded is reported, not required;
   - with a long read held, the writer commits;
   - after the read ends, a checkpoint completes, and a reset brings the `-wal` within the limit;
   - with a reader held across three completed days, the writer stops before the fourth with its reason recorded, and readers serve
     the last completed day.
6. **Opening precondition:** with `-wal`/`-shm` absent and the directory read-only, a reader fails loudly. A busy read is retried
   within the timeout.
7. **A crash:** the writer is killed after committed writes mid-day.
   - Every route's answer, at every allowed bound, equals the answer from a backup taken at the last completed day.
   - The search index and the text sent to the embedding service (recorded by a fake transport) equal the backup's.
   - The partial day's rows are present in the file and invisible to every route and to the index.
8. **Copies:**
   - a backup taken while the writer commits passes an integrity check;
   - preflight refuses a store whose writer holds the lock, opened by its own path or by a symlink to it;
   - a store with a hard link elsewhere is refused by every entry point;
   - a crashed writer's store with committed data still in its WAL: a copy through a symlink equals a copy through the own path;
   - preflight arriving just before the writer: whichever takes the lock first wins. A writer finding preflight's lock refuses to
     start and writes nothing; preflight finding the writer's lock refuses to copy;
   - the store's path replaced after preflight's `stat` and before its open, and again during its copy: each is detected, the
     copy discarded and the request refused;
   - the writer's path replaced between its create and its open: the writer refuses;
   - the lock folder unwritable: both refuse and name it;
   - a held lock file deleted and recreated by hand: a second process can lock the new file, so exclusion is broken until the
     holder's next check. The writer rechecks its lock file's identity before each day and stops if it changed; preflight rechecks
     after its copy and discards it. The test shows detection at those points, not prevention;
   - it accepts a crashed store (lock released by the operating system), a store stopped in order with its WAL kept, a snapshot,
     and every historical input it accepts today;
   - a writer started while preflight holds the lock waits or refuses, and never writes under the copy.
8a. **Lexical search under an unfinished day:** a paused writer and a crashed one, each with more than 50 unfinished views matching a
   query. The search at the last completed day equals the same search on that day's backup: the same results, ranks and mode.
8b. **The index:**
   - a build failing after one batch leaves only correct vectors, and the next build embeds the rest;
   - a store replaced at the same path, with the same first step, whose view `v1` has a different text: the old `v1` vector is not
     used, and search is lexical and lists `v1` as missing;
   - with the same text, the vector is used, being correct by its key;
   - a store restored from an earlier snapshot: only its visible views' vectors are used;
   - a later day completing while the service runs: a new view with no matching vector is listed missing and search is lexical until a
     restart, after which it is embedded and search is semantic; a new view whose matching vector is already in the shared index is
     used at once;
   - a service started on a first-day store, through the API's and MCP's own start-up: after the first day completes, search is
     lexical when a visible view lacks a matching vector, and semantic when the shared index already holds one for every visible
     view; after a restart it is semantic;
   - an invisible view (an unfinished day's) whose cached vector has a different length does not change a search at the last
     completed day: the same results, mode and `missing_vectors`;
   - two concurrent searches for one new query: both answers are well formed, and the cache holds one vector for it; no equality with
     a fresh embedding is asserted;
   - an index build committing between a search's vector read and its scoring changes nothing in that search's answer.
   - All through the API's and MCP's own start-up and search entry points.
8d. **Orderly stop:** with a service reader holding the store, the writer's stop leaves WAL mode in place, records it and releases the
   lock; preflight then accepts the store. With no reader, the store ends in rollback-journal mode.
8c. **The index:** on a store with an unfinished day, the views sent to the (fake) embedding service are exactly those visible as of
   the last completed day.
8d′. **Production matching unchanged:** `store.search_views` gives the same results as before on a stored ledger, and the matching
   tests pass unchanged.
9. **The resolver keeps legacy and empty stores as today:** a legacy ledger with no `days_completed` and an empty store give the
   same answers before and after `resolve_bound` is introduced.
10. **The paused-writer harness** (`page-contract/serving_while_writing.py`) re-run: every check holds and the first-day case passes.

## Row 3's product-facing contract (council rounds 120 to 123; A1, clamping, withdrawn)

**The rule.**

- **On every store with a `days_completed` table**, finished or not, partial rows or not, an explicit upper bound later than the last
  completed day is refused. The same date gets the same answer whenever it is asked.
- An omitted bound gives the last completed day, as today.
- **Steps but no completed day:** refused as the first day.
- **`days_completed` present with no steps and no completed day** (an empty new store): read as today. An omitted bound gives what
  `default_as_of` gives today (none), and an explicit bound passes.
- **A ledger without the `days_completed` table:** today's default already queries that table (`store.last_completed_day`), so such
  a ledger already fails today with SQLite's "no such table" for an omitted bound. Through the resolver, an explicit bound fails
  the same way too, where before it skipped the default and could answer: a change, with none among the 143 stored ledgers.
- **Ranges** (amended in council round 124): a start after its resolved end is refused, for `changes` and `history` alike. A start
  equal to the end reads as before: an empty window for `changes`, whose start is excluded, so a polling client keeps its empty
  answer until a day completes; and that one day for `history`, whose start is included.

**The owner, and what the structural check enforces.**

- **`service.resolve_bound(conn, bound)`** raises `FirstDayNotCompleted` or `BoundNotCompleted(requested, last_completed_day)`, and is
  idempotent: a bound it has already passed passes again. On an empty store (tables, no steps, no completed day) or a legacy ledger,
  an omitted bound resolves to what `default_as_of` gives today, which can be `None`.
- **`service.resolve_range(conn, start, end)`** resolves `end` through `resolve_bound`, then raises `RangeNotOrdered(start, end)`
  when the start is after the end (round 124). When the end resolves to `None` (an empty store), it compares nothing and keeps
  today's outcome.
- `error_response` maps all three exceptions.
- **Every public function that takes a date resolves it at its entry through `resolve_bound`:**
  - `service`: `summaries`, `views`, `view`, `evidence`, `history`, `record`, `changes`, `evaluate`;
  - `bundle`: `not_judged`, `view_bundle`, `days`, `thesis_bundles`, `library`;
  - `idea.read_idea` and `search.search`.
- Nested calls pass a resolved bound, which resolves again unchanged. That covers `view_bundle` called directly with no date (as
  `scripts/mock_data.py` does), or from `_bundles` and `idea.read_idea`.
- **Internal helpers that take a date** (`dependencies`, `dependants`, `evidence_record`, `is_open_as_of`, `state_as_of`, `visible`,
  `_bundles`, …) receive their caller's resolved bound. That is `None` on an empty store, as today, and they behave as today with it.
  Each public function's output on an empty store is the same before and after the change; the test records today's outputs first.
- **A view not visible at the resolved day is refused** (`KeyError`, 404) by `bundle.view_bundle` and `bundle.not_judged` when called
  directly, as `_bundles` already skips it. So a question and its choices created after that day are never returned.
- **The structural check** reads every function of `service`, `bundle`, `search` and `idea` with a date parameter (`as_of`,
  `to_day`). Each must either call `resolve_bound` (or `resolve_range`) or be named in the check's list of internal helpers.
  - A function in neither, or a bound resolved by `or default_as_of(...)`, fails the suite.
  - The check's own mutant (a new public function without the call) must fail it.

**The response, per channel.**

| Channel | First day not completed | Bound after the last completed day | Range start not before its end |
|---|---|---|---|
| API | 503 `{"error": "the store's first day has not completed"}` | 409 `{"error": "day not completed", "requested": X, "last_completed_day": Y}` | 409 `{"error": "range start after its end", "start": S, "end": T}` |
| MCP tools | a tool error whose message carries the same fields | the same | the same |
| Streamed Idea route | the status and body, before any header | the same | — |

- `error_response` returns `(status, payload)`. The three new exceptions get the payloads above, and every other error keeps
  `{"error": message}`. `_answer` and `_stream_answer` send the payload as given.
- **The streamed route, in one transaction:**
  - it opens its connections, begins the read transaction and resolves the bound and first-day check;
  - **only then** does it send its 200 headers and run the Idea work in the same transaction, which it ends after;
  - a refusal is sent as a normal status and body before any header.
  - The Idea work includes model calls, so this transaction lasts the whole request, up to minutes. That is within row 5's
    one-request rule, and it holds back a checkpoint that long.

**Callers.**

- **The page, when its live library read succeeds:** it sends only days from the served dataset (`library.getDay()` to `/ideas`;
  the returned `card.idea.as_of` to `/thesis-bundles`). These are never after the last completed day.
- **The page, when its live library read fails:**
  - it keeps its embedded snapshot silently (as `thesis-ui.md` specifies), and that snapshot's day can be later than the service's
    last completed day;
  - `/ideas` is then refused with 409, and the page shows its existing Idea error naming no day;
  - this is documented here and tested; it is not claimed impossible.
- **MCP clients and direct API users with a later date:**
  - on the running product's store, they would get an error naming 2026-08-28 instead of today's half-processed 2026-08-29 (99
    evidence records, 117 links);
  - on a finished store, they would get an error instead of today's identical answer.
  - This is the behaviour change, recorded for Alex.
- **Not deployed:** no running service is restarted. D439 does not authorize a deploy, and the change reaches the running product
  only on a restart, which is on Alex's page.

**Proofs added to the plan (2b to 2e):**

- 2b. The structural check, and its mutant.
- 2c. Each public function called directly with a future bound, an omitted one and a past one, on the four store states (finished,
  partial, first day, empty with tables) and a copy of the served store's state. Each call's actual output or error is compared
  with the expected one: today's recorded output where the rule keeps it, the named refusal where the rule changes it.
- 2c′. `view_bundle` and `not_judged` called directly for a view created after the resolved day are refused (404). `days()` on an
  empty store returns `[]` as today.
- 2d. The ranges: a start after its end is refused for both; equality reads as before (`changes` empty, `history` that day).
- 2e. The streamed route on a first-day store and with a future date: a status before any header. With a writer committing during
  an Idea request, the request's data are the state at its start.
- 2f. The page verifier (`poc/ui/verify-*.mjs`): live read successful, then the Idea call succeeds; live read failed with a later
  embedded day, then the Idea error shows and nothing else breaks.

## The writer's start, stops and end (slice 4a; council rounds 131 and 132)

**Opening in WAL mode before anything is written.**

- `store.open_db` creates tables and commits as it opens, so WAL is set before it:
  1. the writer creates the store file empty and exclusively (create-new);
  2. it opens it with `sqlite3`, sets `journal_mode=wal` and **checks that the pragma answers `wal`**, refusing to start otherwise;
  3. it closes;
  4. it opens the store through `store.open_db`, which writes its schema in WAL mode (the mode is kept in the file);
  5. **it sets `journal_size_limit` (64 MB) on that writer connection,** since the limit belongs to a connection, not to the file.
- A test reads both `journal_mode` and `journal_size_limit` back on the writer's own connection after `open_db`, and again after the
  first day.

**Stops, through the real launcher (`run_stage_b.send`).**

- **The stop:** `ladder_adapter.WriterStopped(reason, last_completed_day)`, an `Exception` that `run_stage_b.resendable` does not
  accept.
- **Where it is raised:** in `replay`, before a day when the free space is below 20 times the store's size (main file and `-wal`), or
  when the truncating checkpoint after a completed day has failed for 3 consecutive days. Before raising, `replay` writes
  `adapter-counts.json` with the stop's reason and the last completed day, so the partial result is on disk.
- **What the launcher does with it:** its existing handling of a stop no resend can change, with one small change so the stop's
  own reason reaches the run (round 132):
  - `limit.stop(reason)`, where the reason for a `WriterStopped` is `"<run> incomplete: <the stop's reason>"` and not only the
    exception's name;
  - the attempt recorded with its reason;
  - the draw's state `incomplete`;
  - no redo, and every later launch stopped.
  - It is never recorded as complete.
- **The store keeps every completed day,** because the stop comes before a day starts or after a day's checkpoint. Readers keep
  serving the last completed day.
- **A stop before the first day** leaves the store empty (its tables, no step), which readers read as an empty store, and is recorded
  `incomplete` with its reason.
- **Tests through `run_stage_b.send` with the fake judge:**
  - low space before the first day;
  - low space before the third day (the last completed day is the second);
  - three failed checkpoints;
  - in each case: the exact reason in the attempt **and** in the run-level record (`stopped`), the draw's state, no redo, the
    store's last completed day, and the counts file's reason.

**Its end.** After the last day the writer tries `journal_mode=delete` with a short busy timeout. If service readers hold the store,
it stays in WAL mode and "stopped in order, WAL kept" is recorded in `adapter-counts.json`. Tested with and without a reader.

**Limit of 4a, stated:** until slice 4b the writer takes no lock. 4a's proofs run on isolated test stores and do not make a live run,
or preflight beside one, safe. P1 stays unresolved.

## Who writes, and copies: slice 4b (council rounds 134 and 135)

**The lock's owner and life.**

- `replay` owns both the writer's connection and its lock, in one `try`/`finally`. It acquires the lock in `open_wal_store` before
  the first write.
- **`open_wal_store` cleans up after itself:** if anything fails after it has taken the lock and before it returns (the WAL pragma,
  `store.open_db`, the identity check), it closes whatever connection it opened and releases the lock before raising. So `replay`
  only ever owns a fully opened store. Tested by making `store.open_db` fail after the lock is taken: afterwards the lock is free at
  once and no connection is open.
- **On every exit** (a normal end, `WriterStopped`, a judge or schema error, a spending stop, an interrupt, a failure while opening)
  it first closes the writer's connection, then releases the lock. No writable connection outlives the lock.
- No caller uses the runner's connection after `replay` returns (searched: `stage_b/*.py`, `serving_while_writing.py`).
- Tested on each exit: afterwards the connection is closed, and a new `acquire` takes the lock at once.
- **A killed writer process** (a subprocess running `replay`, ended with `SIGKILL` after committed partial-day writes) leaves the
  lock released by the operating system:
  - preflight then takes it and copies;
  - the copy answers as the last completed day;
  - this replaces 4a's in-process interrupt as the crash proof for the lock.

**The snapshot helper** (`live_lock.snapshot(store_path, destination)`, used by `scripts/snapshot_store.py`, its user-facing entry
point).

- **The same path rules as `acquire`:** the source's `realpath`, and a source with more than one hard link refused. It takes no lock,
  since it is AGENTS §9's route beside a running writer.
- **The destination must be a new path:**
  - it must not exist, and must not resolve to the source;
  - the copy is made into a temporary file beside it, converted out of WAL mode (`journal_mode=delete`, checked) and integrity
    checked;
  - it is then published **without replacing**: a hard link from the temporary file to the destination, which fails if the
    destination exists, then the temporary file is removed. A plain rename could replace a file that appeared during the copy
    (round 135).
  - on any failure (the backup, the conversion, the check) the temporary file is removed, nothing is left at the destination, and
    the helper raises.
  - An incomplete copy is never offered as a snapshot.
- **Tested through `scripts/snapshot_store.py`:**
  - a snapshot while the writer commits;
  - a refused hard-linked source;
  - an existing destination;
  - a destination equal to the source;
  - a failing conversion (made to fail by a test hook on the helper's conversion step), leaving nothing at the destination;
  - a destination created just before publication, which stays untouched while the helper refuses and removes its temporary
    copy.

**The filesystem-full proof is separate from the suite.**

- It is `live-service/filesystem_full_proof.py`, run explicitly. It never fills the workspace's filesystem.
- It creates a unique small disk image and mount point under the session's temporary folder (`hdiutil create`, a few MB;
  `hdiutil attach`), and always detaches and deletes them in a `finally`.
- It runs the writer on a store there until the filesystem is full. It checks that the writer exits as a crash and that readers
  serve the last completed day, and it reports whether the reason was recorded.
- If the image cannot be created or mounted, it reports **unexercised**, never passed.

**Found while building 4b (D598).**

- **A read-only reader could not open a WAL-mode store whose side files did not exist** ("unable to open database file"; tested on
  this machine's SQLite 3.51.0 through Python 3.10, on scratch stores). A read-only connection cannot create the `-shm` it needs.
  The product's own readers open `mode=ro` (`store.open_read_only`). The state can arise when the last connection to close is a
  read-write one and the mode is still WAL. In two direct checks the writer itself did not leave it: the side files remained after
  a stop. So what follows is a guard on that reachable state, not a fix of an observed writer failure.
  - So the writer now leaves WAL mode on **every** exit (`LadderAdapter.close`), not only at its normal end: before closing its
    connection it tries `journal_mode=delete`. WAL stays in two cases, kept distinct:
    - **a reader holds the store:** that reader is read-only, so it leaves the side files in place when it closes;
    - **the mode change fails for another reason** (for example the store's path changed): it is recorded as `wal`, and the
      connection is still closed and the lock released.
  - Tested on each exit: the store's mode is `delete` afterwards.
- **Preflight read each store twice:** once for its checks (now under the lock) and once more, unlocked, for its keyed-views count.
  It now makes one locked copy of each store before any part runs (`preflight.store_copies`), and both parts read that copy.
  - Tested through `preflight.main` with the parts recording what they were given.
- **`verify` reports a missing store and a newly added hard link** as a changed path (`PathChanged`), so the writer stops at its
  next day instead of failing with another error.
- **The filesystem-full proof** (`filesystem_full_proof.py`, run separately; `filesystem-full-proof.output.txt`), each variant on its
  own new 2 MB disk image, both detached and deleted:
  - **A, the free-space stop switched off:** the disk filled inside the tenth day. The writer exited with "database or disk is
    full", and no reason was recorded beside the store (as expected for a crash). Nine completed days were kept; readers and
    preflight's copy both serve 2026-07-09; the lock was free once the process had ended.
  - **B, the stop as built:** before the first day the writer stopped with its reason recorded, because it needed 17.6 MB free
    (20 times the 0.88 MB store, schema and `-wal` included) and the disk had 1.9 MB.

**Round 137's corrections (D599).**

- **Every reader opens a store by its own path.** `store.open_read_only`, which the API, MCP, `service` and reports all use,
  resolves a symlink and refuses a store with another hard link (`live_lock.LockRefused`, naming the reason).
  - The API refuses at start (`index_at_start`) and per request (500, the reason in the body).
  - MCP refuses at start and per tool call.
  - Census before the change: none of the 702 `.sqlite` files under `poc/data` and `clean-arch` has a second hard link.
- **Cleanup when cleanup itself fails:**
  - **`LadderAdapter.close`:** if leaving WAL mode fails, the connection is still closed and then the lock released. If closing
    the connection fails, the lock is kept until the process ends (the operating system releases it then). So a writable
    connection never outlives its lock.
  - **`snapshot`:** if the target cannot be opened, the source is closed and nothing is left.
  - **`scripts/snapshot_store.py`** also reports a SQLite error as a refusal (exit 1) instead of a traceback.
- **A store moved mid-run, a finding, not understood and not fixed:**
  - What was seen: SQLite raised "disk I/O error" on the writer's next statement after its store file was renamed, before the
    writer's own path check. This happened only in a process that had first run the API/MCP hard-link test. Which SQLite state in
    that process makes the difference was not identified.
  - A moved store breaks the contract's operating precondition (a store's path is never replaced while it may be in use). This
    finding is therefore a stated limit of that test case, not a claim that the writer handles a moved store.
  - What the writer records no longer depends on it:
    - its stop takes the last completed day from its loop;
    - before each day it checks the path first, then any checkpoint failure.

**Round 138's correction (D600): a reader holding the store is reported apart from every other failure.**

- `truncate_checkpoint` answers `done`, `busy` or the error's own text. `busy` means SQLite's own "database is locked" messages,
  or a checkpoint held back by another connection. That shows contention, not which connection; round 139 renamed the recorded
  reasons to "another connection held the store".
  - Only `busy` counts toward the three-day stop "another connection held the store".
  - Any other error stops the writer before the next day with "the truncating checkpoint after <day> failed: <error>". After the
    last day it is recorded in the counts.
- `leave_wal` answers the mode it ends in and why WAL was kept: "another connection held the store at the end", or "leaving WAL
  failed: <error>".
- Tested with a connection whose checkpoint, or whose change out of WAL, fails with "disk I/O error":
  - the stop's reason, and the record at the end, name that error and not a reader;
  - the lock is free afterwards.
- The real held-reader test still reports a reader.

## Proof 10's design (council rounds 140 and 141)

**What it runs.**

- A new harness, `live-service/proof10_serving_while_writing.py`. It reuses the D573 harness's page rendering and checks, and leaves
  that file as the record of its own run.
- It re-runs the extension draw's c1 through the accepted loop into a new scratch store to 2027-04-02.
  - Every judge request is answered from the stored archive by identity: $0, no model or embedding call.
  - The writer is the built `replay`: WAL, its lock, the checks before each day, its end.
- It runs detached with a log after the council's yes.

**Starting the API.** The API is started on the store being written at the first pause, lexical. It is ready when `/days` answers
200, or 503 with exactly "the store's first day has not completed". Any other answer fails the proof, and the D573 harness's "known
finding" exception is gone.

**At each of the seven pauses (states labelled):**

1. **The API, `/days` and `/library`:** every D573 check holds, the first-day one included.
   - At 2026-09-22 before close (the first day, nothing completed), both answer 503 with that body.
   - Fresh pages are rendered at the same two pauses as before.
2. **MCP, a module-level check:** the MCP module is loaded once at the first pause, as its entry point builds it, lexical, and its
   tool functions are called in-process. This exercises the tools' implementation, not the MCP transport, which stays a stated
   limit.
   - On the first day, its instructions say no day has completed, and `thesis_library()` and `views()` refuse.
   - Afterwards, `thesis_library()`'s day and view ids equal `/library`'s.
3. **Lock and copies:**
   - `live_lock.acquire` is refused, and so is preflight's `store_copies`, which names the snapshot route;
   - the store is in WAL mode.
4. **Snapshots in two distinct states:**
   - **2026-09-25 before judging, a day's articles committed and the day not completed:** the copy's last day is 2026-09-24 and it
     holds processing steps dated 2026-09-25;
   - **2027-01-31 before close, a due-day closing not yet completed (no articles that day):** the copy's last day is 2027-01-30 and
     none of the three questions due that day (v3, v4, v7) is closed in it. A switch has no day of its own, so the first run's query
     of a day column failed: my error, the harness's, not the product's.
   - Both copies are out of WAL mode, with integrity `ok`.

**Concurrent reads.** A poller asks `GET /library` back to back from the API's start to the writer's return. The harness brackets
each day's completion with the times just before and just after `close_and_complete`. For every answer:

- the status is 200, or 503 only for a request sent before the first day's completion ended;
- the day it serves completed no later than the answer arrived (the day's completion started before the answer was received);
- it is no older than the last day whose completion had ended before the request was sent;
- the days never go backwards;
- after the run, `GET /library?as_of=<that day>` decodes to the same JSON (compared by a hash of its canonical form). The first
  difference is read before anything is called a leak; this is a test of the historical filter, not a guarantee row 3 already
  gives.
- **The polling must not be vacuous:** at least 20 answers, and at least one day whose completion has answers on both sides (one
  served an earlier day and arrived before the completion started; one served that day or later).

**After the writer ends:**

- the lock is free;
- the store is out of WAL mode, or WAL is kept with "another connection held the store at the end" recorded (the poller may hold a
  read at that moment);
- the API answers as of the store's last completed day.

**It exits 1 unless every check holds.** A failure is read to its first differing value before anything is changed.

## Slice 5: row 1's reader rules and the proofs still open (council rounds 143 and 144)

**Row 1, made true in code** (a product change: today readers set no busy timeout of their own, and a failed open names no path):

- **One opener for a reader's pinned state:** `service.open_pinned(path)` opens with `mode=ro`, runs `BEGIN` and the first read, and
  returns the connection. The API's `Connections` and MCP's `connections()` both call it, replacing their own copies of those three
  steps.
- **Loud, with the store's path:** if the open, the `BEGIN` or the first read fails with a SQLite error, `open_pinned` closes what it
  opened and raises `service.StoreUnreadable("<path>: <SQLite's message>")`, a `LedgerError`.
  - The API answers 500 with that message, before any header on the streamed route.
  - MCP raises it from the tool.
  - It never serves an empty or stale answer in its place.
- **An explicit busy timeout:** `store.open_read_only` connects with `timeout=READ_BUSY_TIMEOUT_SECONDS` (5 s, the value Python
  applied by default until now). SQLite's busy handler retries `SQLITE_BUSY` within it; there is no application-level retry, and
  row 1's wording is narrowed to say so.

**Tests, at $0:**

- **6a.** A WAL store whose side files are absent, in a read-only directory:
  - `open_pinned` raises `StoreUnreadable` naming the path;
  - `GET /days` answers 500 with the path;
  - the streamed Idea route answers 500 before any header;
  - an MCP tool raises it.
- **6b.** A WAL store held by a connection in exclusive locking mode, a stand-in for SQLite's rare WAL busy cases (such as WAL-index
  recovery), which cannot be timed in a test:
  - released after 0.5 s, a reader's `open_pinned` waits and succeeds;
  - with the timeout set to 0.3 s and the hold kept for 1.5 s, it raises `StoreUnreadable` with "database is locked" and the path.
- **5a.** `max_page_count` set on the writer's connection during a day, so the day fails with SQLite's "database or disk is full":
  - through `run_stage_b.send`, the draw is incomplete with no redo;
  - readers serve the last completed day;
  - the lock is free.
  - Kept beside the real-disk proof, which it does not replace.
- **5b.** A real reader held across one completed day, then released:
  - the checkpoint after that day is `busy`;
  - the next one is `done`, and the `-wal` is then 0 bytes.
- **7′.** In the `SIGKILL` test, the killed writer takes a reference backup through its own connection right after its second day
  completes, before any write of the third. After the kill, the crashed store and preflight's copy are each compared with the
  reference.
  - The calls are `tests/bound_cases.calls`: 8 service functions, 5 bundle functions and lexical search.
  - Each runs at the omitted bound, an explicit past bound (the first completed day), an explicit bound equal to the last completed
    day, and a future bound (refused alike).
  - Equality is of the outcome (the canonical JSON's hash or the error).
  - The API and MCP routes call these functions. Idea functions are not in the list, and the report says so.
- **8′.** On the same crashed store, `scripts/snapshot_store.py` through a symlink and through the own path gives two copies whose
  every table is equal row by row.

**Slice 5's results (D603).**

- **Built:**
  - `store.READ_BUSY_TIMEOUT_SECONDS` and the explicit timeout;
  - `service.open_pinned` and `StoreUnreadable`, used by the API's `Connections` and MCP's `connections()`.
- **Tests:**
  - `tests/test_reader_rules.py` (5): 6a through `open_pinned`, the API's `/days` and streamed Idea route (500 with the path,
    before headers), and MCP at start and per tool; 6b waits about 0.5 s and then reads, and held past a 0.3 s timeout it fails
    with the path. The exclusive-lock fixture was first checked to make the read wait.
  - `stage_b/test_writer_proofs.py` (2): 5a, a `max_page_count` failure on the third day, incomplete with no redo, the lock free,
    and readers on the second day; 5b, `busy` while a reader is held, then `done` with the `-wal` at 0 bytes.
  - The `SIGKILL` test now does 7′ and 8′. 7′ is 88 outcomes over the listed 14 functions at 4 bounds in 2 states, the crashed
    store and preflight's copy each equal to the reference taken before the third day. 8′ is the symlink and own-path snapshots
    equal in every table.
- The suite passes (346), the new system's folders (192), and the frozen checks. Mutants 6 of 6 (`slice5-mutants.txt`).

## Not covered

- Resuming a stopped live store.
- The Idea planner on a new-system ledger.
- A long-running service's restart and monitoring.
- The page's note when its live read fails, which is Alex's presentation choice.
