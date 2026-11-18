# The slice (D450): one fresh day through the wired path, live — reading (2026-11-13)

**Answer: the wiring works live.** Both draws completed (`poc/data/clean-e2e-slice-2026-11-13/`: clean `s1`, production `sp1`, both
2026-07-01, launched 05:31:38, ended 05:39:40); every component ran with real sends on one shared ledger; no stop, no overrun, no refusal,
no retry; 60 ledger lines, every one attributed to its component, summing to the ledger's spent exactly. A wiring check, not a draw and not
evidence of quality (WIRING-DESIGN.md §G).

## Spend and time

| component | time | attempts | ledger charge | archive tokens at `model.PRICES` | note |
|---|---|---|---|---|---|
| Step 1 (c8, 13 items, sequential) | 7 min 23 s | 13 | $0.1324 | $0.1324 | equal |
| Step 2 (embeddings 1, Jev 22) | 3 s | 23 | $0.0110 | Jev $0.0036 | Jev charged at three times its tokens, embeddings likewise (5,874 tokens) |
| cases | 1 s | 0 | 0 | — | 2 cases, equal to the theses the trace opened |
| ladder step (pass 1) | 16 s | 2 | $0.0021 | $0.0024 at the full input rate | the ledger counts cached input at its share |
| judge | 18 s | 2 | $0.0019 | $0.0021 at the full input rate | same |
| production v118 (16 workers) | 41 s | 20 (LLM 15, Jev 5) | $0.0119 | $0.0150 at the full rate, Jev once | same |
| **total** | | 60 | **$0.1593** | about $0.152 at `model.call`'s formula | |

Spend under D439: $7.11 before, about $0.15 now (ledger $0.16): **about $7.26 of $40**.

**Projection for the full run** (an estimate from this day's per-item rates and the stored runs, labelled as such): Step 1 about $0.010
an item → about $2.5 a clean draw (243 items), sequential about 2 h 20 min a draw; Step 2 about $0.36 of ledger a draw (the stored u1);
the ladder step three passes about $0.04 a draw; the judge about $0.14 a draw (Stage B); production about $0.45 a draw (q1–q3). Three of
each: about **$10.4 of ledger**, inside $15.00 − $0.16.

## What each component produced (read by Claude, every answer)

- **Step 1** (13 answers beside their articles): two theses opened, the same two matters the stored draw u1 opened that day: the amount of
  credit support NVIDIA will have extended to AI cloud partners at its next annual report (from NVIDIA's own announcement), and whether
  NVIDIA will guarantee OpenAI's Ohio data-centre lease by 2027-12-31 (from The Information's report carried by moomoo). Seven evidence
  items link to them (the announcement, Sharon AI and Firmus as first partners, the CoreWeave $6.3bn backstop, the later $3.5bn lease
  guarantees, the equity stakes, the CFO's blog post). The other articles (Intel's $5bn stake and Xeon 6 choice, Valar's nuclear data
  centre, Wistron in Texas, NN's liquid cooling, Palantir and Nemotron, Verkada, an RTX 5090 price piece, an agentic-RL blog post, Burry's
  bets) opened nothing and their statements are unlinked, as the standard's "lean cautious" asks. One field to log: the Ohio item's
  original party is "NVIDIA" for The Information's report about NVIDIA (the known original-speaker class), not a wiring matter.
- **Step 2:** 23 records, 20 new groups, 3 repeats, 0 refused, 0 pending, 0 unresolved links.
- **The ladder step:** the credit-support thesis → a figure ladder (USD, five bands from below $1bn to $30bn and above, the lower end
  favourable, due 2027-02-28 at the FY2027 report's expected publication); the Ohio thesis → an event ladder (signed by 2027-12-31 against
  formally abandoned; the amount marked not judged, one bet per question). Both pass the step's checks at the first request; the
  configuration is the frozen one (`clean-ladder-stage-a d3b4a5f696c7cc82`).
- **The judge:** credit support at rung 3 ($5bn–$15bn), implied about $10bn ($6.3bn CoreWeave + $3.5bn lease guarantees ≈ $9.8bn, the new
  model unquantified), every one of the 8 evidence items it cited shown in its request; the Ohio guarantee at rung 3 (unresolved at the due
  day), reading the $500bn as the asset's cost, not the guarantee. Twelve quotes cut by the judge at 400 characters (its frozen
  behaviour).
- **Production:** 13 items, 0 failed; one view (the credit-support amount, due 2027-02-28), judged rung 2 ($1bn–$5bn), anchored on the
  $3.5bn lease guarantees; its five evidence items do not include the CoreWeave backstop. It did not open the Ohio guarantee. One day,
  one draw: an observation of where the two systems differ, not a comparison.

## What the slice does not show

The ladder step's passes 2 and 3; a draw that opens many theses; the judge over many days (the due-day guard, changes, dependencies);
Stage A's and Stage B's readings; any quality line. Those are the full run's (WIRING-DESIGN.md §E).
