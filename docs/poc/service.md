# Hivemind service: a thesis database with search

D76, October 24, 2026; English edition and current-document refresh, October 25 (D163). Alex defined Hivemind as a database with a search engine on top. Its read service lets an agent or page find theses, choose what to use and inspect the state, history and evidence. Hivemind stores shared **theses**, not user ideas, positions or commitments. This distinction replaces the ambiguous use of “thesis” for both in the earlier document. The [historical source](../research/2026-10-25-english/service.original.md) retains prior wording and verification details.

The core read service does not choose or arrange results for a caller. The separate [`POST /ideas` application flow](idea-card.md) decomposes an idea and maps it to theses through two model calls, then returns a UI-ready response. This supersedes the earlier one-call and agent-loop descriptions.

## Historical visibility

Readers accept an `as_of` calendar day, defaulting to the ledger's last completed day. They do not use today's clock to reinterpret history. A row is visible when its dispatch sequence belongs to an item or daily round dated on or before that day. This applies to theses, switches, judgements, evidence links, sources, replacements, dependencies and resolutions. `history` and `changes` use explicit date spans.

The historical sealed-ledger check found 28 dependency rows and 750 source rows newer than the theses/judgements they attach to; those rows must stay hidden in earlier reads. A later quotation or relationship must not appear in an old snapshot.

## Interfaces and readers

Field and route names are compatibility identifiers; `view` in an API name means the glossary's **thesis**.

| Interface | Returned content | Reader |
|---|---|---|
| `search(query, k, as_of, include_closed)` | Query/day, semantic or lexical mode, missing current vectors, ranked results or null; each result includes ID, subject, kind, focus, question, due date, lifecycle, relationships and score components | Caller chooses relevant theses; search evaluation |
| `views(object, as_of, include_closed)` | Thesis records | Agent or page |
| `view(view_id, as_of)` | Identity, source, dates, ladder, current state or null, dependencies, dependants and counts | Agent or detail panel |
| `history(view_id, from_day, to_day)` | Judgements, rung changes, evidence arrivals, replacements and lifecycle switches | History chart and replay |
| `evidence(view_id, as_of, tier)` | Evidence in force, original quotes, summaries, tiers, speakers, dates and sources | Agent or evidence list |
| `record(view_id, as_of)` | Last completed check with day/round and processed/arriving counts, or null | “Last checked” display |
| `changes(since_day, to_day)` | Changed judgements with previous/current positions, reasons and historically visible citations | Polling agent |
| `evaluate(view_id, comparator, value_usd, as_of)` | Whether evaluable and why; otherwise claim position, judged position/label/condition and verdict | Numeric claim display |
| `thesis_bundles(view_ids, as_of)` / `GET /thesis-bundles?ids=...` | Complete dated bundles with ladder, judgements, historical evidence, sources, dependencies and switches | `fromBundles` in the modular UI |
| `POST /ideas` | Idea, search summary, mapped parts and chosen theses, related theses, evaluation, optional bundles, days, trace and cost | Idea application/UI; see its contract |
| Derived index | Content hashes, embedding model, vectors, token counts and build timestamps | Search only; not the thesis ledger |

The service returns stored prose as stored. D163's new English-generation path is not yet active; historical Chinese records remain readable. The choice between a fresh English library and cross-language continued ingestion is pending. Do not infer cross-language matching guarantees from enum compatibility.

## Numeric claim evaluation

Use structured numeric rung bounds where supplied; the legacy path parses text. Bounds must form an unbroken, non-overlapping partition. Each shared boundary belongs to exactly one band; a lowest money range may begin at zero. A non-money or unparseable ladder returns `evaluable: false` with a reason.

Legacy parsing recognises comparator phrases, ranges, postfix bounds and exact amounts. It follows the clauses specifying the amount, ignoring preceding datelines and later remarks. A bare nonzero number is not automatically money; percentages, gigawatts and years are not dollar amounts. Chinese magnitude units remain accepted input. For example, 269.79 hundred-million dollars is exactly $26,979,000,000. The original-language regression strings remain in tests and the historical source document.

The evaluation asks whether every amount in the judged band satisfies the user's claim (`holds`), none does (`not_yet`), or only some do (`borderline`). An equality claim holds only for a singleton amount. Missing judgement returns `not_judged`; an unassigned boundary is not guessed.

Historical validation covered all 43 money ladders selected independently by text pattern and refused six non-money ladders. Boundary, exact-amount and dateline cases remain regression requirements. That result does not validate newly translated English-only bands; D163 must test those separately.

## Search contract

The index embeds each thesis's own text, not its evidence. A content hash detects outdated vectors. Search can report semantic mode only when all relevant candidates have usable current vectors; absent, empty or stale vectors require lexical mode and explicit missing-vector reporting. A second unchanged index build embeds nothing. A failed batch reports already stored progress.

D91's null means no recorded coverage, not low relevance. D132 checks named subjects using IDs, full names and configured aliases (including products), the text index, and semantic coverage where enabled. An off-subject similarity floor is not a universal relevance threshold: an irrelevant sentence naming NVDA can score above a relevant narrower query. The caller still judges relevance.

`--lexical` disables embedding calls throughout startup and requests. Query vectors are cached by text and model. The historical evaluation checks four example questions within their top three accepted matches, plus day-zero coverage; mapper suggestions are not human gold labels.

## State × event and failures

| State/event | Required behavior |
|---|---|
| Historical read | Filter every attached value by its own sequence/day, not only the thesis creation date |
| Missing thesis | HTTP 404 or MCP tool error |
| Invalid parameter | HTTP 400 |
| Corrupt judgement | Raise `LedgerError`; HTTP 500, not fabricated state |
| Missing/stale vector | Truthful lexical mode and missing-vector list |
| Lexical configuration | No embedder invocation |
| Read request | No ledger writes; derived index/cache writes remain separate |
| Concurrent HTTP requests | Each request owns its SQLite connections |
| Embedding failure | Report status/type without exposing the response body or credentials |

No query opens, closes or rejudges a thesis. No read route stores user commitments or performs trades. The ingestion pipeline remains the ledger writer.

## Transports and local operation

- `scripts/hivemind_mcp.py` exposes the readers as tools over stdio or streamable HTTP at `/mcp`.
- `scripts/hivemind_api.py` is the threaded HTTP front, listening on localhost by default.
- Both build required index content at startup unless lexical mode is selected.
- `Dockerfile`, `Dockerfile.mcp` and `docker-compose.yml` mount the ledger/items read-only and service index/archive storage read-write. Credentials remain server-side and are never included in a bundle.

The October 24 environment check found both containers could answer local HTTP/MCP reads, but the host VPN did not carry Docker VM traffic for external model calls. The recorded options were host networking or an explicitly configured reachable proxy. This is an environment observation, not a current connectivity claim or authorisation to change networking.

Verification requirements live in `tests/test_service.py`, `tests/test_search.py` and transport/bundle tests. New language behavior must retain their historical visibility, numeric, cache and failure guarantees. The [UI integration](../../poc/ui/README.md) documents the rendering boundary.
