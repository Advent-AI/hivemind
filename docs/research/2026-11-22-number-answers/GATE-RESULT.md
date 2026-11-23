# judging-v13 $0 gate: PASS (council round 46ad, 2026-11-22; D729)

**Verdict:** GATE PASS STANDS (`codex-r46ad.md`).
- **Gate run 26** (`gate-run26.txt`, fixtures in `gate-run26.fixtures.json`): 87 of 87 items pass, identically under PYTHONHASHSEED 1 to 3.
- **Mutants** (`mutants.py`, `mutants.log`): 47 of 47 caught; the unmutated control passes.
- **The rendered request** (`render_v13.py`, `render-r1.*`): one stored family (old-2, 2026-09-20) is rendered, with system text 4,373
  characters and 237 evidence items. A conforming answer passes the schema and every check.

## What the gate shows

- **The five stored defects:** each is caught by its named check, for its own reason:
  - a segment quarter above the company quarter (C3);
  - two Q3 bases (C4);
  - an unknown-overlap addition, shown with its alternate and the boundary it decides (recorded);
  - a scope conversion with no stated assumption (C8);
  - a trim across $40B (recorded, definite).
- **The self-made reference:** refused (C5, C10). The request no longer shows earlier forecasts (D728).
- **The frozen gold's reasoning stays expressible:** q01, q02 (paired scenarios), q19 (with the per-unit identity) and q22 (per
  scenario on q01's published range).
- **About 80 relabelling and routing variants found by the council are refused,** each kept as a gate item.

## How it got there

Design v1 to v10, then council rounds 46 to 46e (READY on v5) and 46f to 46ad (gate reviews). The run history:

| Run | Items | Outcome | Main change after it |
|---|---|---|---|
| 1 | 28 | FAIL (G3) | the per-unit identity added (a general identity, not fitted to the case) |
| 2–6 | 29–41 | pass, council FAIL | fixture faithfulness, bound direction, same-base, earlier-forecast authentication, scenario rules |
| 7–26 | 46–87 | pass, council FAIL until 46ad | scenario derivation, value-determining dependencies, operand counts, signs, base sensitivity at one point per figure, open and closed bounds everywhere, one recomputed result for checks and publication, change detection by member |

**Structural rules that closed whole classes:**
- code derives every relation from the calculation graph and the passage text, never from the answer's own declarations;
- scenario membership is derived along the whole path;
- earlier-forecast status comes from the basis, not the label;
- one recomputed result governs every check and the published amount;
- open and closed bounds are carried through all arithmetic.

## What the gate does not show

- **How a model uses the format.** That is the paid gate's question, registered in D725: joint against separate on the three draws'
  09-20 pair, plus O, S and E singletons, 36 calls, read blind against the sources.
- **A model can always state a number as its own estimate.** Estimates stay visible and boundary-deciding ones are flagged, and the
  blind readers judge whether each is supported.
- **Production lifecycle:** members closing or opening, and families changing.
- **The product request builder and the sender:** both are build work before the paid gate.

## Before the paid gate

1. Build the sender: stored families rebuilt byte for byte, the v13 request, the strict schema, retry once, unresolved after two
   refusals, a ledger at Alex's ceiling.
2. Build the blind reading packets.
3. Rehearse everything at $0.
4. Council review.
5. Alex names the ceiling: estimated $0.2–0.4 for 36 calls.
