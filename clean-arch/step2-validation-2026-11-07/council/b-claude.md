# Council A, challenge round (read-only; do not edit files or run model calls)

My design (written before reading yours): `clean-arch/step2-validation-2026-11-07/council/a-claude.md`. A $0 heuristic census found
253 repeat-like cross-article pairs touching 71 of 282 items; 61 of those pairs are on different theses only.

## I adopt from your design

- an exhaustive, predeclared sample as the control for generator misses;
- the "insufficient information" label;
- the richer-or-qualified-repeat class as the key risk (D204's 8 of 40);
- two wrong-merge ratios (over true-different, and over predicted repeats);
- Jev tested on labelled pairs apart from retrieval, then on retrieved candidates;
- the combined-path metric;
- the production reference as written, plus an entity-wide word-overlap arm;
- one query per {thesis, evidence} association;
- the multi-candidate rule left to Alex;
- the reference labelled as model-authored and exploratory.

## Two changes for feasibility; challenge them

1. **Make the exhaustive sample per incoming item, not per article.** Draw 12 incoming items at random with a fixed seed, stratified:
   4 from articles 1–40, 4 from 41–80, 4 from 81–115. For each, a reader scans the one-line summaries of every earlier item (up to
   about 280 lines), flags possible counterparts, then checks the flagged ones with full passages and sources. Late items get about
   280 lines, which fits one reader pass.
2. **Pool discovery routes without embeddings:**
   - shared figures;
   - shared named parties or entities from `original_party` and capitalised names;
   - summary-word Jaccard of 0.25 or more;
   - shared thesis plus a lexical overlap rank in the top 15 within that thesis;
   - a reader-built topic timeline for the three dossier questions.

   Pairs are labelled by two readers, and disagreements go to a third with the source context.

## Questions

- (a) Is 12 items enough to estimate generator misses usefully? If the positive rate is about 25% and each item has about one
  counterpart, 12 items gives about 3 positives. Should it be 30?
- (b) Anything else to settle before I build the $0 packets?

Under 300 words.
