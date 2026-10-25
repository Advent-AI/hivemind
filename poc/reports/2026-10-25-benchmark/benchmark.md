# Matching benchmark by state (seed + week 2026-07-24..31; log row 41)

Arms: control = the generative matching call (poc-v21); jev = Jev matching (poc-v22, the engine as run that day). Golds: `week-benchmark-2026-10-25.json`, `evidence-decisions-seed-2026-10-25.json`, `grouping-identity-gold-2026-10-25.json`; retrieval from `recall-oracle/summary.md`. Every count is a reading of the texts; "either" and "debatable" are not scored.

## Layer 1: the candidate thesis against the library

| state | control right/n | jev right/n |
|---|---:|---:|
| merge | 5/5 | 2/5 |
| succession | 2/2 | 2/2 |
| new | 41/41 | 46/46 |
| set aside (either) | 2 | 1 |
| skipped by code (object not on the list) | 2 | 0 |

- jev gnews:04f9b244186ad52647b6931e|c1: gold merge → new  (Aggregate spending to fund artificial intelligence)
- jev gnews:d67077a64d61e214e5d9ac06|c1: gold merge → new  (Calendar-year spending by tech giants on data cent)
- jev gnews:39deea97b690ac7b56dada0b|c1: gold merge → new  (Vera revenue)

## Layer 1b: group memberships (each arm against its own ledger)

| measure | control | jev |
|---|---:|---:|
| required members recovered | 11/13 | 14/17 |
| forbidden members admitted | 0 | 2 |
| memberships written | 13 | 23 |
| groups holding two matters (F1) | ['g1'] | ['g1'] |

- missed required: v24 in hyperscaler_capex_cycle
- missed required: v30 in hyperscaler_capex_cycle

- forbidden admitted: v27 into rubin_rollout via ['g1']
- forbidden admitted: v23 into rubin_rollout via ['g1']
- missed required: v32 in hyperscaler_capex_cycle
- missed required: v35 in hyperscaler_capex_cycle
- forbidden admitted: v23 into hyperscaler_capex_cycle via ['g1']
- forbidden admitted: v27 into hyperscaler_capex_cycle via ['g1']
- missed required: v23 in openai_nvidia_financing (no group for this matter in the ledger)

## Layer 2: evidence against the thesis's pieces

### Seed (gold: all 65 decisions, 64 judged)

```
gold: 65 decisions, 64 judged, 1 uncertain; by class {'new': 41, 'repeat': 21, 'replace': 2}

control: 53/64 right (11 wrong kind, 0 wrong target, 0 not decided in this ledger)
  repeat: 13/21
  replace: 1/2
  new: 39/41
- q4fy26cfocommentary.htm|e5|v2: gold repeat → control new ()
- q4fy26cfocommentary.htm|e5|v3: gold repeat → control new ()
- q4fy26pr.htm|e2|v3: gold repeat → control new ()
- nvda-20260125.htm|e5|v5: gold repeat → control new ()
- nvda-20260125.htm|e6|v9: gold repeat → control new ()
- truenorth:transcript:NVDA:2026-05-20|e5|v5: gold replace → control repeat (NVIDIA management said it shipped initial Vera Rubin samples to custom)
- q1fy27cfocommentary.htm|e1|v2: gold repeat → control new ()
- q1fy27cfocommentary.htm|e2|v3: gold repeat → control new ()
- q1fy27cfocommentary.htm|e8|v8: gold repeat → control replace (NVIDIA CFO Colette Kress said FY2027 GAAP and non-GAAP tax rates are e)
- q1fy27pr.htm|e5|v7: gold new → control repeat (NVIDIA reported Q1 FY2027 GAAP operating expenses up 52% year over yea)
- nvda-20260426.htm|e6|v9: gold new → control repeat (NVIDIA said H200 shipments under the new licensing program would be su)

jev: 59/64 right (5 wrong kind, 0 wrong target, 0 not decided in this ledger)
  repeat: 20/21
  replace: 2/2
  new: 37/41
- nvda-20260125.htm|e5|v5: gold repeat → jev replace (NVIDIA management said it shipped initial Vera Rubin samples to custom)
- q1fy27cfocommentary.htm|e3|v3: gold new → jev repeat (NVIDIA CFO Colette Kress reported Q1 FY2027 Data Center revenue of $75)
- q1fy27pr.htm|e4|v6: gold new → jev repeat (NVIDIA attributed Q1 FY2027 year-over-year gross-margin improvement to)
- q1fy27pr.htm|e5|v7: gold new → jev repeat (NVIDIA reported Q1 FY2027 GAAP operating expenses up 52% year over yea)
- nvda-20260426.htm|e6|v9: gold new → jev repeat (NVIDIA said H200 shipments under the new licensing program would be su)
```

### Week samples (all replacements + 30 repeats + 30 new per arm, read from the texts)

| state | control right/wrong/debatable | jev right/wrong/debatable |
|---|---|---|
| repeat | 30/0/0 | 29/0/1 |
| replace | 2/0/0 | 8/7/0 |
| new | 25/3/2 | 30/0/0 |

jev replace, why wrong: {'third_party_view_superseded_a_fact': 2, 'should_have_been_repeat': 1, 'older_than_target_caught_by_writer': 2, 'unstated_date': 1, 'caveat_superseded_the_fact': 1}
control new, why wrong: {'retelling_written_as_new': 3}

## Retrieval, measured apart

- theses: every open thesis of the item's objects is shown and is a legal target; in all six known duplicates the earlier thesis was in the later candidate's list.
- evidence: Evidence retriever recall@k, oracle over every piece in force (120 sampled truncated decisions of 330; $0.0537)
- evidence: decisions where the oracle finds a same-statement piece anywhere: 45
- evidence: of which the strongest lies only OUTSIDE the shown top-10 (candidate recall misses, to read): **5**
- evidence: inside and outside both ≥ 0.5: 4
- evidence: recall@k estimate on decisions with a true repeat (before reading the misses): 40/45

## Robustness: the same archived Jev answers under other thresholds

462 evidence calls and 44 candidate calls in the jev archive.

| threshold | evidence calls deciding repeat | deciding replace | candidate calls with a `same` ≥ t |
|---:|---:|---:|---:|
| 0.4 | 213 | 17 | 2 |
| 0.5 | 201 | 19 | 2 |
| 0.6 | 191 | 13 | 2 |
| 0.7 | 167 | 6 | 2 |

The decisions were taken at 0.5 (pre-set, never tuned). Rows show how many calls would change their first-stage outcome if the threshold moved; the writer's and checker's rules apply after.

## Cost and time per stage (archives; published rates)

| stage | control | jev |
|---|---|---|
| extract gpt-6-luna | {'calls': 274, 'seconds': 2224, 'cost': 0.3331} | {'calls': 510, 'seconds': 4272, 'cost': 0.5927} |
| judge gpt-6-luna | {'calls': 144, 'seconds': 2086, 'cost': 0.1379} | {'calls': 274, 'seconds': 4937, 'cost': 0.2569} |
| match gpt-6-luna | {'calls': 155, 'seconds': 1602, 'cost': 0.1959} | {'calls': 155, 'seconds': 1602, 'cost': 0.1959} |
| match jev-1.14.0 | — | {'calls': 506, 'seconds': 289, 'cost': 0.0708} |

The jev archive began as a copy of the control's, so its gpt-6-luna rows include the control's calls; the jev rows are the new engine's own.

