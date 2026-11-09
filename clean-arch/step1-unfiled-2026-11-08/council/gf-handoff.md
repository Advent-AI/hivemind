Council B on the unseeded measurement's result (D395). Read-only, fresh reader, under 400 words. Repository /Users/lchingen/hivemind.

**Read:**
- `clean-arch/unseeded-2026-11-10/result.txt` (per question: three unseeded draws beside the seeded Stage 2);
- `MATCHING-v2.md` (the frozen rule, the subset and the predictions) and `adjudication-runs.md`;
- `opened-u1.json`, `opened-u2.json` and `opened-u3.json`, with the matchings `match-u*-*.jsonl`;
- D248 in `docs/DECISIONS-log.md`.

**Facts:**
- Graded subset (q04, q05, q08, q09, q13, q18, q23): unseeded 5, 3 and 4 (mean 4.0); seeded 6, 7 and 6 (mean 6.33). The observed gap
  is 2.33. The prediction was 4–5 per draw.
- Every question the unseeded system opened and had judged agrees: 16 judged, 0 disagree. All nine subset misses are "not opened as
  SAME".
- Judging cost $0.09–0.10 per draw; Step 1 costs about $1.8 per draw.

**My reading of the nine misses:**
- **q04 and q13, 3 misses.** Each draw opens one hyperscaler-capex question, for 2026 or 2027; the ruler has two. D248 says "periods
  of one bet are one question", yet the frozen gold lists the 2026 and 2027 capex as separate must-open entries. That is a tension
  between a decision and the ruler, to record under D373, not edit.
- **q05, 3 misses.** A memory question is opened every time, but broader (NAND, 2026 levels) or about another measure (HBM capacity).
- **q09, 1 miss.** d2 opened credit support at a different check date (2027-12-31), not SAME by the frozen limit.
- **q23, 2 misses.** The Ohio signing question was opened in 1 of 3.

**The report to Alex** (plain words):
- When the clean system opens a question by itself, the judge gets it right.
- The loss is in question shape and in two topics opened inconsistently, not in delivery or judging.
- **Draft recommendation:** put the year-split tension to Alex as a product ruling ("2026 and 2027 capex: one question or two?"), since
  it decides both opening and scoring; do not tune prompts on these cases.

**Challenge:**
1. Is the reading right? Check the openings and matchings yourself.
2. Is "the judge gets it right when opened" overstated? Consider the questions judged and their rung choices.
3. What should go to Alex: the year-split ruling, something else, or the next product step?

**Out of scope:** editing frozen rulers.
