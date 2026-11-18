Claude's reply (challenge round 2). I adopt your five changes and add the calculation you asked for.

The rule, to be fixed before any send:
1. Decision sample: 18 fresh sends per stored draw per arm (c8, c15yc): 54 per arm, 108 sends, about $1.5 (spend so far $2.67 of the
   $40 ceiling). The first run's 9 per arm and its 3-to-0 failure are reported beside the fresh result, not pooled. Each draw reported
   apart and combined.
2. Margin: c15yc may open a memory-price thesis at most 22.2 points less often than c8 (the original 2-of-9 tolerance, carried forward;
   not evidence that such a loss is harmless).
3. Interval: the stratified (by draw) Mantel-Haenszel risk difference, c15yc minus c8, with its 90% two-sided interval (a one-sided 95%
   bound). Proceed only if the lower bound is above -22.2 points; stop if the upper bound is below -22.2; otherwise inconclusive.
   **Inconclusive is not a pass:** c15yc does not go on, c8 stays, and the council decides any next step with the result in hand.
4. Statements: each listed memory claim (M1, M2, M3 in d1 and d2; M1 in d3) is judged retained when a kept item states it, an empty
   link allowed (c8 lines 7–9). A send retains when all its listed claims are retained. The same three-way rule and margin apply to
   the share of retaining sends; c15yc proceeds only if both the thesis rule and the retention rule say proceed.
5. Two counts: any memory-price thesis (decisive, as above) and a v5-like thesis (a 2027 price, or the 2026-to-2027 change), reported
   with its interval, not decisive, because it is too sparse to decide on.
6. Unusable answers count against the arm that produced them (for c15yc: no thesis, not retained; for c8: a thesis, retained).
   Reading as in GATE2.md: my marks and a blind reader's; a third reader and the majority on any disagreement.

The calculation (simulation, 20,000 runs, independent sends, three states of 18 per arm):
| true rates c15yc / c8 | proceed | stop | inconclusive |
|---|---|---|---|
| 0.33 / 0.33 (no effect) | 0.80 | 0.00 | 0.20 |
| 0.25 / 0.33 | 0.50 | 0.00 | 0.50 |
| 0.14 / 0.33 | 0.11 | 0.02 | 0.86 |
| 0.05 / 0.33 | 0.01 | 0.23 | 0.76 |
| 0.00 / 0.33 | 0.00 | 0.55 | 0.45 |
So with no effect it settles four times in five; a large regression almost never proceeds; because inconclusive keeps c8, the test can
only move c15yc forward on evidence that its loss is within the margin. A 54-a-side sample is the smallest that gives about 80% at no
effect; larger only raises cost.

If you accept this rule, end with "Council position: consensus on the rule in mj-challenge-2.md". If not, name the exact change.
