# D181: the parallel day, measured end to end on live APIs

**Answer.** On the complete July 27 day (53 items), the parallel day finishes in a median **112.5 s** against
**501.8 s** for the serial product path: **4.46× end to end**, **5.91×** for the item work (extract, match, write).
Every trial passes its audit, and every trial's own answers, replayed through the other mode with no network, give a
ledger identical in all ten product tables plus handovers and match decisions. Its drift from the recorded golden is
inside the range the serial trials show against each other.

Picture it as a kitchen with one cook who must plate dishes in order. Before, the cook prepared and plated one dish at a
time. Now helpers prepare later dishes early; at each dish's turn the cook checks that its preparation used exactly
what is on the pass now, and redoes it if an earlier dish changed that. Plating order and plates are unchanged.

## Speed: three serial against three parallel trials, interleaved

Order `serial-1, parallel-1, parallel-2, serial-2, serial-3, parallel-3`; each trial a fresh ledger copy and a fresh
archive, so every answer is a fresh live call. Parallel: 16 extraction workers, 8 Jev workers per matching phase.

| Trial | Total s | Item work s | Daily judging s | Extraction calls | Jev calls | Retried attempts | Published-rate $ |
|---|---:|---:|---:|---:|---:|---:|---:|
| serial-1 | 501.8 | 461.4 | 40.4 | 53 | 58 | 0 | 0.0680 |
| parallel-1 | 112.5 | 78.1 | 34.5 | 68 | 63 | 0 | 0.0836 |
| parallel-2 | 130.2 | 91.2 | 38.9 | 77 | 73 | 2 | 0.0936 |
| serial-2 | 524.4 | 481.4 | 43.0 | 53 | 75 | 0 | 0.0738 |
| serial-3 | 481.4 | 440.9 | 40.5 | 53 | 63 | 0 | 0.0669 |
| parallel-3 | 104.2 | 67.4 | 36.8 | 61 | 78 | 0 | 0.0810 |

| Median | Serial | Parallel | Speed-up |
|---|---:|---:|---:|
| Whole day | 501.8 s | 112.5 s | **4.46×** |
| Item work | 461.4 s | 78.1 s | **5.91×** |
| Daily judging | 40.5 s | 36.8 s | 1.10× (same code in both: six workers per dependency level) |

The parallel day pays for its early requests: 8–24 extraction requests per day were prepared, then changed by an
earlier commit and prepared again; published-rate cost is $0.086 against $0.070 per day (+24%). Under 16 concurrent
calls the provider did not slow down: median extraction call 6.9–7.5 s parallel, 6.9–7.4 s serial.

The product entry point was also run once as a user runs it, `scripts/replay.py --workers 16 --jev-workers 8` with the
product's own OpenAI and Jev clients: **135.5 s** wall time including interpreter start, $0.09, audit clean,
cross-replay identical, 31/53 items identical to the golden ([check](product-cli/check.json)).

## Where the parallel day's time goes

In parallel-1 the 78 s of item work split into 60 s of waiting for an item's extraction at its turn and 17 s of
matching and writing. The waiting is mostly real dependency, not scheduling: in the recorded replay, when item 33 commits it changes what
items 34–38 must be shown, so their extraction can only start after it. A recorded replay that prepares the whole day
ahead (lookahead 53, ordered by item) left the chain unchanged (95 s at recorded durations), so that change was not
kept. What remains:

- **Dependency chains** (~45–60 s): inherent to the rule that an item sees everything committed before it (D159).
- **Daily judging** (~37 s): one round per day after the last item (D63), already concurrent within a dependency level.
- **Matching chain** (~17 s): each item's two matching phases run in order; sending the next item's first phase early
  would save at most ~10 s and add a second speculative path. Not built.

Ten times end to end on this day would need judging and dependency chains to shrink; neither is a scheduling change.

## Correctness

| Check | Result |
|---|---|
| Audit: each accepted extraction rebuilt from its committed prefix, bound to the exact archived answer; judging population, day completion, memberships | 6/6 trials clean, plus the product CLI run |
| The runner's own record of the request each turn accepted equals the rebuilt request | 53/53 in every parallel trial ([re-audit](reaudit.json)) |
| Parallel answers replayed through the serial path, no network | 3/3 identical (998–1,031 rows over 12 tables) |
| Serial answers replayed through the parallel runner | 3/3 identical (965–1,028 rows); the runner's discarded early requests 8–24 |
| Recorded golden, full day, product module, 16 workers | all 10 tables identical ([summary](recorded-16/summary.json)) |
| Deliberate mutant: accept the prepared answer without re-checking | caught: 17 handovers without an exact current-prefix request; cross-replay refuses |

Drift census against the recorded sequential golden (fresh answers are samples; this is not an identity check):

| Pair | Items identical (of 53) | Same existing theses linked |
|---|---:|---:|
| golden ~ serial trials | 27, 31, 34 | 37, 39, 40 |
| golden ~ parallel trials | 29, 30, 30 | 39, 42, 43 |
| serial ~ serial | 27, 29, 30 | 36, 37, 40 |
| parallel ~ parallel | 26, 27, 28 | 34, 38, 39 |
| serial ~ parallel (9 pairs) | 25–32 | 35–44 |

Parallel trials sit inside the serial trials' own spread. The per-item spread comes from the extraction model's
sampling, the same in both modes.

## Robustness

- Two Jev requests in parallel-2 failed without a reply (connection error) and succeeded on the study transport's
  retry. The product's Jev client did not retry a dropped connection; it now makes up to three attempts on a
  connection failure or a 429/529, like the OpenAI client, and none on any other status.
- A failed earlier item still accepts no later handover; queued early work is cancelled and running calls drain
  (offline tests on real storage). A partially processed day resumes only against its manifest when run in parallel.
- The spend cap is checked after each committed item; in parallel, in-flight early requests can pass it by at most
  the worker count's calls. The product cap counts archived calls; a retried attempt whose reply was lost is not in
  the archive (true of the OpenAI client before this change, and now of the Jev client, about $0.0002 a retry).

## Budget

New study journal: 836 provider attempts, two failed attempts held at their reservation; conservative accounting
$1.712 of the $4.00 cap; $0.467 at published rates for the six trials, plus $0.09 for the product CLI run.

Files: [plan](../../../docs/research/2026-10-26-e2e-parallel/plan.md), [summary](live/summary.json), per-trial
`live/<trial>/result.json` (timings, call events, runner events). SQLite ledgers and archives stay on disk
(`*.sqlite` is ignored in this folder) and are listed in the data manifest.
