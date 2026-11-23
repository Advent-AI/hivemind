# Proof 10: serving while the built writer runs (D601), 2026-11-16, $0

`proof10_serving_while_writing.py` → `proof10-output.txt`. The extension draw's c1 was judged again through the accepted loop by the
built writer (WAL, its lock, its checks, its end) into a new scratch store, to 2027-04-02. Every judge answer came from the stored
archive: no model or embedding call. The API ran lexical on the store being written, and MCP's tool functions were called in-process.
**All 23 checks hold** (exit 0).

## At the seven pauses

| Pause (state) | `/days`, `/library` | MCP's `thesis_library` | Lock, preflight, mode | Snapshot |
|---|---|---|---|---|
| 2026-09-22 before close (first day, nothing completed) | 503 and 503, "the store's first day has not completed" | refused; the instructions say no day has completed; `views` refused | held, refused naming the snapshot route, WAL | |
| 2026-09-24 after close | 200, as of 09-24, 5 questions | as of 09-24, v1 to v5 | held, refused, WAL | |
| 2026-09-25 before judging (articles committed, day not completed) | as of 09-24, equal to the previous pause | as of 09-24 | held, refused, WAL | last day 09-24, steps dated 09-25 present, out of WAL, integrity ok |
| 2026-09-25 after close | as of 09-25, 6 questions | as of 09-25, v1 to v6 | held, refused, WAL | |
| 2027-01-30 after close | as of 01-30, 7 questions | as of 01-30 | held, refused, WAL | |
| 2027-01-31 before close (due-day closing not completed) | as of 01-30, equal to the previous pause | as of 01-30 | held, refused, WAL | last day 01-30, v3, v4 and v7 not yet closed, out of WAL, integrity ok |
| 2027-01-31 after close | as of 01-31; v3, v4 and v7 closed on that day | as of 01-31 | held, refused, WAL | |

Fresh pages at 09-25 before judging and 01-31 after close show exactly the questions and statuses served on the page's day, as in D573.
The first-day case, a "known finding" in D573, now passes as a required check.

## Concurrent reads

- **169 answers in 5.7 s,** spanning the writer's whole run from the first completion to the last. The replay from stored answers
  completes about 190 calendar days in about 5.4 s; days without articles take almost no time.
  - 9 were 503 before the first day completed. 160 were 200, serving 16 distinct days.
  - The days never went backwards.
  - Every 200 answer decodes to the same JSON as `GET /library?as_of=<its day>` on the finished store.
- **Stricter counts than the harness's own line:**
  - 8 answers were in flight while a day was completing, and each served either the previous day or the completing day;
  - 10 completions were seen directly: the last answer before them served an earlier day, and the first after them served exactly
    that day.
  - The harness line "162 completions with answers on both sides" counts any earlier and any later answer, so it is loose; the
    numbers above are the evidence.
- **What the timing shows** (council round 141): each answer's day is compatible with its completion brackets. The brackets alone do
  not prove the exact commit time; the dated-read equality and the pause checks are the further evidence.

## After the writer

- The lock was free.
- The store ended in rollback-journal mode.
- The API answered as of the last completed day, 2027-04-02.

## Limits

- MCP was checked at module level, its tool functions, not through its transport.
- One run.
- The store and the readers ran on this machine's local disk.
- The two runs (the first stopped on my error) created the contract's lock folder `~/.hivemind-locks`, with two empty lock files
  named by the scratch stores' device and inode. Lock files are never deleted while a store may be written, under the contract's own
  rule.

## My error

The first run stopped at the 2026-09-25 snapshot, on my query of a `day` column that `view_switches` does not have (a switch has only a
sequence). I wrote it without reading the table. The January state is now asserted by which questions are closed.
