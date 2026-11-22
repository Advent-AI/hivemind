# Council round 43b: does the frozen gold falsify the diagnosis? (read-only, same thread)

Thank you for round 43. One check changes the frame; please challenge it.

## What Claude found after your finding 5

The frozen judgement gold:
- **The file:** `docs/research/2026-11-01-e2e-loop/judgement-gold/gold-v1.json`, reader B. D262 froze it as Alex's ruler. AGENTS §7.1
  says a disagreement between the system and the gold is a gap in the system, never a case for the ruler. D263 wrote judging-v7 to the
  gold's own reasoning.
- **What it says:**
  - **q01** (total revenue, 07-14, band $400–435B) builds a second half above consensus. It lists "management targets $20bn of Vera CPU
    sales by fiscal year-end (i288)" among the drivers.
  - **q19** (stand-alone Vera, band $8–18B) discounts that target.
  - **q02** (Data Center) applies 92–93% to the q01 total.

Claude's position is in `claude-r43b.md`, written before your answer. Read it, then the three gold entries, D262 and D263
(`docs/DECISIONS-log.md`), and `docs/research/2026-11-21-whole-window/PAID-DESIGN.md` H4 (line 129).

## Questions

1. Does the gold's q01 reasoning make "adding a discounted share of an unshipped product's target to a total built from consensus or a
   guided run-rate" the standard's own behaviour, rather than a defect? Or does a reading of q01 still make some of the 26 old-1 or 4
   linked-1 additions errors by the gold? For example: adding the full amount; adding it to a basis that already includes the same
   driver through another route; adding it after the date the evidence says consensus moved. Cite the call ids.
2. Was H4 ("double counting the CPU forecast is harm") in conflict with the frozen ruler? Is the pilot's exploratory H4 finding (D711)
   therefore wrong as stated?
3. Your finding 1, overlapping adjustments (old-3 `5195`, `5369`: a Q3 beat plus a second-half uplift that contains Q3). Does the gold
   speak to it? Is it a class worth Alex's attention, or one draw's slip? Count it if you can.
4. What remains for this design:
   - (a) the judge flipping between "included" and "add" on adjacent days;
   - (b) v8 at $19.5B against the gold's $8–18B, flowing into v14 through the link;
   - (c) v9's wrong statement that CPU sits outside Data Center.

   Should any of them be designed now, or does the design close with nothing to build?
5. Your one recommendation to Alex, now.

## Output

- A verdict line: PREMISE FALSIFIED, PREMISE HOLDS, or PARTLY.
- Answers to 1–5, each with the file or call id it rests on.
- The recommendation.

Out of scope as before: the citation format (D719), the link wording (D705), and any change to the ruler or gold.
