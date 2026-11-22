# Claude's marks on the July test, written before the blind reader (`reading-rule.md`, sha256 cc876b60…)

Run: `poc/data/july-link-test-2026-11-21/` (send-summary.json: complete, $0.0689 spent of $0.15, 39 provider attempts, nothing refused;
every sequence comparable; every v9 and v14 judgement a fresh call; "v9 reads v14" (`first_is_bullish`, seq 148) committed in all three
linked sequences, no other link). Every answer was read in full (`all-answers.txt` there). Reference points: Q1 total $81.6B, Q1 Data
Center $75.25B, Q2 total guide $91B; the C floor is $6B.

## 07-12 answers, marked line by line

| Sequence | v14 (total) | v9 (Data Center) | A | B | C (annual room; comparable quarters) | D | Meets |
|---|---|---|---|---|---|---|---|
| control-1 | ~$411B ($216B base x 1.905, the mean of Q1 85% and the Q2 96% expectation) | ~$370B: a $356B run-rate (75.25 + 83.7 + 93.3 + 104.0) raised by an unsized ~$14B for the acceleration comment, visibility and wallet share | yes | yes, with a note: the uplift is disclosed with its reasons but not sized; it moves no rung and C holds without it ($356B) | $41B; Q2 $84B < $91B | n/a | **A–C yes** |
| control-2 | ~$412B ($216B x ~1.91) | ~$405B: the $357B run-rate raised by ~$48B for the $1T two-year visibility, "discounted rather than taken in full" | yes | **no**: the uplift that sizes the result (13%, across the rung boundary) has no derivation from the material | $7B: passes as written; quarters Q1, Q2 within; (beside the mark: the implied second half, $245.75B Data Center against $239.4B total, puts the segment above the whole) | n/a | **no** (B) |
| control-3 | ~$411B (as control-1) | $390–395B: Q1 75.25 + Q2 ~84 "with some allowance", then "strong sequential growth" unstated on 07-12 | yes | **no**: the second-half growth that sizes the result is not stated, so the arithmetic cannot follow from stated inputs | $16B at the high end: passes as written; (beside the mark: implied second half leaves the rest of NVIDIA about $2.6B against $6.35B in Q1 alone) | n/a | **no** (B) |
| linked-1 | ~$410B ($216B x ~1.90) | ~$378B = v14's $410B x 92.2% (75.25 / 81.6) | yes | yes: 410 x 0.922 = 378.0; the steady-mix assumption is disclosed and taken from the reported quarter | $32B | yes: committed at 148; v9 computes from v14's forecast | **A–D yes** |
| linked-2 | ~$400B (Q1 85% growth carried on the $216B base, "around $400B") | ~$356B run-rate (75.25 + 83.7 + 93.3 + 104.0), checked against v14: "below the whole and implies about an 89% share" | yes | yes: the run-rate arithmetic holds; v14's ~$400B follows from 216 x 1.85 | $44B | yes, as a stated bound (the answer states the segment must sit below v14's ~$400B and checks the share); not used in the calculation | **A–D yes** (D as a stated bound) |
| linked-3 | ~$387B (Q3 $101.5B, Q4 $113.2B at 11.5% sequential) | ~$356–360B = v14's $387B x 92%, plus a ~$4B unsized uplift | yes | yes: 387 x 0.92 = 356.0; the uplift is immaterial (1%) | $27B; v9 gives no quarters on 07-12 | yes: computes from v14's forecast | **A–D yes** |

## The window, 07-10 to 07-12 (harm checks)
- **First-attempt refusals:** none in any sequence.
- **Grounding errors** (the rule's two examples): none found. Linked v9 answers translate Bloomberg's $393B total-revenue projection
  into a Data Center figure and say so ("not a direct Data Center consensus", "translated at ... 92%"); none calls it a Data Center
  consensus. v14's own forecasts are called "the current v14 forecast" or "the dependency forecast", never a market estimate.
- **The market figure:** delivered to v9 and used as its reference in all three linked sequences on every day; in the controls v9
  states that no Data Center consensus is supplied and uses the Q2 guide (no self-made reference in the window, either arm).

## Verdict by the rule as written
- Linked meeting A–D: **3 of 3** (2 of 3 without linked-2, whose D rests on "a stated bound").
- Controls meeting A–C: **1 of 3** (control-1).
- No added refusal; no new material grounding error.
- **PASS.**

## What the verdict rests on, and what it does not show
- **It turns on B for the controls.** Read leniently (a disclosed judgement uplift counts as supported), control-2 and control-3 also
  meet A–C, two or more controls reconcile, and the result is **inconclusive**. As written ("each assumption that materially sizes the
  result is disclosed and supported"), control-2's unsized $48B and control-3's unstated second-half growth fail it.
- **The stored contradiction did not recur on the annual figures.** In the stored run, 07-12 had Data Center $400–410B against a total
  of $387B; in all three fresh controls the total rose to ~$411B on 07-12, so the annual Data Center figure sat below it. The
  remaining control contradictions are in the second half (control-2's segment above the whole, control-3's $2.6B for the rest), which C
  as written does not catch because v14 states no second-half quarters.
- **Coherence is not accuracy.** Two linked answers take v14's forecast times the Q1 mix; they inherit v14's growth assumption.
- One window, one pair, three days; the market figure was in hand for the total from the start.
