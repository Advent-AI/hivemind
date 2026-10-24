# Disposition of Codex's review of the service (2026-10-24)

Review: `codex-review.md` (read-only, prompt `codex-prompt.md`). Every finding was reproduced on the sealed ledger
before a change; each fix has a test that fails on the old code (`tests/test_service.py`, `tests/test_search.py`).

| # | Finding | Checked | Done |
|---|---|---|---|
| 1 | [P1] HTTP routes fail: the SQLite connections were opened on the main thread and used by request threads (`ThreadingHTTPServer`) | Reproduced (the first start crashed on `/days`) | Single-threaded `HTTPServer`; an entry-point test starts the server as a user does and calls `/days`, `/views`, `/search`, `/evaluate`, the 400/404 paths |
| 2 | [P1] `view()` returned dependencies and dependants recorded after `as_of` (28 relationship rows late; v94 as a dependant of v1 on 02-25) | Reproduced; Codex's count confirmed | `dependencies(conn, view_id, as_of)` and `dependants(conn, view_id, as_of)` filter by the row's sequence day; resolutions too; test asserts the 28 and v94's absence |
| 3 | [P1] `changes()` cited evidence with every source known today (750 later outlets) | Reproduced | `evidence_record(conn, evidence_id, as_of)` filters sources by day; `changes` uses it with the judgement's day; test on v4/e3 |
| 4 | [P1] Band parsing: first-two-numbers plus left-closed/right-open misread 18 of 42 money ladders (v17 "0至不足1000亿", v27 "不高于 1690 亿") | Reproduced on all 42 | Parser rewritten: comparator words bound to the next amount (longest match wins: 大于或等于 is not 大于 + 等于), ranges, postfixes, exact amounts, inclusive/exclusive bounds, remarks and parentheses skipped, bare numbers only when zero; `ladder_bands` accepts a ladder only as one unbroken partition, else `evaluable: false` with the reason. 42 of 42 money ladders read; the 6 ladders that read partially are percentages/gigawatts and are refused |
| 5 | [P1] "=" treated "threshold inside the judged band" as holds | Reproduced | `verdict_for`: "=" holds only for a single-amount band, borderline inside a band, not_yet outside; test |
| 6 | [P2] Search said "semantic" with missing or stale vectors (zero scores ranked) | Reproduced | `fresh_vectors` compares the stored text hash with the current text; any candidate without a fresh vector makes the whole answer `mode: lexical` with `missing_vectors` listed; both fronts call `ensure_index` at start (or `--lexical` to skip without network) |
| 7 | [P2] `search_eval.py` treated the literal `none` as a view id and never failed | Confirmed | `none` is "no lead"; the four examples carry accepted sets and the script exits 1 when one lacks an accepted view in its top 3; day-0 leads are reported, not required |
| 8 | [P2] The embedding error carried the provider's response body (could echo a key) | Confirmed by Codex's fake 401 | Only `HTTP <code> (<error type>)` is kept; test with a fake 401 whose body echoes a key-like string |
| — | HTTP `/evaluate` returned `200 null` for an unknown view; `/changes` invented `since`; MCP returned error dicts as results | Confirmed | 404 / 400; MCP raises (a tool error) |
| — | `_json` turned corrupt JSON into "no citations" | Confirmed | `LedgerError`, HTTP 500; test |
| — | Design table incomplete (index fields, spans, extra fields); checks list thin | Confirmed | `docs/poc/service.md` rewritten: full value × reader table incl. index rows, the span calls, the claim-evaluation rule, the check list that the tests cover |
| — | Tests did not cover the fronts, relationships, nested sources, equality, stale vectors, evidence exclusion, a real text change | Confirmed | All added; the "changed question" test now edits a scratch copy of the ledger |

Not changed: the query-vector cache's primary key is the text hash alone (a model switch overwrites, which costs a
re-embed, never a wrong vector: the row's model is checked on read); the day-0 leads stay leads.

## Second pass (`codex-review-2.md`): six remaining findings

| # | Finding | Checked | Done |
|---|---|---|---|
| 1 | [P1] `269.79亿` converted to 26979000000.000004, so v84's shared boundary belonged to the wrong band | Reproduced | Amounts converted with `Decimal`; test `evaluate(v84, '=', 26979000000)` → position 3, borderline |
| 2 | [P1] v70's conditions start with a dateline ("截至2026-12-31，…"); the parser took the first clause and lost the bound; 43 money ladders, not 42, and the census test used the parser to decide what counts as money | Reproduced | `operative_clause`: the first clause that names an amount plus the clauses that continue it (且/并且/但/或); the census test picks money ladders by a text regex and asserts 43 of 43 read |
| 3 | [P2] `--lexical` only skipped the start-up build; queries still embedded | Confirmed | `search(..., semantic=False)` never looks at vectors or calls the embedder; both fronts pass the flag; test |
| 4 | [P2] An empty `vector_json` with the right hash counted as fresh | Confirmed | `usable(vector)` required for freshness and on build (rebuilt when empty); dimensions must agree; test |
| 5 | [P2] The partition check accepted a boundary nobody owns (both bands exclusive) | Confirmed; none of the sealed ladders has it | Exactly one adjacent band owns each boundary; design wording fixed; test with the synthetic pair |
| 6 | [P2] `ensure_index` reported zero work when a later batch failed | Confirmed by inspection | `build_index` returns (embedded, unchanged, tokens, error) with the work done before the failure; test with a flaky second batch |
| — | No regression test for the eval script's `none` and exit code | Confirmed | `lead_of()` tested; `main()` exits 1 on a miss (monkeypatched search) |

Not changed: the freshness check reads every view's text once per query (13 ms on 94 views); a cached per-ledger
text-hash table is the next step when the ledger has thousands of views, not now.
