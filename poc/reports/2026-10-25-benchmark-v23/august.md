# Matching benchmark by state, D167 arms, August 1-15 (log row 49)

Arms: v23-llm = generative matching (poc-v23-llm), v23-jev = Jev matching (poc-v23), both as run (before D168). Golds: `august-benchmark-v23-2026-10-25.json`, `evidence-decisions-seed-2026-10-25.json`.

## Layer 1: the candidate thesis against the library

| state | v23-llm right/n | v23-jev right/n |
|---|---:|---:|
| merge | 6/6 | 6/7 |
| succession | 1/1 | 0/3 |
| new | 34/35 | 35/35 |
| set aside (either) | 2 | 2 |
| skipped by code (object not on the list) | 8 | 4 |

- v23-llm gnews:dcc5556122de8bb36a458f29|c1: gold new → merge v1 (2026 capital expenditures by Amazon, Microsoft and)
- v23-jev gnews:76e151efcc88dd5dbb954869|c1: gold merge → new  (Hyperscaler capital expenditure on AI in calendar )
- v23-jev 001769628-26-000366:crwv-20260630.htm|c1: gold succession → new  (FY2027 total revenue)
- v23-jev 000541:a2026q2consolidatedreport-.htm|c2: gold succession → new  (TSMC consolidated annual revenue)
- v23-jev gnews:4a6db5f4d17bc985e47b0e49|c2: gold succession → new  (SpaceX cumulative compute capacity online at year-)

## Layer 1b: group memberships (each arm against its own ledger)

| measure | v23-llm | v23-jev |
|---|---:|---:|
| required members recovered | 11/17 | 23/25 |
| forbidden members admitted | 0 | 1 |
| memberships written | 30 | 51 |
| groups holding two matters (F1) | [] | [] |

- missed required: v14 in hyperscaler_capex_cycle
- missed required: v24 in hyperscaler_capex_cycle
- missed required: v40 in hyperscaler_capex_cycle
- missed required: v61 in hyperscaler_capex_cycle
- missed required: v10 in rubin_rollout
- missed required: v27 in china_chip_export_controls

- missed required: v84 in hyperscaler_capex_cycle
- missed required: v11 in rubin_rollout
- forbidden admitted: v64 into naver_expansion via ['g5']

## Layer 2: evidence against the thesis's pieces

### Window samples (all replacements + repeats + new per arm, read from the texts)

| state | v23-llm right/wrong/debatable | v23-jev right/wrong/debatable |
|---|---|---|
| repeat | 18/1/1 | 16/1/3 |
| replace | 1/0/0 | 0/7/0 |
| new | 16/3/1 | 19/0/1 |

v23-llm repeat, why wrong: {'another sentence of the same call as target': 1}
v23-llm new, why wrong: {'same_figure_in_another_document_in_the_list': 2, 'retelling_of_the_same_fact_in_the_list': 1}
v23-jev repeat, why wrong: {'two_commentators_similar_opinion_called_same': 1}

## Retrieval, measured apart

- theses: every open thesis of the item's objects is shown and is a legal target; in all six known duplicates the earlier thesis was in the later candidate's list.
- evidence: (oracle not run)

## Robustness: the same archived Jev answers under other thresholds

686 evidence calls and 95 candidate calls in the v23-jev archive.

| threshold | evidence calls deciding repeat | deciding replace | candidate calls with a `same` ≥ t |
|---:|---:|---:|---:|
| 0.4 | 258 | 23 | 10 |
| 0.5 | 250 | 23 | 8 |
| 0.6 | 222 | 17 | 8 |
| 0.7 | 192 | 13 | 8 |

The decisions were taken at 0.5 (pre-set, never tuned). Rows show how many calls would change their first-stage outcome if the threshold moved; the writer's and checker's rules apply after.

## Cost and time per stage (archives; published rates)

| stage | v23-llm | v23-jev |
|---|---|---|
| extract gpt-6-luna | {'calls': 221, 'seconds': 2216, 'cost': 0.2661} | {'calls': 221, 'seconds': 1929, 'cost': 0.2699} |
| judge gpt-6-luna | {'calls': 108, 'seconds': 2056, 'cost': 0.1525} | {'calls': 109, 'seconds': 2187, 'cost': 0.1812} |
| match gpt-6-luna | {'calls': 124, 'seconds': 1028, 'cost': 0.1319} | — |
| match jev-1.14.0 | — | {'calls': 338, 'seconds': 200, 'cost': 0.0724} |

Each arm counted on its own configuration's calls only (the archives began as copies of an earlier run).

