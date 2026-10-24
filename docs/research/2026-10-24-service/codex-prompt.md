# Review request: the Hivemind service (read-only)

Read-only review. Do not modify files, run nothing that writes, call no model API.

## What was built and why

Alex's scope for the POC's next step (2026-10-24): "hivemind 就是一个数据库上面有个搜索引擎". The views ledger the
pipeline writes gets a read-only service: a search engine over the views and readers for what the ledger holds.
An agent searches, gets views back, chooses which to keep and how to arrange them itself, and reads each view's
state, history and evidence. Hivemind does not choose for the caller (no "issue tree" tool), does not know users,
stores no theses. The design, the calls and the checks they must pass: `docs/poc/service.md`.

## Files under review

- `src/hivemind/service.py` — as-of reads over the ledger: views, view, history, evidence, record, changes, evaluate.
- `src/hivemind/search.py` — the index (one embedding per view, keyed by the sha256 of the view's own text, in a
  derived SQLite beside the ledger) and `search()` (cosine + object boost + trigram-index boost; lexical fallback).
- `scripts/hivemind_api.py` (HTTP, 127.0.0.1) and `scripts/hivemind_mcp.py` (MCP, stdio): thin fronts.
- `scripts/search_eval.py` — builds the index and runs the evaluation sentences.
- `tests/test_service.py`, `tests/test_search.py` — on the sealed ledger `poc/data/sealed-2026-10-24-run3-through-0815/views.sqlite`
  (read-only) with a fake embedding for search.

Context to read, not to review: the ledger's schema and writers `src/hivemind/views/store.py`; the design of views,
judgements, evidence and dependencies `docs/prd/06-views.md`; the no-clock rule `docs/DECISIONS.md` D12, D13, D31;
the experience PRD's boundary and the five items Hivemind must add `docs/experience-prd.md` §三, §十三;
the working rules `AGENTS.md` (§2 design tables, §3 one owner, code over prose, explicit inputs, never the wall
clock; §4 tests; §9 credentials never in logs or arguments).

## What to deliver

1. **as_of correctness.** For every function in service.py: which rows it makes visible for a day, and any row that
   can leak from after the day (a judgement, a link, a replacement, a switch, a view, a dependency, a source).
   Check `seq_day_map`: it maps a sequence number to the day of the item or daily round written under it — are
   there rows whose `seq` has no processing_steps row (and so are never visible), or rows written under a later
   sequence than the day they belong to? Count on the sealed ledger with queries; show the queries.
2. **The search engine.** Does the indexed text follow the design (the view's own text, never evidence)? Is the
   ranking what the design says, and does the lexical fallback rank? Is the index truly derived (keyed by text hash,
   rebuildable, model recorded)? Is the query vector cache correct (same text, same model)? Any way the embedding
   key reaches the index, a log or an argument?
3. **The fronts.** Does each route or tool pass exactly the parameters the function takes, with the same defaults?
   Error handling that lets a failure pass as a result? Anything bound beyond 127.0.0.1? Query text written to logs?
4. **Tests.** Does each test trace to a check in `docs/poc/service.md` or a requirement in 06-views? Is any test
   written to fit the code rather than the spec? Which checks in the design have no test?
5. **The design tables (AGENTS §2).** Does `docs/poc/service.md` hold the value × reader table and the new-path ×
   old-checks list, and do the functions match it? Name any value a function returns that the table does not list
   and any listed value that no function returns.
6. **Rules.** Anything that writes (the index is allowed, the ledger is not), reads the clock for anything but a
   timestamp on an index row, or hides a failure behind a warning.

Rank findings by what they break for a caller. Quote the code line for each. A finding needs a concrete case
(an input and the wrong output); a style remark is not a finding.

## Out of scope

The pipeline (`src/hivemind/{dispatch,extraction,replay,pull,config,model}.py`, `src/hivemind/views/{matching,writing,judging,round}.py`),
the prompts, the corpus scripts, the web mock under `poc/mock/`, and any proposal to add judging, user state or an
issue-tree tool to the service. A gap in a module not listed above is not a finding.
