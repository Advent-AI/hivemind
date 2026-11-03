# TrueNorth event index as a source: NVIDIA, geopolitics, chip supply chain (2026-10-27)

Alex: "你用一下我们的truenorth-api 不是有个event endpoint 吗，你也backfill 一发nvidia, geopolitcs, chip supply chain 相关的数据到我们这个clean source db". The endpoint is the MCP tool `event_v2` (TrueNorth's curated story index). Scripts: `harvest_truenorth.py --events` (selectors per topic in `topics.json`, key `truenorth`), `fetch_bodies.py` (the stories' pages), `assemble.py` (`truenorth_story_topics`, `truenorth_story_row`). Window 2026-07-01..2026-10-27, asked as `time_window=119d`.

## What the index can give (measured)

- The index holds nothing before **2026-07-23**: 0 of 3,191 harvested stories are earlier. "The past three months" is 07-23..10-26 here.
- `include_body` returns no body; no MCP tool returns an article. A story is a title, the provider's summary, the source link and the index's own labels (`event_type`, `final_rank_score`, `token_addresses`).
- Selection by **asset id** (`token_address`) is clean; selection by **text query** matches any word: random samples of query-only hits under export controls, tariffs, supply chain and chip stocks were mostly off topic (Apple Macs, an MSCI index rule, a DEX hack, a satellite contract). The `topic` filter accepts no value we guessed (geopolitics, macro, semiconductors, ai: 0 results). `event_type=geopolitical_event` with a keyword is clean but tiny (China: 18, Taiwan: 0, tariff: 3).
- Harvest: 23 selectors, 3,191 distinct stories (2,918 new files), 2,679 carrying `token_addresses`. SK hynix is `stock_skhy` in the index (the resolver answers `stock_skhx`, 0 stories); Samsung has no id with stories.

| Selection | Stories 07-23..10-26 |
|---|---|
| NVIDIA, `stock_nvda` | 283 |
| Chip supply chain ids: TSM 45, AMD 85, AVGO 57, MU 82, SK hynix 72 (via `token_addresses`), ASML 16, INTC 90 | ~375 distinct |
| Crude oil `comm_wti` (Middle East proxy) | 150 |
| 15 text queries (export controls, Taiwan Strait, tariffs, rare earths, HBM, CoWoS, semiconductor stocks, Iran/Israel oil, Russia/Ukraine) | ~2,500, mostly off topic |

## The rule built

A TrueNorth story enters the corpus **by identity only**: under every topic whose asset selector found it or whose `token_addresses` (topics.json, `truenorth.token_addresses`) the story itself carries. Text queries only find candidates; a query-only hit carrying no listed asset id is not an item (its raw file stays). `fetch_bodies.py` fetches only stories that are items. Test: `test_labels.py::test_truenorth_story_topics_label_tier_and_objects_like_a_listing` (mutant that labels by query: fails).

Under this rule 693 + 15 (second pass, `stock_skhy`) stories are items; no topic of the geopolitics tier other than oil can be selected by identity from this index.

## The databases

`freeze_window.sh`-style chain (assemble → relabel → GDELT drop → check → clean_pages), into new names; the canonical cleaned database of D351 and the paused run's input are untouched:

- `poc/data/items-nvda-2026-07-01-10-27-tn.page.sqlite` (whole pages), `poc/reports/items-nvda-2026-07-01-10-27-tn.page.check.md`
- `poc/data/items-nvda-2026-07-01-10-27-tn.sqlite` (cleaned), `poc/reports/items-nvda-2026-07-01-10-27-tn.clean-census.txt`

TrueNorth event rows in the cleaned database: **708 rows, 72 fed**. The source links are 83% benzinga.com, which answers 403 to the fetcher (576 of 576), so the article text of most stories is unreachable; the other 636 rows carry only the provider's summary (`coverage = provider_summary`, `feed = 0`: not an original document, kept for review). Fed by month: July 54, August 0, September 0, October 18 (the stories whose page a non-blocked site served).

| | canonical cleaned (D351) | with TrueNorth events |
|---|---|---|
| rows | 34,084 | 34,520 |
| fed | 6,874 | 6,950 |

Rows other than TrueNorth events: 33,811 → 33,812 (one Google News page became full because the TrueNorth page fetch served the same URL), 16 rows changed (14 went from title-only to full for the same reason; 2 cleaned-text differences), none removed.

## Why it is not usable as a source (Alex, 2026-10-27: "记录下truenorth 的库不太能用的原因吧，然后先别管他了")

1. **No article text.** `include_body` returns nothing, no tool returns an article, and 83% of the links are benzinga.com, which blocks the fetcher (403 on all 576). 636 of 708 stories are a title and a one-sentence summary; under the original-document rule they are not fed.
2. **No topic selection.** Text queries match any word; random samples of the export-control, tariff and supply-chain hits were mostly off topic. The `topic` filter accepts no value we found. Geopolitics is reachable only through an asset id such as crude oil.
3. **No history.** The index starts 2026-07-23; a window from July 1 loses three weeks.
4. **Thin and one-sided.** 283 NVIDIA stories and about 375 supply-chain stories in three months, 70% from one publisher, against 27,000 Google News listings in the same window.

Set aside on Alex's instruction; the databases above stay as the record and the canonical database is unchanged.

## What this means

As a source for NVIDIA and the chip supply chain, `event_v2` adds a few hundred listings a quarter with summaries, but almost no readable article text, and it cannot select geopolitics by identity. The open choices for Alex: (1) whether the TrueNorth-backfilled database replaces the canonical cleaned one (one rename; it adds 76 fed rows and 636 summary rows); (2) whether a provider summary may be fed, which would change the "original document only" rule (Alex 2026-10-23) and is not done here; (3) whether to ask the TrueNorth team for article bodies in `event_v2` (the schema has `include_body`, the service returns none).
