# Council round 7: Flash draw 2 and the final judgement (read-only)

**Flash draw 2** (`gold-k6b-flash-d2/`, inputs byte-identical to draw 1): 115 of 115, 0 failed.
- Gold: helpful 197 of 234, core 85 of 86, items 265, not-kept 38, unmatched 21.
- Draw 1 for comparison: 205 / 84 / 282 / 40 / 28. Final library 18 against 25.

**Blind library reads** (`library-answer-flash-d2-r{1,2,3}.json`; both draws in one packet):

| | Small | Fragments |
|---|---|---|
| Flash d1 | 2 / 4 / 5 (the round-6 packet gave 3 / 3 / 3; median of six reads: 3) | all 0 |
| Flash d2 | 1 / 3 / 4 (median 3) | all 0 |
| Luna medium (six reads) | 0 / 1 / 0 / 1 / 1 / 1 | 2 of 6 reads flag 1 |

The recurring small theses are the Intel tie-up, orbital data centres, AI-RAN, lidar policy and US production expansion. They are
new initiatives with no stated scale. Alex allowed opening a topic before its impact is known ("no need to be very strict in opening
… just don't open 'noisy' thesis"). The readers' rubric treats them as small. I do not plan to tighten the prompt beyond Alex's
instruction to chase the readers.

**Proposed conclusion for Alex:**
- **Pass line, Flash:**
  - Helpful passes in both draws (205, 197).
  - Fragments are 0 in every read.
  - Small theses sit at the line (median 3; individual reads range from 1 to 5).
- **Pass line, Luna medium:**
  - Small theses pass (median 1).
  - Fragments are flagged in 2 of 6 reads.
  - Helpful is 201.
- **Noise:** Flash 38–40 against production's 30–34. Flash removes reporter framing (15 → 2), generic views (7 → 2) and adjective
  quotes (5 → 0) against Luna; product detail without scale (10) is the remaining shared class and the next target.
- **Recommendation:**
  - K6b on Flash high as the Step 1 configuration candidate.
  - Next: the product-detail noise class, a schema-failure policy, then one validation on the 30 held-out test articles and adoption
    into PRD §12.

**Challenge:**
- (a) Is "small at the line, median 3" an honest reading of the pass line, or should I report it as not robustly met?
- (b) Is anything in draw 2 a regression I should report?
- (c) Do you agree with the next steps and their order?

Under 350 words.
