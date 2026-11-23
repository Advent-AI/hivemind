# Claude's reflection (written before reading Codex's)

## Mechanism

1. **Contradiction (D371).** The do-not-open item "one quarter's figures or guidance … Their statements are evidence for the broader
   thesis they inform, or unfiled" (`k6b-system.txt` ll. 93–96) is read as barring the question of the quantity itself (revenue path,
   margin, cash). That contradicts the same section's big-matter list (ll. 84–85) and Alex's D371. In a thin library no such question is
   open, so the company's own results leave through "or unfiled". It hits the test set (earnings season, empty library), and dev d1
   too: Q1 net income, Q1 FCF, FCF and gross margin, not gold-helpful there.
2. **Link misses (misread).** An open thesis covers the item (AI infrastructure spending under GPU demand), and the model concedes the
   error when asked.
3. **Intended drops** (small integrations and investments, hires, valuation, retail prices). These are the standard's own drops; gold
   counts some as helpful (D373 concern). They are not a target.

## Levers, one per arm

- **L1, the contradiction removed at its owner** (section 3's do-not-open item). The item bars a thesis whose subject is one period's
  figure or one capital-return declaration. Such statements inform the question of the quantity they measure (the company's revenue,
  margin, cash or capital spending path, which section 3 calls a big matter, D371): link them to that question, or open that one
  question with them, never one question per line or period.
  - "Or unfiled" is removed for this case.
  - The same number of characters is cut elsewhere (the redundant l. 99–100 line).
  - Source: D371 and section 3. It names no company or metric beyond the value quantities the standard already names.
  - Falsifier: the target items are still unfiled, or new per-line or per-period theses appear.
- **L2, a readback row in the closing check** (placement). For each item left unfiled, name the question an analyst would file it
  under: an open or new thesis covers it, so link it; the question is a big matter, so open it; otherwise it stays unfiled.
  - Source: AGENTS §6 (a test applied to each statement goes at the end of the same prompt); standard §6 (narrowest open question).
  - Falsifier: wrong links or small theses rise. PRD 10 §3 saw a re-check that "recovers some, and misfiles about as many".
- **L3, a required field** (output contract). Each evidence item carries `filing_question`: the research question it informs, written
  before its links. Code does not act on it.
  - Source: the skill's lever ranking (required per-item fields worked: closest_open_thesis).
  - Falsifier: no change in unfiling, or noise up.
- **L1+L2 combined**, if both help alone.

## Probe

- Dev articles only.
- **Targets:** d1 seq 40, 57 and 62 (the company's results and cash), 66 (an analyst EPS estimate), and a link-miss case.
- **Bootstrap:** each financial article also run with an empty before-state, because the test failure was a thin library and the
  standard's case is a new entity.
- **Guards:** d1 seq 22 (hire), 108 (Gradium), 113 (quantum), 21 (shareholder proposal), 6 (Palantir), 29 (debt raise) must not open
  theses; plus two articles with low noise.
- 3 draws per arm, on DeepSeek Flash high, fixed before-states.

**Score:**
- target items filed (linked or opened) against unfiled;
- theses opened, judged bet, small or duplicate with source;
- link correctness by blind readers;
- noise by the ruler.

**Risks of farming:** a rule that names results or earnings, an example from the test set, or a fix that recovers the gold's
small-matter entries. The guard set and the "per line" falsifier test it.
