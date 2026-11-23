# Deep council on priorities (Claude's reflection, written first; 2026-11-09)

Alex: "感觉现在一直在修一些mknor的原地打转，你是不是要思考下现在具体还差什么high priority big impact 的需要做？还是要收尾step-".

## Where the clean architecture stands

**Step 1 (c8, D387)** is accepted on 50 fresh articles:
- helpful 132/139, core 83/83;
- wrong theses 1 of 10;
- dev ×3 helpful 214, 211 and 212 of 234.

**Steps 2 and 3** (search, Jev comparison, grouping, later linking) are built in isolation:
- search 141/143;
- clear wrong merges 1/57;
- they are not integrated with production storage.

**Step 4 (judging) is not built** on the clean path. Its input selection, output, timing and decision method are open design
questions (PRD §7, §10.7).

**Where the product is judged.** The phase goal (docs/prd/10-filing-phase.md §1) is the final judgement on the frozen judgement ruler:
reader B, 22 seeds plus the Ohio question, at the window end 2026-07-14. No clean-path number exists there.

## What the last day went into

**The D388 line** (§§48–58): arms c9, c10a, c10b and c11, then four rounds of a focused call. It cost about $4 in sends and many
council rounds, all for one question (q23) of 23.

**Results:**
- the focused call opens Ohio in 36 of 36 draws;
- after D389 (5% of profit) and D390 (a plan is undertaken once a deal is signed), it is right on every predeclared case;
- each round, one neighbouring article about the same programme still opens wrongly.

The 32 probe cases have tuned ten configurations.

## My reading

1. **We broke "end to end first" (AGENTS §5, §7.2).** We tuned one step's sub-case without knowing whether the clean system judges
   any of the 23 questions well, or whether Steps 1–3's gains reach the judgement. AGENTS §7.2 says "Before a phase targets one step,
   the upside of that step done perfectly is measured where the product is judged". For Ohio that upside is at most 1 of 23
   questions, and we never measured it.
2. **The highest-impact gap is the missing Step 4 and the missing end-to-end run.** Link clutter, the revenue-share thesis, lidar and
   Ohio cannot be ranked by impact until judgements exist. Production already has a frozen judging step (judging-v5, D354), which a
   port can reuse (AGENTS §10: port the mechanism, leave the patches).
3. **Close Step 1 now:**
   - c8 stays frozen;
   - the focused D388 step is recorded as a candidate, not adopted, with its results and D389/D390;
   - Ohio stays an open defect, to be re-ranked once judgements exist.
4. **What we circle on.** Judgement boundaries (size, signed status, programme versus deal) that the standard leaves open, fixed one
   probe case at a time. The rule that would have stopped it: after two rounds on one class without convergence, measure the class's
   end-to-end impact before a third.

## Proposal

The next phase is the clean system end to end on the gold window, July 1–14:
- Step 1 c8 forward, then Steps 2 and 3;
- then a minimal Step 4 that reuses production's frozen judging on the clean library;
- scored on the frozen judgement ruler against production's stored baseline.

The first test: the 23 questions' judgements at 2026-07-14, clean against production. Each disagreement with reader B is traced to the
step that lost the fact.
