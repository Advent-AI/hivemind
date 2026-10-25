# Matching benchmark by state, D167 arms (seed + week 2026-07-24..31; log row 46)

Arms: v23-llm = generative matching (poc-v23-llm), v23-jev = Jev matching (poc-v23); both on extraction v10 with the D167 writer rule, scored on each arm's week snapshot (views.week.sqlite). Control-arm recall oracle: poc/reports/2026-10-25-recall-oracle-v23-llm (46/49, 3 candidate misses). Golds: `week-benchmark-v23-2026-10-25.json`, `evidence-decisions-seed-v23-llm-2026-10-25.json`.

## Layer 1: the candidate thesis against the library

| state | v23-llm right/n | v23-jev right/n |
|---|---:|---:|
| merge | 1/1 | 1/2 |
| succession | 1/1 | 0/0 |
| new | 36/36 | 47/47 |
| set aside (either) | 6 | 2 |
| skipped by code (object not on the list) | 0 | 0 |

- v23-jev gnews:b5b9996d85745b7ba41d94a7|c1: gold merge → new  (Combined capital expenditures by Alphabet, Amazon,)

## Layer 1b: group memberships (each arm against its own ledger)

| measure | v23-llm | v23-jev |
|---|---:|---:|
| required members recovered | 7/11 | 12/13 |
| forbidden members admitted | 0 | 0 |
| memberships written | 16 | 23 |
| groups holding two matters (F1) | [] | [] |

- missed required: v10 in rubin_rollout
- missed required: v14 in hyperscaler_capex_cycle
- missed required: v24 in hyperscaler_capex_cycle
- missed required: v27 in china_chip_export_controls

- missed required: v11 in rubin_rollout

## Layer 2: evidence against the thesis's pieces

### Seed (golds: v23-llm `evidence-decisions-seed-v23-llm-2026-10-25.json`, v23-jev `evidence-decisions-seed-v23-jev-2026-10-25.json`)

```
gold: 59 decisions, 59 judged, 0 uncertain; by class {'repeat': 23, 'new': 33, 'replace': 3}

v23-llm: 55/59 right (4 wrong kind, 0 wrong target, 0 not decided in this ledger)
  repeat: 20/23
  replace: 3/3
  new: 32/33
- q4fy26cfocommentary.htm|e4|v5: gold repeat → v23-llm new ()
- nvda-20260125.htm|e6|v6: gold repeat → v23-llm new ()
- nvda-20260125.htm|e8|v7: gold repeat → v23-llm new ()
- nvda-20260426.htm|e9|v7: gold new → v23-llm repeat (NVIDIA said the U.S. granted a license in February 2026 for small H200)

gold: 70 decisions, 70 judged, 0 uncertain; by class {'new': 34, 'repeat': 33, 'replace': 3}

v23-jev: 65/70 right (5 wrong kind, 0 wrong target, 0 not decided in this ledger)
  repeat: 30/33
  replace: 3/3
  new: 32/34
- nvda-20260125.htm|e8|v7: gold repeat → v23-jev new ()
- truenorth:transcript:NVDA:2026-05-20|e2|v3: gold new → v23-jev replace (NVIDIA CFO Colette Kress said the Q1 FY2027 revenue growth was expecte)
- q1fy27pr.htm|e4|v2: gold repeat → v23-jev new ()
- q1fy27pr.htm|e6|v9: gold new → v23-jev repeat (NVIDIA reported Q1 FY2027 Compute & Networking revenue of $74.550 bill)
- nvda-20260426.htm|e4|v4: gold repeat → v23-jev new ()
```

### Week samples (all replacements + repeats + new per arm, read from the texts)

| state | v23-llm right/wrong/debatable | v23-jev right/wrong/debatable |
|---|---|---|
| repeat | 29/1/0 | 27/2/1 |
| replace | 0/0/0 | 2/9/1 |
| new | 26/3/1 | 25/4/1 |

v23-llm repeat, why wrong: {'analyst_view_called_repeat_of_management_statement': 1}
v23-llm new, why wrong: {'same_figure_in_another_document_in_the_list': 2, 'retelling_of_the_same_statement_in_the_list': 1}
v23-jev repeat, why wrong: {'two_commentators_similar_opinion_called_same': 2}
v23-jev replace, why wrong: {'third_party_view_over_fact_or_statement_refused_by_writer': 4, 'older_than_target_refused_by_writer': 1, 'unrelated_later_statement_same_tier_written': 2, 'commentary_over_rumour_written': 2}
v23-jev new, why wrong: {'same_figure_in_another_document_in_the_list': 2, 'retelling_of_the_same_report_in_the_list': 2}

## Retrieval, measured apart

- theses: every open thesis of the item's objects is shown and is a legal target; in all six known duplicates the earlier thesis was in the later candidate's list.
- evidence: Evidence retriever recall@k, oracle over every piece in force (120 sampled truncated decisions of 285; $0.0839)
- evidence: decisions where the oracle finds a same-statement piece anywhere: 36
- evidence: of which the strongest lies only OUTSIDE the shown top-10 (candidate recall misses, to read): **0**
- evidence: inside and outside both ≥ 0.5: 4
- evidence: recall@k estimate on decisions with a true repeat (before reading the misses): 36/36

## Robustness: the same archived Jev answers under other thresholds

399 evidence calls and 44 candidate calls in the v23-jev archive.

| threshold | evidence calls deciding repeat | deciding replace | candidate calls with a `same` ≥ t |
|---:|---:|---:|---:|
| 0.4 | 150 | 15 | 2 |
| 0.5 | 148 | 15 | 1 |
| 0.6 | 133 | 11 | 1 |
| 0.7 | 114 | 8 | 1 |

The decisions were taken at 0.5 (pre-set, never tuned). Rows show how many calls would change their first-stage outcome if the threshold moved; the writer's and checker's rules apply after.

## Cost and time per stage (archives; published rates)

| stage | v23-llm | v23-jev |
|---|---|---|
| extract gpt-6-luna | {'calls': 259, 'seconds': 2389, 'cost': 0.2935} | {'calls': 259, 'seconds': 2525, 'cost': 0.3043} |
| judge gpt-6-luna | {'calls': 111, 'seconds': 1893, 'cost': 0.0995} | {'calls': 119, 'seconds': 1666, 'cost': 0.1076} |
| match gpt-6-luna | {'calls': 139, 'seconds': 1108, 'cost': 0.1241} | — |
| match jev-1.14.0 | — | {'calls': 443, 'seconds': 247, 'cost': 0.0697} |

Each arm counted on its own configuration's calls only (the archives began as copies of an earlier run).

