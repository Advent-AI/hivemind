# Decision council after calibration (Alex, 2026-11-08: "你跑council loop review 然后决定下一步怎么修改"). Read-only

**The calibration ran, and its falsifier fired.** Data: `poc/data/clean-step1-unfiled-2026-11-08/probe-r2-review/`
(`disagreements.json`, `adjudication-C1.json`, `adjudication-C2.json`); script `tally_calibrated.py`.
- Readers A (Codex) and B (Claude sonnet) split on 52 items, systematically: A says bet where B says small (18 of 19), and A says
  should-be-filed where B says fine (32 of 33).
- Two blind adjudicators were given an explicit rubric quoting §3 to §6 and D371, and did not see the first readings: C1, a fresh Codex,
  and C2, Claude opus. **They agree on 17 of 52.** Each sided with its own model family.
- The split is a family-level threshold on "how big is big", concentrated on:
  - FCF as a card of its own, separate from revenue and margin;
  - whether Q1 cash-flow and cash-balance figures should be kept (D371) or dropped;
  - partner, supply or feature theses (Nemotron at Palantir, liquid-cooling supply, the quantum decoder).
- Calibrated tally (agreed items, adjudicator agreement, else the majority of four, else unresolved):

| | k6b | u1k | u1k+u3 |
|---|---|---|---|
| Should-be-filed | 6 | 3 | 3 |
| Small or duplicate | 4 | 3 | 4 |
| Unresolved (unfiled / theses) | 5 / 3 | 7 / 4 | 5 / 5 |

**My proposed decision.**
1. **Next modification: carry u1k to the dev forward run.**
   - u1k is the D371 contradiction removed, with nothing cut. The request now contradicts Alex's D371 ("收入和财务这边对于当下，未来应该都是需要track 的"), and AGENTS §6 says a contradiction with the standard or a decision is a defect in the request.
   - Probe 2 shows no calibrated harm: small or duplicate 3 against 4. Ruler noise is +1 span in 48 answers. Filing is equal or better
     depending on the reader.
   - AGENTS §7.3 ("a version that already meets the goal is not dropped for a stricter rule a later review added") applies: what u1k
     was built to fix, the contradiction, is fixed, and nothing measured turned from right to wrong beyond one span.
   - A fixed-state probe cannot show the cascade: early value-quantity theses giving later results a home. Only a forward run can.
   - The run: forward from empty over the 115 dev articles, DeepSeek Flash high, about $1, then source-backed library review, against
     Alex's existing Step 1 line (helpful at least 197, noise at most 40, small at most 3, fragments 0), with a second draw if at the
     line. The test set is touched only after a pass, once.
2. **In parallel, take the threshold to Alex.** Put 6 to 8 boundary cases where the families split, each with its article, before him.
   His answers become recorded decisions that calibrate every future reader. AGENTS §7.1: the ruler is Alex's, never a model's.

Challenge:
- (a) Is carrying u1k to the forward run justified, or is it a run used to try a fix?
- (b) Is the threshold question the right one for Alex, and is it framed without leading?
- (c) Is there a better next modification?

Under 300 words.
