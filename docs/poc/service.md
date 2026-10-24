# Hivemind as a database with a search engine on top (2026-10-24, D76)

Alex, 2026-10-24: "hivemind 就是一个数据库上面有个搜索引擎". The views database (the ledger the pipeline writes) gets a
read-only service: a search engine over the views, and readers for what the ledger holds. Anyone with an idea (an
agent, Claude through MCP, a web page) searches, gets views back, chooses which to keep and how to arrange them, and
reads each view's state, history and evidence. Hivemind does not choose for the caller, does not know users, does
not store theses or bets (experience PRD §三 boundary); those live with the agent.

## The day everything is read as of

Nothing reads the clock (D12, D13). `view`, `views`, `evidence`, `record`, `evaluate` and `search` take `as_of`, a
calendar day (default: the ledger's last completed day); `history` and `changes` take a span of days. A row is
visible as of a day when the sequence number it was written under belongs to an item or a daily round dated on or
before that day (`seq_day_map`): this covers views, switches, judgements, evidence links, sources, replacements,
dependencies and their resolutions. Counted on the sealed ledger: every one of those rows has such a day; 28
dependency rows and 750 source rows are later than the view or judgement they attach to and are hidden by the filter.

## Values and their readers

| Call | Value returned | Read by |
|---|---|---|
| `search(query, k, as_of, include_closed)` | `query`, `as_of`, `mode` (semantic or lexical), `missing_vectors` (views without a vector made from their current text), `results[]`: view_id, object, kind, looks_at, question, due_day, open, dependencies (ids), dependants (ids), score, parts {semantic, object_hit, text_hit}; `results` is null when the library holds no view on anything the idea names (D91) | the agent that chooses; `scripts/search_eval.py` |
| `views(object, as_of, include_closed)` | a list of `view` records | the agent, a page |
| `view(view_id, as_of)` | view_id, object, object_kind, kind, looks_at, question, due_day, year, created_day, created_from, as_of, open, rungs[] {position, label, condition}, state {position, label, condition, judgement_day, since_day, previous_position, rounds, why_changed, reasons} or null, dependencies[] {view_id, direction, wait_chain_view_id, wait_year, since_day}, dependants (ids), counts {rounds, evidence, facts} | the idea card's tile |
| `history(view_id, from_day, to_day)` | judgements[] {day, seq, position, changed, moved_from, why_changed, reasons, cited (ids), pushes, round}, changes (the judgements with moved_from), arrivals {day: {evidence, facts}}, replacements[] {day, old, new, said_day}, switches[] {day, open, reason} | the ladder chart, the replay |
| `evidence(view_id, as_of, tier)` | pieces[] {evidence_id, one_line, quote, tier, speaker, original_who, original_day, event_time, day, sources[] {input_id, category, publication_day, seq}, outlets, replaces}; replaced pieces excluded | the evidence list |
| `record(view_id, as_of)` | last_check {day, round, items_processed_that_day, evidence_arrived_that_day} or null (experience PRD §十三 item 2) | the card's "last checked" line |
| `changes(since_day, to_day)` | changed judgements[] {view_id, day, from_position, to_position, position_moved, why_changed, cited[] (evidence records with the sources known that day)} (§十三 item 1, pull form) | an agent polling for moves |
| `evaluate(view_id, comparator, value_usd, as_of)` | evaluable (bool) and `reason` when not; else comparator, value_usd, claim_position (the rung whose band holds the threshold, or null on an unassigned boundary), judged_position, judged_label, judged_condition, verdict: holds, not_yet, borderline, not_judged | the idea card |
| `thesis_bundles(view_ids, as_of)` / `GET /thesis-bundles?ids=...` | `as_of`, `days`, and complete dated `view_bundle` records, including historical evidence and source metadata; consumed by `fromBundles` | the modular Thesis UI (`poc/ui`), or an agent preparing its input |
| `POST /ideas {text, as_of?, k?}` (`idea.read_idea`) | the idea card: `idea {text, as_of}`, `search {mode, candidates}`, `reading {summary, parts[{question, view_ids, why}], chosen[{view_id, why, part}], claim, dropped[], trace[]}` or null, `evaluation` (the `evaluate` answer) or null, `views[]` (the mapped views in the front end's bundle shape, `hivemind.bundle`), `days[]`, `no_recorded_view`, `cost {usd, input_tokens, output_tokens, seconds, cached, turns}`; the reading is made by an agent with the tools search / view / evaluate (D134); design `docs/poc/idea-card.md` | the FE's idea card; `scripts/idea_probe.py`, `scripts/idea_eval.py` |
| index rows (`view_vectors`, `query_vectors`) | text_sha256, model, vector_json, tokens, built_at; written by `search.build_index` / `query_vector`, read by `search.fresh_vectors` / `query_vector`; input: the view's own text and the embedding answer | the search engine only |

The ledger's text is Chinese (the pipeline writes Chinese); the service returns it as stored.

## How a claim is evaluated

A rung's condition is a sentence ("不低于 1650 亿美元且不高于 1690 亿美元，处于公司指引区间"). Its band is read from the
comparator words and the amount each binds to, a range ("650亿美元至720亿美元（含两端）", "0至不足1000亿"), a postfix
("9000亿美元及以上") or an exact amount ("恰为2500亿美元"); remarks after ；or ， and parenthesised asides are not read,
and a bare number is money only when it is zero (30%, 4吉瓦, 2025年 are not). The bound is read from the first
clause that names an amount and the clauses that continue it (且…), so a dateline before it ("截至2026-12-31，") and
a remark after it are dropped; amounts are converted exactly (269.79亿 is 26,979,000,000). The ladder is evaluated
only when its bands form one unbroken partition (06-views: 格和格不重叠、不留空; adjacent bands share their boundary
amount and exactly one of them owns it; the lowest may start at 0). Otherwise `evaluable` is false with the reason: a
percentage or gigawatt ladder is refused, never guessed. On the sealed ledger all 43 money ladders read. The verdict asks whether every amount in the judged band satisfies the
claim (holds), none does (not_yet), or only some do (borderline); "=" holds only for a single-amount band.

## What is not in the service

- Choosing or arranging views for a caller (no "issue tree" tool).
- Anything written to the ledger: the pipeline is the one writer. The index is a derived file beside the ledger
  (`poc/data/search-index.sqlite`), rebuilt from the views' text by content hash.
- Users, theses, bets, notifications.
- Judging, opening or closing views from a query, or deciding for the caller which returned view fits. The one
  thing code decides is whether the library holds any view on what the idea is about (D91, detection per D132):
  `results` is null only when no company or theme of the universe is named (id, full name or a listed alias,
  product names included), the ledger's text index matches no view (Latin words and three-character Chinese
  windows), and the top similarity is below 0.30, the floor only off-subject ideas reach (measured on 74
  sentences: ideas with a view score 0.33 or more). A similarity cutoff for relevance was measured and rejected
  (a nonsense idea naming NVDA scores 0.49, real theses on CUDA 0.35); the caller judges relevance.

## Checks the new path passes (tests/test_service.py, tests/test_search.py)

- as_of never looks ahead: state (v3 on 05-19 vs 05-20), existence (v16 before 07-24), closure (v24 from 08-02),
  replacement (the 05-20 guidance), relationships (v94 absent from v1's dependants on 02-25; the 28 late rows),
  sources cited by a change (e3 on 02-25 has only that day's outlets).
- The index is derived: a second build embeds nothing; a changed question (on a scratch copy of the ledger) re-embeds
  that view only; the indexed text contains the question and none of the view's evidence.
- Search: semantic only with a usable vector made from the current text for every candidate (a stale hash, an
  empty vector or an absent row all make the answer lexical and name the view); a front started with `--lexical`
  never calls the embedder; the trigram order ranks the lexical fallback; the query vector is cached by text and
  model; as_of hides later views; a batch that fails midway reports the batches already stored.
- Every one of the 43 money ladders in the sealed ledger (picked by a text regex, not by the parser) reads as one
  partition; the six non-money ladders are refused; Codex's cases (v17 ≥ 500亿 borderline, v27 ≥ 1690亿 at position 3
  borderline, v84 = 269.79亿 at position 3 borderline, v70's dateline) and "=" inside a band → borderline; a
  boundary no band owns is refused.
- A corrupt judgement record raises `LedgerError`; the HTTP front turns it into 500, a bad parameter into 400, an
  unknown view into 404 (tested by starting the server as a user does, with `--lexical` so no network is needed).
- The embedding error carries the status and the provider's error type, never the response body (tested with a
  fake 401 whose body echoes a key-like string).
- Null (D91): a house in Austin, Tesla and "黄仁勋是个天才" get null in both modes; "Vera Rubin volume shipments"
  (no company named, found by the text index) and "NVDA 的 logo 比 AMD 好看" (names NVDA) do not.
- Acceptance of the ranking: `scripts/search_eval.py` fails when any of the four example theses lacks an accepted
  view in its top 3 or a day-0 sentence the mapper placed gets null, and reports the day-0 sentences against their
  mapper's lead (a lead, not gold).

## Fronts

- MCP (`scripts/hivemind_mcp.py`): one tool per call; an unknown view is a tool error; `--transport stdio` for a
  local agent, `--transport streamable-http` to serve `/mcp` over HTTP.
- HTTP (`scripts/hivemind_api.py`, 127.0.0.1 by default): threaded, every request opens its own SQLite
  connections; GET routes plus `POST /ideas`.
Both embed what is missing at start (`search.ensure_index`) and print what was embedded, or how far it got before a
failure; `--lexical` turns embedding off altogether (no network): every search answers in lexical mode.
- Docker (`Dockerfile`, `Dockerfile.mcp`, `docker-compose.yml`): two services from two images (the API image is
  standard library only; the MCP image installs `mcp` from wheels downloaded on the host into `build/wheels`,
  because the build network cannot reach PyPI). The ledger and items database are mounted read-only, the
  service folder (`poc/data/service/`: index, idea archive) read-write, the credentials file read-only. Verified
  2026-10-24: both containers answer GET routes and MCP over HTTP; a model or embedding call from inside a container
  fails on this machine because its VPN (Clash Mi in TUN mode) carries the host's traffic but not the Docker VM's.
  Two one-line fixes, Alex's choice: enable host networking in Docker Desktop (then `network_mode: host`), or open an
  HTTP proxy port in Clash with LAN access (then `HTTPS_PROXY=http://host.docker.internal:<port>` for both services).
