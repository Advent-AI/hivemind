# The core problem behind the filing symptoms (2026-11-04, Claude; for review)

Alex: "这些只是类型题，你需要抽象拔高我们现在的核心问题和卡点。这个很重要这样改下去才是对的".

## Claim

The questions are wired backwards. The design (D208, Alex, 2026-10-28) is a thesis tree: driver questions (demand, supply/inputs,
competition/share, pricing, product cycle, policy, capital) are judged from their own evidence, and "root judgements read driver and theme
conclusions, not their evidence". What was built reads the same edges the other way: the root is judged first from its own evidence pile and
every driver reads the root's conclusion. The filing symptoms are this structure's consequences, not wording defects:

1. The root (total revenue) is the only question that must reason from raw evidence about the whole business, so everything that bears on
   the business must be filed there; the fallback sentence (D273: "the company-wide revenue question as the home of indirect evidence") was
   added for exactly that, and the pile follows (its judgements cite another company's or the market's news in 24–44% of citations).
2. Drivers are anchored to the root top-down (Data Center revenue = total × 92%; Blackwell/Rubin = Data Center × 84%), so their own
   evidence matters little, the facts that measure them are not needed by their judgements, and a root error cascades (q02 flips with q01).
3. Facts that measure a driver (Broadcom's AI revenue for custom silicon; a rack price for Rubin revenue) never reach the root as a driver
   conclusion, so the analyst's build-up (market × share → segment → total) cannot happen anywhere.
Every "type" seen so far (Broadcom, Morgan Stanley pricing, NVL72x2, Google backlog, the ecosystem pile) is one of these three.

## Evidence (each re-derivable)

- D208 (DECISIONS.md): "each driver declaring the root it feeds through `dependencies`" and "Root judgements read driver and theme conclusions,
  not their evidence"; build order "bootstrap seeding with dependencies, the judge's 'drivers in force' block, re-placement …". D273: the
  next lever is "specific homes for indirect evidence (D208's driver questions, designed, not built)".
- Seeds (`poc/seeds/nvda-2026-07-01-v2.json`, `src/hivemind/seeding.py` docstring: "the driver's dependency on the root it feeds"): 17
  edges in the frozen ledger, each driver → root (v2→v1, v3→v1, v4→v1, v6→v2, v7→v2, v8→v2, v13→v2, v16→v6, v20→v2, v5→v3 …).
- PRD 06 "Dependencies: reading the arrows": "B depends on A means B reads A's conclusion" (examples: a bank's net interest income depends on
  the policy rate). Code: `judging.build_prompt` shows `store.dependencies_of(view)` (the views this view depends on); `judging.upstream` and
  `topological` judge those first. No "drivers in force" block exists anywhere in `src/` (grep).
- Stored requests of the frozen draw d1 on 2026-07-14: v1's judge is shown no dependency conclusion; v2 is shown v1, v16 is shown v6, v20 v2,
  v5 v3; the day's judging order starts v1, v11, v22, v4, v2 …
- Stored judgements, three frozen draws: v2's implied outcome is computed from the v1 dependency in 13/14, 14/14, 11/14 judgements
  ("the total-revenue dependency implies about $421 billion; × 92.2% ≈ $388 billion"); v20's in 7/13, 2/13, 6/12 ("Data Center dependency
  implies $388B; × 84% ≈ $326B").
- Reader B (the frozen gold) answers q01 bottom-up from driver-level facts (Q1 and Q2 guidance, growth acceleration, SemiAnalysis shipment
  tracking, Rubin ramp and rack price, Vera CPU target), not from a pile of ecosystem news.

## What this implies for the fix (one recommendation, to be reviewed)

Build the missing half of D208 instead of tuning the filing sentence: give each dependency edge one meaning the code reads the same
everywhere (a typed field: a seed edge "feeds" its root; a matching edge "reads" its driver, PRD 06), judge feeding drivers before their root
from their own evidence, and show a root's judge its drivers' current conclusions ("drivers in force", like the theme block, D195) — and
stop showing drivers the root's conclusion. Filing stays as frozen for the first test, so the test isolates the structure.

The one test: the 14-day frozen window (2026-07-01..14), extraction and matching replayed from the frozen draw's archive, only judging
re-run under the corrected flow, three draws; scored on the frozen judgement ruler, with q01, q02, q16, q20 and the cascade read trace by
trace. Judging is frozen (D354) and the seeds belong to the frozen ruler: the edge semantics change in code, the seed file does not.
