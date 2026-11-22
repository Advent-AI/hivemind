# The version-2 link question: gate PASS by its registered rule; two unsupported links gone, one weak link added (D703, D704)

Run: `poc/data/link-census-2026-11-21/probe-v2-{1,2,3}` (each counted: complete, every job carrying the version-2 texts, equal to old-2
with no link row; D700's ledger: $0.0309 settled for the probe, $0.0575 in all of $0.10, 103 attempts, nothing refused or overrun).
Scored by `read_census.py --v2` against `expected-links-v2.json` (written before the probe's answers): `probe-v2-pairs.md`.

## By the registered rule
- Known positive (v9 reads v14, together): right in 3 of 3; margins 0.03, 0.07, 0.13 (fragile in two).
- W (40, the census's 38 plus the two links across periods with no bridge): no link in any draw.
- F (a growth rate reading an earlier revenue amount with the sign together): none.
- **Gate: PASS.** By WORDING-V2.md §3, version 2 becomes the candidate for the paid design.

## Against the current wording (every pair proposed in some draw of either; "3/3" = proposed in all three draws)

| pair | current wording (census) | version 2 | reading |
|---|---|---|---|
| v9 reads v14 | 3/3 (margins 0.05, 0.09, 0.03) | 3/3 (0.03, 0.07, 0.13) | kept; still fragile |
| v17 (FY2028 growth) reads v16 (FY2027 CPU), together | 3/3 | 0/3 | **removed** (the base-effect risk) |
| v35 (FY2028 total) reads v9 (FY2027 Data Center) | 1/3 | 0/3 | **removed** (no bridge) |
| v21–v9 | 3/3, direction flips (v21 reads v9 twice, v9 reads v21 once) | v21 reads v9 2/3, never reversed | **no flip** |
| v21 (FY2027 growth) reads v16 (FY2027 CPU) | 3/3 | 3/3 | kept |
| v16 (total CPU) reads v14 (total revenue) | 3/3 | 3/3 | kept |
| v2 (all credit support) reads v1 (AI-cloud credit support) | 2/3 | 0/3 | lost (defensible, round 17) |
| v35 (FY2028 total) reads v14 (FY2027 total) | 2/3 | 0/3 | lost (defensible: the outlook bridges the base, round 18) |
| **v14 (total revenue) reads v8 (stand-alone CPU)** | 0/3 (0.47, 0.46, 0.44: below the line) | **3/3 (0.53, 0.54, 0.58)** | **added**: a whole reading a part about 5% of it; the tie-break points the other way (the total carries the full-year estimate) |
| v16 (total CPU) reads v8 (stand-alone CPU) | 0/3 | 1/3 | added once: a whole reading its part |

Proposals per draw: current wording 7, 8, 5; version 2 5, 5, 6.

## What it shows
- The periods clause did what it was written for: both unsupported links across periods are gone, and so is the defensible one
  (v35 reads v14), whose bridge Jev did not credit.
- The tie-break did not settle direction as written: it kept v9 reads v14 at the same thin margins, and it moved v14–v8 above the line
  in the direction it should have refused. A whole reading a part a twentieth its size gives the total little; it also makes v14 a
  reader, so in a paid run the total's own judgements change and the Data Center question reads a changed total.
- Stability improved where the census flipped (v21–v9), not where it was thin (v9–v14).

## Council round 20 (`codex-r20.md`): TAKE VERSION 2 TO THE PAID DESIGN, agreed
- The PASS holds (Codex re-derived both tables, 51 jobs, the ledger and the nine store projections; no invalid draw).
- v14 reads v8 is weak with plausible downstream harm: the total had a direct $393B FY2027 estimate and the CPU card no full-year
  NVIDIA CPU forecast, so the tie-break favoured the CPU question reading the total; the risk is the total treating an uncertain CPU
  forecast as incremental to an estimate that may already include it. Unmeasured: the probe bought no judgements.
- The three sentences changed together; which sentence moved which link is unmeasured.
- Next: version 2 as a separately versioned, reviewed product configuration, then the paid design. No third wording chosen on these
  105 pairs (that would be selection on the probe set).
- For the paid design: keep the whole chain (v9 reads v14, v14 reads v8); prove at $0 that the product version reproduces the probe's
  request hashes and graph; in each paired control sample v14 and v9 fresh from their first affected judgement; per common date show
  which CPU conclusion the linked total saw, how that total compares with its control, and which total Data Center saw; judge Data
  Center against its own sequence's total; report days added by propagation apart; credit reconciliation only with sound arithmetic
  and sourcing.
