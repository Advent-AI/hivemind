# Full-configuration review: Claude's own judgement, written before Codex reads (2026-11-08)

## What the final configuration would be
- **Step 1 prompt** = c7 (`arms/c7-*`), carrying:
  - c2's figures and condition bullet;
  - c4's unlinked keep (D383) and valuation row (now D385);
  - c6's "do not fold another party's statement";
  - c7's closed set of four opening reasons (D384), with `opens_as` and `settled_by`.
- **Settings:** DeepSeek Flash, high effort, 64k output cap, JSON mode.
- **Runner:**
  - keeps every returned item;
  - checks every figure value is quoted;
  - retries a format failure or a cut answer once (D380).
- **Step 2:**
  - full passages;
  - own-text search for unlinked or figure records;
  - figures out of comparison text;
  - the clean Jev piece criteria ("main statement");
  - later linking with the tightened criteria and the judged-pair ledger;
  - manifest-position numbering.

## Open issues I see
1. **c6's not-folding rule** has 2-draw evidence. It may split context that belongs together. Its claimed gain (no bundle cascade) is
   measured on a rare event (1 in 9 samples).
2. **The clean Jev criteria and the later-linking criteria** were tuned and judged on the same cases. Later linking was never checked for
   missed links: 242 to 325 pairs judged, 1 to 4 linked. It may be far too strict now.
3. **c7 keeps more unlinked items** (test: 52 of 63) and showed noise 13 on test. If the unlinked pile carries noise, D383's "keep" makes
   it permanent. The closing check is supposed to drop noise whatever the linking; is it applied as strictly to unlinked items?
4. **D382 against the gold's class A must_open** (test: FY2028 data-centre revenue): a by-design miss. It should be stated in the
   acceptance criteria, not discovered after.
5. **The reference mapping by greatest overlap** can mis-map bundled records; the line-1 score covers mapped records only.
6. **The question measure** used one reader per run.
7. **Prompt size:** system 15.1k characters against K6b's 13.5k. The growth needs its reason per §6.

## What I think should happen before freezing
- A source-backed review of the c7 request against the standard and D380–D386, clause by clause, including the unchanged K6b text it now
  sits beside.
- A missed-link check for later linking, on a sample of judged-false pairs read against the source.
- A check that unlinked items obey the closing check's not-kept rows: read the c7 dev unlinked pile when the run ends.
- Then freeze, and fix the acceptance protocol **before** choosing articles: a fresh NVDA slice, its size, readers, criteria, and the
  by-design misses stated.
