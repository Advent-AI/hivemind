# Tries toward the comparison's criteria (D674)

**The criteria:**
- D665's verdict on the frozen instruments: `stage0/verdict-rule.json` and `stage0/census/matters.json`. A **practical lead** means
  a − b ≥ max(3, ⌈0.15·N⌉) and a ≥ 2b under both countings, with every guardrail exercised and passing.
- The hard checks:
  - D400's code-decided parts;
  - Step 2's three lines.

**Rules for every try:**
- The ruler and the instruments never move to make a try pass.
- A try that does not pass goes through the council loop on its traces before the next one.
- Each row records the try, its result, and what it taught.

| # | Date | Try | Result | What it taught |
|---|---|---|---|---|
| 0a | 2026-11-17 | Slice 1 (07-01..07-07) | Old system complete. The new system stopped at the ladder: a $10 guard against about $10.7 of concurrent astra reservations | Size every guard for the concurrent worst-case reservations, not the expected spend |
| 0b | 2026-11-17 | Slice 2 (07-01..07-03, new guard $25) | All six slice checks pass after two of the checks were corrected (copies merged by the old system; day-end judgements carry their day) | Read a failing check to its first differing line: both failures were the check's error, not the system's |
| 1 | 2026-11-17 22:36 | Full comparison, try 1: three draws of each system, 07-01..09-20, frozen instruments | running | — |

| 2026-11-19 | Release comparison D665: old poc-v118 against new clean c8, 07-01 to 09-20, scored 09-07 to 09-20, N = 32 | **DIAGNOSTIC (5 draws): the new system loses.** Served: new 2–3, old 10. a = 0, b = 7–8. Controls pass. Even a perfect new-1 gives a = 1, b ≥ 6. The new libraries miss the core revenue, margin and capex matters. | new-1's Step 1 redo (about $21, 17 h) was wasted: the failure was a sampler format slip on one item, and an item-level re-send fixed it for $0.12. Re-send the single failed request before any full redo. |
| 2026-11-19 | Council on the comparison itself (D676) | Measurement sound. Loss = D382 figures + Step1→ladder bundled-question loss (27/60, 19/60). Ceiling if repaired: new 5–6 vs old 10, no winner, never a lead. Keep the old system. | Compute the attainable verdict before any paid comparison; search the decisions (D432, D489–D505) before proposing a fix. |
| 2026-11-19 | One-outcome closing check (D676's mechanism 2, inside D382) | Fixes two-period bundles (capex 4/4 sends single-year, laddered) but not two-outcome deal bundles (Anthropic, Hugging Face): line 1 fails, at most 3 of 6. | A sentence fixes a period split; a deal's completion and size stay bundled; the split belongs where the deal is judged (a later step), not in Step 1's wording. |
| 2026-11-19 | $0 census of the 14 rule-allowed matters the old system misses | Lost in three places: bundled questions dropped by the ladder (capex 2026/27, DRAM, Hugging Face); opened and laddered but framed beside the analysts' matter (residual-value amount vs the Goldman/Blackstone signing; Groq review closure vs enforcement; neocloud commitments in one draw); never opened (worldwide semis, investment commitments). | No one-sentence fix reaches a pass. A pass also needs a full comparison (about $110), above D439's $40, so it is Alex's call. The loop stops here. |
| 2026-11-19 | Proposed a cents probe of fix 1: Step 1 resent with the dropped theses removed from the open list | **Council HOLD** (`council-g-codex.md`): D677 bars paid sends with no cents exception, and the probe needs a matched control (each article sent with and without the dropped theses, the same day). | Any paid probe waits for Alex to reopen D677. If he does, the design is the matched pair. |
| 2026-11-19 | Merge test (D678–D680): old opens questions, c8 files under them, the frozen judge answers; 70 articles × 2 draws, hybrid and control arms, $2.13 | **Registered test not passed.** Delivery 4/4, talks stay talks, 4/4 hybrid answers supported by both readers; missed P2's proxy clause (old misses it too) and V (control v47, judge fork on 09-16, reconstruction effect not ruled out). Capex rests partly on 09-06 history; the Anthropic answers wholly on c8 | Read census numbers through `census/numbering.json`; a pre-registered line is scored as written, never relaxed after the result; the merge's value lies in matters old misses, which this test could not reach |
