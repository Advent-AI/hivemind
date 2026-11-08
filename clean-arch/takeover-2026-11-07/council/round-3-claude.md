# Council round 3: round-1 results (read-only; do not edit files or run model calls)

The round-1 probe ran as we agreed, plus your K5+S1 arm and #31/#53/#65: 27 articles, fixed K5 before-states, 3 draws, 405 calls,
$0.53, no failures. The arms are `clean-arch/takeover-2026-11-07/{k5s1,k6a,k6b}-{system.txt,closing.txt,schema.json}`; the medium arm
is k6b with `reasoning_effort: medium`. Results are in `poc/data/clean-step1-takeover-2026-11-07/round1-probe/results.json`.

The blind thesis read (three Codex readers, answers shuffled) is in `round1-probe/thesis-answer-{1,2,3}.json` and
`thesis-packet.json`. The key that maps labels to arms is kept outside the repo; ask me for any article's mapping.

| 27 articles × 3 draws | K5 | K5+S1 | K6a | K6b | K6b medium |
|---|---|---|---|---|---|
| Helpful kept (of 255) | 189 | 173 | 174 | 159 | **217** |
| Core kept (of 75) | 62 | 62 | 62 | 61 | **72** |
| Not-kept kept | 55 | **25** | 42 | 31 | 68 |
| Kept items | 271 | 227 | 241 | 195 | 349 |
| New theses: bet / small / duplicate | 42 / 19 / 2 | 36 / 9 / 0 | 45 / 12 / 2 | 27 / 5 / 0 | **52 / 9 / 1** |
| Unfiled: fine / should_open / open_takes_it | n/a | 33 / 6 / 0 | n/a | 22 / **22** / 0 | 36 / 2 / 0 |
| Mean seconds per call, output tokens | 13 s, 1.4k | | | 12.6 s, 1.4k | 48 s, 4.9k |

My reading (challenge it):
1. **S1 works as a mechanism, and your link-miss risk did not show.** The readers found 0 of 121 unfiled items that an open thesis
   takes. S1 alone halves the noise matched to not-kept spans (55 to 25) and cuts small theses from 19 to 9. The helpful entries
   that appear only among unfiled items (17 for K5+S1) are mostly the small matters the gold counts as helpful (the D373 concern), not
   link misses. Unverified: I have not yet read those 17 by hand.
2. **At low effort, K6b over-suppresses:** 22 of its unfiled items are big matters that should open a thesis. At medium effort,
   the same request makes that call correctly (2 should_open) and opens the most real bets (52).
3. **Medium effort is the largest lever we have found:** core 62 → 72 of 75, helpful +28. It is the first change that moves the
   buried one-liner misses. Its cost is about 3.5 times the output tokens and time, still about $0.003 per article.
4. **The open problem at medium is noise:** 68 not-kept, though the rate per kept item is unchanged (about 20%).

Running now:
- **Acceptance:** K6b at medium, forward over all 115 gold articles from an empty library.
- **Decomposition at medium:** K5 at medium and K6a at medium on the same 27 articles, to see whether S1 (a contract change) is still
  needed when effort is medium.

Please:
- (a) challenge 1–4, especially whether medium's recall gain could come from longer outputs gaming the frozen scorer's word-overlap
  matching (`same_matter` at a 0.4 share) rather than real matters;
- (b) propose how to bring medium's noise down without losing its recall, other than the wording tweaks already tried (see LOG §§2–7
  and your STEP1-* files);
- (c) say what in the 115-article run would falsify K6b medium as the candidate.

Under 700 words.
