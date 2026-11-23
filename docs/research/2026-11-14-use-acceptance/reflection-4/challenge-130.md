# Round 131: slice 3 built and proven (D596); the writer's slices 4a and 4b proposed

## Slice 3 (D596)

- **Built:**
  - lexical ranking over the views visible at the bound, in an in-memory full-text table;
  - `fresh_vectors` over visible candidates in creation order;
  - `build_index` embeds only views visible at the last completed day and refuses a first-day store;
  - both start-ups skip a first-day store;
  - `store.search_views` unchanged for matching.
- **Tests:** `tests/test_search_live.py` (10), including the backup equality with 60 matching unfinished views, both newly visible
  cases through MCP, and the first-day start through MCP and the API. The suite passes (327), and so do the new system's folders
  (164).
- **Mutants:** 4 of 4 caught. My first invisible-view control was not decisive, because my creation-order walk kept the invisible view
  last. It was rebuilt so the invisible view has the lower sequence.
- **Found:** a backup of a WAL store keeps WAL mode, and a read-only reader of the copy fails ("unable to open database file"). Row 7
  now says the copy is set to `journal_mode=delete` first.
- **My error:** a fake embedder wrapped `search.fake_embed` twice. I had not read the function, and five tests failed for that before
  any real result.

## The writer (`ladder_adapter.LadderAdapter` and `replay`), proposed in two slices

**4a: the store's mode and life, rows 1, 5 and 6.**

1. `LadderAdapter` creates its store file empty and exclusively, then sets WAL and `journal_size_limit` (64 MB) before writing.
2. **Before each day** `replay` checks the free space (at least 20 times the store's size, stated in its limits). Below that, it
   stops before the day with its reason recorded in `adapter-counts.json`.
3. **After each completed day** it asks for a truncating checkpoint with a short busy timeout. Three consecutive failures stop it
   before the next day with its reason.
4. **At its end** it tries `journal_mode=delete`. If readers hold the store, it keeps WAL and records "stopped in order, WAL kept".
5. **Proofs:**
   - 1: WAL and the limit set; production's stores unchanged;
   - 5: a long reader held across three completed days stops the writer, and readers keep the last completed day; below the free
     space, a stop before the day; a database-full error mid-day (`max_page_count`) as a crash;
   - 6: the writer killed after committed partial-day writes, then every service, bundle and search answer at every allowed bound
     equal to a converted backup at the last completed day, with nothing of the partial day embedded;
   - 8d: orderly stop with and without a reader.
   - The filesystem-full test on a small disk image goes in 4b, with the lock.

**4b: who writes, and copies, row 7.**

- A `live_lock` module: the one lock folder (`~/.hivemind-locks`, 0700, fail closed), locks named by device and inode, checked on
  both sides of the open, symlinks resolved, hard links refused.
- The writer creates, locks, opens and verifies before writing.
- Preflight locks without waiting, copies with the backup API and sets `journal_mode=delete` on the copy.
- A repository snapshot helper does the same.
- The filesystem-full test.

**Asked of you:** whether this split and 4a's plan are faithful to rows 1, 5, 6 and 8d, and anything missing.

End with `CONSENSUS: yes` (build 4a) or `CONSENSUS: no, because …`.
