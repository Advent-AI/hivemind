# Council B on probe 1. Challenge the results before the next step (read-only)

Files: `poc/data/clean-step1-unfiled-2026-11-08/probe-r1/` (`records.json`, reader answers); scripts `score_probe.py`,
`tally_readers.py`.
- 192 sends, $2.51. 3 format failures, all in the u3 family: DeepSeek added an extra `tier_note` field.
- Two blind readers judged 189 answers under shuffled labels. Their thesis and unfiled counts came out identical (the notes differ;
  they are the same model family, so not independent); wrong links differ.

| Sum of 3 draws | k6b | u1 | u3 | u1u3 |
|---|---|---|---|---|
| Ruler helpful | 69/96 | 69/96 | 66/96 | 70/91 (1 failed) |
| Ruler not-kept spans kept | 11 | 16 | 12 | **18** |
| Unfiled | 34 | 42 | 46 | 36 |
| Readers: unfiled that should be filed (existing + should_open) | 15 | 16 | 22 | **6** |
| New theses (bet / small / duplicate) | 27/2/0 | 37/4/1 | 28/3/0 | 41/4/0 |
| Wrong links (reader A / B) | 3/0 | 7/4 | 7/4 | 4/2 |

**Read by hand:**
- At the stored states where the revenue home clean-11 is open (d1-40, d1-57), u1u3 opens a gross-margin and profitability thesis in
  3 of 3 draws. clean-11 asks about Vera Rubin shipping and revenue. Section 3 names gross margin as a big matter, so this is not a
  duplicate.
- d1-62: dividends are still unfiled, as the standard intends.
- d1-66: valuation is unfiled; an EPS and margin thesis opens in 1 of 3 draws.
- At the empty state, **k6b also opens** data-centre revenue and gross-margin theses for article 57. The test-set seq 2 miss is partly
  chance.
- The noise increase is mostly empty-85 (nk 4 → 9; u1 alone 11): another company's matters (Hesai's lawsuit, Hesai's cost cut) kept
  under an empty library, not financial lines.

**My process error.** u1 also cut two sentences to stay length-neutral. One of them is "A number, date or headline alone is not enough
to open a separate thesis…", and the other is the role paragraph's restatement of the unfiled rule. So u1 is not one lever, and the
cuts may cause the extra keeping and noise.

**Proposed probe 2** (about $0.70): **u1k** (the D371 line added, nothing cut, +372 characters with a written reason) + u3, against
u1u3 and k6b.
- Cases: empty-85, empty-62, d1-40, d1-57, empty-57, d1-38, d2-66 and guard d1-113.
- 3 draws.
- If u1k+u3 keeps the filing gain without the noise, it goes to the dev forward run. If neither does, stop and re-diagnose.

Challenge:
1. Is the u1u3 gain real (6 against 15), given that the readers are not independent?
2. Is the decomposition right: only the combination works, neither lever alone?
3. Is probe 2 the right isolating step, or should the dev forward run go now?
4. Is anything overfitted?

Under 300 words.
