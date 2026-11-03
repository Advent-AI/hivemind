# Trace: is extraction unstable, and is it our mistake? (2026-10-27 07:40–08:05)

Alex: "为什么会有这个抽取不稳定的问题？你确定不是你自己犯错了吗，你得清晰的看trace benchmark 不然我们没法修".

## 1. Not the test harness ($0)

- Every fresh-control request I re-sent has the same request identity (sha of the full request: model, messages, schema,
  max tokens, reasoning effort) as a request the run itself sent: 30 of 30 match. Same bytes in.
- The responses carry no `system_fingerprint` (None in all 1,553 run calls and all 65 test calls), so a backend change can
  neither be shown nor excluded.
- The run's own data shows the same swings without my code: the parallel runner re-extracted 363 articles whose article
  section was identical (a thesis had been added to the shown list in between); 87 of 349 such pairs differ by three pieces
  or more, 35 pairs go from zero pieces to three or more (0 → 10, 3 → 11, 15 → 3). Among the 14 pairs whose shown list was
  also identical, 2 differ by three or more.
- A zero-piece answer is a real answer: 292 reasoning tokens, then `{"candidates": [], "evidence": [], "new_groups": []}`,
  for a 31k-character request that holds the CoreWeave article and the revenue theses v6 and v11. Across the run, empty
  answers spent less reasoning (median 155 tokens) than answers with pieces (335).

## 2. The benchmark (`benchmark.py`, `benchmark-results.md`; same bytes, five sends each, $0.04)

| article | effort | pieces per send | reasoning tokens | distinct pieces over 5 sends | in every send |
|---|---|---|---|---|---|
| CoreWeave / Tom's Hardware | low | 6, 4, 3, 5, 3 | 205–254 | 11 | 0 |
| | medium | 8, 4, 2, 9, 7 | 1,678–2,356 | 16 | 1 |
| Motley Fool (share may have peaked) | low | 6, 7, 9, 8, 3 | 321–389 | 17 | 0 |
| | medium | 10, 8, 4, 5, 13 | 1,425–3,753 | 19 | 0 |
| Rest of World | low | 7, 8, 9, 6, 12 | 327–571 | 20 | 2 |
| | medium | 7, 10, 7, 10, 7 | 1,201–2,443 | 15 | 3 |

A fixed `seed` (7, three sends, CoreWeave article): 3, 8, 4 pieces, 2 common of 10 distinct. The request sends no
temperature (reasoning models take none). `reasoning_effort` medium does not narrow the spread; it costs 2.2× and 1.8× the time.

## 3. What this is

The extraction call is one sample from a wide distribution: one call reads a 16k-character article against 29 theses and
decides in one pass which statements to quote, how to cut each quote, which tier, which links, whether to open a candidate,
which groups. The set of statements it chooses varies from send to send; the article's ten to twenty candidate statements
each appear in some sends and not others, and almost none in all five. The provider offers no determinism (no seed effect,
no fingerprint). So which pieces the library holds, and therefore what the judge reads, is drawn by lot at extraction. Every
arm-against-control comparison of extraction made on one sample (today's gate test included) sits inside this noise unless
it is sampled several times.

## 4. What could fix it (not built; Alex's call)

1. **Enumerate, then classify.** Split the call: first list every statement that carries a figure, a date or an attributed
   claim about the subject (exhaustive, mechanical, checkable against the text: a count that a second send must reproduce);
   then classify each listed statement against the theses (tier, links, repeat). Coverage becomes a checkable property of
   step one; the judgement stays in step two. Largest change; the design's own shape (05-extraction reads whole files).
2. **Sample and keep what repeats.** Send the same request three times and keep the pieces that appear in at least two
   answers (a piece is the same statement when its quotes overlap). Costs 3× extraction (today ≈ $1 per thousand articles →
   $3); mechanical; measurable at once on the three benchmark articles ($0.03). Stability by majority, not by design.
3. **Thesis-driven reading.** Ask per shown thesis "which statements in this article bear on it", so coverage is organised by
   the question rather than by what catches the model's eye on one pass. Changes the request shape and the answer's size.

Lean: measure 2 now on the stored samples ($0: the five sends per article are already on disk, so "keep what two of three
agree on" can be computed and compared with the judge's cites), and design 1 as the next slice if 2 does not hold.
